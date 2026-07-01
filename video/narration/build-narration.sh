#!/usr/bin/env bash
# Render the voiceover from scripts.md into per-section audio clips, using macOS's
# built-in `say` (free, offline TTS) + `afconvert` (AIFF -> AAC/m4a). Also writes
# durations.json so the Remotion timeline and YouTube chapters stay in sync.
#
#   bash video/narration/build-narration.sh
#   VOICE="Ava (Enhanced)" RATE=175 bash video/narration/build-narration.sh
#
# Output: video/remotion/public/narration/NN-slug.m4a  +  durations.json
# Swap in a higher-end voice later (fal.ai / ElevenLabs) by replacing the `say` call.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/scripts.md"
OUT="$HERE/../remotion/public/narration"
VOICE="${VOICE:-Samantha}"     # fallback voice present on every mac; override via env
RATE="${RATE:-180}"
mkdir -p "$OUT"

command -v say >/dev/null || { echo "macOS 'say' not found (this step needs macOS)"; exit 1; }
# fall back to the system default voice if the requested one isn't installed
if ! say -v '?' | grep -qi "$(printf '%s' "$VOICE" | cut -d' ' -f1)"; then
  echo "voice '$VOICE' not installed — using system default"; VOICE=""
fi

# split scripts.md into per-section bodies (one file per '## ' header, in order)
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
awk '
  /^## / {
    n++; hdr=$0; sub(/^## /,"",hdr); sub(/ *\([0-9]+s\) *$/,"",hdr);
    slug=tolower(hdr); gsub(/[^a-z0-9]+/,"-",slug); gsub(/^-|-$/,"",slug);
    file=sprintf("%s/%02d_%s.txt", dir, n-1, slug);
    print hdr > (file ".hdr"); next
  }
  n>0 && !/^#/ && !/^---/ && NF { printf "%s ", $0 >> file }
' dir="$TMP" "$SRC"

echo "{" > "$OUT/durations.json"
first=1
for body in "$TMP"/*.txt; do
  [ -e "$body" ] || continue
  base="$(basename "${body%.txt}")"
  hdr="$(cat "${body}.hdr")"
  aiff="$TMP/$base.aiff"; m4a="$OUT/$base.m4a"
  text="$(cat "$body")"
  if [ -n "$VOICE" ]; then say -v "$VOICE" -r "$RATE" -o "$aiff" "$text"
  else say -r "$RATE" -o "$aiff" "$text"; fi
  afconvert "$aiff" "$m4a" -f m4af -d aac >/dev/null
  dur="$(afinfo "$m4a" | awk -F'[:=]' '/estimated duration/ {gsub(/[^0-9.]/,"",$2); print $2}')"
  [ $first -eq 1 ] && first=0 || echo "," >> "$OUT/durations.json"
  printf '  "%s": { "seconds": %s, "title": "%s" }' "$base" "${dur:-0}" "$hdr" >> "$OUT/durations.json"
  echo "rendered $base  (${dur:-?}s)"
done
printf '\n}\n' >> "$OUT/durations.json"
echo "Wrote $OUT/durations.json"
