# Graph Report - aproria  (2026-10-05)

## Corpus Check
- 185 files · ~919,934 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .aiff 9, .woff2 8, .otf 5)

## Summary
- 1394 nodes · 3391 edges · 108 communities (64 shown, 44 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 273 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- engine.mjs
- package.json
- APORIA landing page
- index.mjs
- Store
- APORIA
- APORIA — explicit-state research laboratory
- APORIA landing page
- video/source/build.py
- Particle observatory
- LLMClient
- aporia/source/build.py
- index.py
- APORIA
- ref_node_fs
- Design System: Aproria
- APORIA
- App.jsx
- APORIA — one-minute motion film
- APORIA identity proposal
- ResearchEngine
- Laboratory.jsx
- Q: Which existing APORIA components should inform the new brand identity?
- APORIA — décisions de logo
- Landing.jsx
- colors/CONTRAST.md
- colors/README.md
- VERIFICATION.md
- aporia/CONTRAST.md
- APORIA-speaking-script.md
- Intelligence.jsx
- dependencies
- APORIA — audit du challenge 3
- scripts
- APORIA — challenge 3
- parse
- render
- export.py
- assess.py
- test_failure_states.py
- schema.py
- Provider
- cli.py
- Completion
- .fake
- Objection
- novelty.py
- Settings
- extract.py
- corpus/build.py
- targets.py
- client.py
- discovery.test.mjs
- config.py
- discovery-live-retry.mjs
- engine.test.mjs
- work_of
- http.py
- director.py
- rank_directions
- Claim
- formalize.py
- .chat
- Embedder
- philarchive_oai.py
- verify-landing.mjs
- bridge.py
- resolve.py
- aporia_profiles.py
- colors/build.py
- pdf.py
- server.py
- Handler
- defender.md

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 102 edges
2. `Claim` - 55 edges
3. `render()` - 48 edges
4. `Objection` - 48 edges
5. `Store` - 43 edges
6. `HybridIndex` - 42 edges
7. `run_target()` - 40 edges
8. `Argument` - 35 edges
9. `ModelSpec` - 34 edges
10. `run_trial()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `2. Reconstruct a published argument with source evidence` --references--> `run_target()`  [INFERRED]
  REFERENCE_PIPELINE_AUDIT.md → research/crux_lab/lab/run.py
- `Important implementation limits to preserve or improve` --references--> `run_target()`  [INFERRED]
  REFERENCE_PIPELINE_AUDIT.md → research/crux_lab/lab/run.py
- `Integrated paper discovery extension (5 October 2026)` --references--> `DiscoveryPanel()`  [INFERRED]
  ARCHITECTURE.md → src/DiscoveryPanel.jsx
- `Integrated paper discovery extension (5 October 2026)` --references--> `DiscoveryManager`  [INFERRED]
  ARCHITECTURE.md → server/discovery.mjs
- `one()` --indirect_call--> `text()`  [INFERRED]
  research/crux_lab/eval/e2_calibration.py → brand/aporia/video/team/build.py

## Import Cycles
- None detected.

## Communities (108 total, 44 thin omitted)

### Community 0 - "engine.mjs"
Cohesion: 0.17
Nodes (23): addAssumption(), availableAssumption(), chooseOperation(), contextFor(), count(), distribution(), draw(), edge() (+15 more)

### Community 1 - "package.json"
Cohesion: 0.12
Nodes (15): devDependencies, @playwright/test, vite, @vitejs/plugin-react, engines, node, name, private (+7 more)

### Community 3 - "index.mjs"
Cohesion: 0.07
Nodes (31): zod, app, discovery, discoverySchema, engine, provider, schema, server (+23 more)

### Community 4 - "Store"
Cohesion: 0.11
Nodes (7): engine, provider, questions, results, store, Store, setup()

### Community 5 - "APORIA"
Cohesion: 0.17
Nodes (11): APORIA, Brand Commitments, Capabilities and Constraints, Evidence on Hand, Open Decisions, Operating Context, Platform, Product Principles (+3 more)

### Community 6 - "APORIA — explicit-state research laboratory"
Cohesion: 0.11
Nodes (13): APORIA — explicit-state research laboratory, Components, Feasible now vs experimental, Integrated paper discovery extension (5 October 2026), LobBot findings, Metrics and visual state, Protocol and durable experiments, Real differentiation (+5 more)

### Community 8 - "video/source/build.py"
Cohesion: 0.12
Nodes (45): audio(), base(), bezier(), caption_chunks(), chrome(), clamp(), command(), cubic() (+37 more)

### Community 9 - "Particle observatory"
Cohesion: 0.33
Nodes (5): First viewport, Particle observatory, Quality and scope, Research inspection, Signature interaction and motion grammar

### Community 10 - "LLMClient"
Cohesion: 0.13
Nodes (14): load_targets(), argument_text(), attacker_spec(), dependence(), _is_revised_id(), main_all(), run_target(), assess() (+6 more)

### Community 11 - "aporia/source/build.py"
Cohesion: 0.09
Nodes (16): arc(), contrast(), fmt(), inline(), luminance(), mark(), markdown(), opened() (+8 more)

### Community 12 - "index.py"
Cohesion: 0.09
Nodes (3): test_complete_worker_pipeline_with_isolated_providers(), fulltext(), Plan

### Community 13 - "APORIA"
Cohesion: 0.06
Nodes (31): 01 — Brand essence, 01. Shared Aperture, 02 — Brand positioning, 02. Divergent Apertures — recommended, 03 — Brand personality, 03. Displaced Orbits, 04. Counter-Orbits, 04 — Visual principles (+23 more)

### Community 14 - "ref_node_fs"
Cohesion: 0.08
Nodes (23): data, errors, interactions, originalPaths, root, sizes, checks, errors (+15 more)

### Community 15 - "Design System: Aproria"
Cohesion: 0.10
Nodes (20): Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Colors (+12 more)

### Community 16 - "APORIA"
Cohesion: 0.05
Nodes (37): Actual results, APORIA — experiment record, Complete discovery integration — 5 October 2026, Controlled comparison plan, Final bounded pilot outcome, Live mapping failure and targeted repair, Preserved artifacts, Protocol (+29 more)

### Community 17 - "App.jsx"
Cohesion: 0.23
Nodes (10): api(), App(), modeLabels, profileNames, Assessment(), Brief(), DiscoveryPanel(), labels (+2 more)

### Community 18 - "APORIA — one-minute motion film"
Cohesion: 0.25
Nodes (7): APORIA — one-minute motion film, Exports, Identity, Product sources, Rebuild, Sound, Verification

### Community 19 - "APORIA identity proposal"
Cohesion: 0.29
Nodes (6): APORIA identity proposal, Contents, Rebuilding, Sources and font licensing, Status and scope, Verification and design review

### Community 20 - "ResearchEngine"
Cohesion: 0.31
Nodes (5): ResearchEngine, digest(), atomic(), runStudy(), studyReport()

### Community 21 - "Laboratory.jsx"
Cohesion: 0.28
Nodes (10): react, ArgumentGraph(), colors, ConfidencePlot(), Laboratory(), names, percent(), policyValue() (+2 more)

### Community 22 - "Q: Which existing APORIA components should inform the new brand identity?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Which existing APORIA components should inform the new brand identity?, Source Nodes

### Community 23 - "APORIA — décisions de logo"
Cohesion: 0.40
Nodes (4): 4 octobre 2026 — préférence explicite de l’utilisateur, APORIA — décisions de logo, Color exploration — 4 October 2026, Landing page — 4 October 2026

### Community 24 - "Landing.jsx"
Cohesion: 0.14
Nodes (13): lucide-react, react-dom, Intelligence, LabLink(), Landing(), Mark(), profiles, questions (+5 more)

### Community 34 - "Intelligence.jsx"
Cohesion: 0.24
Nodes (7): @react-three/fiber, three, Intelligence(), RenderBoundary, Sculpture(), modes, SIMULATION

### Community 35 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, express, @fontsource-variable/manrope, @fontsource-variable/newsreader, lucide-react, react, react-dom, @react-three/fiber (+2 more)

### Community 36 - "APORIA — audit du challenge 3"
Cohesion: 0.25
Nodes (7): APORIA — audit du challenge 3, Ce qui fonctionne et doit rester, Constats prioritaires et traitement, Limites scientifiques persistantes, Qualité technique — avant ce lot, Validation de ce lot, Verdict sur l’intégrité

### Community 37 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, build, dev, experiment, model-check, research:setup, research:test, start (+2 more)

### Community 38 - "APORIA — challenge 3"
Cohesion: 0.20
Nodes (9): APORIA — challenge 3, Authorized extension — complete paper discovery, Checkpoint — final delivery validation, Continuation rules, Current delivery pass, Current evidence, Delivery criteria, Final integration checkpoint (+1 more)

### Community 39 - "parse"
Cohesion: 0.14
Nodes (24): check_skeleton(), counterexample(), is_valid(), missing_premise_fixes(), Node, parse(), conj(), disj() (+16 more)

### Community 40 - "render"
Cohesion: 0.07
Nodes (31): _load(), render(), load_corpus(), canonical_argument(), canonical_text(), model_ids(), stamp(), write() (+23 more)

### Community 41 - "export.py"
Cohesion: 0.12
Nodes (15): topic_paths(), brief_eligibility(), calibration_note(), headline(), main(), normalize_run(), paper_of_claim(), _read() (+7 more)

### Community 42 - "assess.py"
Cohesion: 0.08
Nodes (42): available(), client(), ensure_index(), main(), query(), _sql(), write_claims_table(), Brief (+34 more)

### Community 43 - "test_failure_states.py"
Cohesion: 0.14
Nodes (10): trial_complete(), BrokenIx, EmptyIx, label_responder(), test_both_labels_valid_keeps_the_normal_result(), test_legacy_novelty_records_are_screened(), test_no_labels_fails_the_trial(), test_one_missing_label_fails_the_trial_and_keeps_the_evidence() (+2 more)

### Community 44 - "schema.py"
Cohesion: 0.11
Nodes (19): Trial, Turn, write_brief(), attacker_turn(), cited_ids(), defender_turn(), DefenderOut, render_transcript() (+11 more)

### Community 45 - "Provider"
Cohesion: 0.13
Nodes (4): DiskCache, FakeProvider, Provider, Ollama

### Community 46 - "cli.py"
Cohesion: 0.11
Nodes (20): font(), text(), _assess(), _bridge(), _check(), _corpus(), _demo(), _demo_video() (+12 more)

### Community 47 - "Completion"
Cohesion: 0.23
Nodes (5): estimate_cost(), approx_tokens(), ClaudeCLIProvider, Completion, flatten()

### Community 48 - ".fake"
Cohesion: 0.30
Nodes (16): all_different(), check(), test_all_candidates_excluded_as_the_target_paper_are_not_assessed(), test_all_candidates_judged_different_is_a_valid_score(), test_empty_indexes_are_not_assessed(), test_live_openalex_unavailable_keeps_a_local_assessment(), test_reranker_failure_after_retries_is_not_assessed(), test_retrieval_failure_is_not_assessed() (+8 more)

### Community 49 - "Objection"
Cohesion: 0.11
Nodes (33): constrained(), Plain, one(), Argument, Objection, choose_premise(), learned_values(), move_of() (+25 more)

### Community 50 - "novelty.py"
Cohesion: 0.18
Nodes (11): check(), keywords(), live_openalex(), _live_today(), NoveltyResult, Passage, RerankOut, Restatements (+3 more)

### Community 51 - "Settings"
Cohesion: 0.12
Nodes (7): Settings, AnthropicProvider, CodexCLIProvider, DatabricksProvider, EvrocProvider, _OpenAICompatible, OpenRouterProvider

### Community 52 - "extract.py"
Cohesion: 0.16
Nodes (15): AbstractBatch, AbstractClaims, ArgumentsOut, chunk_text(), ChunkOut, extract_paper_claims(), one(), normalize() (+7 more)

### Community 53 - "corpus/build.py"
Cohesion: 0.21
Nodes (10): harvest_classic(), harvest_fresh(), main(), mark_recent(), refine(), harvest(), rebuild_abstract(), search() (+2 more)

### Community 54 - "targets.py"
Cohesion: 0.19
Nodes (10): english_fulltext(), journal_article(), main(), manual_targets(), score(), Screen, one(), select() (+2 more)

### Community 55 - "client.py"
Cohesion: 0.11
Nodes (7): Budget, BudgetExceeded, cache_key(), extract_json(), ProviderError, _run(), LocalClient

### Community 56 - "discovery.test.mjs"
Cohesion: 0.12
Nodes (6): r, children, close(), run(), stages, Worker

### Community 57 - "config.py"
Cohesion: 0.21
Nodes (6): _codex_default(), _env(), load_settings(), _setup(), trace_call(), tracing_target()

### Community 58 - "discovery-live-retry.mjs"
Cohesion: 0.22
Nodes (8): health, newRoot, oldRoot, previous, prior, request, reuse, sessions

### Community 59 - "engine.test.mjs"
Cohesion: 0.17
Nodes (15): models, provider, result, computeMetrics(), bibliography, checkLogic(), evaluate(), parseFormula() (+7 more)

### Community 60 - "work_of"
Cohesion: 0.24
Nodes (9): distinct_nearest(), _norm(), work_ids(), work_key(), work_of(), is_own(), add(), test_distinct_nearest_skips_second_copy_of_a_work() (+1 more)

### Community 61 - "http.py"
Cohesion: 0.22
Nodes (4): health(), get(), _host_lock(), public_url()

### Community 62 - "director.py"
Cohesion: 0.21
Nodes (10): priority(), QueueRow, rank(), realized(), snapshot(), obj(), test_priority_formula(), test_rank_orders_by_priority_and_exploration() (+2 more)

### Community 63 - "rank_directions"
Cohesion: 0.31
Nodes (7): latest_assessment(), rank_directions(), b(), test_empty(), test_lead_score_is_survival_novelty_quality(), test_ungraded_counts_as_middling(), test_ranking_drops_directions_without_assessed_novelty()

### Community 64 - "Claim"
Cohesion: 0.13
Nodes (21): pick_items(), build_indexes(), main(), map_target(), target_text(), abstract_claims(), ExtractStats, reconstruct_arguments() (+13 more)

### Community 65 - "formalize.py"
Cohesion: 0.31
Nodes (5): FormalOut, MissingPremise, skeleton_of(), validator(), check()

### Community 66 - ".chat"
Cohesion: 0.22
Nodes (4): _compact_schema(), strip(), _log_jsonl(), test_argument_title_is_preserved_in_compact_generation_schema()

### Community 67 - "Embedder"
Cohesion: 0.18
Nodes (4): APORIA — hackathon team presentation, Embedder, Hit, tokenize()

### Community 68 - "philarchive_oai.py"
Cohesion: 0.24
Nodes (8): _call(), get_record(), identify(), list_records(), main_harvest(), parse_records(), rec_id(), to_paper()

### Community 69 - "verify-landing.mjs"
Cohesion: 0.18
Nodes (9): @playwright/test, brief, errors, fixture, original, errors, review, root (+1 more)

### Community 70 - "bridge.py"
Cohesion: 0.32
Nodes (3): load_objections(), main(), summarize()

### Community 71 - "resolve.py"
Cohesion: 0.29
Nodes (9): available_providers(), build_provider(), assign_roles(), spec(), family_of(), main(), _norm(), _probe() (+1 more)

### Community 72 - "aporia_profiles.py"
Cohesion: 0.47
Nodes (3): _lerp(), persona(), policy()

### Community 76 - "pdf.py"
Cohesion: 0.33
Nodes (6): fulltexts(), extract_text(), fetch_pdf(), get_fulltext(), safe_name(), text_path()

### Community 80 - "server.py"
Cohesion: 0.17
Nodes (11): claims_index(), _live(), go(), on_event(), prior_art(), _replay(), run(), emit() (+3 more)

## Knowledge Gaps
- **238 isolated node(s):** `root`, `data`, `errors`, `interactions`, `sizes` (+233 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 556 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `Claim`, `formalize.py`, `.chat`, `bridge.py`, `render`, `assess.py`, `test_failure_states.py`, `schema.py`, `Provider`, `index.py`, `Completion`, `.fake`, `Objection`, `novelty.py`, `extract.py`, `targets.py`, `client.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `run_target()` connect `LLMClient` to `Claim`, `render`, `export.py`, `assess.py`, `schema.py`, `APORIA`, `Objection`, `server.py`, `client.py`, `director.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Important implementation limits to preserve or improve` connect `APORIA` to `LLMClient`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `LLMClient` (e.g. with `model_ids()` and `method4()`) actually correct?**
  _`LLMClient` has 56 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Claim` (e.g. with `main()` and `write_claims_table()`) actually correct?**
  _`Claim` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Objection` (e.g. with `constrained()` and `one()`) actually correct?**
  _`Objection` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Store` (e.g. with `pick_items()` and `build_known()`) actually correct?**
  _`Store` has 9 INFERRED edges - model-reasoned connections that need verification._