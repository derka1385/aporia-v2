---
name: Aproria
description: A local particle observatory for philosophical inquiry.
colors:
  bg: "#080b10"
  surface: "#10161e"
  ink: "#d5dbe4"
  muted: "#91a0b2"
  line: "#25303d"
  accent: "#a8cbe0"
  warm: "#d99c74"
  focus: "#99c7df"
  chrome-line: "#17202c"
  action-bg: "#bdd3e1"
  action-ink: "#111c27"
  action-hover: "#deebf3"
  action-disabled: "#718491"
  field-line: "#354454"
  field-focus: "#8ab2ce"
  quiet-ink: "#a6b5c7"
  quiet-hover: "#edf4fa"
  nav-ink: "#8b99aa"
  nav-active: "#dbe6f0"
  nav-line: "#8eaec9"
  mode-ink: "#9aacbf"
  mode-selected: "#14202d"
  mode-line: "#32485d"
  mode-active-ink: "#d1e2f0"
  mode-hover: "#111b26"
  archive-bg: "#0e151e"
  confidence: "#90c7db"
  uncertainty: "#b5a4d4"
  graph-hypothesis: "#abc5db"
  graph-premise: "#719bc1"
  graph-assumption: "#b0a1d7"
  graph-counterexample: "#d9aa77"
  graph-objection: "#dc8e6a"
  graph-evidence: "#82bbb0"
  graph-question: "#8ba7b5"
  particle-blue: "rgb(19% 33% 63%)"
  particle-cyan: "rgb(46% 78% 89%)"
  particle-violet: "rgb(58% 49% 84%)"
  particle-conflict: "rgb(95% 53% 30%)"
  particle-insight: "rgb(90% 97% 100%)"
  landing-obsidian: "#121416"
  landing-surface: "#1B1F23"
  landing-paper: "#F4F1E9"
  landing-muted: "#B4BBC2"
  landing-rule: "#353B42"
  landing-boundary: "#747E88"
  landing-iris: "#B7A2E8"
  landing-cyan: "#79C5CF"
  landing-amber: "#DDB16B"
  landing-paper-muted: "#596168"
  landing-paper-rule: "#D1CDC3"
  landing-paper-boundary: "#76736C"
  landing-paper-iris: "#65509A"
  landing-paper-cyan: "#24636C"
  landing-paper-amber: "#805B22"
  landing-paper-hover: "#E9E5DB"
  landing-action-hover: "#DAD3C6"
typography:
  display:
    fontFamily: "'Newsreader Variable', serif"
    fontSize: "clamp(40px, 4vw, 56px)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-.025em"
  headline:
    fontFamily: "'Newsreader Variable', serif"
    fontSize: "35px"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "-.025em"
  inquiry:
    fontFamily: "'Newsreader Variable', serif"
    fontSize: "28px"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "-.025em"
  position:
    fontFamily: "'Newsreader Variable', serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "'Manrope Variable', sans-serif"
    fontSize: "12px"
    lineHeight: 1.7
  label:
    fontFamily: "'Manrope Variable', sans-serif"
    fontSize: "10px"
  control:
    fontFamily: "'Manrope Variable', sans-serif"
    fontSize: "11px"
  micro:
    fontFamily: "'Manrope Variable', sans-serif"
    fontSize: "9px"
  mono:
    fontFamily: "ui-monospace, SFMono-Regular, monospace"
    fontSize: "11px"
  landing-display:
    fontFamily: "'APORIA Serif', Georgia, serif"
    fontSize: "clamp(54px, 5.65vw, 82px)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-.025em"
  landing-headline:
    fontFamily: "'APORIA Serif', Georgia, serif"
    fontSize: "clamp(42px, 4.1vw, 60px)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-.025em"
  landing-title:
    fontFamily: "'APORIA Serif', Georgia, serif"
    fontSize: "32px"
    fontWeight: 400
    lineHeight: 1.3
  landing-body:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.6
  landing-prose:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.65
  landing-label:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
  landing-control:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.5
  landing-state-label:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  landing-navigation:
    fontFamily: "'APORIA Sans', Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  action: "4px"
  control: "5px"
  archive: "6px"
  field: "8px"
  round: "50%"
  landing-control: "3px"
