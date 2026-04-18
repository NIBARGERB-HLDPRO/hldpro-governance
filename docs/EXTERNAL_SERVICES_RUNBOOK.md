# External Services Runbook — hldpro-governance

Version: 2026-04-16
Owner: Operator (nibarger.ben@gmail.com)
Scope: **SSOT for all HLDPRO external services.** This runbook supersedes the downstream repo runbooks (`ai-integration-services/docs/EXTERNAL_SERVICES_RUNBOOK.md`, `HealthcarePlatform/docs/EXTERNAL_SERVICES_RUNBOOK.md`). Those files may be kept as stubs pointing here but should not be independently maintained.

## 1. Codex CLI (OpenAI)

**Purpose:** Tier-1 Dual-Planner partner (`gpt-5.4` high) and Tier-2 Worker (`gpt-5.3-codex-spark` high) in the Society of Minds charter. See `STANDARDS.md §Society of Minds` and the charter decision at `wiki/decisions/2026-04-14-society-of-minds-charter.md`.

### Install & auth
- Binary: `~/.nvm/versions/node/v24.14.1/bin/codex` (OpenAI Codex v0.120.0)
- Login: `codex login` (interactive browser OAuth)
- Config: `~/.codex/config.toml` — must include:
  - `model = "gpt-5.4"`
  - `model_reasoning_effort = "medium"`
  - `[shell_environment_policy] inherit = "all"` (required for Claude-as-reviewer cross-model flow — see AIS runbook §Claude Code)

### Quota preflight (run before every spark fire)

Codex-spark has a rolling 5-hour primary window and a 7-day secondary window. Both are quota-limited (NOT unlimited as legacy memory entries may claim).

**One-shot probe:**
```bash
echo 'say "codex ok"' | codex exec -m gpt-5.3-codex-spark \
  -c model_reasoning_effort=low --sandbox read-only \
  --skip-git-repo-check - 2>&1 | tail -5
```

`ERROR: You've hit your usage limit ...` means blocked; `say "codex ok"` reply means available.

**Inspect most recent quota snapshot:**
```bash
rg '"limit_id":"codex_bengalfox"' ~/.codex/sessions/$(date +%Y/%m/%d)/*.jsonl | tail -n 5
```

Spark-specific `limit_id` is `codex_bengalfox`. GPT-5.4 has a different `limit_id`; list them all:
```bash
rg '"limit_id":"[^"]+"' ~/.codex/sessions/$(date +%Y/%m/%d)/*.jsonl -o | sort | uniq -c
```

**Translate a `resets_at` epoch to local time:**
```bash
date -r <epoch_seconds> '+%Y-%m-%d %H:%M:%S %Z'
```

Example: `resets_at: <epoch>` → run the `date -r` command above to see the local reset time.

### Wrapper script

Repeatable one-command preflight: `bash scripts/codex-preflight.sh [--log|--probe]`

- default (no args) — log-check first; if logs are OK or inconclusive, run a live probe
- `--log` — log-check only (no API call)
- `--probe` — live probe only (consumes a tiny bit of quota)

Exit codes: `0` available · `1` blocked · `2` config error or log inconclusive.

### Rate-limit shape (from live token_count events)

```json
{
  "limit_id": "codex_bengalfox",
  "limit_name": "GPT-5.3-Codex-Spark",
  "primary":   {"used_percent": 100.0, "window_minutes": 300,  "resets_at": <epoch>},
  "secondary": {"used_percent":  30.0, "window_minutes": 10080,"resets_at": <epoch>},
  "credits":   {"has_credits": false, "unlimited": false, "balance": null}
}
```

Block condition: `primary.used_percent >= 100` OR `secondary.used_percent >= 100`.

### Fallback ladder (when spark blocked)

Per `STANDARDS.md §Society of Minds`, Tier-2 ladder is:

1. `gpt-5.3-codex-spark` @ `high` ← primary
2. `gpt-5.3-codex-spark` @ `medium` ← same quota pool, also blocked when primary is
3. `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (warm daemon) — see §4 below
4. `claude-sonnet-4-6` (cost-flagged; log to `raw/model-fallbacks/`)

Every fallback MUST be logged via `scripts/model-fallback-log.sh`:
```bash
bash scripts/model-fallback-log.sh \
  --tier 2 \
  --primary gpt-5.3-codex-spark \
  --fallback qwen2.5-coder-7b-instruct-4bit \
  --reason "codex-spark primary window 100%, reset <local-time>" \
  --caller <slug>
