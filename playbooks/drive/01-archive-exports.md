# D1 — Drive as shared source + live ops tracker

**Goal:** use Google Drive as (1) the team's shared source for prospect lists / campaign briefs,
and (2) a live tracking Sheet the agent updates after each run.
**Server:** `google-drive` (`@isaacphi/mcp-gdrive`).

## Reality check (what this server can/can't do)

This server is **read-only for Drive** (`drive.readonly`) + **read/write for Google Sheets**
(`spreadsheets`). Tools: `gdrive_search`, `gdrive_read_file`, `gsheets_read`,
`gsheets_update_cell`. **It cannot upload or create arbitrary files in Drive.** So "archiving"
means writing to a **Google Sheet**, not dropping CSVs into a folder. Designed around that:

### Use A — Ingest a shared list / brief from Drive (read)

> 1. "Use google-drive `gdrive_search` to find the sheet 'Q3 Target Accounts'."
> 2. "Use `gsheets_read` to read it, then save it to `data/exports/drive-q3-targets-<today>.csv`."
> 3. Feed that CSV into **G3** (Gmail merge) or enrich it via **A1**.

This makes Drive the single shared source of truth: marketing maintains the list/brief in Drive,
the agent pulls the current version each run — no copy-paste, no stale files.

### Use B — Log run results back to a tracking Sheet (write)

Keep one "Ops Tracker" Google Sheet (columns: date, playbook, audience, count, sent, replies,
notes). After any run:

> "Use google-drive `gsheets_update_cell` to append today's row to the 'Ops Tracker' sheet:
> date, 'H2 stagnant deals', '—', <count>, '—', '—', '<N> deals > 30d, $<X> at risk'."

Now H2's weekly stagnant-deal count, A2's sequence open rates, and G-series send counts all land
in one Sheet the whole team sees — the read-only-Drive-friendly version of "archive the report."

## Output

- Use A: `data/exports/drive-<sheet-slug>-<today>.csv` pulled from Drive.
- Use B: a row appended to the shared Ops Tracker Sheet.

## Notes

- `gsheets_update_cell` writes **one cell at a time** — for a row, the agent updates each column
  cell; tell it the target range (e.g. `A12:G12`) explicitly.
- Needs `gcp-oauth.keys.json` in `GDRIVE_CREDS_DIR` and `make auth-gdrive` once.
- If you truly need CSVs *files* in Drive (not Sheets), that requires a write-scoped gdrive server
  (`drive.file`) — out of scope for this server; note it and swap the server if the team wants it.
