# Event-loop video pipeline

A reusable pipeline that turns an adopter's **closed-loop playbook** into an explainer-video
package: an Excalidraw diagram doc, a narrated MP4, and a YouTube publish post — all driven by
one structured file, `data/loops.json`.

First run is **Parker (adopter #001)** — SMMT's *Twelve Compounding Closed Loops* across
Shopify · Klaviyo · Meta/IG · Amazon (source: `Adopters/playbooks--001.parker.docx`).

```
data/loops.json ──┬─► excalidraw/build-excalidraw.mjs ─► parker-twelve-loops.excalidraw   (diagram doc)
                  ├─► narration/scripts.md ─► build-narration.sh ─► public/narration/*.m4a + durations.json
                  ├─► remotion/ (LoopScene × 12 + Intro/Outro) ─► out/twelve-loops.mp4     (the MP4)
                  └─► youtube/post.md  (title · description · chapters · tags)
```

## Deliverables (this run)

| Deliverable | File |
|---|---|
| Excalidraw document | `excalidraw/parker-twelve-loops.excalidraw` (open at excalidraw.com or the VS Code/desktop app) |
| Narration | `narration/scripts.md` → rendered to `remotion/public/narration/*.m4a` (~5:37) |
| MP4 | `remotion/out/twelve-loops.mp4` (after `npm run render`) |
| YouTube post | `youtube/post.md` (chapters match the render) |
| Reusable prompts | `prompts/00..05` — re-run the whole pipeline for any future adopter |

## Build / regenerate

```bash
# 1. diagram doc (any OS)
node video/excalidraw/build-excalidraw.mjs

# 2. voiceover  (macOS — uses built-in `say`; no API keys)
bash video/narration/build-narration.sh
#    override the voice:  VOICE="Ava (Enhanced)" RATE=175 bash video/narration/build-narration.sh

# 3. the MP4
cd video/remotion
npm install
npm run studio     # live preview / scrub
npm run render     # -> out/twelve-loops.mp4
```

## Design notes

- **Single source of truth.** Everything reads `data/loops.json`. Edit a loop there and every
  artifact regenerates consistently — that's what makes the pipeline reusable.
- **Colour legend is 1:1 with the source diagrams:** Shopify `#95BF47`, Klaviyo `#1A1A1A`,
  Meta/IG `#0866FF`, Amazon `#FF9900`, smmt `#7C5CFF`, loop-closing return `#B7A8F2` (lavender).
- **Timeline stays in sync.** `build-narration.sh` writes `durations.json`; the Remotion
  timeline (`src/timeline.ts`) and the YouTube chapters are both derived from it, so audio,
  visuals, and chapters never drift.
- **Voice.** Default is macOS `say` (free, offline). Swap in a premium voice (the `fal` MCP we
  added, or ElevenLabs) by replacing the `say` call in `build-narration.sh` — durations.json
  regenerates either way.

## Reuse for the next adopter

1. Extract their playbook with `prompts/01-extract-loops-to-json.md` → new `data/loops.json`.
2. Regenerate narration scripts (`prompts/03`) and run steps 1–3 above.
3. Generate the YouTube post (`prompts/05`) with the fresh timecodes.
