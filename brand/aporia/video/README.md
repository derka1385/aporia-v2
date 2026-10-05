# APORIA — one-minute motion film

English explanatory film, 1920 × 1080, 30 fps, exactly 60 seconds. Open `index.html` for the local player, captions, downloads and transcript. The MP4 plays independently of the project.

The film explains the current repository's research-directions finder: philosophy students need to identify a tractable question; plausible AI answers can repeat prior objections or omit assumptions; APORIA reconstructs arguments, varies cognitive policies, checks the literature, runs two independent defenses, verifies citations, learns which trial to run next, and exports ranked research briefs. It describes an experimental workflow and retains human assessment. The diagrams and sample brief are illustrations, not reported experiments.

## Identity

The retained **Divergent Apertures** symbol and outlined wordmark are rasterized directly from the existing SVG masters. The symbol keeps its geometry and neutral color; Δ only changes the illustrated investigation paths. Typography uses the bundled Source Serif 4, Source Sans 3 and IBM Plex Mono fonts. Colors come from the original brand proposal's Obsidian & Iris tokens; this film does not record a new palette selection or alter the running laboratory.

The folded particle object is a deterministic CPU port of `src/Intelligence.jsx`'s trefoil shader. No generated image, stock image or generic sphere replaces it. Motion is authored frame by frame with the Animate skill's ease-out `(0.23, 1, 0.32, 1)` and ease-in-out `(0.77, 0, 0.175, 1)` curves. The logo fades into place; the paths separate with Δ; argument edges build; signals pass through checks; the Director's learning loop closes. The player has native pause, seeking, captions and no autoplay.

## Sound

English UK narration uses the installed macOS **Daniel** synthetic voice. The stereo ambient score and transition chimes are composed procedurally, without stock recordings or third-party music. The final soundtrack is normalized to −16 LUFS with a −1.5 dBTP ceiling. `assets/voiceover.wav` and `assets/original-score.wav` are separate edit stems.

## Exports

- `exports/APORIA-60s-No-Voice-1080p.mp4`: finished motion with music only, ready for the user's live narration; no synthetic voice or narration-caption track.
- `APORIA-speaking-script.md`: English script with eight scene timings.
- `exports/soundtrack-music-only.wav`: quiet music master at −27 LUFS for speaking over.
- `exports/APORIA-60s-English-1080p.mp4`: H.264 / AAC, 16:9, 60 seconds.
- `exports/aporia-en.srt` and `.vtt`: timed English narration captions.
- `exports/soundtrack.wav`: 48 kHz stereo master.
- `exports/poster.jpg`: title image.
- `exports/storyboard.jpg` and `scene-*.jpg`: eight keyframes.
- `source/timeline.json`: editable English copy and chapter timing.
- `source/build.py`: editable motion, composition and sound renderer.

## Product sources

Read on 4 October 2026 at repository tree `1d04fb4004a64b65644d465c9c63adcf42cf250b`:

- [Repository README](https://github.com/derka1385/APORIA/blob/1d04fb4004a64b65644d465c9c63adcf42cf250b/README.md): unified discovery loop, five profiles, Δ, citation verification and ranked briefs.
- [Directions README](https://github.com/derka1385/APORIA/blob/1d04fb4004a64b65644d465c9c63adcf42cf250b/directions/README.md): intended users, source-grounded reconstruction, two defenders, referee, Director, Assessor and limits.
- [Cognitive profiles](https://github.com/derka1385/APORIA/blob/1d04fb4004a64b65644d465c9c63adcf42cf250b/directions/crux_lab/lab/aporia_profiles.py): actual policy interpolation.
- Local `../DECISIONS.md`, `../tokens.json` and existing logo masters: retained identity.

## Rebuild

The renderer requires Python with NumPy and Pillow, local Chrome with Playwright for initial SVG rasterization, macOS `say`, and FFmpeg. This machine already supplies these dependencies. No network is needed to rebuild.

```sh
node brand/aporia/video/source/render-assets.mjs
python3 brand/aporia/video/source/build.py --stills
python3 brand/aporia/video/source/build.py --audio
python3 brand/aporia/video/source/build.py --render
python3 brand/aporia/video/source/build.py --music-only
```

For the captioned browser player, run `python3 brand/aporia/video/source/serve.py` and open `http://127.0.0.1:8767/`. This preview server supports byte-range requests for reliable seeking. It binds only to localhost and serves only this video folder.

Use the Python environment with NumPy/Pillow installed. `APORIA_FFMPEG` overrides the FFmpeg binary path. Default: the existing bundled binary at `/Applications/ClipGrab.app/Contents/MacOS/ffmpeg`.

## Verification

`exports/layout-verification.json` records text-bound checks across settled and intermediate animation frames. `exports/audio-verification.json` records each voice segment's duration and tempo. `exports/video-verification.json` records final encoding, duration, frame count, caption coverage, decoding and representative frame checks.

The final MP4 passes a full decode: 1,800 frames, 30 fps, 60 seconds of picture, H.264, English AAC audio and English soft captions. Desktop/mobile player layout, media metadata, caption loading and playback were verified. Browser seeking exposed the basic preview server's missing byte-range support, which was fixed in `source/serve.py`. Restarting that improved server was not executed because automatic approval review reached its usage limit. Final browser confirmation of seeking remains pending; `exports/player-verification.json` records that limitation. The standalone MP4 is complete and independent of this preview server.

Design review: particle framing, profile-label entry and short caption fragments were corrected. The player's existing brand-book fonts, colors and readable text sizes use narrow, file-scoped detector exceptions in `.impeccable/config.json`. No laboratory design tokens or logo masters were changed.
