# Playbook — Apollo: people & organizations

**Servers:** `apollo` (read-only: `search_people` is free; `enrich_person` costs ~1 credit).
**Produces:** `person`, `organization` records → *customers / customer information*.

## Prompt (people)

> Use **apollo** `search_people` to find VP or Director of Marketing at US B2B SaaS companies
> with 50–500 employees. Return the first 100 results. Then save the raw tool result to
> `data/raw/apollo.search_people.json` as JSON in the shape
> `{"source":"apollo","tool":"search_people","data": <the raw result> }` — write the tool's
> output verbatim under `data`, do not summarize or reshape it.

*(Enrich only what you need — `search_people` is free, `enrich_person` costs a credit.)*

## Prompt (organizations)

> Use **apollo** `search_organizations` for US B2B SaaS companies, 50–500 employees, and save
> the raw result to `data/raw/apollo.search_organizations.json` in the same envelope shape.

## Then

```bash
make normalize     # -> data/normalized/person.jsonl, organization.jsonl (+ .csv)
```
