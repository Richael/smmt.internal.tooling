import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme, chipTextColor } from "../theme";
import { legend, type Loop } from "../timeline";

const CHIP_W = 250;
const CHIP_H = 96;
const GAP = 86;
const ROW_Y = 590; // top of chip row
const MID = ROW_Y + CHIP_H / 2;
const RETURN_Y = ROW_Y + CHIP_H + 90;

export const LoopScene: React.FC<{ loop: Loop; durationInFrames: number }> = ({
  loop,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const systems = loop.systems;
  const n = systems.length;
  const chipStart = 24;
  const reserveForReturn = 54;
  const span = Math.max(60, durationInFrames - chipStart - reserveForReturn);
  const chipStep = span / n;
  const returnStart = chipStart + n * chipStep + 4;

  const total = n * CHIP_W + (n - 1) * GAP;
  const startX = (1920 - total) / 2;
  const cx = (i: number) => startX + i * (CHIP_W + GAP) + CHIP_W / 2;

  const headerIn = interpolate(frame, [0, 18], [0, 1], { extrapolateRight: "clamp" });
  const headerY = interpolate(frame, [0, 18], [-24, 0], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ fontFamily: "Inter, Helvetica, Arial, sans-serif" }}>
      {/* header */}
      <div
        style={{
          position: "absolute",
          top: 90,
          left: 120,
          right: 120,
          opacity: headerIn,
          transform: `translateY(${headerY}px)`,
          display: "flex",
          alignItems: "center",
          gap: 28,
        }}
      >
        <div
          style={{
            backgroundColor: theme.systems.smmt,
            color: "#fff",
            width: 92,
            height: 92,
            borderRadius: 20,
            fontSize: 50,
            fontWeight: 800,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
        >
          {loop.id}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ color: theme.text, fontSize: 56, fontWeight: 800, lineHeight: 1.05 }}>
            {loop.title}
          </div>
          <div style={{ color: theme.textDim, fontSize: 28, marginTop: 10 }}>
            closes on {loop.closes} · {loop.segment} · {loop.latency} · {loop.section}
          </div>
        </div>
      </div>

      {/* objective + legs (left list) */}
      <div style={{ position: "absolute", top: 250, left: 120, width: 760 }}>
        <div
          style={{
            color: theme.text,
            fontSize: 30,
            lineHeight: 1.4,
            opacity: interpolate(frame, [10, 30], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          {loop.objective}
        </div>
        <div style={{ marginTop: 36, display: "flex", flexDirection: "column", gap: 16 }}>
          {loop.legs.map((leg, j) => {
            const at = chipStart + (j + 0.5) * chipStep;
            const op = interpolate(frame, [at - 10, at + 8], [0.15, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <div key={j} style={{ display: "flex", gap: 14, opacity: op }}>
                <div style={{ color: theme.return, fontSize: 26, fontWeight: 700 }}>{j + 1}.</div>
                <div style={{ color: theme.textDim, fontSize: 26, lineHeight: 1.3 }}>{leg}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* arrows (SVG overlay) */}
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <marker id="ah" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
            <path d="M0,0 L7,3 L0,6 Z" fill={theme.textDim} />
          </marker>
          <marker id="ahr" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
            <path d="M0,0 L7,3 L0,6 Z" fill={theme.return} />
          </marker>
        </defs>

        {/* forward arrows */}
        {systems.slice(1).map((_, i) => {
          const at = chipStart + (i + 1) * chipStep;
          const p = interpolate(frame, [at - 12, at], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const x1 = cx(i) + CHIP_W / 2 + 8;
          const x2 = cx(i + 1) - CHIP_W / 2 - 12;
          return (
            <line
              key={i}
              x1={x1}
              y1={MID}
              x2={x2}
              y2={MID}
              stroke={theme.textDim}
              strokeWidth={4}
              markerEnd="url(#ah)"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - p}
            />
          );
        })}

        {/* lavender return arc: last chip -> down -> across -> up to first chip */}
        {n > 1 &&
          (() => {
            const p = interpolate(frame, [returnStart, returnStart + 26], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const d = `M ${cx(n - 1)} ${ROW_Y + CHIP_H + 6} V ${RETURN_Y} H ${cx(0)} V ${ROW_Y + CHIP_H + 6}`;
            return (
              <path
                d={d}
                fill="none"
                stroke={theme.return}
                strokeWidth={6}
                markerEnd="url(#ahr)"
                pathLength={1}
                strokeDasharray={1}
                strokeDashoffset={1 - p}
              />
            );
          })()}
      </svg>

      {/* chips */}
      {systems.map((key, i) => {
        const s = spring({ frame: frame - (chipStart + i * chipStep), fps, config: { damping: 13 } });
        const item = legend[key as keyof typeof legend];
        return (
          <div
            key={key}
            style={{
              position: "absolute",
              left: cx(i) - CHIP_W / 2,
              top: ROW_Y,
              width: CHIP_W,
              height: CHIP_H,
              transform: `scale(${s})`,
              backgroundColor: theme.systems[key] ?? theme.systems.multi,
              color: chipTextColor(key),
              borderRadius: 18,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 36,
              fontWeight: 800,
              boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
            }}
          >
            {item?.label ?? key}
          </div>
        );
      })}

      {/* closes label under the return arc */}
      <div
        style={{
          position: "absolute",
          top: RETURN_Y + 14,
          left: 0,
          width: 1920,
          textAlign: "center",
          color: theme.return,
          fontSize: 30,
          fontWeight: 700,
          opacity: interpolate(frame, [returnStart + 10, returnStart + 28], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        ↩ {loop.closes} re-enters — compounds the next cycle
      </div>
    </AbsoluteFill>
  );
};
