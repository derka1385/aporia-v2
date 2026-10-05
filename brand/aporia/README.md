# APORIA identity proposal

Open **index.html** in a browser for the complete illustrated, 18-part proposal. It works offline. **overview.html** is the compact overview board. **PROPOSAL.md** is the authoritative written proposal.

The recommended identity is **Divergent Apertures**: three open concentric paths with a common center and staggered openings. Public name: **APORIA**, as supplied in the brief.

## Contents

- `PROPOSAL.md` — all 18 requested topics, including a complete evaluation of ten concepts.
- `index.html` — visual brand book, chapter navigation, light/dark logo comparison and size previews.
- `overview.html` — compact identity board.
- `applications.html` — static website, dashboard and 16:9 presentation studies.
- `assets/visuals/brand-overview.png` — rendered identity board.
- `assets/visuals/logo-contact-sheet.svg` and `.png` — ten logo constructions in monochrome.
- `assets/logos/concept-*.svg` — each concept as an individual vector file.
- `assets/logos/symbol-*.svg` — standard and micro masters in dark and light.
- `assets/logos/lockup-*.svg`, `wordmark-*.svg` — outlined, portable letters with no font dependency.
- `assets/logos/app-icon.svg` and `app-icon-{192,512,1024}.png` — square platform masters.
- `assets/logos/favicon.ico`, `favicon-{16,32,48}.png` and `favicon-adaptive.svg` — browser assets.
- `assets/visuals/particle-*.svg` — six deterministic, illustrative folded particle surfaces.
- `assets/visuals/*-study.png` — rendered website, dashboard and presentation studies.
- `assets/fonts/` — official open-source fonts, WOFF2 conversions and license notices.
- `tokens.json`, `tokens.css` — proposed primitives and semantic theme mappings.
- `CONTRAST.md` — calculated contrast ratios and usage limits.
- `VERIFICATION.json` — browser checks at 1440, 768 and 390 px.
- `aporia-brand-proposal.zip` — portable proposal and asset pack.

## Status and scope

The assets are a concrete identity **proposal**. They have not been applied to the running laboratory. Website, dashboard, particle and slide examples are labeled studies or illustrations; none represent experimental findings. The proposal uses APORIA, while existing application files retain their provisional Aproria name.

Concept 02 is the master recommendation. Concept 03 supplies a potential displacement rule for supporting compositions; concept 09 supplies a sampling rule for particle imagery. Those rules are not alternate production logos. The fixed symbol does not animate with Δ.

## Verification and design review

All 18 chapters and ten concepts are present. The book has no page-level overflow or broken image resources at the three checked widths. Logo background and size controls work; no browser script errors were reported. All 22 prescribed text, accent and control-boundary pairings pass their stated WCAG contrast threshold at full opacity. The smallest text pairing is 4.86:1; primary paper/obsidian text is 16.36:1. This is verification of the proposal assets, not a full product accessibility audit.

Design hook findings were triaged: small labels were enlarged to at least 12 px, with explanatory body text generally 14 px or larger. Three font-rule exceptions were deliberately scoped to `brand/aporia/applications.html` because this isolated proposal evaluates a new type system documented in section 07. No whole-file or whole-rule ignore was added. A subsequent review added explicit insets for navigation and the particle panel, set comfortable default leading, and corrected the dashboard heading hierarchy. Browser-computed leading confirmed all ordinary text is at least 1.35×; only the large editorial headings use tighter display spacing. A tight-leading exception is scoped to this application-study file for that intentional display treatment and the static detector’s unobserved 1.28× report. None of the reported mechanical findings remains unresolved.

## Sources and font licensing

Font binaries were downloaded from their official repositories on 4 October 2026. The associated OFL license notices are bundled in `assets/fonts/` and must accompany redistribution.

- [Adobe Source Serif](https://github.com/adobe-fonts/source-serif) and [official specimen](https://adobe-fonts.github.io/source-serif/).
- [Adobe Source Sans](https://github.com/adobe-fonts/source-sans).
- [IBM Plex](https://github.com/IBM/plex).
- [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Rebuilding

`source/build.py` creates vector geometry, outlines the wordmark, converts local fonts to WOFF2, computes contrast, writes tokens and renders the proposal HTML from PROPOSAL.md. It requires Python with FontTools and Brotli, declared in `source/requirements.txt`.

`source/render.mjs` rasterizes the local assets and verifies the book with the existing project Playwright dependency. It launches a separate temporary browser profile. Set `APORIA_BROWSER_PATH` if Google Chrome is installed somewhere other than `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

Run the builder first, then the renderer. Recreate the ZIP after changes, excluding the ZIP itself. No app dependency or application source change is needed to view the proposal.
