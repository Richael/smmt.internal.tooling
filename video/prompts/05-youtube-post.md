# Prompt 05 — YouTube post

**Use when:** generating the publish package in `video/youtube/post.md` (title, description,
chapters, tags, pinned comment). Chapters must line up with the rendered section timecodes.

---

```
Write the YouTube publish package for an explainer video on a closed-loop marketing
architecture (Shopify · Klaviyo · Meta/IG · Amazon). Output markdown with these sections:

1. TITLE — 3 options, ≤70 chars, specific and clicky-but-honest (no clickbait). Lead with the
   concrete payoff ("12 marketing loops that compound", not "you won't believe...").
2. DESCRIPTION — 2 short paragraphs: what the video covers + who it's for, then the core idea
   (a closed loop returns signal so each cycle improves the next). End with a one-line CTA.
3. CHAPTERS — "0:00 Intro" then one line per loop using the REAL timecodes from the render
   (read them from the narration durations / Remotion sequence offsets). YouTube needs the
   first chapter at 0:00 and ≥3 chapters of ≥10s each.
4. TAGS — 12–15, mixing broad (marketing automation, Shopify, Klaviyo, Meta ads, Amazon ads)
   and specific (CAPI, lookalike audiences, abandoned cart, Amazon Attribution).
5. PINNED COMMENT — one short paragraph inviting the specific audience (DTC operators / agency
   engineers) to ask which loop to break down next.

Tone: technical, confident, no hype. Respect the principles (outbound-only Meta audiences,
Amazon no-email wall) if you reference them.

DATA:
<<< paste loops.json + the section timecodes >>>
```