spacing:
  "4": "4px"
  "8": "8px"
  "10": "10px"
  "12": "12px"
  "16": "16px"
  "18": "18px"
  "20": "20px"
  "24": "24px"
  "30": "30px"
  "32": "32px"
  "44": "44px"
  "56": "56px"
  "14": "14px"
  "22": "22px"
  "28": "28px"
  "40": "40px"
  "48": "48px"
  "100": "100px"
  "120": "120px"
components:
  button-primary:
    backgroundColor: "{colors.action-bg}"
    textColor: "{colors.action-ink}"
    typography: "{typography.control}"
    rounded: "{rounded.action}"
    padding: "0 19px"
  button-primary-hover:
    backgroundColor: "{colors.action-hover}"
  button-primary-disabled:
    backgroundColor: "{colors.action-disabled}"
  button-quiet:
    textColor: "{colors.quiet-ink}"
    typography: "{typography.control}"
    padding: "4px 0"
  button-quiet-hover:
    textColor: "{colors.quiet-hover}"
  button-icon:
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    size: "34px"
  question-field:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.field}"
    padding: "7px 7px 7px 22px"
  navigation:
    textColor: "{colors.nav-ink}"
    typography: "{typography.body}"
    padding: "0 3px"
    height: "86px"
  navigation-active:
    textColor: "{colors.nav-active}"
  mode-button:
    textColor: "{colors.mode-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "10px"
  mode-button-selected:
    backgroundColor: "{colors.mode-selected}"
    textColor: "{colors.mode-active-ink}"
  archive-container:
    backgroundColor: "{colors.archive-bg}"
    rounded: "{rounded.archive}"
    padding: "24px"
  landing-action-filled:
    backgroundColor: "{colors.landing-paper}"
    textColor: "{colors.landing-obsidian}"
    typography: "{typography.landing-control}"
    rounded: "{rounded.landing-control}"
    padding: "14px 22px"
  landing-action-filled-hover:
    backgroundColor: "{colors.landing-action-hover}"
  landing-action-on-paper:
    backgroundColor: "{colors.landing-obsidian}"
    textColor: "{colors.landing-paper}"
    typography: "{typography.landing-control}"
    rounded: "{rounded.landing-control}"
    padding: "14px 22px"
  landing-action-on-paper-hover:
    backgroundColor: "{colors.landing-rule}"
  landing-navigation:
    textColor: "{colors.landing-paper}"
    typography: "{typography.landing-navigation}"
    height: "108px"
  landing-state-button:
    typography: "{typography.landing-state-label}"
    rounded: "{rounded.landing-control}"
    padding: "9px 10px"
  landing-state-button-reasoning:
    textColor: "{colors.landing-iris}"
  landing-state-button-exploration:
    textColor: "{colors.landing-cyan}"
  landing-state-button-conflict:
    textColor: "{colors.landing-amber}"
  landing-state-button-selected:
    backgroundColor: "{colors.landing-surface}"
  landing-motion-control:
    textColor: "{colors.landing-muted}"
    rounded: "{rounded.landing-control}"
    size: "44px"
  landing-policy-tab:
    textColor: "{colors.landing-paper-muted}"
    padding: "19px 15px"
  landing-policy-tab-selected:
    textColor: "{colors.landing-obsidian}"
  landing-policy-tab-hover:
    backgroundColor: "{colors.landing-paper-hover}"
  landing-policy-specimen:
    backgroundColor: "{colors.landing-paper}"
    textColor: "{colors.landing-obsidian}"
  landing-faq:
    textColor: "{colors.landing-paper}"
    padding: "22px 0"
---
# Design System: Aproria

## Overview

**Creative North Star: "Particle observatory"**

A near-black field holds a folded, point-based volumetric topology. Cool blue, cyan and violet describe the object; warm regions signal conflict and pale regions signal insight. Manrope controls and Newsreader display copy keep the surrounding interface restrained.

The sculpture supplies spatial depth. Inspection uses flat sections, thin dividers and compact readouts rather than ornamental chrome. This is a code-authored WebGL medium; raster compositions are not part of the implemented design.

