# G3 — Send templated email to a CSV list

**Goal:** mail-merge a template over a CSV and send via Gmail. This is the **generic** send flow;
G1 (HubSpot) and G2 (Apollo) just produce the CSV first.
**Servers:** `gmail` (the merge/dry-run needs no server).

## Steps

```bash
# 1. DRY RUN — render every message, no send. Fails loud on missing fields.
node playbooks/gmail/merge/render.mjs \
  --template playbooks/gmail/templates/email.example.md \
  --list playbooks/gmail/sample-list.csv
#    -> data/exports/gmail-drafts-<list>-<date>.{json,md}
```

> 2. **Review** the `.md` preview. Fix the list or template and re-run until clean.
> 3. "Use gmail to send each message in `data/exports/gmail-drafts-<list>-<date>.json`
>    (fields: to, subject, from, body). Send in batches of 25, pause between batches, and report
>    any failures — **do not** retry-loop."

## Input CSV shape

An `email` column plus one column per `{{field}}` in the template. Example:
`email,first_name,company,sender_name` (see `sample-list.csv`).

## Notes

- Gmail server: `@gongrzhe/server-gmail-autoauth-mcp` — run `make auth-gmail` once (browser OAuth).
- Respect Gmail sending limits (~500/day consumer, ~2000/day Workspace). Throttle; warm up new
  domains. High volume cold outreach belongs in Apollo sequences (A3), not raw Gmail.
- The rendered manifest is the audit trail — keep it; it's what actually went out.
