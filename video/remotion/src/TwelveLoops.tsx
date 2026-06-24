import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { buildTimeline } from "./timeline";
import { theme } from "./theme";
import { Intro } from "./scenes/Intro";
import { Outro } from "./scenes/Outro";
import { LoopScene } from "./scenes/LoopScene";

export const TwelveLoops: React.FC = () => {
  const { sections } = buildTimeline();

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      {sections.map((s) => (
        <Sequence key={s.key} from={s.from} durationInFrames={s.durationInFrames} name={s.title}>
          {s.kind === "intro" && <Intro />}
          {s.kind === "outro" && <Outro />}
          {s.kind === "loop" && s.loop && (
            <LoopScene loop={s.loop} durationInFrames={s.durationInFrames} />
          )}
          <Audio src={staticFile(`narration/${s.key}.m4a`)} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