**Key Characteristics:**
- Folded particle geometry with cavities and asymmetry.
- Near-black surfaces, cool information and warm conflict.
- Quiet controls, fine dividers and compact numeric readouts.
- State-driven deformation with reduced-motion and pause support.

### Approved landing extension · `/`

**Approved visual world: "Obsidian & Iris"**

The user-selected original Divergent Apertures mark and Obsidian & Iris concept extend this system for the public landing route (`/`). The landing uses warm paper against obsidian, Source Serif 4 display typography and Source Sans 3 interface text. The folded particle object retains spatial depth; the surrounding surface stays flat and ruled. This is an approved route-specific addition, recorded from the finished implementation rather than a replacement of the research instrument.

The existing unprefixed frontmatter tokens and incumbent descriptions continue to govern the research application at (`/app`). All `landing-*` tokens govern only `src/landing/Landing.jsx` and `src/landing/landing.css`; the shared particle renderer selects the Obsidian & Iris palette when explicitly requested, including the approved laboratory particle adaptation documented below. The two APORIA font aliases are intentional additions to the system, not substitutions for Manrope or Newsreader.

**Key Characteristics:**
- Original Divergent Apertures SVG mark with a spaced APORIA wordmark.
- Obsidian and warm-paper surfaces with iris, cyan and amber cognitive-state accents.
- Source Serif 4 display and italic paired with readable Source Sans 3 controls and prose.
- Flat fine-rule components, neutral policy identities and responsive illustrative paths.

## Colors

The frontmatter preserves the implemented CSS colors. Particle entries transcribe the shader's RGB channel values to CSS percentages; the shader remains authoritative for its rendering.

- **Primary:** muted cool accent for running state and graph hover; blue and cyan dominate particle flow.
- **Secondary:** violet distinguishes assumptions, uncertainty and selected regions of the topology.
- **Tertiary:** warm conflict, counterexamples and objections. Pale particle insight lightens a coherent region.
- **Neutral:** near-black background, slightly lighter surface, pale ink, muted readouts and fine structural lines. The action button is the strongest flat control contrast.
- **Graph roles:** hypothesis and premise are cool blue; assumption is violet; counterexample and objection are warm; evidence is muted green; question and concept share a blue-gray token.

**The State Color Rule.** Color carries cognitive or control state; preserve the existing cool, warm and pale state meanings.

### Approved landing extension · `/`

- **Primary — Iris:** `landing-iris` identifies reasoning on obsidian; `landing-paper-iris` is its darker counterpart on paper. Text selection and the initial path node reuse this meaning.
- **Secondary — Exploration Cyan:** `landing-cyan` identifies exploration on obsidian; `landing-paper-cyan` supplies the darker paper-context token and visible focus outline there.
- **Tertiary — Conflict Amber:** `landing-amber` identifies conflict on obsidian; `landing-paper-amber` preserves that meaning in the paper context. These paper-context accents are defined by the finished stylesheet even where a current component does not display them.
- **Neutral — Obsidian and Warm Paper:** `landing-obsidian` is the dark canvas and the text color on paper; `landing-paper` is the light surface and the primary text on obsidian. `landing-surface` gives selected controls a shallow tonal fill. Muted text, structural rules and interactive boundaries each have separate dark- and paper-context tokens.
- **Control states:** `landing-action-hover` warms the pale action on obsidian; `landing-rule` supplies the dark action's hover fill on paper. `landing-paper-hover` is the policy-tab hover surface.

**The Landing State Color Rule.** On the landing, iris means reasoning, cyan means exploration and amber means conflict. Policy identities stay neutral; selected policy tabs use ink and an underline.

**The Paper Contrast Rule.** Switch to the darker paper-context accents and muted text whenever controls sit on warm paper; the pale obsidian-context accents are not text colors for the paper surface.

## Typography

Manrope Variable supplies interface text; Newsreader Variable supplies display copy and provisional positions. Both are bundled through Fontsource imports, including Newsreader italic. System monospace is reserved for code and audit payloads.