```

### Rotation
- Re-run `codex login` when token expires (1 year cadence)
- Keep `config.toml` backed up; never commit it to git

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-14 | Spark quota preflight via `rg limit_id` + `codex exec` probe | Primary 100%, secondary 30%, reset 00:28 CDT next day |
| 2026-04-14 | GPT-5.4 Tier-1 planner probe (implicit — used all session) | OK |

---

## 2. Claude Code CLI (Anthropic)

**Purpose:** Tier-1 Dual-Planner partner (`claude-opus-4-6`), Tier-3 code reviewer (`claude-sonnet-4-6`), Tier-4 gate (`claude-haiku-4-5-20251001`). Also serves as cross-model reviewer invoked FROM codex via `scripts/codex-review.sh claude`.

### Auth
- `CLAUDE_CODE_OAUTH_TOKEN` in repo-level `.env` (NOT committed)
- Issued via `claude setup-token` (operator Max subscription)
- 1-year expiry; current token: 2026-04-09
- Same token shared across all HLD Pro repos

### Preflight
```bash
claude -p "say ok" 2>&1 | tail -3
```

### Rotation
1. `claude setup-token` (browser OAuth)
2. Update `.env` in every governed repo (governance, AIS, HP, knocktracker, local-ai-machine)
3. Note rotation in this runbook's Changelog

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-09 | Token issued, deployed to all 5 repos | OK |

---

## 3. Anthropic API (direct SDK)

**Purpose:** Used by graphify (wiki extraction) and any scripts that invoke Claude without the CLI OAuth path.

### Auth
- `ANTHROPIC_API_KEY` in `.env` of consuming repo
- Console: https://console.anthropic.com/
- Key scope: full (Messages API + tool use)

### Preflight
```bash
curl -sS https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" | jq '.data[].id' | head -5
```

Expected: lineup includes `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`.

### Rotation
- Via Anthropic Console → API Keys → Rotate
- Update `.env` in consuming repos
- No shared-across-repos pattern here — each repo can have its own key

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-07 | `/v1/models` 200 with current lineup | OK (per AIS runbook) |

---

## 4. Local Qwen daemons (MLX, Apple Silicon only)

**Purpose:** Local-lane workers (PII / bulk / embeddings / offline) and Tier-2 Worker fallback when codex-spark is blocked.

### 4a. SoM MCP daemon (always-warm local orchestrator)

- Model: `mlx-community/Qwen3-1.7B-4bit` (primary) / `Phi-4-mini-instruct-4bit` (reserve)
- Location: `local-ai-machine/services/som-mcp/`
- Role: MCP stdio orchestrator for intent parsing + packet routing
- Budget: ~1.2 GB resident, evictable under memory pressure
- Control: configured via `local-ai-machine/.lam-config.yml mcp` block

**Preflight (from any governed repo):**
```bash
# assumes daemon exposes MCP over stdio to registered Claude sessions
# see local-ai-machine/services/som-mcp/README.md for bootstrap
pgrep -fl som-mcp
```

### 4b. Qwen-Coder warm worker (Tier-2 fallback)

- Model: `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (~4.5 GB peak)
- Location: `local-ai-machine/services/som-worker/` (worktree: `_worktrees/lam-som-mcp/services/som-worker/`)
- Role: Tier-2 Worker when codex-spark unavailable
- Inbox: reads job JSON from configured inbox; writes outputs + moves to done

**Start:**
```bash
bash ~/Developer/HLDPRO/_worktrees/lam-som-mcp/services/som-worker/bin/start-som-worker.sh
```

Script guards duplicate via `/tmp/som-worker.pid`. Waits up to 90s for `watching` in log.

**Stop:**
```bash
bash ~/Developer/HLDPRO/_worktrees/lam-som-mcp/services/som-worker/bin/stop-som-worker.sh
```

**Preflight:**
```bash
test -f /tmp/som-worker.pid && kill -0 "$(cat /tmp/som-worker.pid)" 2>&1 && echo "som-worker up" || echo "som-worker down"
```

