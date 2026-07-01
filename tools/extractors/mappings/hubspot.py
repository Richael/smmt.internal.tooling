"""HubSpot (shinzo-labs hubspot-mcp, CRM v3 objects) -> normalized records."""
from typing import Any, List
from schema import NormalizedRecord, coalesce
from mappings import as_list

SOURCE = "hubspot"


def _props(r: dict) -> dict:
    # HubSpot objects look like {"id": "...", "properties": {...}}
    return r.get("properties") or r


def _contact(r: dict, tool: str) -> NormalizedRecord:
    p = _props(r)
    name = " ".join(x for x in (p.get("firstname"), p.get("lastname")) if x) or None
    return NormalizedRecord(
        entity_type="person", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), p.get("email"))),
        attributes={
            "email": p.get("email"),
            "full_name": name,
            "first_name": p.get("firstname"),
            "last_name": p.get("lastname"),
            "title": p.get("jobtitle"),
            "company": p.get("company"),
            "phone": p.get("phone"),
            "location": coalesce(p.get("city"), p.get("country")),
            "tags": [t for t in (p.get("lifecyclestage"), p.get("hs_lead_status")) if t],
        }, raw=r)


def _company(r: dict, tool: str) -> NormalizedRecord:
    p = _props(r)
    return NormalizedRecord(
        entity_type="organization", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), p.get("domain"), p.get("name"))),
        attributes={
            "name": p.get("name"),
            "domain": p.get("domain"),
            "website": p.get("website"),
            "industry": p.get("industry"),
            "size": p.get("numberofemployees"),
            "location": coalesce(p.get("city"), p.get("country")),
        }, raw=r)


def _deal(r: dict, tool: str) -> NormalizedRecord:
    p = _props(r)
    return NormalizedRecord(
        entity_type="transaction", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), p.get("dealname"))),
        attributes={
            "name": p.get("dealname"),
            "amount": p.get("amount"),
            "currency": coalesce(p.get("deal_currency_code"), "USD"),
            "status": p.get("dealstage"),
            "occurred_at": coalesce(p.get("closedate"), p.get("createdate")),
            "channel": "hubspot",
        }, raw=r)


def _campaign(r: dict, tool: str) -> NormalizedRecord:
    p = _props(r)
    return NormalizedRecord(
        entity_type="campaign", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), p.get("name"))),
        attributes={
            "name": coalesce(p.get("name"), p.get("subject")),
            "platform": "hubspot-email",
            "status": p.get("state"),
            "starts_at": p.get("publish_date"),
        }, raw=r)


def _list_segment(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="segment", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("listId"), r.get("id"), r.get("name"))),
        attributes={
            "name": r.get("name"),
            "platform": "hubspot",
            "count": coalesce(r.get("size"), r.get("metaData", {}).get("size") if isinstance(r.get("metaData"), dict) else None),
            "rule": r.get("processingType"),
        }, raw=r)


def _timeline_event(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="behavior_event", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("eventType"))),
        attributes={
            "type": coalesce(r.get("eventType"), "timeline"),
            "occurred_at": coalesce(r.get("timestamp"), r.get("occurredAt")),
            "subject_ref": r.get("objectId"),
        }, raw=r)


_HANDLERS = {
    # tool-name patterns are matched loosely (see records())
    "contacts": (_contact, ("results", "contacts")),
    "companies": (_company, ("results", "companies")),
    "deals": (_deal, ("results", "deals")),
    "emails": (_campaign, ("results",)),
    "campaigns": (_campaign, ("results", "campaigns")),
    "lists": (_list_segment, ("lists", "results")),
    "events": (_timeline_event, ("results", "events")),
}


def records(tool: str, data: Any) -> List[NormalizedRecord]:
    t = tool.lower()
    for key, (fn, listkeys) in _HANDLERS.items():
        if key in t:                       # e.g. "crm_contacts_search" matches "contacts"
            return [fn(r, tool) for r in as_list(data, *listkeys)]
    return []
