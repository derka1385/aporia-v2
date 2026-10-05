# Paper discovery backend provenance

The integration vendors all 78 backend files from [univerdread/crux-lab](https://github.com/univerdread/crux-lab/tree/22299f7f31178cdd357a410cac8d0808f5dcd179), pinned revision `22299f7f31178cdd357a410cac8d0808f5dcd179`. The corresponding files under [derka1385/APORIA/directions](https://github.com/derka1385/APORIA/tree/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions) have identical Git blob IDs at revision `d45ef58f19a2dd3ae0a8195b1b01763348b2084a`. `upstream.json` records each original blob identity. Materialization appended a terminal LF: 66 files match their original blobs after removing that extra LF, while twelve files have the functional modifications listed below. These files are local source copies; the integration does not execute remote repository code at runtime.

## Integration entry points

- `worker.py`: topic planning, normalized OpenAlex records, incremental corpus snapshots, bounded OA acquisition, screening, mapping/indexes, source-to-cognition handshake, saved-profile premise mapping, complete Crux trials and final completion.
- `local_provider.py`: exclusively installed Ollama models, structured schemas, per-job cache, local usage and call ceiling. Distinct-family defense/referee/assessment when available, with explicit single-family fallback.
- `discovery.py`: automatic assessment → revision → fresh assessment → final-contribution prior art → ranked JSON/Markdown. Original judgments remain inspectable.
- `../server/discovery.mjs`: one existing APORIA session, shared inference lock/control, Python JSON-line events, immutable source provenance, cancellation and cleanup.

`requirements.lock.txt` pins the installed Python runtime packages; `npm run research:setup` installs them into this project's `.venv` through uv. The bundled Python 3.12 runtime on this Mac is supported; `APORIA_PYTHON` overrides its selection. No global Python packages, cloud inference or subscription CLI providers are configured. Vendored auxiliary API, export and cloud/evaluation CLI modules are retained as reference source; the active application enters through the four integration files above and does not require their unused optional services.

## Local modifications to upstream files

- `config.py`: isolated job paths and dynamically generated topic JSON; subscription CLIs default off.
- `corpus/http.py`: public HTTP(S) retrieval, private/loopback-address and redirect guards; retains polite rate limits and timeout/retry behavior.
- `corpus/targets.py`: actual configured freshness boundary in selection reasons.
- `graph/index.py`: local Ollama Nomic embeddings/cache; load the recorded backend; keep LSA projections independent across claims and abstract collections.
- `graph/extract.py`: argument cardinality and known premise/conclusion IDs in the structured generation grammar; distinct-premise validation.
- `graph/formalize.py`: constrain source premise keys, allowed atom names and Boolean formula syntax in generation; the truth-table validator remains authoritative.
- `graph/schema.py`: preserve final contribution novelty on each brief.
- `lab/run.py`: include mapped objections from the existing stateful reasoners in the actual first wave.
- `lab/debate.py`: invalid defender output fails the trial rather than contributing a placeholder defense.
- `llm/client.py`: preserve real `title` properties while stripping schema metadata, including nested argument schemas.
- `llm/budget.py`: count local Ollama calls in the call-budget guard.
- `lab/novelty.py`: final-thesis assessment rubric and refreshed duplicate-version exclusions after live lookup.

The local completion path deliberately improves the upstream workflow: assessment/revision run automatically after the live debate; final ranking uses fresh prior art for the effective paper thesis; missing academic grades or final novelty are withheld from ranking instead of receiving a default quality multiplier.

## Coverage boundaries

The active harvest uses OpenAlex. The default job selects two targets, attempts sixteen OA full texts and returns at most sixty records per planned query. Recent/classic balance falls back to classics when recent full texts are unavailable. Mapping covers at most eight chunks per target, and the original trial engine tests its first reconstructed argument. Wider comparison records can be abstract-only. Target, extraction, source text, search scope, model assignments, transcripts and failures are retained per job. A stopped or interrupted job is a partial record, not an automatic claim of completion; pause/resume is available while the service remains running.

Novelty is an assessment over retrieved material, not a completeness guarantee. Academic scores and debate labels are model judgments; source quotation presence and citation-ID checks establish traceability rather than philosophical correctness. The desktop browser fixture is a clearly labeled recorded upstream brief and never becomes a user research result. Consult `../EXPERIMENTS.md` for actual validation evidence.
