# Playbook — HubSpot: contacts, companies, deals

**Server:** `hubspot` (read scopes: `crm.objects.contacts.read`, `companies.read`, `deals.read`).
**Produces:** `person`, `organization`, `transaction` (+ `segment` from lists, `campaign` from
marketing emails) → *customers · transaction history · segments · campaigns*.

## Prompts (run each, save raw)

> Use **hubspot** to search CRM **contacts** (properties: email, firstname, lastname, jobtitle,
> company, phone, lifecyclestage, city). Save the raw result to
> `data/raw/hubspot.crm_contacts.json` as `{"source":"hubspot","tool":"crm_contacts_search","data": <raw> }`.

> Use **hubspot** to search CRM **companies** (name, domain, industry, numberofemployees, city)
> → save to `data/raw/hubspot.crm_companies.json` with tool `crm_companies_search`.

> Use **hubspot** to search CRM **deals** (dealname, amount, dealstage, closedate,
> deal_currency_code) → save to `data/raw/hubspot.crm_deals.json` with tool `crm_deals_search`.

*(Optional: lists → `segment`, marketing emails → `campaign`. Filenames must contain
`lists` / `emails` so the mapper routes them.)*

## Then

```bash
make normalize     # -> person / organization / transaction (+ segment/campaign) .jsonl + .csv
```
