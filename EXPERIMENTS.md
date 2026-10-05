# APORIA — experiment record

Recorded 5 October 2026. These are real local Qwen2.5:3B feasibility runs, not canned demonstrations or evidence that APORIA has made a scientific discovery.

## Protocol

All four records use Explorer and Formalist, architecture condition, Δ=0.8, seed 31, fresh memory and Qwen2.5:3B Q4_K_M (model digest `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`). The first three use 8 operations per profile. The targeted identity retest uses 14 and an explicit maximum-three-assumptions instruction after a format failure. Both instruction and budget changed; this is a troubleshooting retest, not a controlled estimate of improvement.

Source fingerprints: first study `66bc697019e7e936f881178534d6ab36621ace7e43eb11e53258f13196626637`; retest `aae91d947833d5afc72383c528ed4fc9fa75d13fd5bcd29620945310974c1737`. Subsequent API/UI recovery changes do not rewrite these recorded identities. The code fingerprint identifies inputs but does not archive an entire executable source revision; preserve the corresponding checkout before an external reproducibility study.

## Actual results

| Case | Status | Completed profiles | Input tokens | Generated tokens | Recorded inference seconds | Path similarity | Nomic conclusion similarity |
|---|---|---:|---:|---:|---:|---:|---:|
| Identity — first run | partial | 1/2 | 15,334 | 2,518 | 97 | — | — |
| Free will | complete | 2/2 | 21,056 | 2,934 | 119 | 87.5% | 91.5% |
| Moral responsibility | complete | 2/2 | 22,375 | 3,064 | 126 | 75.0% | 85.5% |
| Identity — targeted retest | complete | 2/2 | 42,302 | 4,360 | 191 | 64.3% | 95.3% |

Inference seconds sum the provider's generation durations, including measured repairs/failures; they are not wall-clock runtime and exclude embedding analysis. Unknown usage after transport failures cannot be recovered.

- **Initial identity run:** Formalist produced more than three assumptions in both structured-output attempts. That operation failed with no belief update and is preserved. Its position is excluded from comparison; its compute remains counted. Explorer finished, but its revised root has no completed test.
- **Free will:** both profiles finished, with different operation paths. Each revised its root near the budget boundary, so both new hypotheses remain untested. The dossier exposes this warning rather than inheriting the old root's coverage.
- **Moral responsibility:** both profiles finished. Explorer has two current-root judgments and Formalist one. Pending challenges remain (one and two respectively). The generated Formalist formalization supplies no valid support.
- **Identity retest:** both profiles finished with no failed or repaired requests. Both have three current-root model judgments, one tested assumption (Explorer 1/6, Formalist 1/2), and one pending challenge. Formalist's formalization still supplies no valid support. Finishing is not the same as resolving the inquiry.

In the retest, conclusion similarity is 95.3% while the categorical stances differ (`conditional` versus `yes`). This illustrates why a stance-disagreement percentage, embedding distance and argument quality cannot be treated as interchangeable measures. With two profiles there is only one pair; a 100% categorical disagreement is not a population result.

The retest Explorer also generated several redundant imaginative branches and a metalinguistic assumption about its context limit. These are substantive small-model quality limitations. The controller and dossier make them inspectable; they do not guarantee philosophically useful arguments. Independent human scoring and source-grounded evaluation are still needed.

## Preserved artifacts

- `data/studies/challenge3-v3/manifest.json`, `case-001.json` through `case-003.json`, `report.json`.
- `data/studies/challenge3-v3-retest/manifest.json`, `case-001.json`, `report.json`. Only 1 of 3 planned cases was intentionally executed in this targeted invocation.
- The four case records are available in the browser's Research archive. Their validation memories/rewards were not imported into the primary research memory.
- The downloaded retest export was checked: it includes `{ memories: [], rewards: [] }`, and its SHA-256 matches the recorded initial-state digest.
- Earlier v1/v2 validation files under `data/experiments/` are preserved. They are not pooled with this protocol. The previous Q4/Q8 model check is a single-case feasibility comparison, not causal evidence.

## Repeatable validation

23 automated tests passed for controller routing, formal logic, Δ=0, profile isolation, current-root coverage after revision, initial snapshots, resolved memory, failure denominators, usage, study resume and model identity drift. Production build and final browser review are recorded in RESEARCH_ROADMAP.md.

The browser inspected a real archived record at 1440 and 390 CSS px; tested seed/memory controls and a JSON download. A review required the active mobile view to remain visible, now addressed by wrapping the inspector navigation. Browser long-page capture truncation is covered by an overlapping bottom-of-page capture. Static captures do not certify animation timing or accessibility conformance.

## Controlled comparison plan

`npm run study -- --suite compare --budget 14 --out data/studies/paired-v3` prints eight paired cases: seeds 31/73 × base, prompt-only, architecture Δ=0, architecture Δ=1. An explicitly chosen alternate model adds two model-condition cases. Add `--run --limit 2` to execute a bounded batch; repeat unchanged to resume. Use a new output directory after code/model/protocol changes. This plan is implemented and tested, but these eight live cases have not been executed as part of this delivery.

