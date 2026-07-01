# OpenClaw extraction playbooks

Paste a playbook's prompt into OpenClaw. It calls the named MCP tool and **saves the raw
result** to `data/raw/<source>.<tool>.json` in the envelope shape below. Then run
`make normalize` (see `tools/extractors/`).

**Every prompt ends with the same save instruction** so the normalizer can read it:

> Save the raw tool result to `data/raw/<source>.<tool>.json` as JSON in the shape
> `{"source":"<source>","tool":"<tool>","data": <the raw result> }`. Do not summarize or
> reshape it — write the tool's output verbatim under `data`.

Rules:
- Name the server in the prompt (e.g. *"use apollo to…"*) so OpenClaw routes correctly.
- Read-only/safe servers only here (apollo, hubspot, youtube). Anything that spends money or
  posts stays out of automated extraction.
- These are test keys — still keep volume sane and one session per scraping cookie.
