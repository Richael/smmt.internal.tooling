# H1 — Identify people by filter

**Goal:** find HubSpot contacts matching configurable criteria and export them.
**Server:** `hubspot` (shinzo-labs `@shinzo-labs/hubspot-mcp`).

## Tools used

CRM object search over contacts (search with `filterGroups`/properties), plus property reads.
The shinzo-labs server wraps HubSpot's CRM v3 search API, so filters are HubSpot property
filters (AND within a group, OR across groups).

## Common filters (parameterize per run)

| Want | Filter |
|---|---|
| Leads not yet contacted | `lifecyclestage = lead` AND `hs_lead_status` is empty / `NEW` |
| MQLs in a region | `lifecyclestage = marketingqualifiedlead` AND `state` / `country` in [...] |
| By title / seniority | `jobtitle` contains [...] |
| Recently created | `createdate` > N days ago |
| Owned by a rep | `hubspot_owner_id = <id>` |
| In a static list | search the list membership, or filter `ils_list_memberships` |

## Steps (prompts)

> 1. "Use hubspot to search contacts where lifecycle stage is 'lead', country is United States,
>    and create date is within the last 30 days. Return first_name, last_name, email, jobtitle,
>    company, createdate. Show me the count and first 25."
> 2. "Export all matches to `data/exports/hubspot-leads-us-30d-<today>.csv`."

## Output

`data/exports/hubspot-<filter-slug>-<YYYY-MM-DD>.csv` — feeds **G1** (templated send).

## Notes

- The Private App token must include `crm.objects.contacts.read` or search returns nothing.
- Search is paginated (`after` cursor) — for big result sets, ask OpenClaw to page through fully
  before exporting, or it'll stop at the first page.
- Property internal names ≠ UI labels (e.g. `jobtitle`, not "Job Title"). Confirm names via a
  properties read if a filter returns zero unexpectedly.
