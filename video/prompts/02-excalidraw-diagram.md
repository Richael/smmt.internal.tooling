# Prompt 02 — Excalidraw diagram doc

**Use when:** you want to (re)generate or restyle the diagram document from `loops.json`.

The deterministic generator `video/excalidraw/build-excalidraw.mjs` already produces a valid
`.excalidraw` file (title + legend + one card per loop with the lavender return arrow). Prefer
editing that script for structural changes. Use the prompt below when you want an AI to
**redesign** a card layout or hand-author a richer single-loop diagram.

---

```
You produce Excalidraw scene JSON (schema: { type:"excalidraw", version:2, elements:[...],
appState:{viewBackgroundColor:"#ffffff"}, files:{} }).

Draw ONE diagram for the loop below. Requirements:
- A node (rounded rectangle) per system in `systems`, coloured per the legend:
  Shopify #95BF47, Klaviyo #1A1A1A, Meta/IG #0866FF, Amazon #FF9900, smmt #7C5CFF.
  Dark nodes (Klaviyo, Meta, smmt) use #ffffff label text.
- Forward arrows (#6B7280) connecting the systems in `systems` order, each labelled with the
  matching leg from `legs` (short — 3–6 words).
- A LAVENDER (#B7A8F2, thick) return arrow from the last node back to the first, labelled with
  `closes` — this is the loop-closing step and must be visually distinct.
- A title with the loop id + `short`, and a caption line: "closes on {closes} · {segment} · {latency} · {section}".
- Lay it out as a clean cycle (ring) when systems.length ≥ 3; left-to-right + return arc otherwise.
- Every element needs: id, type, x, y, width, height, angle:0, strokeColor, backgroundColor,
  fillStyle, strokeWidth, strokeStyle, roughness:1, opacity:100, groupIds:[], seed, version:1,
  versionNonce, isDeleted:false. Text elements add: text, fontSize, fontFamily:1, textAlign,
  verticalAlign, originalText, lineHeight:1.25. Arrows add: points:[[0,0],[dx,dy]],
  endArrowhead:"arrow", roundness:{type:2}.
- Output ONLY the JSON.

LOOP:
<<< paste one loop object from loops.json >>>
```
