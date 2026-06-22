# smmt-internal-tooling

Internal tooling that connects **ten MCP servers** to a local **OpenClaw** agent — sales/marketing prospecting, CRM, email, and ad-platform automation through natural-language instructions. Setup is driven by a `Makefile`; secrets live in `envs/.env`; the full reference lives in `docs/`.

---

## Contents

- [Project structure](#project-structure)
- [Quick start (macOS)](#quick-start-macos)
- [Make targets](#make-targets)
- [Credentials (envs/.env)](#credentials-envsenv)
- [Playbooks](#playbooks)
  - [1. Build a targeted prospect list (Apollo)](#1-build-a-targeted-prospect-list-apollo)
  - [2. Find consulting opportunities on LinkedIn](#2-find-consulting-opportunities-on-linkedin)
  - [3. Apply to jobs on Upwork](#3-apply-to-jobs-on-upwork)
  - [4. Launch a lookalike campaign on Meta (FB + IG)](#4-launch-a-lookalike-campaign-on-meta-fb--ig)
  - [5. Push enriched contacts into HubSpot](#5-push-enriched-contacts-into-hubspot)
  - [6. Cross-platform audience push (advanced)](#6-cross-platform-audience-push-advanced)
- [What does NOT work end-to-end](#what-does-not-work-end-to-end)
- [Safety](#safety)
- [The full guide](#the-full-guide)

---

## Project structure

```
smmt-internal-tooling/
├── docs/
│   └── mcp.openclaw.setup.guide.docx   # full reference: every service, tokens, capabilities
├── data/
│   └── .gitkeep                         # placeholder (exports, scratch data, etc.)
├── config/
│   └── all.services.json                # all 10 MCP servers; values read from envs/.env
├── envs/
│   └── .env                             # your credentials (stubbed; fill these in)
├── Makefile                             # install / render / load / verify automation
├── .gitignore                           # keeps rendered config + .bak out of git
└── README.md
```

The ten servers: `apollo`, `hubspot`, `linkedin`, `upwork`, `google-drive`, `gmail`, `meta-ads` (Facebook + Instagram), `x`, `youtube`, `youtube-ads`.

> `config/all.services.json` is a **template** — its values are `${VAR}` references. `make config` substitutes them from `envs/.env` into a rendered file and merges that into OpenClaw's config. You only ever edit `envs/.env`.

> **Note on the Makefile name:** your spec listed it as `make`; it's named **`Makefile`** so the `make` command finds it automatically. Rename if you prefer (`make -f make …`).

---

## Quick start (macOS)

```bash
cd smmt-internal-tooling

make install        # Homebrew: node, uv, pipx, jq + mcporter   (one time)
make doctor         # confirm the toolchain is present

# 1) put your credentials in envs/.env  (see the table below)
make check-env      # shows which values are still empty/placeholder

make config         # render config from envs/.env + merge into ~/.openclaw/openclaw.json (backs it up)
make verify         # openclaw mcp list — all 10 servers should appear
```

One-time browser sign-ins for the Google services (run after filling `.env`):

```bash
make auth-gmail     # Gmail OAuth  (needs gcp-oauth.keys.json in ~/.gmail-mcp/)
make auth-gdrive    # Google Drive OAuth (browser opens on first run)
```

There is no single "MCP" to install — `make install` sets up the runtimes the servers run on (`node`/`npx`, `uv`/`uvx`, `pipx`) plus `jq` and `mcporter`.

---

## Make targets

| Target | What it does |
|---|---|
| `make help` | List all targets (default). |
| `make install` | Install the macOS toolchain (Homebrew packages + `mcporter`). |
| `make doctor` | Check that `node`, `uv`, `pipx`, `jq`, `perl`, `openclaw`, `mcporter`, … are installed. |
| `make check-env` | Report which `envs/.env` values are still empty or placeholders. |
| `make render` | Substitute `envs/.env` into `config/all.services.json` → `config/all.services.rendered.json` (validates JSON). |
| `make config` | `render`, then deep-merge the servers into `~/.openclaw/openclaw.json` (with a `.bak` backup). |
| `make verify` | `openclaw mcp list`. |
| `make auth-gmail` / `make auth-gdrive` | One-time Google OAuth flows. |
| `make upwork-login` | Notes for switching Upwork to the browser server (needed to apply to jobs). |
| `make clean` | Remove the rendered config artifact. |
| `make all` | `install` → `config` → `verify`. |

---

## Credentials (envs/.env)

Fill these in `envs/.env`, then run `make config`. "Gotcha" is what usually trips people up.

| Variable(s) | Service | Where to get it | Gotcha |
|---|---|---|---|
| `APOLLO_MCP_PATH`, `APOLLO_API_KEY` | Apollo | Clone+build `apollo-io-mcp`; key from Settings → Integrations → Apollo API | Path is the built `dist/index.js`; some endpoints need a **master** key. |
| `HUBSPOT_ACCESS_TOKEN` | HubSpot | Settings → Integrations → Private Apps → Auth tab | Pick read/write scopes; legacy API keys retired Nov 2022. |
| `LINKEDIN_COOKIE` | LinkedIn | `uvx linkedin-scraper-mcp --get-cookie` | Keep `li_at=` prefix; expires ~30 days; **violates LinkedIn ToS**. |
| `UPWORK_ACCESS_TOKEN` | Upwork | `developers.upwork.com` (approval, ~2 wks) | API can't reliably submit proposals — use the browser server to apply. |
| `GDRIVE_CLIENT_ID/SECRET`, `GDRIVE_CREDS_DIR` | Google Drive | Google Cloud OAuth (Desktop client) | `CREDS_DIR` must hold `gcp-oauth.keys.json`; publish consent screen to **Production**. |
| *(none)* | Gmail | — | No vars; run `make auth-gmail` once. |
| `META_ADS_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, `META_APP_ID/SECRET`, `META_BUSINESS_ID` | Meta Ads (FB+IG) | Meta App → Marketing API → System User token (`ads_management`) | 1–3 day app review; **real ad spend**. |
| `X_API_KEY/SECRET`, `X_ACCESS_TOKEN/SECRET` | X | X Developer Portal (Basic ~$200/mo) | This server is **organic only**; X *Ads* needs a managed MCP. |
| `YOUTUBE_API_KEY` | YouTube (content) | Google Cloud → YouTube Data API v3 → API key | 10k units/day; search = 100 units each. |
| `GOOGLE_PROJECT_ID`, `GOOGLE_ADS_DEVELOPER_TOKEN` | YouTube Ads | Google Ads API Center | Official server is **read-only**; Customer Match uploads restricted (Apr 2026). |

---

## Playbooks

Once `make verify` shows the servers, drive them with natural-language instructions. Name the server (e.g. "use apollo to…") so OpenClaw routes correctly.

### 1. Build a targeted prospect list (Apollo)

**Goal:** a filtered, enriched list of people matching your ICP.
**Needs:** `apollo`.

> "Use apollo to find VP or Director of Marketing at US B2B SaaS companies with 50–500 employees that posted a marketing-hire job in the last 30 days. Enrich the top 100 with verified work emails, then give me the list as a table."

**Functionality available** — the Apollo server in use (Chainscore `apollo-io-mcp`) exposes the tools below. This is the complete surface; nothing beyond it:

- **People search & enrichment:** `search_people`, `enrich_person`, `bulk_enrich_people`
- **Company / organization:** `search_organizations`, `enrich_organization`, `get_organization`, `get_organization_job_postings`
- **CRM — contacts:** `create_contact`, `update_contact`, `get_contact`, `search_contacts`, `delete_contact`, `bulk_create_contacts`, `bulk_update_contacts`
- **CRM — accounts:** `create_account`, `update_account`, `search_accounts`
- **CRM — deals/opportunities:** `search_opportunities`, `get_opportunity`, `create_opportunity`, `update_opportunity`
- **CRM — tasks:** `search_tasks`, `get_task`, `create_task`, `update_task`
- **CRM — notes:** `search_notes`, `create_note`, `delete_note`
- **Email sequences & outreach:** `search_sequences`, `add_contacts_to_sequence`, `update_sequence_status`, `search_outreach_emails`, `get_email_activities`, `list_email_accounts`
- **Labels & tags:** `list_labels`, `create_label`, `update_label`, `delete_label`
- **Pipeline stages:** `list_contact_stages`, `list_account_stages`, `list_opportunity_stages`
- **Team & users:** `search_users`
- **Activity tracking:** `search_activities`, `search_phone_calls`
- **Custom fields & metadata:** `list_fields`, `create_custom_field`, `list_custom_fields_deprecated`
- **News, usage & health:** `search_news_articles`, `get_api_usage_stats`, `health_check`

**Not available here:** creating saved **List** objects or named **Persona** templates, and **Bombora buying-intent** filtering. Hiring signals come only via `get_organization_job_postings` / `search_news_articles`. Build the filtered set with `search_people` + enrichment and act on it (sequence, label, export).

**Notes:** `search_people` is FREE while `enrich_person` costs ~1 credit — prospect first, then enrich. `health_check` / `get_api_usage_stats` are FREE.

### 2. Find consulting opportunities on LinkedIn

**Goal:** surface contract/consulting gigs and the companies behind them, then find and reach decision-makers — using Apollo for the people step, since the LinkedIn server cannot search people.
**Needs:** `linkedin` (scraping) → `apollo` → `gmail`.

**Functionality available** — the LinkedIn server in use (stickerdaniel `linkedin-scraper-mcp`) exposes exactly **6 read-only tools**. This is the complete surface:

- `search_jobs` — search jobs by keyword + location
- `get_job_details` — full details for a specific job posting
- `get_recommended_jobs` — your personalized recommended jobs
- `get_person_profile` — fetch a **specific** profile by URL (experience, education, skills, certifications, projects, …)
- `get_company_profile` — fetch a specific company's profile
- `close_session` — close the browser session / clean up

**Not available here:** **no people search** (you must already have a profile's URL), **no messaging/InMail**, **no posting/commenting/liking**, **no connection export**. Read-only scraping. (Those need a different server or a fork.)

Prompts (run in sequence):

> 1. "Use linkedin `search_jobs` to find contract, fractional, or consulting roles in [your niche] posted recently, and list the hiring companies."
> 2. "Use linkedin `get_company_profile` to research the top 5 hiring companies."
> 3. "Use apollo `search_people` to find the head of [department] at those companies, then `enrich_person` for verified work emails." *(Apollo does the people search the LinkedIn server can't.)*
> 4. "Use gmail to draft a short, tailored outreach email to each — reference the role they're hiring for."

**Notes:** no LinkedIn freelance-marketplace API — this is job listings + company research + outreach. The scraping server **violates LinkedIn's User Agreement**; keep volume low and one session per cookie. Don't auto-send; review drafts first.

### 3. Apply to jobs on Upwork

**Goal:** find relevant jobs and submit proposals.
**Needs:** an Upwork **browser-automation** server (the API server can't reliably submit proposals).

Swap the `upwork` block in `config/all.services.json` to a browser server, then authenticate once (`make upwork-login` prints the steps):

```jsonc
"upwork": { "command": "uv", "args": ["--directory", "/path/to/upwork-mcp", "run", "upwork-mcp"] }
```
```bash
uv run upwork-mcp --login   # logs into your real Chrome once; session persists
```

> 1. "Use upwork to search for [skill] jobs posted today with budget over $[X], and summarize the top 10."
> 2. "Draft a proposal for job #3 tailored to my profile and rate, show it to me, and submit it once I approve."

**Notes:** browser automation runs against Upwork's terms and can flag your account — throttle, keep a human in the loop, never apply on a loop.

### 4. Launch a lookalike campaign on Meta (FB + IG)

**Goal:** the cleanest end-to-end "list → asset → lookalike → campaign" pipeline.
**Needs:** `apollo` (seed list) + `meta-ads`. One Meta server covers both Facebook and Instagram.

> 1. "Use apollo to export my best-fit customer list (work emails) for [ICP]."
> 2. "Use meta-ads to create a custom audience from that list, then a 1% lookalike audience targeting the US."
> 3. "Use meta-ads to upload `/path/to/creative.mp4` as ad creative." *(9:16 for Instagram Reels/Stories)*
> 4. "Use meta-ads to create a conversions campaign targeting that lookalike, $100/day, Facebook + Instagram placements — leave it **paused** for my review."

**Notes:** token needs `ads_management` (1–3 day review). Spends **real money** — always create paused and review before enabling.

### 5. Push enriched contacts into HubSpot

**Goal:** sync a prospect list into your CRM.
**Needs:** `hubspot` + a list (e.g. from Playbook 1).

> "Use hubspot to create or update contacts from this enriched list, set lifecycle stage to 'lead', and add them all to the '[list name]' static list."

**Notes:** the Private App token must include matching `crm.objects.*.write` scopes or writes silently fail.

### 6. Cross-platform audience push (advanced)

No single MCP does all of it, and "lookalike" is a different feature on each platform:

| Platform | Feasible today? | "Lookalike" = | What it takes |
|---|---|---|---|
| **Meta (FB + IG)** | ✅ Full pipeline | Lookalike Audience | `meta-ads` + `ads_management` token |
| **LinkedIn** | ⚠️ Partial | **Predictive Audience** (classic lookalikes removed Feb 2024) | Marketing API approval (`rw_dmp_segments`) + a write-capable LinkedIn **Ads** MCP |
| **X** | ⚠️ Partial | Tailored Audience + "Similar to Followers Of" | X **Ads** API approval + a **managed** MCP (no OSS X Ads server) |
| **YouTube / Google** | ❌ Mostly blocked | Customer Match + optimized targeting | New list uploads restricted since Apr 1, 2026 → Data Manager API (rare allowlist) |

See `docs/mcp.openclaw.setup.guide.docx` → *"The 'list to asset to lookalike' workflow, per platform"* for the per-platform steps.

---

## What does NOT work end-to-end

- **LinkedIn classic lookalikes are gone** (Feb 2024, incl. the Lookalike API). The modern equivalent is **Predictive Audiences** (needs Marketing Developer Platform approval + a write-capable LinkedIn **Ads** MCP — the `linkedin` scraping server here cannot touch ads).
- **X Ads has no dedicated open-source MCP.** The `x` server is **organic only**. Ad campaigns need a managed multi-platform MCP or the X Ads API directly.
- **Google/YouTube Customer Match uploads are restricted** (since Apr 1, 2026 — new list uploads go through the Data Manager API). The `youtube-ads` server is **read-only**.
- **Apollo can't "create a List/Persona/apply intent" via MCP** — it searches with filters + signals and acts on the results (see Playbook 1).

---

## Safety

- **Sanctioned API paths** (Apollo, HubSpot, Google Drive, Gmail, Meta Ads, Google Ads, the official LinkedIn/X/Upwork APIs) respect your permissions — the safe default.
- **Scraping/browser paths** (LinkedIn cookie, Upwork CDP) bypass API limits but **violate platform terms** — rate-limit, don't run on a loop.
- **Ad accounts are real money.** Prefer read-only or "create paused"; confirm before enabling or changing budgets.
- **Secrets:** `envs/.env` is a stubbed template tracked in the repo. Once you add **real** credentials, don't commit them — `git rm --cached envs/.env` or keep secrets out of version control. `config/all.services.rendered.json` (generated by `make config`) contains live tokens and is git-ignored; never force-add it.
- **Community servers are not vendor-endorsed.** Review the source before granting a live session or token; pin to a version rather than `latest`.

---

## The full guide

`docs/mcp.openclaw.setup.guide.docx` is the complete reference: per-service official vs community servers, a Can-do / Cannot-do breakdown per server, token generation, config entries, the cross-platform workflow analysis, and an *"Answers to your specific questions"* section.

*Compiled mid-2026 — MCP servers, package names, auth rules, and ad-API policies change frequently; re-verify before deploying.*
