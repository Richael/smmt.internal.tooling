# Extractors — raw MCP output → normalized data points

OpenClaw-driven extraction, Python normalization.

```
OpenClaw  ──calls MCP tools──▶  data/raw/<source>.<tool>.json   (raw, via a playbook)
                                        │
python3 normalize.py  ──maps──▶  data/normalized/<entity>.jsonl (+ .csv, _summary.json)
```

- **OpenClaw** does the extraction (it has the API keys via `bws run`, and writes files).
- **`normalize.py`** does the deterministic mapping — **no secrets, no network**, stdlib only.
  It just reads the raw files OpenClaw saved.

## Run it

```bash
# 1) extract: paste a playbook prompt (tools/playbooks/*.md) into OpenClaw.
#    OpenClaw calls the tool and saves data/raw/<source>.<tool>.json
# 2) normalize:
make normalize                      # data/raw -> data/normalized  (+ CSV)
#   or:  python3 tools/extractors/normalize.py --input data/raw --out data/normalized --csv
```

## The raw-file contract

OpenClaw saves each tool result as JSON in this **envelope**:

```json
{ "source": "apollo", "tool": "search_people", "data": { "...": "the raw tool result" } }
```

A file may also hold a **list** of envelopes, or a **bare** result if named
`<source>.<tool>.json` (source/tool are then inferred from the filename).

## Normalized record

```json
{
  "entity_type": "person",
  "id": "p1",
  "source": "apollo",
  "source_tool": "search_people",
  "attributes": { "email": "...", "full_name": "...", "title": "...", "company": "..." },
  "extracted_at": "2026-06-22T16:36:55Z",
  "schema_version": "1.0"
}
```

## Entity types → target data points

| entity_type | target data point |
|---|---|
| `person`, `organization` | customers / customer information |
| `transaction` | transaction history |
| `behavior_event` | behavior |
| `event` | events |
| `ticket` | ticketing |
| `inventory_item` | merch or inventory |
| `audience` | audiences |
| `segment` | segments |
| `campaign` | campaigns / pushes |
| `lookalike` | lookalike functionality |

## Coverage today (read-only / safe servers first)

| Source | Tools mapped | → entity types |
|---|---|---|
| **apollo** | `search_people`, `search_contacts`, `enrich_person`, `bulk_enrich_people`, `get_contact`, `search_organizations`, `enrich_organization`, `get_organization`, `search_accounts`, `search_opportunities`, `get_opportunity`, `get_organization_job_postings`, `search_activities` | person, organization, transaction, behavior_event |
| **hubspot** | `*contacts*`, `*companies*`, `*deals*`, `*emails*`/`*campaigns*`, `*lists*`, `*events*` | person, organization, transaction, campaign, segment, behavior_event |
| **youtube** | `*channel*`, `*video*`/`*search*`, `*comment*` | organization, audience, behavior_event |

Adding a source = drop `mappings/<source>.py` exposing `records(tool, data)` and register it
in `normalize.py`'s `REGISTRY`. Meta-Ads / X / LinkedIn mappers come next (audiences, segments,
campaigns, lookalike) — but those touch ad spend or scraping, so they stay opt-in.

## Validate without live keys

`tools/extractors/examples/raw/` holds sample raw payloads. Run:

```bash
python3 tools/extractors/normalize.py --input tools/extractors/examples/raw --out /tmp/norm --csv
```
