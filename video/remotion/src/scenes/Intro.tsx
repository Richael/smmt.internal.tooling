import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { meta, legend } from "../timeline";

const SYSTEMS = ["shopify", "klaviyo", "meta", "amazon"];

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleY = interpolate(frame, [0, 20], [30, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Inter, Helvetica, Arial, sans-serif",
        textAlign: "center",
        padding: 120,
      }}
    >
      <div style={{ opacity: titleIn, transform: `translateY(${titleY}px)` }}>
        <div style={{ color: theme.textDim, fontSize: 30, letterSpacing: 4, marginBottom: 16 }}>
          SMMT · CLOSED-LOOP ARCHITECTURE
        </div>
        <div style={{ color: theme.text, fontSize: 92, fontWeight: 800, lineHeight: 1.05 }}>
          {meta.title}
        </div>
        <div style={{ color: theme.textDim, fontSize: 38, marginTop: 20 }}>{meta.subtitle}</div>
      </div>

      <div style={{ display: "flex", gap: 28, marginTop: 70 }}>
        {SYSTEMS.map((key, i) => {
          const s = spring({ frame: frame - 25 - i * 8, fps, config: { damping: 14 } });
          return (
            <div
              key={key}
              style={{
                transform: `scale(${s})`,
                backgroundColor: theme.systems[key],
                color: ["klaviyo", "meta"].includes(key) ? "#fff" : "#10131a",
                fontSize: 34,
                fontWeight: 700,
                padding: "20px 36px",
                borderRadius: 18,
              }}
            >
              {legend[key as keyof typeof legend].label}
            </div>
          );
        })}
      </div>

      <div
        style={{
          opacity: interpolate(frame, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          color: theme.return,
          fontSize: 40,
          fontWeight: 700,
          marginTop: 70,
        }}
      >
        Twelve loops. Each cycle improves the next.
      </div>
    </AbsoluteFill>
  );
};