Fresh memory controls carryover; it does not equalize compute. Compare generated/input tokens, repair rate, duration and errors as well as trajectories. Δ=0 request reuse is an exact within-run control, not an independent sampling experiment. Larger question sets, multiple seeds, matched checkpoints and blinded independent argument-quality scoring are prerequisites for a research claim.

## Complete discovery integration — 5 October 2026

The subsequent user request adds the actual literature-based discovery pipeline. Software checks now cover 30 Node invariants and 63 Python checks, including the vendored research tests and a complete disposable worker subprocess. That subprocess mocks external metadata, PDF acquisition and model completions while running the real extraction/quotation validation, argument reconstruction, truth table, indexes, cognitive objection mapping, generation, prior art, two-defender/referee trial, brief, assessment/revision/reassessment and final-contribution ranking. Its scores are synthetic test fixtures, not academic findings. Tests also verify no early completion at the cognitive handoff, cancellation while paused, fatal-worker inference cleanup, stop waiting for slot release and preserved provenance when developing an existing record.

The real service probe `data/verification/research-smoke.json` validates a structured local Ollama completion and three actual OpenAlex divine-simplicity records. A repeat reused the exact cached completion rather than generating again. Metadata retrieval alone does not validate full discovery. Desktop UI checks use a recorded upstream brief exclusively through browser route interception, with no insertion into application storage. Production build and view navigation passed. The independent reviewer scored both listed desktop fixes resolved (`ship` at correction scope); tokens and approved identity remain intact.

The single live bounded integration run is `2537f538-9d06-4880-8369-116f12ec8738`, reusing record `0e16d975-2fa1-436b-b2b2-d68d9cf138c3` for “Look into divine simplicity and its objections.” It requests one target and one trial, twenty records per query and three attempted OA texts. The preserved failures and bounded pilot outcome are recorded below. Existing source-profile failures remain part of the provenance and are not erased. No repeated full-scale research run or mobile validation was started.

### Live mapping failure and targeted repair

The first bounded live run retrieved 51 OpenAlex works, one readable 78,430-character source and 48 checked claims. Cached source endpoint returned HTTP 200 and its SHA-256 matched the saved digest. Argument reconstruction failed after three validly recorded requests because the upstream schema compactor removed real properties named `title`. The corrected compactor retains them while removing descriptive metadata; a nested argument-schema regression passes. The failed session/job is preserved.

A conflict-guard probe raced with that completed failure and unintentionally created `f1cd06ae-3d01-4861-a3d5-7229155cfba0`; it was stopped through the API, returned `ok: true` and is confirmed cancelled. This was a validation mistake, not an intended second experiment. The failed probe is not evidence for the conflict invariant; automated lifecycle checks remain the evidence.

The targeted retry is `f12c903a-90ff-458d-971b-59c57e11e2d9`. `scripts/discovery-live-retry.mjs` verifies unchanged installed model digests and an idle slot, creates the same bounded job, and seeds its source/graph/completion cache from the failed job before mapping. It copies no results or failure logs and preserves the original. `verification-reuse.json` records this reuse. Invalid argument completions have different corrected schema cache keys and are not reused. This is a directed troubleshooting retest, not an independent scientific replication.

The title-schema retest failed a different, explicit check: its proposed conclusion also appeared among its premises, and the second argument exceeded the six-premise maximum. No invalid argument was accepted. Known source IDs, typed conclusion IDs and the original 2–6/1–2 cardinality constraints now appear in the generation schema, rather than relying only on instruction/after-the-fact rejection. Distinct premises are checked. The regression rejects invented IDs, classified conclusions used as premises and oversized arrays. The resulting cached retest is `5ebad433-d188-4e42-9f5f-a78e6da1ef8f`; both earlier failed runs are preserved.

### Final bounded pilot outcome

The constrained retest `5ebad433-d188-4e42-9f5f-a78e6da1ef8f` reconstructed two arguments with known source IDs and distinct premise/conclusion roles. Its formalizer outputs were rejected (missing exact premise keys and unsupported equality syntax), so both remain `valid: null`; no Boolean proof was accepted. The wider comparison corpus held 131 records after merging earlier literature metadata. The pilot was stopped during abstract-level literature indexing, after 15 completed fresh model calls, with no briefs produced. API stop returned HTTP 200 / `ok: true`, persisted `cancelled`, and zero active sessions. This run does not validate an end-to-end live academic brief.

The formalizer now receives required source premise keys, allowed atom names and Boolean syntax in its generation schema. Failed verification remains provisional and is reported in the result; the full worker's failure-path regression checks this explicitly. Claims and reconstructed arguments publish before later stages, so partial exports preserve them. Corpus snapshots use atomic replacement. All original pilot records and files remain intact. No further live inference was launched. Full pipeline functionality is verified with isolated deterministic providers; scientific usefulness, faithful interpretation and academic originality remain unvalidated by these software checks.
