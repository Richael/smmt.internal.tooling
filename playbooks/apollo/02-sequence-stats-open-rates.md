# A2 — Sequence stats + email open rates

**Goal:** pull outreach performance (sends, opens, replies) per sequence and produce a report.
**Server:** `apollo`.

## Tools used

`search_sequences`, `search_outreach_emails`, `get_email_activities`, `list_email_accounts`.

## Steps (prompts)

> 1. "Use apollo `search_sequences` to list all active sequences with their ids and names."
> 2. "Use apollo `get_email_activities` / `search_outreach_emails` for each sequence to get
>    sends, opens, clicks, replies, and bounces."
> 3. "Compute per-sequence open rate = opens / delivered, reply rate = replies / delivered, and
>    bounce rate. Rank sequences by reply rate."
> 4. "Write the report to `data/exports/apollo-sequence-stats-<today>.md` using the template in
>    `templates/comparison-report.md`, and also save the raw rows as
>    `data/exports/apollo-sequence-stats-<today>.csv`."

## Output

A ranked markdown report + CSV in `data/exports/`.

## Notes

- Open rate is **directional** — Apple Mail Privacy Protection and image-blocking inflate/deflate
  opens; weight **reply rate** higher when judging a sequence.
- `list_email_accounts` shows which sending mailbox each sequence used — useful when one mailbox's
  deliverability is dragging a sequence's numbers down.
- This report is the input to **A4** (list/lane comparison).
