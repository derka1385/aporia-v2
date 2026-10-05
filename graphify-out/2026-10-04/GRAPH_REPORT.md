# Graph Report - aproria  (2026-10-04)

## Corpus Check
- 62 files · ~848,552 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 29 file(s) not represented in the graph (top: .aiff 9, .woff2 8, .otf 5)

## Summary
- 433 nodes · 706 edges · 34 communities (24 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- engine.mjs
- package.json
- Intelligence.jsx
- index.mjs
- Store
- Aproria
- Aproria — smallest complete cognitive laboratory
- dependencies
- video/source/build.py
- Particle observatory
- start.mjs
- aporia/source/build.py
- colors/build.py
- APORIA
- colors/render.mjs
- Design System: Aproria
- Aproria
- Laboratory.jsx
- APORIA — one-minute motion film
- APORIA identity proposal
- scripts
- App.jsx
- Q: Which existing APORIA components should inform the new brand identity?
- APORIA — décisions de logo
- devDependencies
- colors/CONTRAST.md
- colors/README.md
- VERIFICATION.md
- aporia/CONTRAST.md
- APORIA-speaking-script.md

## God Nodes (most connected - your core abstractions)
1. `APORIA` - 20 edges
2. `Store` - 16 edges
3. `txt()` - 15 edges
4. `scene4()` - 14 edges
5. `enter()` - 13 edges
6. `chrome()` - 13 edges
7. `ResearchEngine` - 13 edges
8. `reveal()` - 12 edges
9. `06 — Ten logo concepts` - 12 edges
10. `base()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `setup()` --calls--> `ResearchEngine`  [EXTRACTED]
  tests/engine.test.mjs → server/engine.mjs
- `setup()` --calls--> `Store`  [EXTRACTED]
  tests/engine.test.mjs → server/store.mjs
- `App()` --calls--> `Intelligence()`  [EXTRACTED]
  src/App.jsx → src/Intelligence.jsx
- `App()` --calls--> `Laboratory()`  [EXTRACTED]
  src/App.jsx → src/Laboratory.jsx
- `node()` --calls--> `similarity()`  [EXTRACTED]
  server/engine.mjs → server/tools.mjs

## Import Cycles
- None detected.

## Communities (34 total, 10 thin omitted)

### Community 0 - "engine.mjs"
Cohesion: 0.09
Nodes (31): models, provider, result, availableAssumption(), chooseOperation(), computeMetrics(), contextFor(), count() (+23 more)

### Community 1 - "package.json"
Cohesion: 0.13
Nodes (14): engines, node, name, private, type, version, express, @fontsource-variable/manrope (+6 more)

### Community 2 - "Intelligence.jsx"
Cohesion: 0.24
Nodes (7): @react-three/fiber, three, Intelligence(), modes, RenderBoundary, Sculpture(), SIMULATION

### Community 3 - "index.mjs"
Cohesion: 0.07
Nodes (25): zod, engine, provider, questions, results, store, app, engine (+17 more)

### Community 5 - "Aproria"
Cohesion: 0.17
Nodes (11): Aproria, Brand Commitments, Capabilities and Constraints, Evidence on Hand, Open Decisions, Operating Context, Platform, Product Principles (+3 more)

### Community 6 - "Aproria — smallest complete cognitive laboratory"
Cohesion: 0.20
Nodes (9): Aproria — smallest complete cognitive laboratory, Components, Feasible now vs experimental, Inspection and scope (4 October 2026), LobBot findings, Metrics and visual state, Real differentiation, Tools and memory (+1 more)

### Community 7 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, express, @fontsource-variable/manrope, @fontsource-variable/newsreader, lucide-react, react, react-dom, @react-three/fiber (+2 more)

### Community 8 - "video/source/build.py"
Cohesion: 0.11
Nodes (45): audio(), base(), bezier(), caption_chunks(), chrome(), clamp(), command(), cubic() (+37 more)

### Community 9 - "Particle observatory"
Cohesion: 0.33
Nodes (5): First viewport, Particle observatory, Quality and scope, Research inspection, Signature interaction and motion grammar

### Community 10 - "start.mjs"
Cohesion: 0.50
Nodes (3): children, close(), run()

### Community 11 - "aporia/source/build.py"
Cohesion: 0.09
Nodes (16): arc(), contrast(), fmt(), inline(), luminance(), mark(), markdown(), opened() (+8 more)

### Community 12 - "colors/build.py"
Cohesion: 0.07
Nodes (5): contrast(), lum(), Handler, font(), text()

### Community 13 - "APORIA"
Cohesion: 0.06
Nodes (31): 01 — Brand essence, 01. Shared Aperture, 02 — Brand positioning, 02. Divergent Apertures — recommended, 03 — Brand personality, 03. Displaced Orbits, 04. Counter-Orbits, 04 — Visual principles (+23 more)

### Community 14 - "colors/render.mjs"
Cohesion: 0.12
Nodes (15): data, errors, interactions, originalPaths, root, sizes, checks, errors (+7 more)

### Community 15 - "Design System: Aproria"
Cohesion: 0.17
Nodes (11): Colors, Components, Design System: Aproria, Do:, Do's and Don'ts, Don't:, Elevation & Depth, Layout (+3 more)

### Community 16 - "Aproria"
Cohesion: 0.20
Nodes (9): Aproria, Controls, How it thinks, Launch, Layout, Measurements and limits, Particle topology, Research conditions (+1 more)

### Community 17 - "Laboratory.jsx"
Cohesion: 0.39
Nodes (7): react, ArgumentGraph(), colors, ConfidencePlot(), Laboratory(), names, percent()

### Community 18 - "APORIA — one-minute motion film"
Cohesion: 0.25
Nodes (7): APORIA — one-minute motion film, Exports, Identity, Product sources, Rebuild, Sound, Verification

### Community 19 - "APORIA identity proposal"
Cohesion: 0.29
Nodes (6): APORIA identity proposal, Contents, Rebuilding, Sources and font licensing, Status and scope, Verification and design review

### Community 20 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, experiment, model-check, start, test

### Community 21 - "App.jsx"
Cohesion: 0.47
Nodes (5): api(), App(), Mark(), modeLabels, profileNames

### Community 22 - "Q: Which existing APORIA components should inform the new brand identity?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Which existing APORIA components should inform the new brand identity?, Source Nodes

### Community 23 - "APORIA — décisions de logo"
Cohesion: 0.50
Nodes (3): 4 octobre 2026 — préférence explicite de l’utilisateur, APORIA — décisions de logo, Color exploration — 4 October 2026

### Community 24 - "devDependencies"
Cohesion: 0.50
Nodes (4): devDependencies, @playwright/test, vite, @vitejs/plugin-react

## Knowledge Gaps
- **162 isolated node(s):** `root`, `data`, `errors`, `interactions`, `sizes` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 235 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `zod` connect `index.mjs` to `package.json`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `express` connect `package.json` to `index.mjs`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Store` connect `Store` to `engine.mjs`, `index.mjs`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **What connects `root`, `data`, `errors` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `engine.mjs` be split into smaller, more focused modules?**
  _Cohesion score 0.09224489795918367 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13071895424836602 - nodes in this community are weakly interconnected._
- **Should `index.mjs` be split into smaller, more focused modules?**
  _Cohesion score 0.06722689075630252 - nodes in this community are weakly interconnected._