"""
Normalized record schema for smmt-internal-tooling extractors.

Every MCP server's raw output is mapped into ONE record shape so the data lines up
across sources and against the smmt "target data points". Stdlib only — no deps.

Target data points  ->  canonical entity_type
  customers / customer information   ->  person, organization
  transaction history                ->  transaction
  behavior                           ->  behavior_event
  events                             ->  event
  ticketing                          ->  ticket
  merch or inventory                 ->  inventory_item
  audiences                          ->  audience
  segments                           ->  segment
  campaigns / pushes                 ->  campaign
  lookalike functionality            ->  lookalike
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional

SCHEMA_VERSION = "1.0"

# canonical entity_type -> the target data point(s) it serves
ENTITY_TYPES: Dict[str, str] = {
    "person":          "customers / customer information",
    "organization":    "customers / customer information",
    "transaction":     "transaction history",
    "behavior_event":  "behavior",
    "event":           "events",
    "ticket":          "ticketing",
    "inventory_item":  "merch or inventory",
    "audience":        "audiences",
    "segment":         "segments",
    "campaign":        "campaigns / pushes",
    "lookalike":       "lookalike functionality",
}

# canonical attribute keys per entity_type (documentation + light validation).
# Mappers should populate from this set; unknown keys go under attributes anyway,
# but staying on-vocabulary keeps cross-source joins clean.
CANONICAL_ATTRS: Dict[str, tuple] = {
    "person":         ("email", "full_name", "first_name", "last_name", "title",
                       "company", "company_domain", "linkedin_url", "location",
                       "phone", "tags"),
    "organization":   ("name", "domain", "website", "industry", "size",
                       "location", "linkedin_url"),
    "transaction":    ("amount", "currency", "status", "occurred_at",
                       "customer_email", "customer_id", "channel", "line_items",
                       "name"),
    "behavior_event": ("type", "occurred_at", "subject_ref", "object_ref",
                       "count", "metadata"),
    "event":          ("title", "starts_at", "ends_at", "venue", "city",
                       "country", "url"),
    "ticket":         ("event_ref", "buyer_email", "tier", "price", "currency",
                       "quantity", "ordered_at"),
    "inventory_item": ("sku", "title", "category", "price", "currency", "stock",
                       "location"),
    "audience":       ("name", "platform", "type", "size"),
    "segment":        ("name", "platform", "rule", "count"),
    "campaign":       ("name", "platform", "objective", "status", "spend",
                       "currency", "impressions", "clicks", "conversions",
                       "starts_at", "ends_at"),
    "lookalike":      ("name", "platform", "seed_ref", "ratio", "country", "size"),
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class NormalizedRecord:
    entity_type: str
    id: str
    source: str                       # mcp server name, e.g. "apollo"
    source_tool: str                  # tool that produced it, e.g. "search_people"
    attributes: Dict[str, Any] = field(default_factory=dict)
    extracted_at: str = field(default_factory=_now)
    schema_version: str = SCHEMA_VERSION
    raw: Optional[Dict[str, Any]] = None   # original payload (optional; can be dropped)

    def __post_init__(self):
        if self.entity_type not in ENTITY_TYPES:
            raise ValueError(
                f"unknown entity_type {self.entity_type!r}; "
                f"valid: {', '.join(ENTITY_TYPES)}"
            )
        # drop None-valued attributes for clean output
        self.attributes = {k: v for k, v in self.attributes.items() if v not in (None, "", [])}

    def to_dict(self, include_raw: bool = False) -> Dict[str, Any]:
        d = asdict(self)
        if not include_raw:
            d.pop("raw", None)
        return d


def coalesce(*vals):
    """First non-empty value."""
    for v in vals:
        if v not in (None, "", [], {}):
            return v
    return None
