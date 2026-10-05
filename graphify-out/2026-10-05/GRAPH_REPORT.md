# Graph Report - aproria  (2026-10-05)

## Corpus Check
- 185 files · ~919,244 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 32 file(s) not represented in the graph (top: .aiff 9, .woff2 8, .otf 5)

## Summary
- 1389 nodes · 3379 edges · 100 communities (52 shown, 48 thin omitted)
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
- run
- aporia/source/build.py
- json
- APORIA
- ref_node_fs
- Design System: Aproria
- APORIA
- App.jsx
- APORIA — one-minute motion film
- APORIA identity proposal
- server/study.mjs
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
- e3_diversity.py
- export.py
- schema.py
- LLMClient
- render
- DiscoveryPanel.jsx
- cli.py
- Completion
- Claim
- providers.py
- extract.py
- corpus/build.py
- Budget
- discovery.test.mjs
- client.py
- discovery-live-retry.mjs
- engine.test.mjs
- http.py
- run_trial
- Store
- .chat
- HybridIndex
- philarchive_oai.py
- verify-landing.mjs
- resolve.py
- re
- pdf.py
- worker_fixture.py
- server.py
- Handler
- defender.md

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 102 edges
2. `Claim` - 54 edges
3. `render()` - 48 edges
4. `Objection` - 48 edges
5. `Store` - 43 edges
6. `HybridIndex` - 42 edges
7. `run_target()` - 40 edges
8. `ModelSpec` - 34 edges
9. `Argument` - 33 edges
10. `run_trial()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `2. Reconstruct a published argument with source evidence` --references--> `run_target()`  [INFERRED]
  REFERENCE_PIPELINE_AUDIT.md → research/crux_lab/lab/run.py
- `Important implementation limits to preserve or improve` --references--> `run_target()`  [INFERRED]
  REFERENCE_PIPELINE_AUDIT.md → research/crux_lab/lab/run.py
- `Integrated paper discovery extension (5 October 2026)` --references--> `DiscoveryManager`  [INFERRED]
  ARCHITECTURE.md → server/discovery.mjs
- `Integrated paper discovery extension (5 October 2026)` --references--> `DiscoveryPanel()`  [INFERRED]
  ARCHITECTURE.md → src/DiscoveryPanel.jsx
- `responder()` --indirect_call--> `text()`  [INFERRED]
  research/tests/test_discovery.py → brand/aporia/video/team/build.py

## Import Cycles
- None detected.

## Communities (100 total, 48 thin omitted)

### Community 0 - "engine.mjs"
Cohesion: 0.17
Nodes (23): addAssumption(), availableAssumption(), chooseOperation(), contextFor(), count(), distribution(), draw(), edge() (+15 more)

### Community 1 - "package.json"
Cohesion: 0.12
Nodes (15): devDependencies, @playwright/test, vite, @vitejs/plugin-react, engines, node, name, private (+7 more)

### Community 3 - "index.mjs"
Cohesion: 0.06
Nodes (39): zod, engine, provider, questions, results, store, models, provider (+31 more)

### Community 5 - "APORIA"
Cohesion: 0.17
Nodes (11): APORIA, Brand Commitments, Capabilities and Constraints, Evidence on Hand, Open Decisions, Operating Context, Platform, Product Principles (+3 more)

### Community 6 - "APORIA — explicit-state research laboratory"
Cohesion: 0.17
Nodes (11): APORIA — explicit-state research laboratory, Components, Feasible now vs experimental, Integrated paper discovery extension (5 October 2026), LobBot findings, Metrics and visual state, Protocol and durable experiments, Real differentiation (+3 more)

### Community 8 - "video/source/build.py"
Cohesion: 0.12
Nodes (45): audio(), base(), bezier(), caption_chunks(), chrome(), clamp(), command(), cubic() (+37 more)

### Community 9 - "Particle observatory"
Cohesion: 0.33
Nodes (5): First viewport, Particle observatory, Quality and scope, Research inspection, Signature interaction and motion grammar

### Community 10 - "run"
Cohesion: 0.31
Nodes (9): text(), canonical_text(), build_known(), one(), build_misreadings(), one(), run(), guarded() (+1 more)

### Community 11 - "aporia/source/build.py"
Cohesion: 0.09
Nodes (16): arc(), contrast(), fmt(), inline(), luminance(), mark(), markdown(), opened() (+8 more)

### Community 13 - "APORIA"
Cohesion: 0.06
Nodes (31): 01 — Brand essence, 01. Shared Aperture, 02 — Brand positioning, 02. Divergent Apertures — recommended, 03 — Brand personality, 03. Displaced Orbits, 04. Counter-Orbits, 04 — Visual principles (+23 more)

### Community 14 - "ref_node_fs"
Cohesion: 0.08
Nodes (21): data, errors, interactions, originalPaths, root, sizes, checks, errors (+13 more)

### Community 15 - "Design System: Aproria"
Cohesion: 0.10
Nodes (20): Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Approved landing extension · `/`, Colors (+12 more)

### Community 16 - "APORIA"
Cohesion: 0.05
Nodes (36): Actual results, APORIA — experiment record, Complete discovery integration — 5 October 2026, Controlled comparison plan, Live mapping failure and targeted repair, Preserved artifacts, Protocol, Repeatable validation (+28 more)

### Community 17 - "App.jsx"
Cohesion: 0.16
Nodes (8): react-dom, api(), App(), modeLabels, profileNames, isLaboratory, LaboratoryApp, Landing

### Community 18 - "APORIA — one-minute motion film"
Cohesion: 0.25
Nodes (7): APORIA — one-minute motion film, Exports, Identity, Product sources, Rebuild, Sound, Verification

### Community 19 - "APORIA identity proposal"
Cohesion: 0.29
Nodes (6): APORIA identity proposal, Contents, Rebuilding, Sources and font licensing, Status and scope, Verification and design review

### Community 20 - "server/study.mjs"
Cohesion: 0.15
Nodes (12): budget, cases, directory, limit, { values }, ResearchEngine, digest(), atomic() (+4 more)

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
Cohesion: 0.23
Nodes (9): lucide-react, Intelligence, LabLink(), Landing(), Mark(), profiles, questions, Signature() (+1 more)

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
Cohesion: 0.22
Nodes (8): APORIA — challenge 3, Authorized extension — complete paper discovery, Checkpoint — final delivery validation, Continuation rules, Current delivery pass, Current evidence, Delivery criteria, Research beyond the prototype

### Community 39 - "parse"
Cohesion: 0.14
Nodes (24): check_skeleton(), counterexample(), is_valid(), missing_premise_fixes(), Node, parse(), conj(), disj() (+16 more)

### Community 40 - "e3_diversity.py"
Cohesion: 0.10
Nodes (13): canonical_argument(), model_ids(), stamp(), write(), method4(), papers_from_hits(), pick_items(), Reworded (+5 more)

### Community 41 - "export.py"
Cohesion: 0.07
Nodes (32): topic_paths(), distinct_nearest(), _norm(), work_ids(), work_key(), work_of(), brief_eligibility(), calibration_note() (+24 more)

### Community 42 - "schema.py"
Cohesion: 0.08
Nodes (43): available(), client(), ensure_index(), main(), query(), _sql(), write_claims_table(), Brief (+35 more)

### Community 43 - "LLMClient"
Cohesion: 0.05
Nodes (48): APORIA — hackathon team presentation, Embedder, tokenize(), trial_complete(), load_objections(), main(), summarize(), check() (+40 more)

### Community 44 - "render"
Cohesion: 0.16
Nodes (13): _load(), render(), Turn, attacker_turn(), cited_ids(), defender_turn(), DefenderOut, render_transcript() (+5 more)

### Community 45 - "DiscoveryPanel.jsx"
Cohesion: 0.62
Nodes (6): Assessment(), Brief(), DiscoveryPanel(), labels, num(), url()

### Community 46 - "cli.py"
Cohesion: 0.18
Nodes (19): _assess(), _bridge(), _check(), _corpus(), _demo(), _demo_video(), _eval(), _export() (+11 more)

### Community 47 - "Completion"
Cohesion: 0.16
Nodes (8): estimate_cost(), approx_tokens(), ClaudeCLIProvider, Completion, flatten(), ProviderError, _run(), Ollama

### Community 49 - "Claim"
Cohesion: 0.06
Nodes (62): constrained(), Plain, one(), build_indexes(), Argument, Claim, Objection, Paper (+54 more)

### Community 51 - "providers.py"
Cohesion: 0.10
Nodes (9): Settings, AnthropicProvider, CodexCLIProvider, DatabricksProvider, EvrocProvider, FakeProvider, _OpenAICompatible, OpenRouterProvider (+1 more)

### Community 52 - "extract.py"
Cohesion: 0.05
Nodes (46): load_corpus(), english_fulltext(), journal_article(), load_targets(), main(), manual_targets(), score(), Screen (+38 more)

### Community 53 - "corpus/build.py"
Cohesion: 0.20
Nodes (11): fulltexts(), harvest_classic(), harvest_fresh(), main(), mark_recent(), refine(), harvest(), rebuild_abstract() (+3 more)

### Community 55 - "Budget"
Cohesion: 0.15
Nodes (4): Budget, BudgetExceeded, DiskCache, LocalClient

### Community 56 - "discovery.test.mjs"
Cohesion: 0.16
Nodes (3): DiscoveryManager, setup(), Worker

### Community 57 - "client.py"
Cohesion: 0.13
Nodes (7): _codex_default(), _env(), load_settings(), cache_key(), _setup(), trace_call(), tracing_target()

### Community 58 - "discovery-live-retry.mjs"
Cohesion: 0.22
Nodes (8): health, newRoot, oldRoot, previous, prior, request, reuse, sessions

### Community 59 - "engine.test.mjs"
Cohesion: 0.23
Nodes (12): computeMetrics(), bibliography, checkLogic(), evaluate(), parseFormula(), pathSimilarity(), readingSearch(), similarity() (+4 more)

### Community 61 - "http.py"
Cohesion: 0.22
Nodes (5): health(), prior_art(), get(), _host_lock(), public_url()

### Community 62 - "run_trial"
Cohesion: 0.21
Nodes (10): pairwise_distance(), run(), assess(), attacker_for(), own_prefix(), run_trial(), make_env(), responder_factory() (+2 more)

### Community 67 - "HybridIndex"
Cohesion: 0.15
Nodes (4): claims_index(), Hit, HybridIndex, check_all()

### Community 68 - "philarchive_oai.py"
Cohesion: 0.24
Nodes (8): _call(), get_record(), identify(), list_records(), main_harvest(), parse_records(), rec_id(), to_paper()

### Community 69 - "verify-landing.mjs"
Cohesion: 0.18
Nodes (9): @playwright/test, brief, errors, fixture, original, errors, review, root (+1 more)

### Community 71 - "resolve.py"
Cohesion: 0.29
Nodes (9): available_providers(), build_provider(), assign_roles(), spec(), family_of(), main(), _norm(), _probe() (+1 more)

### Community 76 - "pdf.py"
Cohesion: 0.42
Nodes (5): extract_text(), fetch_pdf(), get_fulltext(), safe_name(), text_path()

### Community 80 - "server.py"
Cohesion: 0.22
Nodes (8): _live(), go(), on_event(), _replay(), run(), emit(), emit(), find_target()

## Knowledge Gaps
- **236 isolated node(s):** `root`, `data`, `errors`, `interactions`, `sizes` (+231 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 553 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `.chat`, `HybridIndex`, `e3_diversity.py`, `run`, `schema.py`, `render`, `json`, `cli.py`, `Completion`, `worker_fixture.py`, `Claim`, `providers.py`, `extract.py`, `Budget`, `client.py`, `run_trial`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `run_target()` connect `Claim` to `Store`, `HybridIndex`, `export.py`, `schema.py`, `LLMClient`, `cli.py`, `APORIA`, `server.py`, `extract.py`, `Budget`, `run_trial`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `Important implementation limits to preserve or improve` connect `APORIA` to `Claim`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `LLMClient` (e.g. with `model_ids()` and `method4()`) actually correct?**
  _`LLMClient` has 56 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Claim` (e.g. with `main()` and `write_claims_table()`) actually correct?**
  _`Claim` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Objection` (e.g. with `constrained()` and `one()`) actually correct?**
  _`Objection` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Store` (e.g. with `pick_items()` and `build_known()`) actually correct?**
  _`Store` has 9 INFERRED edges - model-reasoned connections that need verification._