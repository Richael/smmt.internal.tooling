#!/usr/bin/env node
// Generate an Excalidraw document (one diagram per loop) from ../data/loops.json.
// Output is a plain .excalidraw JSON file you can open at excalidraw.com or in the
// Excalidraw VS Code / desktop app. Re-run after editing loops.json to regenerate.
//
//   node video/excalidraw/build-excalidraw.mjs
//
// Design: a title block + colour legend, then a vertical stack of loop cards.
// Each card shows the loop number/title, the systems it spans as coloured chips
// connected left-to-right by grey arrows, and a lavender return arrow closing the
// loop (the source doc's convention for "converters/signal re-enter to compound").

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(readFileSync(join(here, "../data/loops.json"), "utf8"));

let seq = 1;
const seed = () => seq++ * 1009; // deterministic, so output is diffable
const els = [];

const base = (type, x, y, w, h, extra = {}) => ({
  id: `el-${seq}`,
  type,
  x,
  y,
  width: w,
  height: h,
  angle: 0,
  strokeColor: "#1e1e1e",
  backgroundColor: "transparent",
  fillStyle: "solid",
  strokeWidth: 2,
  strokeStyle: "solid",
  roughness: 1,
  opacity: 100,
  groupIds: [],
  frameId: null,
  roundness: type === "rectangle" ? { type: 3 } : null,
  seed: seed(),
  version: 1,
  versionNonce: seed(),
  isDeleted: false,
  boundElements: [],
  updated: 1,
  link: null,
  locked: false,
  ...extra,
});

const rect = (x, y, w, h, extra) => els.push(base("rectangle", x, y, w, h, extra));

const text = (x, y, str, { size = 20, color = "#1e1e1e", w, align = "left", bold } = {}) => {
  const fontFamily = bold ? 2 : 1; // 1 = hand-drawn, 2 = normal, 3 = code
  const width = w ?? Math.max(20, str.length * size * 0.55);
  els.push(
    base("text", x, y, width, size * 1.25, {
      strokeColor: color,
      text: str,
      fontSize: size,
      fontFamily,
      textAlign: align,
      verticalAlign: "top",
      baseline: size,
      containerId: null,
      originalText: str,
      lineHeight: 1.25,
    })
  );
};

const arrow = (x1, y1, x2, y2, { color = "#6B7280", width = 2, dashed = false } = {}) => {
  els.push(
    base("arrow", x1, y1, x2 - x1, y2 - y1, {
      strokeColor: color,
      strokeWidth: width,
      strokeStyle: dashed ? "dashed" : "solid",
      points: [
        [0, 0],
        [x2 - x1, y2 - y1],
      ],
      lastCommittedPoint: null,
      startBinding: null,
      endBinding: null,
      startArrowhead: null,
      endArrowhead: "arrow",
      roundness: { type: 2 },
    })
  );
};

const L = data.legend;

// ---- title block -----------------------------------------------------------
let y = 40;
text(60, y, data.meta.title, { size: 36, bold: true });
y += 50;
text(60, y, data.meta.subtitle, { size: 20, color: "#6B7280" });
y += 36;
text(60, y, data.meta.tagline, { size: 14, color: "#6B7280", w: 1000 });
y += 50;

// ---- legend ----------------------------------------------------------------
let lx = 60;
for (const key of ["shopify", "klaviyo", "meta", "amazon", "multi", "smmt", "return"]) {
  const item = L[key];
  rect(lx, y, 18, 18, { backgroundColor: item.color, strokeColor: item.color });
  text(lx + 26, y - 2, item.label, { size: 14 });
  lx += item.label.length * 9 + 70;
}
y += 60;

// ---- loop cards ------------------------------------------------------------
const CARD_W = 1180;
const CARD_H = 240;
const CHIP_W = 150;
const CHIP_H = 56;
const CHIP_GAP = 70;

for (const loop of data.loops) {
  const top = y;
  // card frame
  rect(40, top, CARD_W, CARD_H, { strokeColor: "#cbd5e1", strokeWidth: 1.5, backgroundColor: "#fbfbfd" });

  // header: number badge + title + section ref
  rect(64, top + 24, 44, 44, { backgroundColor: L.smmt.color, strokeColor: L.smmt.color });
  text(64 + 14, top + 32, String(loop.id), { size: 24, color: "#ffffff", bold: true });
  text(124, top + 22, loop.short, { size: 22, bold: true, w: 820 });
  text(124, top + 52, `closes on: ${loop.closes}   ·   ${loop.segment}   ·   ${loop.latency}`, {
    size: 14,
    color: "#6B7280",
    w: 820,
  });
  text(CARD_W - 60, top + 24, loop.section, { size: 16, color: "#94a3b8", align: "right" });

  // system chips row
  const chipY = top + 110;
  const chips = loop.systems.map((s) => ({ key: s, ...L[s] }));
  const rowW = chips.length * CHIP_W + (chips.length - 1) * CHIP_GAP;
  let cx = 64 + Math.max(0, (CARD_W - 128 - rowW) / 2);
  const centers = [];
  for (let i = 0; i < chips.length; i++) {
    const c = chips[i];
    rect(cx, chipY, CHIP_W, CHIP_H, { backgroundColor: c.color, strokeColor: c.color });
    // readable label colour: dark chips get white text
    const dark = ["klaviyo", "meta", "smmt"].includes(c.key);
    text(cx + 12, chipY + 16, c.label, { size: 18, color: dark ? "#ffffff" : "#1e1e1e", bold: true });
    centers.push({ x: cx + CHIP_W / 2, leftEdge: cx, rightEdge: cx + CHIP_W });
    if (i > 0) {
      // forward arrow from previous chip to this one
      arrow(centers[i - 1].rightEdge + 6, chipY + CHIP_H / 2, cx - 6, chipY + CHIP_H / 2);
    }
    cx += CHIP_W + CHIP_GAP;
  }

  // lavender return arrow: from last chip, down and back to the first chip
  if (centers.length > 1) {
    const first = centers[0];
    const last = centers[centers.length - 1];
    const ry = chipY + CHIP_H + 34;
    arrow(last.x, chipY + CHIP_H + 4, last.x, ry, { color: L.return.color, width: 3 });
    arrow(last.x, ry, first.x, ry, { color: L.return.color, width: 3 });
    arrow(first.x, ry, first.x, chipY + CHIP_H + 4, { color: L.return.color, width: 3 });
    text(64 + (CARD_W - 128) / 2 - 90, ry + 6, "↩ converters / signal re-enter — compounds next cycle", {
      size: 13,
      color: L.return.color,
    });
  }

  y += CARD_H + 40;
}

const doc = {
  type: "excalidraw",
  version: 2,
  source: "smmt video pipeline — build-excalidraw.mjs",
  elements: els,
  appState: { gridSize: null, viewBackgroundColor: "#ffffff" },
  files: {},
};

const out = join(here, "parker-twelve-loops.excalidraw");
writeFileSync(out, JSON.stringify(doc, null, 2));
console.log(`Wrote ${out} — ${els.length} elements, ${data.loops.length} loops.`);
