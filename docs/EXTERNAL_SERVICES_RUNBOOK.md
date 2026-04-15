# External Services Runbook — hldpro-governance

Version: 2026-04-14
Owner: Operator (nibarger.ben@gmail.com)
Scope: external services that govern work in this repo depends on. Repo-local services (Cloudflare, Stripe, Supabase, Twilio, etc.) live in each downstream repo's own runbook (`ai-integration-services/docs/EXTERNAL_SERVICES_RUNBOOK.md`, `HealthcarePlatform/docs/EXTERNAL_SERVICES_RUNBOOK.md`).

## 1. Codex CLI (OpenAI)

**Purpose:** Tier-1 Dual-Planner partner (`gpt-5.4` high) and Tier-2 Worker (`gpt-5.3-codex-spark` high) in the Society of Minds charter. See `STANDARDS.md §Society of Minds`.

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
bash scripts/windows-ollama/preflight.sh
```

Returns 0 if endpoint reachable + at least one pinned model present; 1 if unreachable; 2 if reachable but no pinned models.

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
| ai-integration-services | 14283171 | MAIN |
| local-ai-machine | 13152679 | Main branch PR-only policy |

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

## Changelog

| Date | Change |
|------|--------|
| 2026-04-14 | Initial runbook created in governance. Covers Codex CLI (with spark quota preflight), Claude Code CLI, Anthropic API, local Qwen daemons (MCP + Qwen-Coder warm + Qwen3-14B), GitHub governance token, and emergency procedures. Companion to AIS `docs/EXTERNAL_SERVICES_RUNBOOK.md` and HP `docs/EXTERNAL_SERVICES_RUNBOOK.md` (each scoped to its own repo's external deps). |
