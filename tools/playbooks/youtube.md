# Playbook — YouTube: channel, videos, comments

**Server:** `youtube` (Data API v3 key; read-only; no PII).
**Produces:** `organization` (creator) + `audience` (subscribers) from a channel; `behavior_event`
from video stats and comments → *customers · audiences · behavior*.

## Prompts (save raw)

> Use **youtube** to get the channel for [channel id or handle] with its `snippet` + `statistics`.
> Save the raw result to `data/raw/youtube.get_channel.json` as
> `{"source":"youtube","tool":"get_channel","data": <raw> }`.

> Use **youtube** to search/list the channel's recent **videos** with `snippet` + `statistics`
> (viewCount, likeCount, commentCount). Save to `data/raw/youtube.search_videos.json` with tool
> `search_videos`.

> *(Optional)* Use **youtube** to fetch `commentThreads` for a video → save to
> `data/raw/youtube.commentThreads.json` with tool `commentThreads`.

## Then

```bash
make normalize     # -> organization.jsonl, audience.jsonl, behavior_event.jsonl (+ .csv)
```

Note: YouTube here is organic analytics only (no person-level identity) — `audience` carries the
subscriber count, `behavior_event` carries view/like/comment counts keyed to the video, not to a fan.
