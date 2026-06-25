# H2 — Identify stagnant deals by N days

**Goal:** surface deals with no movement for more than **N** days, so reps can act or close-lost.
**Server:** `hubspot`.

## Definition of "stagnant" (pick one, or combine)

- **No activity:** `notes_last_updated` / `hs_lastmodifieddate` older than N days.
- **Stuck in stage:** `hs_date_entered_<stage>` older than N days and `dealstage` unchanged.
- Exclude `closedwon` / `closedlost` (those aren't stagnant, they're done).

## Steps (prompts)

> 1. "Use hubspot to search deals where dealstage is not closedwon or closedlost AND
>    hs_lastmodifieddate is older than 30 days. Return dealname, amount, dealstage,
>    hubspot_owner_id, hs_lastmodifieddate, days since modified. Sort by oldest first."
> 2. "Also flag any deal still in its current stage for more than 30 days using
>    hs_date_entered_{stage}."
> 3. "Export to `data/exports/hubspot-stagnant-deals-30d-<today>.csv` and give me a short summary:
>    count, total $ at risk, and the top 10 oldest by owner."

## Parameterize

`N` (days) and the stage set are the only knobs — change "30" and the excluded stages. Common
values: 14 (fast cycles), 30 (default), 60 (enterprise).

## Output

`data/exports/hubspot-stagnant-deals-<N>d-<YYYY-MM-DD>.csv` + a summary (count, $ at risk, by owner).

## Notes

- Needs `crm.objects.deals.read`.
- "Days since modified" is computed client-side from `hs_lastmodifieddate` vs today — HubSpot
  search can't subtract dates, so filter on an absolute timestamp (today − N days) in the query.
- Great as a **scheduled** weekly pull → pairs with **D1** (archive the report to Drive) and can
  feed a re-engagement send (G-series) to the deal contacts.
