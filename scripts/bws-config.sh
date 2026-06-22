#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# bws-config.sh — render + load the 10 MCP servers into OpenClaw, with all
# credentials pulled LIVE from Bitwarden Secrets Manager (nothing secret on disk
# except OpenClaw's own rendered config, which is git-ignored).
#
# How it works:
#   `bws run` injects every secret in the project as an env var, then runs
#   `make config`. The Makefile's `render` step substitutes ${VAR} in
#   config/all.services.json from the environment — so the injected secrets
#   resolve, and envs/.env only needs the two non-secret machine PATHS.
#
# Usage:
#   export BWS_ACCESS_TOKEN=...        # the openclaw-runner machine-account token
#   export BWS_PROJECT_ID=...          # the api-testing-keys project id
#   ./scripts/bws-config.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

: "${BWS_ACCESS_TOKEN:?set BWS_ACCESS_TOKEN — the openclaw-runner machine-account token}"
: "${BWS_PROJECT_ID:?set BWS_PROJECT_ID — the Secrets Manager project holding the API keys}"

command -v bws  >/dev/null 2>&1 || { echo "Install the Bitwarden Secrets Manager CLI: https://bitwarden.com/help/secrets-manager-cli/"; exit 1; }
command -v make >/dev/null 2>&1 || { echo "make not found"; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# envs/.env must exist (the Makefile sources it for the machine paths). It must NOT
# contain secrets anymore — those come from `bws run`.
[ -f envs/.env ] || { echo "Missing envs/.env (copy envs/.env.example and fill the two paths)"; exit 1; }
if grep -qE '^(APOLLO_API_KEY|HUBSPOT_ACCESS_TOKEN|META_ADS_ACCESS_TOKEN|X_API_KEY|YOUTUBE_API_KEY)=[^[:space:]]' envs/.env; then
  echo "⚠️  envs/.env still has secret values. Migrate them to Bitwarden (scripts/bws-seed.sh), blank them out, then rerun." >&2
  exit 1
fi

# Inject secrets from Bitwarden, then render + merge into OpenClaw.
# (Layout now matches the Makefile defaults: ENV_FILE=envs/.env, TEMPLATE=config/all.services.json.)
exec bws run --project-id "$BWS_PROJECT_ID" -- make config