**Known limits (issue #105):** full-file regen >200 lines emits stubs; see `docs/runbooks/qwen-coder-driver.md` workarounds.

### 4c. Qwen3-14B structured-output worker (HP/ASC content pipeline)

- Model: `mlx-community/Qwen3-14B-4bit` (~7-8 GB peak when active)
- Script: `/tmp/qwen_warm_worker.py` (template; owner: HP training pipeline)
- Inbox: `/tmp/qwen_jobs/` · Output: `/tmp/qwen_results/` · Done: `/tmp/qwen_done/`
- Role: outlines-schema prompt generation for ASC survey / training content
- Independent of §4b — different model, different inbox, different pidfile; can run concurrently

**Preflight:**
```bash
pgrep -fl qwen_warm_worker.py
```

### 4d. Coexistence on 24 GB M-series

- M7 Guardrail-LAM (always-resident): 4.67 GB
- SoM MCP daemon (warm): ~1.2 GB
- Qwen3-14B active: ~7-8 GB
- Qwen-Coder-7B active: ~4.5 GB
- System baseline: ~8-10 GB

Running both §4b and §4c concurrently is supported but tight — watch `vm_stat` during active generation; evict in order: Qwen-Coder-7B → MCP daemon (never M7).

### 4e. Windows host Ollama (LAN, Tier-2 fallback)

- Host: Windows 10 workstation, 64 GB RAM, 16 GB VRAM (12 GB usable envelope per LAM #68 pinned `vram_target_mb`)
- IP: `172.17.227.49` · adapter `vEthernet (sase-switch)` · Ollama port `11434`
- Role per SoM charter: Tier-2 Worker fallback step 3 (between local Qwen warm daemon and Sonnet cost-flagged); also serves as HP critic via `CRITIC_OLLAMA_URL` (existing integration, LAM #68)
- Operating settings (proven, do not change without re-running LAM #68 ladder probes): `keep_alive=15m`, `num_ctx<=4096`, offload ladder `99 -> 80 -> 60`, call timeout 45000ms
- Source-of-truth runbook: `docs/runbooks/windows-ollama-worker.md`
- LAM #68 closeout for full integration history: `local-ai-machine/_worktrees/lam-issue-68/WINDOWS_HOST_INFERENCE_INTEGRATION_RUNBOOK.md`

**Preflight (LAN reachability + model inventory):**
```bash
# For SoM Tier-2 Worker role (qwen2.5-coder:7b):
bash scripts/windows-ollama/preflight.sh --worker

# For HP critic role (llama3.1:8b):
bash scripts/windows-ollama/preflight.sh --critic
```

Returns 0 if endpoint reachable and required model present; 1 if unreachable; 2 if reachable but required model absent.

**Future surfaces (stubbed, not in scope):**
- Cloudflare Tunnel for off-LAN access (epic deferred)
- Wake-on-LAN provisioning (epic deferred)

---

## 5. GitHub (governance org & API)

**Purpose:** Repo hosting, PR automation, overlord-sweep issue creation, rulesets.

### Auth
- Primary: `GOVERNANCE_GITHUB_TOKEN` in `.env`
- Fallback: `GITHUB_PERSONAL_ACCESS_TOKEN`
- Scope: `repo`, `workflow`, `admin:org` (for ruleset reads)
- Defaults:
  - `GOVERNANCE_REPO_OWNER` = `NIBARGERB-HLDPRO`
  - `GOVERNANCE_REPO_NAME` = `hldpro-governance`
- Alternative: `gh` CLI (operator's logged-in session) — used interactively

### Preflight
```bash
gh api user --jq '.login'           # confirms gh auth
gh api /orgs/NIBARGERB-HLDPRO/rulesets --jq '.[].name'  # confirms admin:org scope
```

### Org rulesets (current)
| ID | Name | Enforcement | Source |
|---|---|---|---|
| 14715976 | Protect main branches | active | Organization |
| 14716006 | Protect develop branches | active | Organization |

Never disable without pairing every change with a restore-from-backup command. See §7 emergency merge procedure.

### Repo-level rulesets observed
| Repo | Ruleset | Name |
|---|---|---|
| hldpro-governance | 15241047 | Require Local CI Gate on main |
| ai-integration-services | 14283171 | MAIN |
| local-ai-machine | 13152679 | Main branch PR-only policy |

### hldpro-governance Local CI Gate enforcement status
Issue #277 adds a CI-visible `local-ci-gate` workflow for `hldpro-governance` and a repo-level required-status ruleset for `main`.

Observed on 2026-04-18:

- Classic branch protection for `NIBARGERB-HLDPRO/hldpro-governance` `main` returned 404 from `/repos/:owner/:repo/branches/main/protection`.
- Org ruleset `14715976` (`Protect main branches`) is active and applies deletion, non-fast-forward, and pull-request rules.
- Org ruleset `14715976` did not include a required-status-check rule at inspection time.
- Repo ruleset `15241047` (`Require Local CI Gate on main`) is active for `refs/heads/main` and requires status context `local-ci-gate` with strict required status checks enabled.
- Record the governance repo status as `CI required gate` for Local CI Gate enforcement.

### Classic branch protection (legacy)
Some repos (e.g., `local-ai-machine`) still use classic `/repos/:o/:r/branches/main/protection`. Inventory via:
```bash
gh api /repos/NIBARGERB-HLDPRO/<repo>/branches/main/protection --jq '.required_status_checks.contexts'
```

### Rotation
- Via https://github.com/settings/tokens (classic) or fine-grained
- Update `.env` in every consuming script/workflow
- Dependabot will flag expiring tokens via secret scanning

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-05 | Org rulesets created + secret scanning enabled | OK |
| 2026-04-14 | Admin API usable for emergency ruleset toggle | OK (restore confirmed) |
| 2026-04-18 | hldpro-governance Local CI Gate hardgate evidence | CI-visible workflow added by #277; repo ruleset `15241047` requires `local-ci-gate` on `main` |

---

## 6. Claude ↔ Codex cross-model review

Pointer only — owned by AIS runbook §Claude Code (Cross-Model Agent Review). The governance repo uses the same `CLAUDE_CODE_OAUTH_TOKEN` and `scripts/codex-review-template.sh` template. Per-repo wrappers live in each governed repo (`scripts/codex-review.sh`).

---

## 7. Emergency procedures

### 7a. Codex-spark blocked during active work
1. Run quota preflight (§1) — record `resets_at` in session notes
2. Log fallback: `scripts/model-fallback-log.sh --primary gpt-5.3-codex-spark --fallback <next>`
3. Pick fallback per ladder (§1)
4. If ladder step 4 (Sonnet cost-flagged), explicitly surface cost to operator before firing

### 7b. Merge blocked by ruleset that must be overridden (operator-authorized only)
1. Back up ALL affected rulesets + classic protection:
   ```bash
   gh api /orgs/NIBARGERB-HLDPRO/rulesets/<id> > /tmp/org-ruleset-<id>-backup.json
   gh api /repos/<owner>/<repo>/rulesets/<id> > /tmp/repo-ruleset-<id>-backup.json
   gh api /repos/<owner>/<repo>/branches/main/protection > /tmp/classic-protection-backup.json
   ```
2. Disable: `gh api -X PUT /orgs/.../rulesets/<id> -f enforcement=disabled` (and repo-level; classic protection: `gh api -X DELETE /repos/.../branches/main/protection`)
3. Merge immediately: `gh pr merge <n> --repo <owner>/<repo> --admin --squash`
4. Re-enable: `gh api -X PUT .../rulesets/<id> -f enforcement=active`
5. For classic: restore via `gh api -X PUT /repos/.../branches/main/protection --input /tmp/classic-protection-backup.json` (shape must match — use `jq` to extract `required_status_checks`, `enforce_admins.enabled`, `required_pull_request_reviews` subset)
6. Log in session notes and update `docs/exception-register.md` with a dated entry if the override is repeatable

### 7c. Qwen daemon crash during active job
1. Check pidfile: `ls -la /tmp/som-worker.pid /tmp/qwen_warm_worker.pid 2>&1`
2. Logs: `tail -50 /tmp/som-worker.log` or `/tmp/qwen-warm.log`
3. Memory check: `vm_stat | awk '/page size|Pages free|Pages active|Pages wired/'`
4. Restart: use start script (§4b/§4c)
5. Re-queue any in-flight job JSON — daemon is idempotent per input hash

### 7d. Anthropic / OpenAI API outage
1. Check status pages:
   - https://status.anthropic.com/
   - https://status.openai.com/
2. If Tier-1 planner family is down → halt per charter Invariant #3
3. If Tier-2 worker family is down → fall through to local (§4b)

---

## 8. Supabase (management operations)

**Purpose:** Governance-level credential management for all 5 HLDPRO Supabase projects. Per-project application keys live in `hldpro-governance/.env.shared` (SSOT). See `docs/ENV_REGISTRY.md` for the full project map and key naming convention.

### Auth
- Personal access token: `SUPABASE_ACCESS_TOKEN` in `.env.shared`
- Console: https://supabase.com/dashboard

### Project refs
| Logical name | ref |
|---|---|
| hp-staging | `nrkrquddydupkemtixom` |
| hp-production | `arvqikuzplxuqnkbxodh` |
| hldpro-staging | `khyadxaiyfdldyuoapyn` |
| ai-integration-services | `gyrtvzvazmvwiirnexls` |
| apex-doorknocking | `kfcqyijmuuafflpjepwr` |

### Fetch API keys (anon + service_role)
```bash
TOKEN=$(grep SUPABASE_ACCESS_TOKEN ~/.../hldpro-governance/.env.shared | cut -d= -f2)
curl -sS "https://api.supabase.com/v1/projects/<ref>/api-keys" \
  -H "Authorization: Bearer $TOKEN"
```

### Reset a DB password
```bash
# Correct endpoint: PATCH /v1/projects/{ref} with name + db_pass
TOKEN=$(grep SUPABASE_ACCESS_TOKEN ~/Developer/HLDPRO/hldpro-governance/.env.shared | cut -d= -f2)
curl -sS -X PATCH "https://api.supabase.com/v1/projects/<ref>" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"<project-name>","db_pass":"<new-password>"}'
# Response: {"id":...,"name":"...","ref":"..."} on success
# After reset: update HP_STAGING_SUPABASE_DB_PASSWORD / HP_PROD_SUPABASE_DB_PASSWORD in .env.shared
```

**Note:** `/v1/projects/{ref}/database/password` (PUT/POST/PATCH) does NOT work — returns 404. The project PATCH endpoint is the only working path via PAT.

### Seed a repo env from SSOT after credential changes
```bash
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>
# repos: hp-staging, hp-worktree, hp-frontend, ais, lam, knocktracker, governance
```

### Rotation
1. Update value in `hldpro-governance/.env.shared`
2. Run `bootstrap-repo-env.sh` for affected repos
3. Update changelog below

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-16 | DB password reset for hp-staging + hp-production via PATCH /v1/projects/{ref} | OK |
| 2026-04-16 | API keys fetched for all 5 projects via /v1/projects/{ref}/api-keys | OK |

---

## 9. Cloudflare (DNS + CDN + Pages + Tunnels)

**Domains managed:**
- `hldpro.com` — Zone ID: `b7dfe6670b831de575c237efcd702f6d`
- `hldpro.dev` — Zone ID: `9f7fa0f1fc1d6da67a1c71a8f3f7fa9d`
- **`ascsurvey.com` is NOT on Cloudflare** — authoritative NS via GoDaddy (ns33/ns34.domaincontrol.com)

**Account ID:** `a1546c2ad5f67006fc1ca72f8054298f`

### Tokens (all in `.env.shared` → `CLOUDFLARE_*`)

| Var | Prefix | Purpose | Status |
|---|---|---|---|
| `CLOUDFLARE_MASTER_OPS_TOKEN` | `cfut_nJ7q...` | Tunnel Write, DNS Write, Access Apps+Policies, CF One Connector | WORKING (2026-04-09) |
| `CLOUDFLARE_DNS_TOKEN` | `cfut_2bQY...` | DNS Edit — use for all DNS changes | WORKING |
| `CLOUDFLARE_PAGES_TOKEN` | `cfat_7mfU...` | Pages Edit — wrangler pages deploy | WORKING |
| `CLOUDFLARE_AGENT_TOKEN` | `cfut_WBnX...` | Read/Write broad + Email Routing | WORKING (2026-04-07) |
| `CLOUDFLARE_USER_TOKEN` | `cfut_VpCF...` | User-level token | Untested |
| `CLOUDFLARE_ORIGIN_API` | `v1.0-c9dd...` | Origin certificate API | Specific use only |
| `CLOUDFLARE_TUNNEL_ID` | `a9124862-...` | LAM tunnel | Active |
| `CF_TEAM_DOMAIN` | `hldpro` | Access JWT validation | — |
| `CF_ACCESS_AUD_TAG` | `e99b8781...` | Access JWT AUD claim | — |
| ~~`CLOUDFLARE_API`~~ | ~~`cfk_Qf...`~~ | Legacy API key | **EXPIRED 2026-04-03** |

### DNS Record Operations

```bash
# List records
curl -s "https://api.cloudflare.com/client/v4/zones/b7dfe6670b831de575c237efcd702f6d/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_DNS_TOKEN" | python3 -m json.tool

# Create CNAME
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/b7dfe6670b831de575c237efcd702f6d/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_DNS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"SUBDOMAIN.hldpro.com","content":"cname.vercel-dns.com","ttl":1,"proxied":false}'

# Delete record
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/b7dfe6670b831de575c237efcd702f6d/dns_records/RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_DNS_TOKEN"
```

### CF Pages Projects

| Project | Custom Domain(s) | Build Command | Status |
|---|---|---|---|
| hldpro-marketing | hldpro.com, www.hldpro.com | `npm run build:marketing` | LIVE (2026-04-03) |
| hldpro-dashboard | dashboard.hldpro.com | `npm run build:dashboard` | LIVE (2026-04-03) |
| hldpro-reseller | hldpro.dev | `npm run build:reseller` | LIVE (2026-04-03) |
| hldpro-pwa | pwa.hldpro.com | `npm run build:pwa` | LIVE (2026-04-03) |

### Current DNS Records (hldpro.com)

| Hostname | Type | Target | Proxied |
|---|---|---|---|
| hldpro.com | CNAME | hldpro-marketing.pages.dev | Yes |
| www.hldpro.com | CNAME | hldpro-marketing.pages.dev | Yes |
| dashboard.hldpro.com | CNAME | hldpro-dashboard.pages.dev | Yes |
| pwa.hldpro.com | CNAME | hldpro-pwa.pages.dev | Yes |
| mail.hldpro.com | — | Resend DKIM + SPF | — |
| hldpro.dev | CNAME | hldpro-reseller.pages.dev (zone: 9f7fa0f1) | Yes |

### Rules
- CF Pages domains: `proxied: true` (orange cloud)
- Vercel domains (if any remain): `proxied: false` (gray cloud)
- TTL 1 = automatic

---

## 10. Stripe (acct_1TDpk4CF7hBNGLjd)

**Dashboard:** https://dashboard.stripe.com

### Keys (all in `.env.shared`)

| Var | Purpose |
|---|---|
| `STRIPE_SECRET_KEY` / `STRIPE_LIVE_SECRET_KEY` | Live API |
| `STRIPE_PUBLISHABLE_KEY` / `STRIPE_LIVE_KEY` | Client-side |
| `STRIPE_RESTRICTED_KEY` | Scoped live key |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature verification |
| `STRIPE_TEST_SECRET_KEY` | Test mode API |
| `STRIPE_TEST_PUBLISHABLE_KEY` | Test mode client-side |

### Price IDs

| Var | Plan |
|---|---|
| `STRIPE_PRICE_STARTER` | Client Starter $297/mo |
| `STRIPE_PRICE_PROFESSIONAL` | Client Pro $597/mo |
| `STRIPE_PRICE_ELITE` | Client Elite $997/mo |
| `STRIPE_RESELLER_PRICE_STARTER/PRO/AGENCY` | Reseller tiers |

### CLI Operations
```bash
# List products
curl -s https://api.stripe.com/v1/products -u "$STRIPE_SECRET_KEY:" -G -d limit=10 | python3 -m json.tool

# Create price
curl -s https://api.stripe.com/v1/prices -u "$STRIPE_SECRET_KEY:" \
  -d product=prod_XXX -d unit_amount=29700 -d currency=usd \
  -d "recurring[interval]=month"
```

### Rules
- Price IDs are immutable — create new prices, never modify existing
- Webhook secret must match between Stripe dashboard and Supabase env
- `STRIPE_LIVE_SECRET_KEY` is a legacy alias of `STRIPE_SECRET_KEY` — both are live

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-07 | `GET /v1/account` live + test | OK |
| 2026-04-07 | Live webhook endpoint at supabase.co/functions/v1/stripe-webhook | Verified |

---

## 11. Twilio

**Dashboard:** https://console.twilio.com

| Var | Purpose |
|---|---|
| `TWILIO_ACCOUNT_SID` | Account identifier (AC...) |
| `TWILIO_AUTH_TOKEN` | API auth |
| `TWILIO_API_SID` + `TWILIO_SECONDARY_AUTH_TOKEN` | API key pair |
| `TWILIO_OAUTH_CLIENT_ID` + `TWILIO_OAUTH_SECRET` | OAuth credentials |
| `TWILIO_TEST_CONSUMER_NUMBER` | CI test phone (+18176806400 as of 2026-04-15) |

### CLI Operations
```bash
# Send test SMS
curl -s -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "From=+1XXXXXXXXXX" -d "To=+1YYYYYYYYYY" -d "Body=Test message"

# Rotate GitHub Actions secret
echo "+1XXXXXXXXXX" | gh secret set TWILIO_TEST_CONSUMER_NUMBER --repo NIBARGERB-HLDPRO/ai-integration-services
```

### Rules
- A2P SMS campaign registration required for production messaging
- Per-customer onboarding: see `ai-integration-services/docs/runbooks/A2P_CUSTOMER_SIGNUP_WORKFLOW.md`

### Verified 2026-04-07
- Account `status=active`. Two messaging services `us_app_to_person_registered=true`.

---

## 12. Resend + Email Infrastructure

**Dashboard:** https://resend.com | **Verified domain:** mail.hldpro.com (legacy), hldpro.com, hldpro.dev

| Var | Purpose |
|---|---|
| `RESEND_API_KEY` | Send-only transactional |
| `RESEND_FULL_API_KEY` | Domain management + send |

### Verified Resend Domains

| Domain | Status | Notes |
|---|---|---|
| mail.hldpro.com | Verified | Legacy — keep until DMARC confirms zero sends, then decommission |
| hldpro.com | Verified 2026-04-07 | Primary |
| hldpro.dev | Verified 2026-04-07 | Reseller |

### Outbound Sender Inventory (AIS `_shared/email.ts`)

| SenderKey | From Address |
|---|---|
| noreply | noreply@hldpro.com |
| support | support@hldpro.com |
| billing | billing@hldpro.com |
| alerts | alerts@hldpro.com |
| sign | sign@hldpro.com |
| estimates | estimates@hldpro.com |

### Inbound Email

| Domain | Provider | Routing |
|---|---|---|
| hldpro.com | Google Workspace | MX → Google. Aliases → ben@hldpro.com |
| hldpro.dev | Cloudflare Email Routing | Forward support/info/hello/billing → ben@hldpro.com. Catch-all: Drop |

### DMARC Posture
- hldpro.com: `p=none` (transitional) — ratchet to `p=quarantine` after 30 clean days
- hldpro.dev: `p=quarantine`

### Test
```bash
curl -s -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" -H "Content-Type: application/json" \
  -d '{"from":"HLD Pro <noreply@hldpro.com>","to":"test@example.com","subject":"Test","html":"<p>Test</p>"}'
```

### Verified 2026-04-07
- `POST /emails` with noreply@hldpro.com and noreply@hldpro.dev both delivered. `RESEND_API_KEY` is send-only (401s on management).

---

## 13. VAPI (Voice AI)

**Dashboard:** https://dashboard.vapi.ai

| Var | Purpose |
|---|---|
| `VAPI_PRIVATE_KEY` | Server-side API |
| `VAPI_PUBLIC_KEY` | Client-side widget |
| `VAPI_TEST_ASSISTANT_ID` | E2E test assistant |

### Rules
- Use native ElevenLabs v3 voice model via VAPI (not custom TTS proxy)
- Webhook URLs configured in VAPI dashboard per-assistant
- CI test phone number: `TWILIO_TEST_CONSUMER_NUMBER` — see §11

---

## 14. ElevenLabs

**Dashboard:** https://elevenlabs.io

| Var | Purpose |
|---|---|
| `ELEVENLABS_API_KEY` | TTS API (sk_...) |
| `ELEVENLABS_VOICE_ID` | Training narration voice (HP only) |
| `ELEVENLABS_MODEL` | Default `eleven_v3` for HP training media |

### Rules
- AIS: optional custom-tts proxy and quota diagnostics only; missing key should not page production
- HP: required for MED-006 training media generation; must resolve to `eleven_v3`; director notes must not be concatenated into ElevenLabs text payload
- Generation is idempotent — reuses existing segments by provider+model+voiceover-text hash

### Verified
| Date | Check | Result |
|---|---|---|
| 2026-04-07 | `GET /v1/user/subscription` | tier=creator, status=active, 100K char limit |
| 2026-04-12 | MED-006 synthesis probe + 9-segment generation | OK; idempotent reuse verified |

---

## 15. DigitalOcean + VPS Infrastructure

**Dashboard:** https://cloud.digitalocean.com
**Token:** `DIGITAL_OCEAN_PERSONAL_ACCESS_TOKEN` in `.env.shared`

### Droplets

| Name | IP | Purpose |
|---|---|---|
| ascsurvey-web | 159.89.50.9 | HP production + staging (Caddy) + Plausible Analytics |
| pentagi | 104.248.60.107 | PentAGI security runner |
| ais-infra | 167.71.22.255 | AIS n8n + Twenty CRM |

```bash
doctl compute droplet list --format ID,Name,PublicIPv4 --no-header
```

### ascsurvey-web (HP droplet — 159.89.50.9)

```bash
ssh root@159.89.50.9     # admin (docker, caddy, system)
ssh deploy@159.89.50.9   # app deploy (no sudo, no docker)

# Deploy Caddyfile
scp HealthcarePlatform/infrastructure/Caddyfile root@159.89.50.9:/etc/caddy/Caddyfile
ssh root@159.89.50.9 "caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy"
```

**App hosts:**
- `app.staging.ascsurvey.com` / `sme.staging.ascsurvey.com` → `/var/www/staging.ascsurvey.com/app`
- `app.ascsurvey.com` → `/var/www/ascsurvey.com/app`

**Plausible Analytics (Docker):**
```bash
ssh root@159.89.50.9 "cd /opt/plausible && docker compose ps"
# UI access: ssh -L 8000:127.0.0.1:8000 root@159.89.50.9 then http://localhost:8000
# Credentials: PLAUSIBLE_EMAIL / PLAUSIBLE_PASSWORD in .env.shared
```

### ais-infra (167.71.22.255)
- n8n: port 5678 — `N8N_SELF_HOSTED_URL`
- Twenty CRM: port 3001 — `TWENTY_WORKSPACE_URL`
- VPS SSH: `root@167.71.22.255` via `~/.ssh/id_ed25519`

---

## 16. GoDaddy DNS (ascsurvey.com)

**Domain:** ascsurvey.com — authoritative NS: ns33/ns34.domaincontrol.com
**Credentials:** `GODADDY_PRODUCTION_KEY` / `GODADDY_PRODUCTION_SECRET` in `.env.shared`

```bash
KEY=$GODADDY_PRODUCTION_KEY
SECRET=$GODADDY_PRODUCTION_SECRET

# Add A record
curl -sS -X PATCH "https://api.godaddy.com/v1/domains/ascsurvey.com/records" \
  -H "Authorization: sso-key ${KEY}:${SECRET}" \
  -H "Content-Type: application/json" \
  -d '[{"type":"A","name":"SUBDOMAIN","data":"159.89.50.9","ttl":600}]'

# Add CAA records (Let's Encrypt only)
curl -sS -X PATCH "https://api.godaddy.com/v1/domains/ascsurvey.com/records" \
  -H "Authorization: sso-key ${KEY}:${SECRET}" \
  -H "Content-Type: application/json" \
  -d '[{"type":"CAA","name":"@","data":"0 issue \"letsencrypt.org\"","ttl":600},{"type":"CAA","name":"@","data":"0 issuewild \"letsencrypt.org\"","ttl":600}]'
```

### Rules
- Do NOT use Cloudflare for ascsurvey.com — it is GoDaddy-authoritative
- Staging: `app.staging.ascsurvey.com` and `sme.staging.ascsurvey.com` → 159.89.50.9
- Production: `app.ascsurvey.com` → 159.89.50.9

---

## 17. PentAGI (Security Testing)

**Droplet:** 104.248.60.107 | **GraphQL:** `https://localhost:8443/api/v1/graphql` (via SSH tunnel)

| Var | Purpose |
|---|---|
| `PENTAGI_HOST` | Droplet IP |
| `PENTAGI_PORT` | 8443 |
| `PENTAGI_ADMIN_EMAIL` / `PENTAGI_ADMIN_PASSWORD` | Web UI |
| `PENTAGI_API_TOKEN` | GraphQL Bearer token (expires 2027-04-03) |

```bash
# SSH tunnel (required)
ssh -f -N -L 8443:localhost:8443 root@104.248.60.107

# List flows
curl -sk https://localhost:8443/api/v1/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PENTAGI_API_TOKEN" \
  -d '{"query": "{ flows { id status title createdAt updatedAt } }"}'
```

### Rules
- GraphQL endpoint is `/api/v1/graphql` (NOT `/api/graphql` — that returns 301)
- Must use `-sk` (self-signed cert)

### Verified 2026-04-07
- Live flow data returned: flow `4` (AIS retest), flow `5` (HP pentest).

---

## 18. Twenty CRM (self-hosted 167.71.22.255:3001)

| Var | Purpose |
|---|---|
| `TWENTY_WORKSPACE_URL` | `http://167.71.22.255:3001` |
| `TWENTY_CRM_APP_SECRET` | App-level auth |
| `TWENTY_API_KEY` | Bearer token |

```bash
# Health check
curl -s "$TWENTY_WORKSPACE_URL" -o /dev/null -w "%{http_code}"

# GraphQL query
curl -s -X POST "$TWENTY_WORKSPACE_URL/graphql" \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ people(first: 2) { edges { node { id name { firstName lastName } } } } }"}'
```

### Verified 2026-04-07 — `200`, live contacts returned.

---

## 19. n8n

| Var | Purpose |
|---|---|
| `N8N_API_KEY` | Cloud instance |
| `N8N_CLOUD_URL` | `https://apex-solutions-1.app.n8n.cloud/api/v1` |
| `N8N_SELF_HOSTED_URL` | `http://167.71.22.255:5678/api/v1` |
| `N8N_SELF_HOSTED_API_KEY` | Self-hosted bearer token |
| `N8N_OWNER_EMAIL` / `N8N_OWNER_PASSWORD` | Web UI admin |

---

## 20. Plaid

| Var | Purpose |
|---|---|
| `PLAID_CLIENT_ID` | Account identifier |
| `PLAID_SANDBOX_SECRET` | Sandbox/test |
| `PLAID_PRODUCTION_SECRET` | Live bank connections |

### Rules
- Sandbox credentials for E2E: institution `ins_109508`, user `user_good`, pass `pass_good`
- Webhook signature: ES256 JWTs via `plaid-verification` header; JWK cached 24h by `kid`

### Verified 2026-04-07 — Sandbox link token issued. Both staging + production Supabase secrets verified.

---

## 21. Google APIs

| Var | Purpose |
|---|---|
| `GOOGLE_MAPS_API_KEY` | Places API (booking pipeline) |
| `GOOGLE_SOLAR_API_KEY` | Solar API (same key value) |

### Rules
- Must be set via `supabase secrets set` for edge functions — `.env` values are not picked up automatically

### Verified 2026-04-07 — Places `textsearch` 200 + Solar `buildingInsights` 200.

---

## 22. Cal.com (self-hosted: schedule.hldpro.com)

| Var | Purpose |
|---|---|
| `CALCOM_API_KEY` | API access (`cal_live_...`) |
| `CALCOM_SELF_HOSTED_URL` | `https://schedule.hldpro.com` |
| `CALCOM_ADMIN_*` | Web UI admin credentials |
| `CALCOM_TRIGUY_*` | Tri Guy Treasures client account |
| `CALCOM_WEBHOOK_SECRET` | Webhook signing |
| `CALCOM_ENCRYPTION_KEY` | App-level encryption |

### Rules
- Use `cal-api-version: 2024-06-14` for all v2 requests (`2024-08-13` returns 404)

### Verified 2026-04-07 — `GET /v2/me` and `GET /v2/event-types` both 200.

---

## 23. Google Drive / rclone / NotebookLM (Compendium Sync)

**Account:** `ben@hldpro.com`
**rclone remote:** `gdrive` in `~/.config/rclone/rclone.conf`
**Drive folder:** `My Drive/HLD-Pro-Compendium/` (124 `.txt` files)
**NotebookLM notebook:** `718ecd1d-4645-4ac2-8150-63d26d2377fc` (authuser=1)

```bash
# Sync compendium to Drive
rclone sync compendium/notebook-pack/ gdrive:HLD-Pro-Compendium/ --delete-during

# Re-authorize (if token expires)
rclone config reconnect gdrive:
```

**Automation:** `scripts/compendium/refresh-and-upload.sh` — launchd daily 7am CT
**NotebookLM source limit:** FROZEN at 126 files (300-source Plus tier limit) — update existing files, do not add new ones
**Kortex:** Chrome extension syncs Drive folder to NotebookLM automatically

---

## 24. Claude.ai (Playwright Compendium Upload)

**Account:** `nibarger.ben@gmail.com`
**Project:** `https://claude.ai/project/019d1304-601d-76b1-a69f-32122d8050b8`
**Browser profile:** `~/.hldpro-automation/chrome-profile-claude/`

```bash
npx tsx scripts/compendium/upload-claude.ts   # upload
npx tsx scripts/compendium/setup-browser.ts claude  # refresh session
```

**Note:** Must run headed (visible window) — Cloudflare blocks headless Playwright.

---

## 25. Other Services

| Service | Var(s) | Purpose |
|---|---|---|
| GoDaddy | `GODADDY_PRODUCTION_KEY/SECRET`, `GODADDY_TEST_KEY/SECRET` | Domain management |
| Vercel | `VERCEL_ACCESS_TOKEN`, `VERCEL_AI_GATEWAY_API_KEY` | **DEPRECATED** for hosting (migrated to CF Pages 2026-04-03); AI Gateway still active |
| QuickBooks | `PROD_CLIENT_ID/SECRET`, `DEV_CLIENT_ID/SECRET` | Accounting integration |
| OpenAI | `OPENAI_API_KEY`, `OPENAI_ADMIN_KEY` | GPT models; admin key for usage dashboards |
| Hugging Face | `HUGGING_FACE_TOKEN` | Model hub access (user: `nibargerb`) |
| LlamaParse | `LLAMA_PARSE_API_KEY` | PDF parsing (local-ai-machine) |
| Gitleaks | `GITLEAKS_LICENSE` | Secret scanning CI |

### Governance Raw Feed Bridge

`operator-context-bridge` (AIS edge function) writes `public.operator_context` rows into governance via GitHub Contents API.

| Var | Default | Notes |
|---|---|---|
| `GOVERNANCE_GITHUB_TOKEN` | — | Preferred (scoped to governance repo contents write) |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | — | Fallback |
| `GOVERNANCE_REPO_OWNER` | `NIBARGERB-HLDPRO` | — |
| `GOVERNANCE_REPO_NAME` | `hldpro-governance` | — |
| `GOVERNANCE_REPO_BRANCH` | `raw-feed/operator-context` | — |
| `GOVERNANCE_OPERATOR_CONTEXT_DIR` | `raw/operator-context` | — |

Rules: bridge is append-only; must write to dedicated branch and open/reuse PR into main; do not write directly to main.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-16 | Added §8 Supabase management. Documents correct DB password reset path (`PATCH /v1/projects/{ref}` with `name`+`db_pass`), all 5 project refs, API key fetch command, and bootstrap script pointer. Passwords reset for hp-staging + hp-production. |
| 2026-04-16 | Promoted to cross-repo SSOT. Consolidated §9–25 from AIS and HP runbooks: Cloudflare, Stripe, Twilio, Resend, VAPI, ElevenLabs, DigitalOcean/VPS, GoDaddy DNS, PentAGI, Twenty CRM, n8n, Plaid, Google APIs, Cal.com, Google Drive/rclone/NotebookLM, Claude.ai Playwright, and Other Services + Governance Raw Feed Bridge. Scope line updated accordingly. |
| 2026-04-14 | Initial runbook created in governance. Covers Codex CLI (with spark quota preflight), Claude Code CLI, Anthropic API, local Qwen daemons (MCP + Qwen-Coder warm + Qwen3-14B), GitHub governance token, and emergency procedures. Companion to AIS `docs/EXTERNAL_SERVICES_RUNBOOK.md` and HP `docs/EXTERNAL_SERVICES_RUNBOOK.md` (each scoped to its own repo's external deps). |
