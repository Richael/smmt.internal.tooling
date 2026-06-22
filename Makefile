# ============================================================================
# smmt-internal-tooling — Makefile
# Automates: toolchain install, rendering config/all.services.json from
# envs/.env, loading the MCP servers into OpenClaw, one-time OAuth flows,
# and verification. Target: macOS (works with stock GNU Make 3.81).
#
#   First run:  make install  ->  edit envs/.env  ->  make config  ->  make verify
# ============================================================================

SHELL        := /bin/bash
ENV_FILE     := envs/.env
TEMPLATE     := config/all.services.json
RENDERED     := config/all.services.rendered.json
OPENCLAW_CFG := $(HOME)/.openclaw/openclaw.json
REQUIRED_TOOLS := node npm npx uv uvx pipx jq perl openclaw mcporter

.DEFAULT_GOAL := help
.PHONY: help doctor install env check-env render config load verify \
        auth-gmail auth-gdrive auth-youtube upwork-login clean all

help: ## Show this help
	@echo "smmt-internal-tooling — make targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-13s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "First run:  make install  ->  edit envs/.env  ->  make config  ->  make verify"

doctor: ## Check that the required tools are installed
	@echo "Checking required tools..."
	@for t in $(REQUIRED_TOOLS); do \
		if command -v $$t >/dev/null 2>&1; then printf "  \033[32mok\033[0m   %s\n" "$$t"; \
		else printf "  \033[31mMISS\033[0m %s\n" "$$t"; fi; \
	done
	@echo "Run 'make install' to install any missing toolchain (macOS/Homebrew)."

install: ## Install the macOS toolchain (Homebrew packages + mcporter)
	@command -v brew >/dev/null 2>&1 || { echo "Homebrew required: https://brew.sh"; exit 1; }
	brew install node uv pipx jq
	pipx ensurepath
	npm install -g @openclaw/mcporter
	@echo "Toolchain ready. Run 'make doctor', then fill envs/.env and 'make config'."

env: ## Verify envs/.env exists (this repo ships it pre-stubbed)
	@if [ -f $(ENV_FILE) ]; then echo "$(ENV_FILE) present."; \
	else echo "Missing $(ENV_FILE) — restore it from version control."; exit 1; fi

check-env: ## Report env vars still empty or left as placeholders
	@test -f $(ENV_FILE) || { echo "Missing $(ENV_FILE)"; exit 1; }
	@echo "Values in $(ENV_FILE) that still need filling:"
	@grep -nE '^[A-Z_]+=[[:space:]]*$$' $(ENV_FILE) | sed 's/^/  empty:       /' || true
	@grep -nE '(=li_at=$$|=act_$$|ABSOLUTE/PATH|YOUR_USERNAME)' $(ENV_FILE) | sed 's/^/  placeholder: /' || true
	@echo "(anything above still needs a real value before its server will work)"

render: ## Render config/all.services.json from envs/.env -> rendered config
	@test -f $(ENV_FILE) || { echo "Missing $(ENV_FILE) — fill it first"; exit 1; }
	@set -a; . $(ENV_FILE); set +a; \
	perl -pe 's/\$$\{(\w+)\}/(exists $$ENV{$$1} && length $$ENV{$$1}) ? $$ENV{$$1} : "<<UNSET:$$1>>"/ge' $(TEMPLATE) > $(RENDERED)
	@if grep -q '<<UNSET:' $(RENDERED); then \
		echo "Note: these variables are unset/empty in envs/.env:"; \
		grep -oE '<<UNSET:[A-Z_]+>>' $(RENDERED) | sort -u | sed 's/^/  /'; fi
	@python3 -c "import json; json.load(open('$(RENDERED)')); print('Rendered -> $(RENDERED) (valid JSON)')"

config: render ## Render, then merge the MCP servers into OpenClaw (with backup)
	@mkdir -p $(dir $(OPENCLAW_CFG))
	@if [ -f $(OPENCLAW_CFG) ]; then \
		cp $(OPENCLAW_CFG) $(OPENCLAW_CFG).bak; \
		echo "Backed up -> $(OPENCLAW_CFG).bak"; \
		jq -s '.[0] * .[1]' $(OPENCLAW_CFG) $(RENDERED) > $(OPENCLAW_CFG).tmp && mv $(OPENCLAW_CFG).tmp $(OPENCLAW_CFG); \
	else \
		cp $(RENDERED) $(OPENCLAW_CFG); echo "Created $(OPENCLAW_CFG)"; \
	fi
	@echo "Merged MCP servers into $(OPENCLAW_CFG). Restart the Gateway, then 'make verify'."

load: config ## Alias for 'config'
	@true

verify: ## List the MCP servers OpenClaw can see
	@command -v openclaw >/dev/null 2>&1 || { echo "openclaw not found — install it first"; exit 1; }
	openclaw mcp list

auth-gmail: ## One-time Gmail OAuth (browser). Put gcp-oauth.keys.json in ~/.gmail-mcp/
	@mkdir -p $$HOME/.gmail-mcp
	@echo "Ensure ~/.gmail-mcp/gcp-oauth.keys.json exists, then approve in the browser:"
	npx -y @gongrzhe/server-gmail-autoauth-mcp auth

auth-gdrive: ## One-time Google Drive OAuth (browser opens on first run)
	@test -f $(ENV_FILE) || { echo "Missing $(ENV_FILE)"; exit 1; }
	@echo "GDRIVE_CREDS_DIR must contain gcp-oauth.keys.json. A browser opens on first run."
	@set -a; . $(ENV_FILE); set +a; npx -y @isaacphi/mcp-gdrive </dev/null || true

auth-youtube: ## YouTube auth notes (API key needs no OAuth)
	@echo "YouTube content (ZubeidHendricks) uses YOUTUBE_API_KEY — no OAuth needed."
	@echo "For uploads/analytics on your own channel, swap to an OAuth YouTube server (see docs)."

upwork-login: ## Note: applying to Upwork jobs needs the browser server
	@echo "The API server (chinchilla) cannot reliably submit proposals."
	@echo "To apply: swap 'upwork' to a browser server in $(TEMPLATE), then run once:"
	@echo "  uv run upwork-mcp --login   # logs into your real Chrome"

clean: ## Remove the rendered config artifact
	@rm -f $(RENDERED)
	@echo "Removed $(RENDERED)."

all: install config verify ## Full setup: install -> config -> verify