- **Display:** centered inquiry introduction; the italic phrase uses the same Newsreader family.
- **Headline / inquiry:** serif laboratory heading and question prompt. Laboratory heading reduces to (30px) below (1000px); inquiry becomes left-aligned at (27px) below (700px).
- **Position:** serif research stance, with a more open line height.
- **Body / control / label / micro:** compact Manrope text for records, buttons, readouts and secondary annotations. Body prose uses the frontmatter body role; sizes are assigned per component rather than a universal body size.
- **Numbers:** delta, steps, policy values and metrics use tabular numerals. Audit prose is capped at (75ch); laboratory question text at (70ch).

### Approved landing extension · `/`

**Display Font:** Source Serif 4, bundled under the exact CSS alias `'APORIA Serif'`, with Georgia and serif fallbacks. The regular display face and the separate italic face both use (400) weight.

**Body Font:** Source Sans 3, bundled under the exact CSS alias `'APORIA Sans'`, with Arial and sans-serif fallbacks. Regular (400) and semibold (600) faces ship locally; font synthesis is disabled. These aliases match the token-bearing `landing-*` typography entries above and the loaded faces in verification evidence.

- **Display:** the two-line serif introduction uses `landing-display`; its italic line stays warm paper. Compact desktop, tablet and phone sizes are specified in Layout.
- **Headline:** the approach heading uses `landing-headline`. Method and closing headings use nearby responsive serif sizes; FAQ uses a smaller serif heading. All landing h1/h2 headings use balanced wrapping and tight tracking.
- **Title:** serif policy names use `landing-title`; method step titles use Source Sans semibold at (23px), reducing to (22px) on phones.
- **Body / prose:** `landing-body` is the surface base; method and policy explanation use (17–19px) text and (1.6–1.7) leading. The hero description is capped at (43ch), policy descriptions at (32ch), and FAQ answers at (58ch). The hero lead uses (23px) regular sans text.
- **Control / navigation / state label:** these roles use the landing-specific tokens. The wordmark uses semibold sans with (.12em) spacing; its lettering belongs to the signature, not ordinary controls.
- **Labels and captions:** compact supporting text stays in Source Sans. Captions use (13px) and labels commonly use `landing-label`; path and method numbers are tabular.

**The Route Typography Rule.** Use the APORIA aliases for the approved landing extension; retain Manrope Variable and Newsreader Variable for the research instrument.

## Layout

The header, hero and footer cap at (1600px), with (56px) side padding. Inquiry caps at (830px); sculpture and instrument divider at (1050px); simulation controls at (870px). The laboratory caps at (1280px) and uses a (270px) summary beside a flexible inspector, separated by (42px).

- At (1500px) and above, the sculpture stage grows from (390px) to (430px).
- At (1000px) and below, side padding becomes (32px), stage height (360px), and the summary column becomes (210px) with a (26px) gap.
- At (700px) and below, side padding becomes (23px), header height (70px), display size (41px), and stage height (335px). Readouts move to the bottom of the stage; the canvas extends (32px) beyond each stage edge. The laboratory stacks, settings become one column, and the instrument footer becomes vertical.
- On phones, the question input uses (16px) actual input text. Profile tabs scroll horizontally; graph and comparison table retain horizontal scrolling. Metrics change from five columns to three. The WebGL camera uses a (52°) field of view below a (600px) renderer width and (43°) otherwise; particle density uses window width instead.
- The page has a (320px) minimum width. Spacing is component-specific; the extracted reusable values are in the frontmatter rather than an invented uniform scale.

### Approved landing extension · `/`

The landing wrapper caps at (1328px), with (56px) margins on ordinary desktop widths. It uses broad paired columns for copy and particle geometry, flat ruled specimens, and generous section gaps rather than a card grid. Main prose remains constrained by the line lengths in Typography.

- At (1600px) and above, the particle stage grows from (420px) to (470px) and the hero gains additional top space.
- At (1100px) and below, margins become (36px), the header becomes (92px) high, section gaps narrow, the particle stage becomes (360px), and the display changes to `clamp(50px, 5.75vw, 64px)`.
- At (800px) and below, margins become (24px), the header becomes (86px) high, navigation becomes a button-controlled drop-down, and major paired sections stack. The display becomes `clamp(49px, 8.5vw, 70px)` with (1.1) leading. The particle stage becomes (390px), capped by a (600px) specimen width. Policy tabs wrap; the policy description and horizontal path follow within the stacked panel.
- At (480px) and below, the display is (49px), the particle stage is (300px), hero actions stack, and the three-node illustrative path becomes vertical. The profile panel reserves a (410px) minimum height; titles and footer text reduce selectively. The pause button is (40px × 42px) minimum here; other state buttons retain (44px) minimum height.
- The page inherits the (320px) minimum width. Shared renderer density and camera width thresholds stay as documented for the incumbent particle geometry; the landing does not introduce a second renderer geometry.

