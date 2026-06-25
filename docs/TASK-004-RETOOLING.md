# Task 004 — RE-TOOLING (consolidated)

Single-branch record of the Task 004 work. Everything below is already merged into `playground`
(via PRs #5/#6/#7) and is reproduced on `feat/-task-004-retooling---playground` as one branch.

## 1. MCP library: 10 → 16 servers

Verified-only (each package confirmed to resolve with a runnable bin), added to **both**
`config/services.json` and `config/all.services.json`, wired through Bitwarden + `envs/.env.example`.

| Server | Package | Creds |
|---|---|---|
| `remotion` | `@remotion/mcp` | none |
| `excalidraw` | `@cmd8/excalidraw-mcp` | none |
| `playwright` | `@playwright/mcp` (MS official) | none |
| `fal` | `fal-mcp-server` (uvx) — image/video/audio gen | `FAL_KEY` |
| `google-analytics` | `analytics-mcp` (Google official, pipx) — GA4 | `GOOGLE_PROJECT_ID` + `GOOGLE_APPLICATION_CREDENTIALS` path |
| `cloudflare-observability` | Cloudflare official remote MCP (`mcp-remote`) | none (browser OAuth) |

GA + Cloudflare were the "DEFINITELY DO THIS" callout — and GA resolves the garbled **"Palytics"**.

## 2. Video pipeline — Parker's twelve closed loops (`video/`)

Reusable Remotion + Excalidraw pipeline driven by one source of truth (`video/data/loops.json`).
Source: `Adopters/playbooks--001.parker.docx` (SMMT's 12 compounding closed loops across
Shopify · Klaviyo · Meta/IG · Amazon).

- `excalidraw/parker-twelve-loops.excalidraw` — generated diagram doc
- `narration/` — voiceover via macOS `say` → 14 clips + `durations.json`
- `remotion/` — `LoopScene ×12` + Intro/Outro → `out/twelve-loops.mp4` (5:37, verified render)
- `youtube/post.md` — title/description/chapters (timecodes match the render)
- `prompts/00–05` — reusable prompts to re-run for any future adopter

## 3. Apollo / HubSpot / Gmail / Drive playbooks (`playbooks/`)

10 MCP-grounded playbooks (respect each server's actual tool surface; write to `data/exports/`,
git-ignored for PII):

- **Apollo A1–A4:** persona+lists, sequence stats/open rates, build sequences, list/lane comparison + why
- **HubSpot H1–H2:** filter people, stagnant deals by N days
- **Gmail G1–G3:** templated sends from HubSpot / Apollo / CSV lists (shared `merge/render.mjs` dry-run tool, tested)
- **Drive D1:** read shared lists/briefs + log results to a tracking Sheet

## Caveats

- **Not yet run live** — no API keys in; configs + playbooks are built and internally validated
  (JSON valid, packages resolve, merge tool tested), not exercised against real accounts. The
  video MP4 is the exception (rendered end-to-end).
- Voice = macOS `say` (free/offline), not ElevenLabs (deprioritized; swap-in documented).

## Outstanding (parked)

- **005** — Apollo list + video asset → lookalike on 2 platforms (no-spend, then with-spend).
- **006** — 3 client taskbooks (needs the Zeev example + which 3 clients).
- **Gmail send-scheduling** — batches today, no scheduler.
- `cacut`/CapCut (no MCP), native Meta AI video-gen (none; `fal` covers), OpenClaw drag-and-drop dashboard idea.

## Recommended next step

Load credentials into Bitwarden, then live smoke test: `make config` → `make verify` (all 16
servers appear), then run one Apollo + one HubSpot playbook against a real account.
