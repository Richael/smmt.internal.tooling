"""Per-source mappers: raw MCP tool output -> NormalizedRecord list."""
from typing import Any, List


def as_list(data: Any, *keys: str) -> List[dict]:
    """Coax a tool payload into a list of dict rows.

    Handles: a bare list, {"people":[...]}/{"results":[...]} style envelopes,
    a nested {"data": ...}, or a single dict row.
    """
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        for k in keys:
            v = data.get(k)
            if isinstance(v, list):
                return [r for r in v if isinstance(r, dict)]
        if isinstance(data.get("data"), (list, dict)):
            return as_list(data["data"], *keys)
        # a single object row
        return [data]
    return []
