# Prompt 03 — Narration script

**Use when:** generating or revising the voiceover in `video/narration/scripts.md`.
One block per loop + an intro and outro. Plain text that reads well aloud (this is fed to
TTS — macOS `say` by default, or a fal.ai / ElevenLabs voice).

---

```
Write the voiceover script for an explainer video on a closed-loop marketing architecture.
Audience: a technical client stakeholder or a new SMMT engineer. Tone: crisp, confident,
concrete; short sentences; no hype. Pronounceable (this goes to TTS) — expand symbols
("CLV" → "C-L-V", "→" → "then", "§6" → "section six"), avoid code.

Structure:
1. INTRO (~25s): what a closed loop is — data leaves one system, is acted on in another, and
   RETURNS as a converted customer or enriched signal, so each cycle improves the next. Name
   the four systems. State the headline (N compounding loops).
2. One BLOCK per loop (~20–35s each). For each: name it, state the objective in one line, walk
   the flow in the order of `systems`/`legs`, then land the **return** — exactly what re-enters
   and why it compounds. Mention the single most important edge case only if it changes the
   mental model (e.g. event_id dedup for the CAPI loop, the Amazon no-email wall).
3. OUTRO (~20s): the meta-point — these loops share one audience and one identity spine; the
   reuse engine (the syndication loop) is what makes the whole system worth more than its parts.

Hard rules:
- Respect the governing principles: audiences only flow OUTBOUND to Meta; Amazon returns no
  marketing email. Never say membership can be pulled back out.
- Each block must end on the loop-closing return. That's the whole point.
- Output as markdown with "## Loop N — <title>" headers and the spoken text beneath. Add an
  estimated duration in seconds after each header in parentheses.

DATA:
<<< paste loops.json >>>
```
