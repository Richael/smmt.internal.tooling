# G2 — Send templated email to an Apollo list

**Goal:** email an Apollo-built audience with a merged template.
**Servers:** `apollo` → `gmail`. Builds on **A1** + **G3**.

## Steps

> 1. Run **A1** to export the enriched list to
>    `data/exports/apollo-<persona>-<today>.csv` (columns include `email`, `first_name`, `company`).

```bash
# 2. DRY RUN over the Apollo export
node playbooks/gmail/merge/render.mjs \
  --template playbooks/gmail/templates/email.example.md \
  --list data/exports/apollo-<persona>-<today>.csv
```

> 3. Review the preview, then **G3 step 3** to send via Gmail in batches.

## When to use Gmail vs an Apollo sequence

| Use Gmail (G2) | Use an Apollo sequence (A3) |
|---|---|
| Small, high-intent, near-1:1 sends | Multi-step cadences at volume |
| You want it from your real inbox | You want built-in opens/replies tracking (A2) |
| One-off | Repeatable lane you'll compare (A4) |

## Notes

- Only email **enriched** rows with a verified `email` — Apollo `search_people` results aren't
  enriched until you run `enrich_person`/`bulk_enrich_people` (A1 step 3). Unverified = bounces.
- Same throttling/consent rules as G3.
