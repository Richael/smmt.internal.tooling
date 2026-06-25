# Playbooks — Apollo · HubSpot · Gmail · Drive (Task 004)

Reusable, copy-pasteable playbooks for driving the MCP servers through OpenClaw. Each file is a
self-contained recipe: **goal · servers needed · the exact prompt(s) · what the server can/can't
do · where output lands**. They follow the same honesty as the root `README.md` Playbooks
section — they never claim a capability the MCP server doesn't actually expose.

> **These run live against real accounts.** They need the relevant credentials in Bitwarden
> (see `docs/bitwarden.secrets.manager.md`) and `make verify` showing the server. Until keys are
> in, treat each playbook as the spec; the merge/render helpers below run with no credentials.

## Index

| # | Playbook | Servers |
|---|---|---|
| A1 | [Persona + target lists (UI + export)](apollo/01-persona-and-lists.md) | apollo |
| A2 | [Sequence stats + email open rates](apollo/02-sequence-stats-open-rates.md) | apollo |
| A3 | [Build sequences](apollo/03-build-sequences.md) | apollo |
| A4 | [List / lane effectiveness comparison + why](apollo/04-list-lane-comparison.md) | apollo |
| H1 | [Identify people by filter](hubspot/01-filter-people.md) | hubspot |
| H2 | [Identify stagnant deals by N days](hubspot/02-stagnant-deals.md) | hubspot |
| G1 | [Send templated email to a HubSpot list](gmail/01-send-to-hubspot-list.md) | hubspot → gmail |
| G2 | [Send templated email to an Apollo list](gmail/02-send-to-apollo-list.md) | apollo → gmail |
| G3 | [Send templated email to a CSV list](gmail/03-send-to-csv-list.md) | gmail |
| D1 | [Archive exports to Drive](drive/01-archive-exports.md) | google-drive |

## Conventions (shared by every playbook)

- **Export data dir:** `data/exports/` — all pulled lists/reports land here as
  `data/exports/<source>-<slug>-<YYYY-MM-DD>.{csv,json,md}`. The merge/render helpers create the
  dir on demand; its contents are git-ignored by the repo-root `.gitignore` (`data/*`) because
  they contain prospect PII — **never commit an export.**
- **Merge fields:** templates use `{{field}}` placeholders (e.g. `{{first_name}}`, `{{company}}`).
  Missing fields fail loud in a dry run, never send blank. See `gmail/merge/render.mjs`.
- **Dry-run first:** every send playbook renders all messages to `data/exports/` and **stops** for
  human review. Sending is a second, explicit step. Never send on a loop.
- **Personas** are reusable filter specs (YAML) in `apollo/personas/` — Apollo's MCP can't store a
  Persona object, so the spec lives here and is replayed into `search_people` filters.
