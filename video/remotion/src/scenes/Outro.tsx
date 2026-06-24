import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { theme } from "../theme";

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 25], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        padding: 140,
        fontFamily: "Inter, Helvetica, Arial, sans-serif",
      }}
    >
      <div style={{ opacity: o }}>
        <div style={{ color: theme.text, fontSize: 70, fontWeight: 800, lineHeight: 1.1 }}>
          One idea, twelve times.
        </div>
        <div style={{ color: theme.textDim, fontSize: 38, marginTop: 30, maxWidth: 1200, lineHeight: 1.35 }}>
          One audience. One identity spine. Email flows outbound to the platforms — never
          extracted back. Build the spine once, and every loop compounds on top of it.
        </div>
        <div style={{ color: theme.return, fontSize: 34, fontWeight: 700, marginTop: 50 }}>
          smmt · Closed-Loop Integration Architecture
        </div>
      </div>
    </AbsoluteFill>
  );
};
