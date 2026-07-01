"""Apollo (Chainscore apollo-io-mcp) -> normalized records."""
from typing import Any, List
from schema import NormalizedRecord, coalesce
from mappings import as_list

SOURCE = "apollo"


def _person(r: dict, tool: str) -> NormalizedRecord:
    org = r.get("organization") or {}
    name = coalesce(r.get("name"),
                    " ".join(x for x in (r.get("first_name"), r.get("last_name")) if x))
    phones = r.get("phone_numbers") or []
    phone = phones[0].get("sanitized_number") if phones and isinstance(phones[0], dict) else None
    return NormalizedRecord(
        entity_type="person", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("email"), name)),
        attributes={
            "email": coalesce(r.get("email"), r.get("work_email")),
            "full_name": name,
            "first_name": r.get("first_name"),
            "last_name": r.get("last_name"),
            "title": r.get("title"),
            "company": org.get("name"),
            "company_domain": coalesce(org.get("primary_domain"), org.get("website_url")),
            "linkedin_url": r.get("linkedin_url"),
            "location": coalesce(r.get("city"),
                                 ", ".join(x for x in (r.get("city"), r.get("state"), r.get("country")) if x)),
            "phone": phone,
        }, raw=r)


def _organization(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="organization", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("primary_domain"), r.get("name"))),
        attributes={
            "name": r.get("name"),
            "domain": coalesce(r.get("primary_domain"), r.get("website_url")),
            "website": r.get("website_url"),
            "industry": r.get("industry"),
            "size": coalesce(r.get("estimated_num_employees"), r.get("organization_num_employees")),
            "location": r.get("city"),
            "linkedin_url": r.get("linkedin_url"),
        }, raw=r)


def _opportunity(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="transaction", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("name"))),
        attributes={
            "name": r.get("name"),
            "amount": r.get("amount"),
            "currency": coalesce(r.get("currency"), "USD"),
            "status": coalesce(r.get("stage"), r.get("opportunity_stage")),
            "occurred_at": coalesce(r.get("closed_date"), r.get("created_at")),
            "channel": "apollo",
        }, raw=r)


def _job_posting(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="behavior_event", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("url"), r.get("title"))),
        attributes={
            "type": "job_posting",
            "occurred_at": coalesce(r.get("posted_at"), r.get("last_seen_at")),
            "object_ref": r.get("title"),
            "metadata": {"url": r.get("url"), "city": r.get("city")},
        }, raw=r)


def _activity(r: dict, tool: str) -> NormalizedRecord:
    return NormalizedRecord(
        entity_type="behavior_event", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), r.get("type"))),
        attributes={
            "type": coalesce(r.get("type"), "activity"),
            "occurred_at": coalesce(r.get("created_at"), r.get("happened_at")),
            "subject_ref": r.get("contact_id"),
            "metadata": {k: r.get(k) for k in ("email", "subject") if r.get(k)},
        }, raw=r)


_HANDLERS = {
    "search_people": (_person, ("people", "contacts")),
    "search_contacts": (_person, ("contacts", "people")),
    "enrich_person": (_person, ("person", "people")),
    "bulk_enrich_people": (_person, ("people",)),
    "get_contact": (_person, ("contact", "contacts")),
    "search_organizations": (_organization, ("organizations", "accounts")),
    "enrich_organization": (_organization, ("organization", "organizations")),
    "get_organization": (_organization, ("organization",)),
    "search_accounts": (_organization, ("accounts", "organizations")),
    "search_opportunities": (_opportunity, ("opportunities", "deals")),
    "get_opportunity": (_opportunity, ("opportunity",)),
    "get_organization_job_postings": (_job_posting, ("job_postings", "organization_job_postings")),
    "search_activities": (_activity, ("activities",)),
}


def records(tool: str, data: Any) -> List[NormalizedRecord]:
    if tool not in _HANDLERS:
        return []
    fn, keys = _HANDLERS[tool]
    return [fn(r, tool) for r in as_list(data, *keys)]
