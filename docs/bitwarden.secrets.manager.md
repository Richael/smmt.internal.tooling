# Bitwarden Secrets Manager — secrets for the OpenClaw runner

This repo loads 10 MCP servers into OpenClaw. Credentials used to live in the `.env`
(tracked in git — not safe). They now live in **Bitwarden Secrets Manager**; `envs/.env`
keeps only the two machine-specific *paths*. Secrets are injected at runtime by `bws run`.

## TL;DR

```bash
# one-time, per machine
export BWS_ACCESS_TOKEN=...      # openclaw-runner machine-account token (the ONLY secret on the box)
export BWS_PROJECT_ID=...        # the project holding the API keys

./scripts/bws-seed.sh            # ONE TIME: migrate existing envs/.env values into Bitwarden
#   → then blank the secret values out of envs/.env, keeping only the 2 paths
#   → rotate any key that was ever committed to git

./scripts/bws-config.sh          # render + merge MCP servers into OpenClaw (secrets pulled live)
make verify                      # openclaw mcp list — all 10 servers should appear
```

## One-time team setup (admin, in the Bitwarden web vault)

1. **Secrets Manager → Projects →** create `api-testing-keys`.
2. **Machine accounts →** create `openclaw-runner`; grant it **read** access to that project
   (a second account with **write** is only needed to run `bws-seed.sh`).
3. **Generate an access token** for the machine account → that's `BWS_ACCESS_TOKEN`.
4. Copy the project's id → that's `BWS_PROJECT_ID`.
5. Install the CLI: `brew install bitwarden/tap/bws` (or see Bitwarden docs).

## Secret naming (key == env var name, 1:1)

`bws run` exposes each secret as an env var **named exactly its Bitwarden key**, and the
services template substitutes those names. So create these 19 secrets with these exact keys:

| Bitwarden secret key | Service | Notes |
|---|---|---|
| `APOLLO_API_KEY` | Apollo | some endpoints need a *master* key |
| `HUBSPOT_ACCESS_TOKEN` | HubSpot | Private App token, matching `crm.objects.*` scopes |
| `LINKEDIN_COOKIE` | LinkedIn | keep `li_at=` prefix; ~30-day expiry; ToS-sensitive |
| `UPWORK_ACCESS_TOKEN` | Upwork | API can't submit proposals (browser server for that) |
| `GDRIVE_CLIENT_ID` / `GDRIVE_CLIENT_SECRET` | Google Drive | OAuth desktop client |
| `META_ADS_ACCESS_TOKEN` | Meta Ads | System User token, `ads_management` |
| `META_AD_ACCOUNT_ID` / `META_APP_ID` / `META_APP_SECRET` / `META_BUSINESS_ID` | Meta Ads | ids + app secret |
| `X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_TOKEN_SECRET` | X | organic only |
| `YOUTUBE_API_KEY` | YouTube | Data API v3 key |
| `GOOGLE_PROJECT_ID` / `GOOGLE_ADS_DEVELOPER_TOKEN` | YouTube Ads | read-only server |
| `FAL_KEY` | Fal.ai | image/video/audio generation (new in Task 004) |

> `remotion`, `excalidraw`, and `playwright` (also added in Task 004) need **no secrets**.

Stay in `envs/.env` (NOT secret, per-machine): `APOLLO_MCP_PATH`, `GDRIVE_CREDS_DIR`.

## How it wires in (no Makefile rewrite needed)

`make render` does `set -a; . $(ENV_FILE); set +a` then substitutes `${VAR}` from the
environment. `bws run` puts the Bitwarden secrets into that environment first, so they
resolve; `envs/.env` supplies only the two paths. The file layout now matches the Makefile
defaults (`ENV_FILE=envs/.env`, `TEMPLATE=config/all.services.json`), so `scripts/bws-config.sh`
just runs `bws run -- make config` with no overrides.

## What still touches disk (important)

OpenClaw reads tokens from its own JSON config, so `make config` writes the resolved
tokens into `config/all.services.rendered.json` and `~/.openclaw/openclaw.json`. Bitwarden
keeps secrets out of **source control** and is the **source of truth**, but those two
rendered files contain live tokens — both are git-ignored (`.gitignore`); never share them,
and `make clean` removes the rendered artifact. (If OpenClaw ever supports `${ENV}` refs in
its config, we can stop materialising values entirely.)

## Security checklist

- [ ] Rotate the ~3 keys that were committed in `envs/.env`.
- [ ] `git rm --cached envs/.env` and confirm `.gitignore` now covers it.
- [ ] Secrets in Bitwarden; `envs/.env` holds only the two paths.
- [ ] `openclaw-runner` machine account has **read-only**, single-project access.
- [ ] OpenClaw approval gates ON for shell + side-effectful tools; **inbound messages are
      untrusted** — never let a WhatsApp/Telegram message trigger a secret read, an ad-spend
      change, or an outbound send without your confirmation.
- [ ] Pin community MCP servers to a version, not `latest`.

## File layout (resolved)

The repo previously shipped `config/.env` + `config/services.json`, which did not match the
Makefile/README (`envs/.env` + `config/all.services.json`). That has been reconciled — the
files now live at `envs/.env` and `config/all.services.json`, so `make` works with no path
overrides. `envs/.env.example` is the non-secret template.
