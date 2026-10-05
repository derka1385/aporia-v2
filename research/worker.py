"""One isolated job: papers -> stateful cognition -> dialectical trials -> assessed directions."""
import asyncio
import hashlib
import json
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path


def emit(type_, **payload):
    print(json.dumps({"type": type_, "time": time.time(), **payload}, ensure_ascii=False), flush=True)


async def run(config):
    from pydantic import BaseModel, Field
    from crux_lab.config import TOPIC, CORPUS, TARGETS, RAW, ROOT, RESOLVED_MODELS
    from crux_lab.corpus import openalex, pdf, targets, dedup
    from crux_lab.graph.schema import Claim, Argument, Paper, Objection
    from crux_lab.graph.store import Store
    from crux_lab.graph.build import map_target, build_indexes
    from crux_lab.graph.extract import ExtractStats, abstract_claims
    from crux_lab.lab.generators import SharpenOut, _check, GenOut, _make
    from crux_lab.lab.run import run_target, argument_text
    from crux_lab.lab import director
    from local_provider import LocalClient
    from discovery import finish_briefs

    class Plan(BaseModel):
        name: str
        area: str
        searches: list[str] = Field(min_length=2, max_length=4)
        schools: list[str] = Field(min_length=2, max_length=8)

    client = LocalClient(config, emit)
    RESOLVED_MODELS.parent.mkdir(parents=True, exist_ok=True)
    RESOLVED_MODELS.write_text(json.dumps(client.resolved))
    emit("models", assignments=client.resolved)
    emit("stage", stage="literature", detail="Planning literature searches for your question")
    plan, _ = await client.json("extractor", config["question"], Plan,
        "Plan precise OpenAlex searches for a philosophical research question. Use short academic "
        "terms, two to four complementary searches and real philosophical traditions. Do not invent papers.")
    if not plan:
        raise RuntimeError("Literature search plan failed validation; no fabricated search results were substituted")
    TOPIC.update(name=plan.name, area=plan.area, queries={q: q for q in plan.searches}, schools=plan.schools,
                 fresh_from=str(date.today() - timedelta(days=730)),
                 targets={"fresh": max(1, config["targetCount"] - 1), "classic": int(config["targetCount"] > 1), "fresh_min_relevance": 2})
    Path(config["topicFile"]).write_text(json.dumps(TOPIC, indent=2))
    from crux_lab.lab import generators
    generators.SCHOOLS = plan.schools
    director.MAX_TRIALS = config["trialBudget"]
    rows, errors = {}, []
    for q in plan.searches:
        emit("stage", stage="literature", detail="Searching OpenAlex: " + q)
        try:
            found = await asyncio.to_thread(lambda: [openalex.to_paper(w, q) for w in openalex.search(q, max_records=config["corpusLimit"], field="search")])
            for p in found:
                if p.get("abstract") and p.get("language") in ("en", None):
                    p["fresh"] = (p.get("publication_date") or "") >= TOPIC["fresh_from"]
                    rows[p["id"]] = p
        except Exception as e:
            errors.append({"stage": "literature", "query": q, "error": str(e)[:350]})
            emit("failure", **errors[-1])
    if not rows:
        raise RuntimeError("OpenAlex returned no usable abstracts. Check connectivity or refine the question")
    # Previous jobs expand the comparison database, while this job keeps its exact corpus snapshot.
    previous = 0
    for f in sorted(ROOT.parent.glob("*/data/corpus.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:12]:
        if f == CORPUS:
            continue
        for line in f.read_text().splitlines():
            p = json.loads(line)
            if p["id"] not in rows and len(rows) < 1200:
                rows[p["id"]] = {**p, "pdf_path": None, "previousCorpus": True}
                previous += 1
    papers = list(rows.values())
    candidates = sorted([p for p in papers if p.get("pdf_url") and not p.get("previousCorpus")],
                        key=lambda p: (not p["fresh"], -(p.get("cited_by_count") or 0)))
    attempts = []
    def snapshot_corpus():
        pending = CORPUS.with_suffix(".pending")
        pending.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in papers) + "\n")
        pending.replace(CORPUS)
        corpus = {"records": len(papers), "distinctWorks": len(set(dedup.work_ids(papers).values())),
                  "fulltexts": sum(bool(p.get("pdf_path")) for p in papers), "previousRecords": previous,
                  "queries": plan.searches, "fetchedAt": time.time(), "downloadAttempts": list(attempts)}
        emit("corpus", corpus=corpus, papers=papers)
        return corpus
    corpus = snapshot_corpus()
    for i, p in enumerate(candidates[:config["fulltextLimit"]]):
        emit("stage", stage="fulltext", detail=f"Reading {i + 1}/{min(len(candidates), config['fulltextLimit'])}: {p['title']}")
        try:
            text = await asyncio.to_thread(pdf.get_fulltext, p["id"], p["pdf_url"])
            if text:
                path = pdf.text_path(p["id"])
                p.update(pdf_path=str(path.relative_to(ROOT)), fulltext_chars=len(text),
                         sourceDigest=hashlib.sha256(text.encode()).hexdigest())
            attempts.append({"paperId": p["id"], "status": "fulltext" if text else "unavailable"})
        except Exception as e:
            attempts.append({"paperId": p["id"], "status": "failed", "error": str(e)[:200]})
        corpus = snapshot_corpus()
    if not corpus["fulltexts"]:
        raise RuntimeError("Papers were found, but no readable open-access full text was available. Try a narrower question")
    emit("stage", stage="selection", detail="Selecting relevant philosophical arguments")
    selected = await targets.select(client)
    if not selected:
        raise RuntimeError("No full-text paper passed relevance, thesis and language screening")
    emit("targets", targets=selected)
    store = Store()
    store.put_many(Paper(**{k: p[k] for k in ("id", "source", "title", "authors", "year", "abstract", "url", "pdf_path")}) for p in papers)
    stats, mapped = ExtractStats(), []
    for t in selected:
        emit("stage", stage="mapping", detail=t["title"])
        result = await map_target(client, store, t, rows, stats)
        if result.get("arguments"):
            mapped.append(t)
            if any(a.valid is None for a in store.all(Argument, parent=t["paper_id"])):
                errors.append({"stage": "formalization", "paperId": t["paper_id"], "error": "Formalization could not be verified; source argument remains provisional"})
                emit("failure", **errors[-1])
        else:
            errors.append({"stage": "mapping", "paperId": t["paper_id"], "error": "No verifiable argument reconstructed"})
            emit("failure", **errors[-1])
        emit("mapping", claims=[c.model_dump(exclude={"embedding"}) for c in store.all(Claim)],
             arguments=[a.model_dump() for a in store.all(Argument)])
    if not mapped:
        raise RuntimeError("No verifiable argument could be reconstructed from the selected papers")
    emit("stage", stage="indexing", detail="Extracting prior objections and replies from corpus abstracts")
    store.put_many(await abstract_claims(client, papers, ExtractStats()))
    indexes = await asyncio.to_thread(build_indexes, store, papers)
    emit("index", index=indexes, extraction={"proposed": stats.proposed, "kept": stats.kept, "dropped": stats.dropped})
    first = mapped[0]
    arg = store.all(Argument, parent=first["paper_id"])[0]
    own = {c.id: c for c in store.all(Claim, parent=first["paper_id"])}
    grounding = {"paper": rows[first["paper_id"]], "argument": arg.model_dump(),
                 "claims": [own[cid].model_dump(exclude={"embedding"}) for cid in arg.premise_ids + [arg.conclusion_id]],
                 "instruction": "Investigate the question using this published argument. Distinguish cited claims from generated hypotheses."}
    emit("cognition_request", grounding=grounding)
    line = await asyncio.to_thread(sys.stdin.readline)
    if not line:
        raise RuntimeError("Cognitive bridge closed before supplying its result")
    cognitive = json.loads(line)
    seeds = []
    for p in cognitive.get("profiles", []):
        nodes = [n for n in p["graph"]["nodes"] if n["type"] in ("objection", "counterexample")]
        if not nodes:
            continue
        raw = max(nodes, key=lambda n: n.get("importance", 0))
        system = "Map a stateful reasoner's objection to one specific premise of this paper. If unrelated, mark usable false. Preserve its substantive move, supply a concrete 40-180 word case, and no citations."
        spec = next((s for s in client.generator_specs() if s.model == p["model"]), client.spec_for("extractor"))
        allowed = set(arg.premise_ids) | ({arg.missing_premise_id} if arg.missing_premise_id else set())
        def validate(o):
            return _check(allowed)(GenOut(**o.model_dump(exclude={"usable"}))) if o.usable else None
        out, _ = await client.json("generator", argument_text(arg, own, {}) + "\nCANDIDATE OBJECTION:\n" + raw["text"],
                                   SharpenOut, system, spec=spec, validate=validate)
        if out and out.usable:
            o = _make(arg, GenOut(**out.model_dump(exclude={"usable"})), "reasoner:" + p["id"], spec, 0, "stateful_bridge")
            seeds.append(o.model_copy(update={"profile": p["id"], "delta": config["delta"]}))
    client.seed_objections[first["paper_id"]] = seeds
    emit("bridge", mappedObjections=len(seeds), paperId=first["paper_id"])
    runs = []
    for i, target in enumerate(mapped):
        emit("stage", stage="debate", detail=target["title"], targetIndex=i, targetCount=len(mapped))
        async def on_event(ev):
            emit("dialectic", event=ev)
        try:
            result = await run_target(target, client, on_event=on_event)
            runs.append(result)
            for t in result["trials"]:
                if t.get("status") == "failed":
                    errors.append({"stage": "trial", "paperId": target["paper_id"], "error": t.get("error") or "Incomplete trial"})
            for oid, n in result["novelty"].items():
                if n.get("novelty") is None:
                    errors.append({"stage": "novelty", "objectionId": oid, "error": n.get("reason", "Prior art not assessed")})
            emit("run", run=result)
        except Exception as e:
            errors.append({"stage": "debate", "paperId": target["paper_id"], "error": str(e)[:350]})
            emit("failure", **errors[-1])
    items, final_failures = await finish_briefs(client, store, runs, rows, emit)
    errors += final_failures
    result = {"briefs": items, "runs": runs, "corpus": corpus, "papers": papers,
              "targets": mapped, "models": client.resolved, "usage": client.local.usage,
              "failures": errors, "claims": [c.model_dump(exclude={"embedding"}) for c in store.all(Claim)],
              "arguments": [a.model_dump() for a in store.all(Argument)], "index": indexes,
              "completedAt": time.time(), "extraction": {"proposed": stats.proposed, "kept": stats.kept},
              "runtime": {"python": sys.version, "embeddingBackend": os.environ.get("APORIA_EMBED_BACKEND", "auto")},
              "limitations": ["Model assessments are provisional; publication quality needs human review.",
                               "Novelty describes retrieved literature, not proof of originality.",
                               "Abstract-only corpus records have limited argumentative coverage."]}
    (ROOT / "discovery.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    emit("result", result=result)
    store.close()


if __name__ == "__main__":
    config = json.loads(Path(sys.argv[1]).read_text())
    try:
        asyncio.run(run(config))
    except BaseException as e:
        emit("fatal", error=str(e)[:700])
        raise
