# Prompt 04 — Remotion scene

**Use when:** adding or restyling an animated section. The project already ships a reusable
`LoopScene` component (in `video/remotion/src/scenes/`) driven by `loops.json`, plus `Intro`
and `Outro`. Use this prompt to generate a *new variant* scene or a bespoke animation.

---

```
You write a Remotion v4 React + TypeScript component for one section of an explainer video.
Canvas 1920×1080, 30fps. Use only: remotion (useCurrentFrame, interpolate, spring,
useVideoConfig, Sequence, AbsoluteFill, Audio, Img), React. No external UI libs.

Build a scene for the loop below that:
- Opens with the loop number + title sliding/fading in (spring on entrance).
- Renders each system as a coloured chip in `systems` order, popping in one at a time, with
  an animated connector arrow drawn between consecutive chips as each appears. Colours:
  Shopify #95BF47, Klaviyo #1A1A1A, Meta/IG #0866FF, Amazon #FF9900, smmt #7C5CFF;
  dark chips use #ffffff text.
- Shows each `leg` as a caption synced to its arrow.
- Finishes with the LAVENDER (#B7A8F2) return arrow animating from the last chip back to the
  first, with the `closes` label — held on screen 1s. This beat must feel like the payoff.
- Reads its duration from the loop's narration length (pass `durationInFrames` as a prop).
- Pulls all copy from a `loop` prop typed to the loops.json schema — NO hardcoded content.

Match the existing theme.ts (background #0b0b12 dark, text #f5f5f7, legend colours above).
Output ONLY the .tsx file.

LOOP:
<<< paste one loop object >>>
```
