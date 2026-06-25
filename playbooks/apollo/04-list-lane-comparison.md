# A4 — List / lane effectiveness comparison + why

**Goal:** compare performance across lists/lanes (personas × sequences) and explain *why* each
performs as it does, with a recommendation.
**Server:** `apollo` (consumes the output of A1–A3).

## What "lane" means

A lane = a (persona/list) × (sequence) pairing. The same sequence sent to two personas, or two
sequences sent to one persona, are different lanes. Comparing lanes — not just sequences — is what
surfaces whether it's the **list** or the **copy** that's driving results.

## Steps (prompts)

> 1. "Use apollo `search_activities` / `get_email_activities` to pull per-contact outcomes, then
>    group by (label, sequence) — that's the lane."
> 2. "For each lane compute delivered, open rate, reply rate, bounce, and meetings booked
>    (`search_tasks`/`search_activities` for meeting-type outcomes). Rank by reply rate."
> 3. "Attribute the difference: is the spread explained by the **list** (same sequence, different
>    persona → ICP fit) or the **copy** (same persona, different sequence → messaging)? State which."
> 4. "Write `data/exports/apollo-lane-comparison-<today>.md` from `templates/comparison-report.md`,
>    filling the 'Why these results' section with the attribution, plus a CSV of the raw lane rows."

## Output

A ranked comparison report with a *why* per lane + recommendations, in `data/exports/`.

## How to read it (the "why")

- **Same sequence, two personas, big reply-rate gap → it's the list** (ICP fit). Fix targeting.
- **Same persona, two sequences, big gap → it's the copy** (subject/offer). Fix messaging.
- **High open, low reply → subject works, body/offer doesn't.**
- **Low open across the board → deliverability** (mailbox warm-up, spam words), not copy.
- **Bounce > 3% → list quality / enrichment staleness** — re-verify before blaming the message.
