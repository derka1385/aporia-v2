# APORIA — color study

The original **Divergent Apertures** logo is the retained reference. This exploration changes color only. The current application and the original brand proposal are separate from this review surface.

Open `index.html` to compare three palettes, two surfaces and five cognitive states. The controls update the logo’s neutral color, particle-region colors, example interface and calculated contrast table together. The particle geometry is identical across palettes and is explicitly labeled illustrative.

**Recommendation: Obsidian & Iris.** It balances warm reading surfaces with precise cognitive accents. Graphite & Mineral is cooler and more technical. Ink & Parchment is warmer and more editorial. These are proposals, rather than a recorded user color choice.

The logo remains a single neutral color. Reasoning uses iris; exploration uses cyan; conflict and candidate insight use amber with different symbols and explicit labels. Uncertainty and divergence use geometry and values rather than extra hues. Avoid assigning those colors to profile identities or graph node types.

`palettes.json` lists exact values. Each palette has a CSS export in `assets/`. `CONTRAST.md` documents all 72 checked pairs. The comparison PNG and individual selected-palette preview PNGs are browser renders of this review surface.

`build.py` reuses existing SVG masters and writes only files in this colors folder. It does not import or execute the original brand builder. No new fonts, dependencies or application changes are required.
