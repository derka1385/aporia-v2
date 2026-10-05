"""Completion, quality and final-contribution prior art for the integrated finder."""
import json
from dataclasses import asdict
from crux_lab.config import BRIEFS, RAW
from crux_lab.graph.schema import Brief, SURVIVAL, Claim
from crux_lab.graph.index import HybridIndex, INDEX_DIR
from crux_lab.lab import assess, brief, novelty


def rank_briefs(items):
    ranked, withheld = [], []
    for item in items:
        b = dict(item)
        latest = (b.get("revision") or {}).get("assessment") or b.get("assessment")
        check = b.get("contribution_novelty")
        reason = ("Academic quality not assessed" if not latest else
                  "Final contribution novelty not assessed" if not novelty.is_assessed(check) else "")
        b["quality"] = latest["overall"] / 5 if latest else None
        b["grade"] = latest.get("grade") if latest else None
        b["finalNovelty"] = check.get("novelty") if check else None
        b["survival"] = SURVIVAL.get(b.get("outcome"), 0)
        b["score"] = round(b["survival"] * b["finalNovelty"] * b["quality"], 4) if not reason else None
        b["rankingReason"] = reason
        (withheld if reason else ranked).append(b)
    ranked.sort(key=lambda b: (-b["score"], -b["finalNovelty"], b["id"]))
    for i, b in enumerate(ranked):
        b["rank"] = i + 1
    return ranked + withheld


async def finish_briefs(client, store, runs, papers, emit):
    items, failures = [], []
    ci, ai = HybridIndex.load(INDEX_DIR / "claims"), HybridIndex.load(INDEX_DIR / "abstracts")
    evaluator = assess.assessor_spec(client)
    writer = assess.reviser_spec(client, evaluator)
    for run in runs:
        obs = {o["id"]: o for o in run["objections"]}
        for bid in run["briefs"]:
            b = store.get(Brief, bid)
            if not b:
                continue
            try:
                emit("stage", stage="assessment", detail=b.research_question)
                first = await assess.assess_brief(client, evaluator, b)
                if not first:
                    raise ValueError("Assessor exhausted validation retries")
                b = b.model_copy(update={"assessment": first})
                persist(b, store)
                emit("brief", brief=b.model_dump())
                emit("stage", stage="revision", detail=b.research_question)
                rev = await assess.revise_brief(client, writer, b)
                if rev:
                    proposal = b.model_copy(update={"research_question": rev["research_question"],
                        "paper_direction": rev["paper_direction"] + "\n\n" + rev["reply_to_strongest_objection"]})
                    again = await assess.assess_brief(client, evaluator, proposal)
                    rev["assessment"] = again
                    if not again:
                        failures.append({"briefId": bid, "stage": "reassessment", "error": "Revised proposal could not be graded"})
                    b = b.model_copy(update={"revision": rev})
                else:
                    failures.append({"briefId": bid, "stage": "revision", "error": "Revision could not be validated; original proposal retained"})
                persist(b, store)
                emit("stage", stage="contribution_novelty", detail=b.research_question)
                # Only a successfully assessed revision replaces the original proposal in ranking.
                effective = b.revision if b.revision and b.revision.get("assessment") else None
                question = effective["research_question"] if effective else b.research_question
                direction = effective["paper_direction"] if effective else b.paper_direction
                prior = await novelty.check(client, "contribution-" + bid,
                    question + "\n" + direction, "PROPOSED PAPER CONTRIBUTION: " + question,
                    b.challenged_premise["id"], b.challenged_premise["text"], ci, ai,
                    exclude_paper=b.argument["paper_id"], use_live=True, contribution=True)
                b = b.model_copy(update={"contribution_novelty": prior.to_dict()})
            except Exception as e:
                failures.append({"briefId": bid, "stage": "completion", "error": str(e)[:500]})
                emit("failure", **failures[-1])
            persist(b, store)
            data = b.model_dump()
            # References remain record-derived, including live OpenAlex results.
            records = dict(papers)
            for f in (RAW / "openalex_live").glob("*.json"):
                for p in json.loads(f.read_text()):
                    records[p["id"]] = p
            for m in (data.get("contribution_novelty") or {}).get("nearest", []):
                if not any(r["record_id"] == m["record_id"] for r in data["closest_literature"]):
                    data["closest_literature"].append({**brief.record_ref(records.get(m["paper_id"]), m["record_id"]),
                        "paper_id": m["paper_id"], "quote": m["quote"], "verdict": m["verdict"],
                        "similarity": m["similarity"], "scope": "final_contribution"})
            data["runId"] = run["run_id"]
            data["markdown"] = markdown(data)
            items.append(data)
            emit("brief", brief=data)
    return rank_briefs(items), failures


def persist(b, store):
    store.put(b)
    brief.save(b)


def markdown(b):
    obj = Brief(**b)
    text = brief.to_markdown(obj)
    check = b.get("contribution_novelty") or {}
    text += f"\n## Final contribution prior art\n\nStatus: {check.get('status', 'unassessed')}. "
    text += f"Score: {check.get('novelty')}. Records searched: {check.get('records_searched', 0)}.\n\n"
    for r in b["closest_literature"]:
        text += f"- {r.get('title', '')} ({r.get('year', '')}). {r.get('url', '')}\n"
    return text
