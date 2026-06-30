#!/usr/bin/env bash
# load-mcp.sh — register the rendered MCP servers into OpenClaw the RIGHT way.
#
# Why this exists: OpenClaw (2026.6.x) stores servers under its own `mcp.servers`
# config and rejects a top-level `mcpServers` key. The old `make config` jq-merged
# the repo's `mcpServers` map straight into ~/.openclaw/openclaw.json, which made the
# whole config invalid. This script instead loops over each server and calls
# `openclaw mcp set <name> '<json>'` — the supported, native registration path.
#
#   bash scripts/load-mcp.sh [rendered.json]      # register (skips unfilled creds)
#   DRY_RUN=1 bash scripts/load-mcp.sh            # print what it WOULD do, change nothing
#
# Input: config/all.services.rendered.json (produced by `make render`). Servers whose
# env still contains <<UNSET:VAR>> markers (empty in envs/.env) are skipped, not
# registered broken. No-credential servers always register.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RENDERED="${1:-$ROOT/config/all.services.rendered.json}"
DRY_RUN="${DRY_RUN:-0}"

[ -f "$RENDERED" ] || { echo "Missing $RENDERED — run 'make render' first."; exit 1; }
command -v jq       >/dev/null 2>&1 || { echo "jq not found.";       exit 1; }
command -v openclaw >/dev/null 2>&1 || { echo "openclaw not found."; exit 1; }
jq empty "$RENDERED" 2>/dev/null   || { echo "$RENDERED is not valid JSON."; exit 1; }

set=0; skipped=0; failed=0
while IFS= read -r name; do
  obj="$(jq -c --arg n "$name" '.mcpServers[$n]' "$RENDERED")"

  if printf '%s' "$obj" | grep -q '<<UNSET:'; then
    miss="$(printf '%s' "$obj" | grep -oE '<<UNSET:[A-Z_]+>>' | tr '\n' ' ')"
    printf 'skip   %-26s (unfilled: %s)\n' "$name" "$miss"
    skipped=$((skipped+1)); continue
  fi

  if [ "$DRY_RUN" = "1" ]; then
    printf 'would set %-23s %s\n' "$name" "$obj"
    set=$((set+1)); continue
  fi

  if openclaw mcp set "$name" "$obj" >/dev/null 2>&1; then
    printf 'set    %s\n' "$name"; set=$((set+1))
  else
    printf 'FAIL   %s  (run: openclaw mcp set %s %s)\n' "$name" "$name" "'$obj'"
    failed=$((failed+1))
  fi
done < <(jq -r '.mcpServers | keys[]' "$RENDERED")

echo "----"
echo "registered: $set   skipped (unfilled creds): $skipped   failed: $failed"
if [ "$DRY_RUN" != "1" ] && [ "$set" -gt 0 ]; then
  openclaw mcp reload >/dev/null 2>&1 && echo "reloaded MCP runtimes." || echo "note: run 'openclaw mcp reload' manually."
  echo "Confirm with:  openclaw mcp list"
fi
