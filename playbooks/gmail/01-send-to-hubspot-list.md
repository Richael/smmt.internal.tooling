# G1 — Send templated email to a HubSpot list

**Goal:** email a HubSpot-filtered audience with a merged template.
**Servers:** `hubspot` → `gmail`. Builds on **H1** + **G3**.

## Steps

> 1. Run **H1** to export the audience to
>    `data/exports/hubspot-<filter>-<today>.csv` (must include `email` + every template field).

```bash
# 2. DRY RUN over the HubSpot export
node playbooks/gmail/merge/render.mjs \
  --template playbooks/gmail/templates/email.example.md \
  --list data/exports/hubspot-<filter>-<today>.csv
```

> 3. Review the preview, then **G3 step 3** to send via Gmail in batches.

## Make the CSV match the template

H1 exports HubSpot property names (`firstname`, `company`, …). Either name your template fields
to match, or have OpenClaw rename columns on export to the template's fields
(`first_name`, `company`, `sender_name`). Keep `email` as the key column.

## Notes

- Prefer Gmail for **warm / 1:1-ish** sends to known contacts. For cold sequences, push the list
  into Apollo (A3) instead — better deliverability controls and unsubscribe handling.
- Respect consent: don't email `hs_email_optout = true` contacts. Filter them out in H1.
