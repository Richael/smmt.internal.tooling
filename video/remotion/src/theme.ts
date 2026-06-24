// Visual identity — colours match the source diagrams' legend 1:1.
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;
export const PAD_FRAMES = 18; // ~0.6s of breathing room after each narration clip

export const theme = {
  bg: "#0b0b12",
  bgPanel: "#15151f",
  text: "#f5f5f7",
  textDim: "#9aa0aa",
  systems: {
    shopify: "#95BF47",
    klaviyo: "#1A1A1A",
    meta: "#0866FF",
    amazon: "#FF9900",
    multi: "#6B7280",
    smmt: "#7C5CFF",
  } as Record<string, string>,
  return: "#B7A8F2",
};

// chips whose fill is dark enough that the label should be white
export const darkChips = new Set(["klaviyo", "meta", "smmt"]);

export const chipTextColor = (key: string) =>
  darkChips.has(key) ? "#ffffff" : "#10131a";
