#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# bws-seed.sh — ONE-TIME migration: push the credentials currently in envs/.env
# into a Bitwarden Secrets Manager project (secret key == variable name).
# After running this successfully:  blank the secret values out of envs/.env
# (keep only APOLLO_MCP_PATH + GDRIVE_CREDS_DIR) and ROTATE any key that was ever
# committed to git.
#
# Usage:
#   export BWS_ACCESS_TOKEN=...   # a machine account with WRITE access to the project
#   export BWS_PROJECT_ID=...     # target project id
#   ./scripts/bws-seed.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
: "${BWS_ACCESS_TOKEN:?set BWS_ACCESS_TOKEN (needs write access to the project)}"
: "${BWS_PROJECT_ID:?set BWS_PROJECT_ID}"
command -v bws >/dev/null 2>&1 || { echo "Install bws CLI first"; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/envs/.env"
[ -f "$SRC" ] || { echo "Missing $SRC"; exit 1; }

# Variables that are SECRETS (everything except the two machine paths).
SECRETS="APOLLO_API_KEY HUBSPOT_ACCESS_TOKEN LINKEDIN_COOKIE UPWORK_ACCESS_TOKEN \
GDRIVE_CLIENT_ID GDRIVE_CLIENT_SECRET META_ADS_ACCESS_TOKEN META_AD_ACCOUNT_ID \
META_APP_ID META_APP_SECRET META_BUSINESS_ID X_API_KEY X_API_SECRET X_ACCESS_TOKEN \
X_ACCESS_TOKEN_SECRET YOUTUBE_API_KEY GOOGLE_PROJECT_ID GOOGLE_ADS_DEVELOPER_TOKEN"

pushed=0; skipped=0
for KEY in $SECRETS; do
  VAL="$(grep -E "^${KEY}=" "$SRC" | head -1 | cut -d= -f2- || true)"
  VAL="${VAL%\"}"; VAL="${VAL#\"}"; VAL="${VAL%\'}"; VAL="${VAL#\'}"
  if [ -z "$VAL" ]; then echo "skip  $KEY (empty)"; skipped=$((skipped+1)); continue; fi
  if bws secret create "$KEY" "$VAL" "$BWS_PROJECT_ID" >/dev/null 2>&1; then
    echo "pushed $KEY"; pushed=$((pushed+1))
  else
    echo "exists/err $KEY — update manually with: bws secret edit <id> --value …"; skipped=$((skipped+1))
  fi
done
echo "── done: $pushed pushed, $skipped skipped. Now blank these out of envs/.env and rotate any committed keys."
