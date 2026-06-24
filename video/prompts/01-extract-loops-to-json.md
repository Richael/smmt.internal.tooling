# Prompt 01 — Extract a playbook into `loops.json`

**Use when:** you have a new adopter's closed-loop playbook (`.docx`/`.pdf`/markdown) and need
the structured data that drives every downstream artifact.

**Input:** the full playbook text (paste it, or give the file path).
**Output:** a single `loops.json` matching the schema in `video/data/loops.json`.

---

```
You are turning a closed-loop marketing-architecture playbook into structured JSON.

Read the playbook below. Produce ONE json object with this exact shape:

{
  "meta": { "title", "subtitle", "source", "tagline", "principles": [ ... ] },
  "legend": { "<systemKey>": { "label", "color" }, ... },
  "loops": [
    {
      "id": <int, 1-based>,
      "title": "<short title>",
      "short": "<the full section title, incl. any [B2B-critical] tag>",
      "systems": ["<systemKey>", ...],   // ORDER = the flow order in the loop
      "closes": "<what closes the loop — from the 'at a glance' table>",
      "segment": "Both | B2C-heavy | B2B-critical",
      "latency": "<return latency from the table>",
      "section": "<§ reference>",
      "objective": "<one sentence>",
      "trigger": "<the trigger leg>",
      "legs": ["<leg a>", "<leg b>", ...],   // plain language, drop code
      "edge": "<the 1-2 highest-signal edge cases / failure modes>"
    }
  ]
}

Rules:
- systemKey ∈ {shopify, klaviyo, meta, amazon, multi, smmt}. Reuse the legend colours from
  video/data/loops.json unless the playbook defines a different palette.
- `systems` order must reflect how data actually moves in that loop (the chips will be drawn
  and animated in this order, then a return arrow closes back to the first).
- Keep `legs` to the essential steps; strip GraphQL/REST snippets — those live in the playbook.
- Preserve the playbook's governing principles verbatim-ish in meta.principles.
- Output ONLY the JSON. No prose.

PLAYBOOK:
<<< paste playbook text here >>>
```