Verification evidence covers widths (1440px), (1280px), (768px), (390px) and (320px), with no clipped text or document-width overflow recorded.

## Elevation & Depth

Interface surfaces have no shadows. Thin borders and modest tonal changes separate controls, archive, settings and inspection sections. Spatial depth belongs to the WebGL object: transparent additive points, perspective, overlap and bounded pointer parallax. There is no glow filter or backdrop blur.

**The Sculpture Depth Rule.** Keep interface chrome flat so the folded particle volume remains the source of spatial depth.

### Approved landing extension · `/`

The landing adds no interface shadows, glow filters or backdrop blur. Warm-paper sections change material tonally; one-pixel rules and stronger boundary strokes distinguish structures and control states. The hero volume remains live additive WebGL with overlap and parallax. A source SVG is the renderer's fallback, not a shipping raster composition.

## Shapes

The volume follows a deformed trefoil centerline with a variable-width tube, not a generic sphere. Seeded points create a continuous surface with irregular folds and openings. Small rounded rectangles define controls and graph nodes; the broader question field uses the field radius. Status dots and slider thumbs are circular. Sections and tabs rely on straight fine rules.

### Approved landing extension · `/`

The original Divergent Apertures mark keeps its three interrupted nested circular paths, current-color stroke, butt ends and rounded joins. Its (128 × 128) viewBox and (7px) stroke are preserved from the approved original geometry; no new logo variant replaces it. The header shows the mark at (40px), reducing to (36px) at the tablet breakpoint; the footer shows (32px).

Landing actions, simulation buttons and pause controls share the small `landing-control` radius. Other structural surfaces stay square and flat. Reasoning uses a circular outline, exploration a rotated square, and conflict an open angular outline; these shapes supplement the state labels and colors. Policy paths use outlined circular nodes joined by a thin rule, horizontally on wider surfaces and vertically on phones.

## Components

- **Primary action:** pale filled button with a thin border, (650) weight and darker text. Hover lightens its fill; disabled fill and border darken, with (.65) opacity. It sits within the question field.
- **Question field:** flex row, thin stroke and a (61px) minimum height. Focus within changes the stroke; the input remains visually unfilled. Phone minimum height is (58px).
- **Quiet and icon buttons:** quiet text actions brighten on hover. Square icon controls have a thin line border and darken their surface on hover. Global disabled controls use (.42) opacity unless a component overrides it.
- **Navigation and profile tabs:** flat text with a one-pixel active underline. Mode simulation buttons add a subtle filled selected state and line border. Research view tabs use a fine text underline.
- **Archive and settings:** shallow tonal containers with modest rounding. Archive rows use dividers; settings use a three-column desktop grid. Detailed research content uses flat separated sections.
- **Delta slider:** a two-pixel track with the filled segment set by the current value and a small circular thumb. It expands across the available phone width; disabled state dims it.
- **Argument graph:** three typed node columns, rounded (170px × 46px) nodes and curved edges. Active nodes use their type color as stroke; rejected nodes use a dashed warm stroke. Nodes support pointer and keyboard selection.
- **Particle topology:** (54,000) points on larger viewports and (25,000) below a (600px) window width, sampled deterministically. Camera field of view responds separately to renderer width as described in Layout. Curiosity extends ridges, attention compresses them, uncertainty perturbs points, conflict separates poles and warms a region, insight lightens a coherent region, and collapse dissolves a fold. State changes damp exponentially; time flow stops when paused or reduced motion is requested. Manual simulation supports keys (1–6) and a (6500ms) cycle, and is visibly labeled.
- **Comparison metrics:** compact flat columns with tabular values and visible limitations. Argument diversity and conclusion similarity use local Nomic embeddings after successful final similarity analysis; live values and failed analysis retain the lexical fallback. The argument label changes from “Lexical argument diversity” to “Semantic argument diversity” when the semantic basis is present. Branch deduplication remains lexical.
- **Focus:** two-pixel cool outline with a (5px) offset; the question input uses its parent stroke for focus. Reduced motion removes CSS animation/transitions and smooth scrolling while retaining state changes.

