# APORIA

A local philosophical research instrument. A question now leads to real OpenAlex papers, reconstructed arguments, adversarial debates and assessed research proposals. The existing five stateful reasoners contribute objections and retain their inspectable trajectories, memory and controller. A continuously deforming particle sculpture follows the run.

## Launch

Requires Node **22.13+** (Node 26 is installed on this Mac) and [Ollama](https://ollama.com). From this folder:

```sh
npm install
npm run research:setup  # one-time Python discovery dependencies; requires uv
npm start
```

Open **http://localhost:5173**. After installation, `npm start` is the single launch command. It starts the API on loopback port 4317 and Vite on 5173, and starts Ollama if it is installed but not running. Ctrl+C stops services started by the launcher; an already-running Ollama service is left alone. No service is published.

The root page is the **APORIA landing page**, using the original Divergent Apertures logo and the Obsidian & Iris identity. Its state controls, policy tabs, mobile navigation and FAQ are interactive. **Open the laboratory** leads to `/app`; the illustrative personal-identity question link pre-fills the research input without starting inference. The original research and visual-study controls remain available there.

The landing is implemented in `src/landing/`. Display and body fonts are bundled with the existing brand assets. The WebGL volume loads separately, honors reduced motion, and stops rendering when its stage is outside the viewport. A source SVG supplies its loading and unavailable-WebGL fallback.

The Mac already has `qwen2.5:3b`, `qwen2.5:1.5b`, `qwen2.5:3b-instruct-q8_0`, `llama3.2:3b` and `nomic-embed-text`. On another machine, first run:

```sh
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

The 3B model is the default. Inference can take several minutes for five profiles; results stream after each operation. The model selector lets you use the faster 1.5B model at a quality tradeoff. If inference is offline, Visual studies remains usable. No API keys or cloud model are needed. Paper discovery retrieves public scholarly metadata and available open-access PDFs from OpenAlex and publisher/repository locations. LLM inference and embeddings remain local. Reflection mode retains its curated bibliography pointers; they are not live evidence.

## Controls

- **Research:** enter a philosophical question, set Δ and start. Paper-based discovery is the default. Setup controls paper targets (default 2) and debate trials per paper (default 6); select Cognitive reflection to use the original workflow alone. Open **Experiment setup** for condition, model, step budget (14 by default), random seed and initial memory. Fresh state is the default; prior research is an explicit choice. Pause suspends the paper worker and waits for the current cognitive operation; resume continues the same job. Stop cancels both, preserves the partial record and waits for the local inference slot to be released. If another active record is hidden, **Open active research** restores its resume/stop controls. A paused experiment still owns the local inference slot.
- **Research directions:** the finished output contains paper theses, original/revised academic assessments, the strongest remaining objection, closest literature, source quotations and unresolved questions. Papers, Debates and Research log expose the evidence and failures. Download a brief as Markdown or export the full record as JSON. Finished proposals missing assessment or final novelty remain visibly unranked.
- **Profiles:** Explorer, Formalist, Skeptic, Synthesizer and Minimalist. Select a profile to inspect its actual state. The argument graph nodes support mouse, Enter and Space; scroll larger graphs. Other views show controller decisions, counterfactual tests, memory provenance and a **Research dossier** with current-hypothesis coverage, unresolved challenges, reproducibility metadata and compute usage.
- **Visual studies:** clearly labeled simulation. Six buttons or keys **1–6** select idle, exploration, concentration, conflict, insight and collapse. **Cycle** transitions every 6.5 seconds. Δ changes geometric divergence. The pause icon stops continuous particle motion; reduced-motion preferences do the same.
- **Archive:** reopen stored sessions. An earlier reflection record has **Find research directions from this record**, which reuses its saved profiles in a new paper-discovery job and preserves their original provenance. **Export record** downloads full JSON containing policies, graph, trajectories, tests, measurements, model metadata, failures and the immutable initial memory/routing snapshot.

In research mode the sculpture uses the run's frozen Δ; changing setup after a completed run affects the next run. At Δ=0 all computational policies and seeds are identical. Identical inference requests within a run are reused and explicitly logged, with zero new generated tokens.

## Research conditions

**Base model** produces a single untested proposal. **Prompt differentiation** changes only a profile instruction, with common routing and sampling policies. **Cognitive architecture** interpolates real controller weights, context visibility, memory depth, tool availability, branch limits, sampling and stopping thresholds. **Model differentiation** additionally assigns explicitly selected local models to profiles; Q4/Q8 comparisons are possible using the installed Qwen checkpoints. Neither quantization nor a model family difference establishes a scientific causal result.

These conditions can be rerun from setup and compared through exported records. Controller budget is measured in operations, with input/output tokens and inference duration logged separately: equal operation counts do **not** imply equal compute. The default seed is 31 and can be changed in setup. Fresh state excludes both earlier beliefs and learned routing rewards. Prior research explicitly reuses an immutable pre-session snapshot. Model digests, engine/code fingerprints and initial-state fingerprints are recorded. Identical seeds alone do not guarantee identical output across runtimes or model versions.

## Complete paper discovery loop

1. Plan two to four complementary searches; normalize and snapshot real OpenAlex works. Reuse earlier job corpus metadata for broader comparison, acquire available OA texts and screen relevant thesis papers. Defaults: at most 60 records per query and 16 attempted full texts.
2. Extract typed claims with checked short quotations, reconstruct source arguments and verify a proposed propositional formalization. Hidden premises are generated and explicitly distinguished from source claims.
3. Build BM25 + local Nomic retrieval indexes over claims and abstracts. Feed a published argument to the existing cognitive engine, or map saved profile objections to its premises when developing an old record.
4. Generate APORIA profile objections, hidden-premise attacks, tradition lenses and sharpened naive questions. Check each objection against local indexes and bounded live OpenAlex prior art, excluding the target and recognized duplicate versions.
5. The adaptive Director chooses trials. Two defenders face attacker rejoinders; a referee checks misreading, verifies citation IDs, labels outcomes and records deciding quotations. Required premise repairs can receive further attacks within the trial/depth budget.
6. Write the strongest eligible research briefs, assess coherence/robustness/significance/specificity, revise against the strongest objection and assess the revised proposal afresh. Preserve both versions and grades.
7. Check the **final proposed contribution** against literature again. Rank only assessed proposals by `survival × final contribution novelty × (academic quality / 5)`; missing judgments do not receive invented scores.

The audited backend is vendored from Crux Lab and old APORIA, with explicit local modifications. See [research/UPSTREAM.md](research/UPSTREAM.md) and [REFERENCE_PIPELINE_AUDIT.md](REFERENCE_PIPELINE_AUDIT.md). Each job has its own corpus, source texts/digests, SQLite graph, caches, model assignments and transcripts under `research/data/jobs/<id>/`. The parent record and events remain in the existing session archive. All inference uses installed Ollama models, with a different family for defense/assessment when available. A job has a 600-call ceiling; full runs can take considerably longer than reflection on small local models.

Unavailable full texts, invalid extractions and failed judgments remain visible. The current corpus is bounded and often abstract-only; novelty describes retrieved prior art, not proof of originality. Model assessments do not replace academic review. No successful scientific discovery is claimed from passing software tests.

## How it thinks

The server tracks typed claim nodes, dependencies, assumptions, objections, confidence, uncertainty, novelty and curiosity. It scores eligible operations, selects a high-value branch, runs a model proposal or real tool, recomputes metacognition and updates the operation's learned utility. No reward is given for disagreement. A coverage guard reserves enough steps for an actual counterfactual/adversarial test and provisional synthesis; later routing is dynamic.

Tools include a real bounded propositional truth-table checker, persistent SQLite retrieval and a curated philosophical reading index. The checker validates a model-generated formalization, not the truth of its philosophical premises. Adversarial outcomes are language-model judgments, clearly labeled. Introspection exposes assumptions in the graph and lowers unsupported confidence; it is a structured mutation rather than a request for private reasoning.

Each profile sees an immutable pre-session memory snapshot, never other profiles' current work. Only unresolved recalled objections and rejected hypotheses exert counterevidence pressure. Stored operation outcomes warm-start routing only when prior research is selected; fresh experiments exclude this learning. All SQLite data is under `data/`; no secrets are stored.

## Particle topology

React Three Fiber renders a hidden parametric **trefoil tube** through a custom Three.js point shader: 54,000 samples on desktop and 25,000 on small screens, with depth variation. The body has folds, overlapping lobes and visible cavities. All particle deformation runs on the GPU; state uniforms interpolate with exponential damping.

Curiosity extends ridges; attention compresses the body; uncertainty diffuses points; confidence reduces turbulence. Contradiction separates poles and warms a region. A rejected root hypothesis dissolves a fold, while a surviving, tested, stable hypothesis permits insight crystallization. The render loop stops outside the viewport and in a hidden tab; paused and reduced-motion states render only as needed. Bounded pointer parallax emphasizes depth. Simulation uses the same uniforms with labeled prescribed values.

## Measurements and limits

Completed runs use **local Nomic embeddings** for argument and conclusion similarity, when available. In-progress and embedding-unavailable records use explicitly labeled token-vector similarity. Branch similarity and assumption/objection deduplication are lexical proxies. Path similarity uses longest common operation subsequences. Stance disagreement excludes undecided positions. Confidence and information gain are operational heuristics, not calibrated probabilities or empirical findings. Diversity is not argument quality, and a single run does not answer the scientific research question.

LobBot was inspected in the sibling checkout; see `ARCHITECTURE.md`. Its GPU task-calibrated MoE pruning, LoRA repair and quantization pipeline remains a future experiment. No training or compression job is run by this app.

## Reproducible studies and verification

```sh
npm test                 # controller, protocol, persistence, study and worker lifecycle invariants
npm run research:test    # upstream research checks plus the complete isolated worker pipeline
npm run build            # production client build
npm run study            # print a plan; does not start inference
npm run study -- --run --suite smoke --budget 14 --limit 3 --out data/studies/my-smoke
npm run study -- --suite compare --budget 14 --out data/studies/my-comparison
```

`smoke` runs identity, free will and moral responsibility with Explorer and Formalist, seed 31 and Δ=0.8. `compare` plans a single identity question across seeds 31/73, base model, prompt differentiation, architecture Δ=0 and architecture Δ=1. Add `--alternate qwen2.5:3b-instruct-q8_0` to include model differentiation. Add `--run` only when ready to execute. `--limit` bounds cases per invocation; repeat the same command to continue the same manifest. Do not run a CLI study concurrently with an inference session in the UI.

Each case has isolated fresh memory. The runner saves every operation atomically and updates `report.json`. Completed and failed cases are preserved and skipped on resume. Interrupted cases are retained separately before being restarted. If code, model identity or protocol changes, use a new output directory: the runner rejects mixing versions. A process lock prevents two CLI runners from executing together.

See [EXPERIMENTS.md](EXPERIMENTS.md) for the actual four feasibility records, including one failed profile, the targeted successful retest, and their limitations. This is not a completed controlled multi-seed scientific study. Reports and SQLite files remain local under `data/` and are ignored by Git.

`npm run experiment` and `npm run model-check` are earlier validation scripts; their older records do not validate the current protocol. Browser checks for this delivery used the running interface at desktop/mobile widths, real archive records, setup controls and a JSON export. The existing `scripts/verify-landing.mjs` is a separate landing-page check. The discovery extension has a desktop-only fixture navigation/capture check, respecting the user’s requested scope. Its recorded upstream brief is browser data only and is never inserted as a new research result.

## Layout

`server/discovery.mjs` coordinates the Python worker and cognitive engine; `research/worker.py` runs literature, mapping and dialectics; `research/discovery.py` completes assessment/revision/final novelty/ranking; `src/DiscoveryPanel.jsx` renders evidence and directions. `server/engine.mjs` controls state and experiments; `policies.mjs` defines Δ; `provider.mjs` validates local JSON proposals and computes embeddings; `tools.mjs` contains logic/similarity/bibliography; `store.mjs` persists SQLite. `protocol.mjs` defines provenance/quality accounting; `study.mjs` isolates and resumes experiments. `src/Intelligence.jsx` renders the object. `App.jsx`, `Laboratory.jsx` and `ArgumentGraph.jsx` provide the interface. All dependencies are project-local.
