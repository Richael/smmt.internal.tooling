// Builds the section timeline from the narration durations + loops.json.
// Section order: intro, loop 1..12, outro — matched to the NN_ prefix in durations.json.
import loopsData from "../../data/loops.json";
import durations from "../public/narration/durations.json";
import { FPS, PAD_FRAMES } from "./theme";

export type Loop = (typeof loopsData)["loops"][number];

export type Section = {
  key: string; // durations.json key == narration filename stem
  kind: "intro" | "loop" | "outro";
  title: string;
  from: number; // start frame
  durationInFrames: number;
  loop?: Loop;
};

type Dur = { seconds: number; title: string };

export const meta = loopsData.meta;
export const legend = loopsData.legend;

export function buildTimeline() {
  const entries = Object.entries(durations as Record<string, Dur>).sort(([a], [b]) =>
    a.localeCompare(b)
  );

  let from = 0;
  let loopIdx = 0;
  const sections: Section[] = entries.map(([key, d]) => {
    const durationInFrames = Math.ceil(d.seconds * FPS) + PAD_FRAMES;
    const kind: Section["kind"] = key.includes("intro")
      ? "intro"
      : key.includes("outro")
        ? "outro"
        : "loop";
    const loop = kind === "loop" ? loopsData.loops[loopIdx++] : undefined;
    const s: Section = { key, kind, title: d.title, from, durationInFrames, loop };
    from += durationInFrames;
    return s;
  });

  return { sections, totalFrames: from };
}