### Verified laboratory extension · `/app`

Source verification of `src/App.jsx`, `src/Laboratory.jsx`, `src/ResearchDossier.jsx`, `src/Intelligence.jsx` and `src/styles.css` confirms an extension of the approved world. Research surfaces retain their unprefixed colors, Manrope controls, Newsreader headings, flat rules and compact readouts. The approved APORIA symbol (`brand/aporia/assets/logos/symbol-light.svg`) replaces the laboratory mark at (32px), reducing to (28px) below (700px), beside a spaced Manrope wordmark. The particle renderer explicitly receives `palette="obsidian"`, reusing the approved iris/cyan/amber/paper shader palette without changing research text or readout colors.

- **Research dossier:** a flat, (74ch) maximum-width record separates current-hypothesis coverage, evidence boundaries, warnings and open questions. Native disclosures expose seed, memory origin, model/code/initial-state fingerprints and compute usage. Newsreader headings use (27px); body and register text use (12px), increasing to (13px) on phones. Two-column registers stack below (700px); fingerprints wrap. Warm warnings reuse `graph-counterexample` (`#d9aa77`); no new global color or type scale is introduced.
- **Reproduction setup and memory:** a bounded numeric seed field and fresh/prior memory selector extend the existing settings container. The setup note and memory inspector distinguish controlled fresh state from prior learning; legacy records show an explicit missing-protocol explanation rather than invented coverage.
- **Research navigation and recovery:** view buttons use (44px) minimum height and retain the active fine underline. The final (700px) rule wraps view buttons with `gap: 0 20px` and visible overflow. Profile tabs still scroll. An in-flow, ruled status notice exposes “Open active research” for a running or paused record; its action is (44px) minimum height and the notice stacks on phones. Source behavior loads the existing record, including recovery from an `activeSessionId` response.
- **Motion:** inspector content enters with opacity (.55 → 1) over (180ms), using `cubic-bezier(.16,1,.3,1)`; reduced motion removes it. Shared WebGL rendering uses `never` outside the visibility intersection (with a 60px observer margin) or in a hidden document, `demand` when paused/reduced motion is active, and `always` otherwise. Demand rendering retains explicit state updates and stops scheduling once uniforms settle.

**Verification boundary:** this section records source behavior, not measured runtime performance, visual overflow or contrast results. The (44px) target is component-specific: mobile research icon controls and profile buttons meet it, but mobile particle pause and quiet controls retain (36px) minima and desktop icon controls remain (34px). These incumbent size differences and the older generic sidecar previews are recorded without broadening this extension into a redesign.

### Compatible discovery extension · `/app`

Paper discovery extends the existing research instrument with the same near-black canvas, pale ink, muted readouts, warm warnings and fine rules. `src/DiscoveryPanel.jsx` and `src/discovery.css` reuse the unprefixed research colors and shared controls; Newsreader remains the heading and quotation face, and Manrope remains the interface and prose face. This is an ordinary desktop extension of the Particle observatory world, with no new palette, raster assets or global token scale.

- **Directions and brief reader:** an ordered, divided list sits beside a flexible reading column. The desktop grid uses a minimum (240px) list, a (1:2.5) column relationship and a (40px) gap. Selected directions use the existing surface fill and pale ink. The brief wrapper uses (14px) text so its (75ch) maximum width follows the prose size; paragraphs use (1.8) leading and preserve line breaks. Newsreader brief titles use (26px), while source quotations use (18px) with a fine left rule. These are component-specific reading values rather than replacements for the compact research body token.
- **Inspection hierarchy:** Directions, Papers, Debates and Research log reuse the existing flat view controls. Brief sections use generous top spacing and a single rule; score labels remain muted and values use tabular numerals. Published premises, original proposals and detailed assessment reasons use native disclosures. The existing Laboratory follows discovery inside “Inspect cognitive trajectories and experiments,” keeping deeper inspection secondary to the reader.
- **Source and record controls:** paper records and debate trials use ruled disclosures with readable prose. Brief downloads and research export reuse quiet text actions and thin SVG icons. Live pause/resume and stop reuse the incumbent bordered icon buttons. Model limitations and ranking exclusions reuse the warm warning treatment, alongside textual state labels.

