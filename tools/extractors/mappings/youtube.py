"""YouTube (zubeid youtube-mcp, Data API v3) -> normalized records.

A channel yields an `organization` (the creator) + an `audience` (subscribers).
A video yields a `behavior_event` (view/engagement counts) — there is no PII here.
A comment yields a `behavior_event`.
"""
from typing import Any, List
from schema import NormalizedRecord, coalesce
from mappings import as_list

SOURCE = "youtube"


def _channel(r: dict, tool: str) -> List[NormalizedRecord]:
    sn = r.get("snippet") or {}
    st = r.get("statistics") or {}
    cid = str(coalesce(r.get("id"), sn.get("title")))
    org = NormalizedRecord(
        entity_type="organization", source=SOURCE, source_tool=tool, id=cid,
        attributes={
            "name": sn.get("title"),
            "website": f"https://youtube.com/channel/{r.get('id')}" if r.get("id") else None,
            "location": sn.get("country"),
        }, raw=r)
    out = [org]
    if st.get("subscriberCount") is not None:
        out.append(NormalizedRecord(
            entity_type="audience", source=SOURCE, source_tool=tool,
            id=f"{cid}:subscribers",
            attributes={
                "name": f"{sn.get('title')} subscribers",
                "platform": "youtube",
                "type": "subscribers",
                "size": _int(st.get("subscriberCount")),
            }, raw=r))
    return out


def _video(r: dict, tool: str) -> NormalizedRecord:
    sn = r.get("snippet") or {}
    st = r.get("statistics") or {}
    vid = r.get("id")
    vid = vid.get("videoId") if isinstance(vid, dict) else vid
    return NormalizedRecord(
        entity_type="behavior_event", source=SOURCE, source_tool=tool,
        id=str(coalesce(vid, sn.get("title"))),
        attributes={
            "type": "video_stats",
            "occurred_at": sn.get("publishedAt"),
            "object_ref": sn.get("title"),
            "count": _int(st.get("viewCount")),
            "metadata": {
                "video_id": vid,
                "likes": _int(st.get("likeCount")),
                "comments": _int(st.get("commentCount")),
                "channel": sn.get("channelTitle"),
            },
        }, raw=r)


def _comment(r: dict, tool: str) -> NormalizedRecord:
    top = (((r.get("snippet") or {}).get("topLevelComment") or {}).get("snippet")) or r.get("snippet") or {}
    return NormalizedRecord(
        entity_type="behavior_event", source=SOURCE, source_tool=tool,
        id=str(coalesce(r.get("id"), top.get("authorDisplayName"))),
        attributes={
            "type": "comment",
            "occurred_at": top.get("publishedAt"),
            "subject_ref": top.get("authorDisplayName"),
            "object_ref": top.get("videoId"),
            "count": _int(top.get("likeCount")),
        }, raw=r)


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def records(tool: str, data: Any) -> List[NormalizedRecord]:
    t = tool.lower()
    if "channel" in t:
        out = []
        for r in as_list(data, "items", "channels"):
            out.extend(_channel(r, tool))
        return out
    if "comment" in t:
        return [_comment(r, tool) for r in as_list(data, "items", "comments")]
    if "video" in t or "search" in t:
        return [_video(r, tool) for r in as_list(data, "items", "videos")]
    return []
