# A1 — Persona + target lists (visible in UI + export)

**Goal:** turn a reusable persona spec into an enriched, grouped, exportable target list.
**Server:** `apollo`.

## Reality check (what Apollo's MCP can/can't do)

Apollo's MCP **cannot** create a saved *List* object or a *Persona* template, and has no Bombora
intent filter (root README, "What does NOT work"). So:

- **Persona** = a YAML filter spec in `personas/` (e.g. `personas/icp-example.yaml`), replayed into
  `search_people`.
- **"List you can see in the UI"** = create the matched people as **contacts** and apply a **label**
  (`create_label` + `bulk_create_contacts` with that label). Labels and contacts are visible in the
  Apollo UI and act as the groupable list.
- **Export** = write the enriched rows to `data/exports/`.

## Steps (prompts)

> 1. "Use apollo `search_people` with these filters: titles VP/Director of Marketing & Head of
>    Growth, seniority vp/director/head, location United States, company 50–500 employees in
>    software/IT. Show me the count and the first 25." *(search is free)*
> 2. "Use apollo `get_organization_job_postings` to keep only companies that posted a marketing
>    hire in the last 30 days." *(hiring signal)*
> 3. "Use apollo `enrich_person` (or `bulk_enrich_people`) on the top 100 for verified work
>    emails." *(~1 credit each — prospect first, enrich last)*
> 4. "Use apollo `create_label` named 'ICP — SaaS Marketing Leaders', then `bulk_create_contacts`
>    for those 100 with that label so they show as a group in the UI."
> 5. "Export the enriched list to `data/exports/apollo-saas-marketing-leaders-<today>.csv` with
>    columns: first_name,last_name,title,company,email,linkedin_url,label."

## Output

`data/exports/apollo-<persona.slug>-<YYYY-MM-DD>.csv` + a label/contact group visible in Apollo.

## Notes

- `search_people` is FREE; `enrich_person` costs credits — always filter to the final set before
  enriching. `get_api_usage_stats` (free) shows remaining credits.
- Re-run for a new ICP by copying `personas/icp-example.yaml` and changing the filters; the
  prompts are otherwise identical (that's the reuse).