**Desktop evidence boundary:** the recorded upstream browser fixture is the sole rendered evidence for this extension. The final correction review marks both the completed “Unranked” label and the brief width correction resolved, with disposition `ship`. It does not establish a newly generated local research result, a new full audit or mobile responsiveness. The frontmatter and existing `.impeccable/design.json` are preserved; their previews remain the incumbent component catalogue.

### Approved landing extension · `/`

- **Original signature:** the inline Divergent Apertures SVG pairs with the semibold APORIA wordmark. It inherits warm paper on obsidian and obsidian on paper, without a raster logo or ornamental container.
- **Laboratory actions:** the primary action is warm paper on obsidian; the closing action reverses to obsidian on paper. Both use semibold `landing-control` type, (14px 22px) padding, a (52px) minimum height, a thin matching border and the small landing radius. Hover uses the corresponding documented tonal fill; a fine arrow indicates entry to (`/app`).
- **Text links and navigation:** plain Source Sans labels pair with thin SVG arrows where appropriate. Hover underlines text. The desktop header is horizontal with a fine bottom rule; at the tablet breakpoint the (44px) menu toggle exposes a stacked menu aligned beneath the header. Escape and selecting a link close it.
- **Visual state controls:** three labeled simulation buttons carry the iris/cyan/amber meanings and corresponding outlined shapes. Selected state adds `landing-surface` fill and a boundary stroke; hover adds the same fill. A separate bordered pause/resume control sits alongside them. State explanations update in a live region and always identify the interaction as visual simulation.
- **Policy specimen:** an open, ruled container on warm paper contains the common question, five neutral policy tabs and a changing three-step illustrative path. Selected tabs use semibold ink and a (2px) underline; hover uses the paper hover tone. Arrow keys, Home and End move the active tab; one panel exposes the selected policy's description and ordered path. Tabs wrap at the tablet breakpoint and the path becomes vertical at the phone breakpoint. The record is visibly labeled illustrative.
- **Method steps:** flat numbered rows with tabular numerals, semibold titles, readable muted prose and fine separators. No cards or artificial elevation surround them.
- **FAQ:** native disclosure rows use readable Source Sans summaries, fine bottom rules and plus/minus SVGs. Hover changes summary text to iris; open answers use muted text with generous leading.
- **Focus and motion:** a (2px) cyan outline with a (6px) offset marks keyboard focus and automatically uses the darker cyan on paper. Action fill, text and border changes transition over (.15s). Reduced motion removes CSS transitions and smooth scrolling and stops time-driven particle flow; explicit state changes and pause remain usable. The shared renderer also stops drawing while the landing specimen is offscreen.

## Do's and Don'ts

### Do:

- Do retain folds, cavities and asymmetry in the particle object at desktop and phone sizes.
- Do use warm colors for conflict, objections, counterexamples and failure; use pale light for insight.
- Do keep numeric readouts tabular and research inspection visually secondary.
- Do preserve visible keyboard focus, reduced-motion behavior and explicit simulation labels.

- Do keep landing-prefixed interface tokens and APORIA font aliases scoped to (`/`); the approved `/app` particle adaptation explicitly reuses the shader palette.
- Do preserve the original Divergent Apertures SVG geometry and its spaced APORIA wordmark.
- Do use darker accent and muted-text tokens on warm paper, and keep policy identities neutral.
- Do retain explicit simulation and illustrative-workflow labels, visible focus, pause and reduced-motion behavior.

### Don't:

- Don't replace the particle topology with a generic sphere, robot avatar or chat interface.
- Don't add neon HUD decoration, ornamental dashboard chrome or fixed overlays.
- Don't present manually selected visual states as measured cognition.
- Don't introduce raster art for the parametric particle object.
- Don't replace research-app tokens or typography with the landing extension without a separate approved scope.
- Don't turn cognitive-state colors into fixed profile-identity colors on the landing.
- Don't replace the live folded geometry or its SVG fallback with a shipping raster illustration.
