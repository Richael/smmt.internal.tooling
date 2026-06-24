# Event-loop video pipeline — reusable prompts

These prompts turn any adopter's **playbook** (a closed-loop / event-loop architecture doc,
e.g. `Adopters/<name>/playbooks--NNN.<name>.docx`) into a full explainer-video package:

```
playbook.docx
   │  prompt 01  → extract
   ▼
data/loops.json            ← single source of truth
   ├─ prompt 02 → excalidraw/<name>.excalidraw      (diagram doc deliverable)
   ├─ prompt 03 → narration/scripts.md              (voiceover, one block per loop)
   ├─ prompt 04 → remotion/src/scenes/*             (animated MP4 sections)
   └─ prompt 05 → youtube/post.md                   (title, description, chapters, tags)
```

## House style (apply in every prompt)

- **Audience:** a smart new SMMT engineer or a technical client stakeholder. Explain the
  *why a loop compounds*, not just the API calls.
- **Tone:** crisp, confident, concrete. Short sentences. No hype words ("revolutionary",
  "seamless"). Name the systems explicitly (Shopify, Klaviyo, Meta/IG, Amazon).
- **Visual identity (the legend — keep colours 1:1 with the source diagrams):**
  - Shopify `#95BF47` · Klaviyo `#1A1A1A` · Meta/IG `#0866FF` · Amazon `#FF9900`
  - Multi-channel `#6B7280` · smmt core `#7C5CFF` · loop-closing return `#B7A8F2` (lavender)
- **The one non-negotiable idea:** a *closed loop* = data leaves one system, is acted on in
  another, and **returns** as a converted customer or enriched signal — so each cycle improves
  the next. Every artifact must show the lavender **return** step.
- **Governing principles** (from the playbook) constrain the story — especially the
  walled-garden rule (audiences only flow *outbound* to Meta) and the Amazon wall (no email
  egress). Never imply membership can be pulled back out.

## How to run the whole thing

```bash
node video/excalidraw/build-excalidraw.mjs     # regenerate the diagram doc
bash video/narration/build-narration.sh        # render voiceover (macOS `say` → m4a)
cd video/remotion && npm install && npm run render   # render the MP4
```
