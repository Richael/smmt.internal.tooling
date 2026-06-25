import { Composition } from "remotion";
import { TwelveLoops } from "./TwelveLoops";
import { FPS, WIDTH, HEIGHT } from "./theme";
import { buildTimeline } from "./timeline";

export const RemotionRoot: React.FC = () => {
  const timeline = buildTimeline();
  return (
    <Composition
      id="TwelveLoops"
      component={TwelveLoops}
      durationInFrames={timeline.totalFrames}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
      defaultProps={{}}
    />
  );
};
