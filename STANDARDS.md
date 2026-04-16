# HLD Pro — Shared Standards Manifest

> The overlord agent checks every repo against these standards.
> Update this file to change what the overlord enforces.

## Required Files (all code repos)
- `CLAUDE.md` at repo root (or workspace root for monorepos)
- `docs/PROGRESS.md` — feature status tracker (uppercase filename)
- `docs/FEATURE_REGISTRY.md` — detailed feature inventory and readiness matrix
- `docs/FAIL_FAST_LOG.md` — error patterns and resolutions
- `docs/DATA_DICTIONARY.md` — schema/source-of-truth reference (may be a validated pointer doc for monorepos)
- `docs/SERVICE_REGISTRY.md` — service/function inventory
- `.gitignore` covering: `.env`, `node_modules/`, `dist/`, `.DS_Store`

## Required Governance
- `.claude/hooks/governance-check.sh` — blocks commits missing doc co-staging
- `.claude/hooks/backlog-check.sh` — **hard gate**: blocks branch creation unless a matching `PLANNED` or `IN_PROGRESS` entry exists in `docs/PROGRESS.md` Plans table. Enforces backlog-first workflow (plan with AC before code).
- `.claude/hooks/check-errors.sh` — PostToolUse hard gate: auto-grep FAIL_FAST_LOG on errors, 3-attempt max, then STOP and ask user
- `check-backlog-gh-sync.yml` — **hard gate**: every `OVERLORD_BACKLOG.md` Planned entry must reference an open GitHub issue (`#NNN` in the `Issue` column). GitHub is canonical — create the issue before adding to Planned. CI validates all refs are open on every push.
- `check-pr-commit-scope.yml` — **scope guard**: PRs to main must contain ≤ 10 commits. Excess commits indicate stale-worktree base contamination (2026-04-15 incident). Threshold configurable via `MAX_COMMITS` env var.
- `.claude/settings.json` PostToolUse matcher must be `"*"` (all tools), NOT `"Bash"` — errors from MCP, Agent, Read, etc. must also trigger the 3-attempt gate
- **Hook commands in `.claude/settings.json` must use absolute paths** (e.g. `bash $HOME/Developer/HLDPRO/<repo>/.claude/hooks/<hook>.sh`) — relative paths break silently when the session CWD shifts to a subdirectory, causing the hook to no-op without a hard error
- Session start must check `~/Developer/hldpro/.codex-ingestion/{repo}/backlog-*.md` for pending Codex findings — surface to user if any exist
- If repo governance requires specialist agents/subagents, the session must use them. Codex sessions may satisfy this by spawning equivalent Codex subagents and loading the repo's persona definitions from `CODEX.md`, `AGENTS.md`, `.agents/`, or repo-local standards instead of relying on Claude-only agent files.
- Conventional commits: `feat/fix/docs/chore` with scope
- **Never push to main/master** — always branch → staging → test → deploy
- **Never force-push** (`--force`, `--force-with-lease`) — if a branch has a merge conflict, resolve via `git merge origin/develop` into the branch (merge commit), never via rebase + force-push
- **Stagger parallel PR merges** — when merging 2+ PRs that touch the same files, add a 10-second pause (`sleep 10`) between merges to avoid race conditions
- `.github/workflows/ci-workflow-lint.yml` — actionlint CI: install + run on PRs/pushes (all code repos)
- **CI runners:** All workflows must use `ubuntu-latest`. The `sase-microvm` self-hosted runner was decommissioned 2026-04-02. Do NOT add `self-hosted` runner refs.

### Structured Agent Cycle Plans
- Canonical plan artifacts are structured JSON, not freeform Markdown.
- The canonical org-wide schema lives in `hldpro-governance/docs/schemas/structured-agent-cycle-plan.schema.json`.
- Human-readable Markdown plan notes are optional companion material, not the source of truth.
- Structured plans must capture:
  - sprint/task/acceptance data
  - `specialist_reviews`
  - `alternate_model_review`
  - `execution_handoff`
  - `material_deviation_rules`
- Issue-driven execution branches (`issue-*`) and risk-fix branches (`riskfix/*`) must have at least one valid `*structured-agent-cycle-plan.json` file before execution is governance-ready. Note: `riskfix/<slug>-YYYYMMDD` (with date suffix) is the **required** implementation branch pattern for `local-ai-machine`, enforced by `edge_breaker_mcp_contract.yml`. Other repos accept `riskfix/*` as an optional prefix alongside standard `feat/fix/chore/docs` conventions but do not require it.
- Reusable governance CI validates structured plans through `scripts/overlord/validate_structured_agent_cycle_plan.py`.
- Cross-model review results from `scripts/codex-review.sh claude` belong in `alternate_model_review`.

### Branch Isolation (global hook)
- `~/.claude/hooks/branch-switch-guard.sh` — **global PreToolUse hook** that blocks `git checkout <branch>` and `git switch <branch>` in all repos
- Prevents multi-session conflicts where one session's branch switch corrupts another session's working directory
- **Allowed:** `git checkout -- <file>` (file restore), `git checkout .`, `git worktree add`
- **Blocked:** `git checkout <branch>`, `git switch <branch>`, `git checkout -b <branch>`, `git checkout -`
- **Alternative:** Use `EnterWorktree` tool or `git worktree add` for branch work in concurrent sessions
- Configured in `~/.claude/settings.json` PreToolUse hooks (absolute path, not `~`)

### Shared Dependency Symlinks In Clean Worktrees
- **Allowed only in isolated worktrees** when the root checkout for the same repo already has installed workspace dependencies and repeating the install would be materially slower or wasteful.
- **Allowed artifacts:** dependency install trees and package-manager metadata needed to consume that same install for the same repo checkout, such as `node_modules/` and matching workspace dependency metadata directories created from the current lockfile.
- **Forbidden artifacts:** `.env*`, `.git`, build outputs (`dist/`, `build/`, `.next/`, coverage), database files, generated app data, secret-bearing caches, or any artifact borrowed from a different repo.
- **Verification required before linking:** confirm the root checkout and worktree are the same repo, confirm the relevant lockfile/manifests match, and confirm the dependency target already exists in the root checkout.
- **Post-link verification required:** run at least one normal repo command from the worktree that proves the borrowed toolchain actually works before treating the lane as ready.
- **Cleanup expectation:** these symlinks are local-only lane setup. Never commit them as tracked files, and remove them when the worktree no longer needs the borrowed install.
- **Preferred helper path:** use `bash hldpro-governance/scripts/overlord/worktree_shared_dependencies.sh link ...` and `clean ...` instead of ad hoc manual linking whenever the helper covers the lane.
- **Escalation rule:** if a lane needs more than the documented helper path, create an issue-backed follow-up instead of normalizing hidden tribal steps.

### Doc Co-Staging Rules (governance-check.sh + CI)
- **ANY source file change** (`.ts`, `.tsx`, `.sql`, `.html`, `.css`, `.js`, `.svg`) → co-stage `docs/PROGRESS.md`
- **ANY source file change** (`.ts`, `.tsx`, `.sql`, `.html`, `.css`, `.js`, `.svg`) → co-stage `docs/FEATURE_REGISTRY.md`
- **Bug fix commits** (fix/bug/patch/hotfix in message) → co-stage `docs/FAIL_FAST_LOG.md`
- **Marketing file changes** (`marketing/`) → co-stage `marketing/MARKETING_PAGE.md` (if repo has marketing dir)
- **Infrastructure changes** (`infrastructure/`, `.github/workflows/`) → co-stage `docs/PROGRESS.md`
- **New edge functions** → co-stage `docs/SERVICE_REGISTRY.md` (if exists)
- **Migrations** → co-stage `docs/DATA_DICTIONARY.md` (if exists)
- **Any schema/table/column change** → co-stage `docs/DATA_DICTIONARY.md` (mandatory, no exceptions)
- **PENDING_ placeholders** → blocked in committed `.html`, `.ts`, `.tsx`, `.js`, `.json` files. All placeholders must be resolved before merge.

### CI Governance Workflow
- Must trigger on PRs to **both** `main` and `develop` (not just main)
- Must check for PENDING_ placeholders across all changed files
- Must report marketing doc sync status if marketing files changed

## Governance Doc Contract

These files must be consistent at the contract level. They do **not** need to be structurally identical across all repos.

### `docs/PROGRESS.md`
- Must remain the repo's single source of truth for planned work, open bugs, feature requests, and operational items
- For governed product repos, active backlog sections in `docs/PROGRESS.md` must stay aligned with backlog-labeled GitHub issues: open backlog issues must appear there, and closed backlog issues must not remain listed as active.
- Default required sections:
  - `## Plans`
  - `## Known Bugs`
  - `## Feature Requests`
  - `## Operational Items`
- Default backlog table header:
  - `| Plan | Status | Priority | Est. Hours | Deliverables | Notes |`
- **AIS exception:** `ai-integration-services` may satisfy the backlog contract with its existing backlog model (`# Backlog` / `## Backlog — Open Plans & Action Items`) plus `## Known Bugs`

### `docs/FEATURE_REGISTRY.md`
- Must contain:
  - a top-level title
  - `Last Updated` metadata
  - `## Summary Table`
  - a summary table whose leading columns are `Feature ID`, `Domain`, `Feature`, `Status`, `Readiness`
- Extra columns (for example test coverage) and appendices are allowed

### `docs/DATA_DICTIONARY.md`
- Must contain a top-level `# Data Dictionary` title
- Must include `Last updated` or `Last Updated` metadata
- Must include explicit source-of-truth metadata or pointer language
- Must either:
  - be the canonical root schema dictionary, or
  - explicitly point to the canonical workspace-level dictionary
- Canonical dictionaries may use detailed schema sections or a compact table format; both are acceptable
- Placeholder-only rows such as `(tables will be documented here)` are not acceptable
- **HealthcarePlatform exception:** root `docs/DATA_DICTIONARY.md` may remain a pointer to `backend/DATA_DICTIONARY.md`

### `docs/SERVICE_REGISTRY.md`
- Must contain a top-level `# Service Registry` title
- Must include `Last updated` or `Last Updated` metadata
- Must include explicit source-of-truth metadata or pointer language
- Must include at least one registry table covering services or functions
- Placeholder-only rows such as `(services will be documented here)` are not acceptable
- Repo-specific shapes are allowed (for example `Function / Method / Path` or `Service / Type / Description`)

## Monorepo Handling
- Required governance files (CLAUDE.md, docs/PROGRESS.md, docs/FAIL_FAST_LOG.md, .claude/hooks/, .github/workflows/) go at **repo root**
- Monorepos may have ADDITIONAL docs at workspace level (e.g., `backend/docs/`, `frontend/docs/`)
- When checking or creating files, always `ls` the root AND workspace directories first
- HealthcarePlatform structure: root (governance baseline) + `backend/` (agents, standards, detailed docs, .gitignore) + `frontend/` (subagent approvals, .gitignore)

## HIPAA Repos (HealthcarePlatform)
- Must have agents for: PHI redaction, break-glass gate, audit retention, RLS auditing
- Zero-fail policy: no PHI in logs, no direct DB access from frontend
- Subagent approval system for cross-boundary (frontend↔backend) operations
- Detailed project tracking lives in `backend/docs/PROJECT_STATUS.md` (supplements root `docs/PROGRESS.md`)

## Security Standards (Tiered)

Each repo has a security tier that determines which security artifacts the overlord agents verify.

### Full + PentAGI (ai-integration-services)
- `.gitleaks.toml` at repo root
- `.github/workflows/security.yml` with gitleaks + npm audit jobs
- `scripts/security-audit.sh` (6-check audit: credential leak, RLS, frontend secrets, auth order, PII in logs, dependency audit)
- `.claude/skills/hldpro-security-audit.md` installed
- `docs/security-reports/` directory with ≥1 PentAGI report; freshest report < 30 days old
- `docs/SECURITY_IMPLEMENTATION_PLAN.md` exists
- `docs/INFOSEC_POLICY.md` exists with active risk register

### Full + PentAGI + HIPAA (HealthcarePlatform)
- `.gitleaks.toml` at repo root (with HIPAA patterns: SSN, MRN)
- `.github/workflows/security.yml` with gitleaks + npm audit jobs
- RLS auditor agent (already required under HIPAA agents)
- PHI-in-logs guard agent (already required under HIPAA agents)
- Dependency audit in CI (`npm audit` or equivalent)
- `docs/security-reports/` directory with ≥1 PentAGI report; freshest report < 30 days old
- PentAGI scope includes Caddy proxy layer and DO droplet surface (not just Supabase)

### Baseline Security (knocktracker, local-ai-machine)
- `.gitleaks.toml` at repo root
- `.gitignore` covers `.env` (already required under general standards)
- Dependency audit in CI (`npm audit --audit-level=high`)

### Exempt (ASC-Evaluator)
- No security checks required

## Repo Registry

| Repo | Type | Governance Tier | Security Tier |
|------|------|-----------------|---------------|
| hldpro-governance | Meta-governance repo (scripts + CI + agents) | Governance-owner (see note below) | Baseline |
| ai-integration-services | SaaS platform (Supabase + Deno + Vite) | Full (hooks + CI + agents) | Full + PentAGI |
| HealthcarePlatform | Monorepo (backend + frontend), HIPAA | Full + HIPAA (zero-fail) | Full + PentAGI + HIPAA |
| local-ai-machine | AI/ML infrastructure | Full (lane-based + session locks) | Baseline |
| knocktracker | Field operations app | Standard (rules + CI) | Baseline |
| ASC-Evaluator | Knowledge repo (no code) | Exempt from code governance | Exempt |

> **hldpro-governance hook path note:** Product repos store hooks under `.claude/hooks/` (local-only, gitignored). hldpro-governance stores its committed hooks under `hooks/` at repo root (checked in, enforced repo-wide). Both satisfy the Required Governance hook contract — the difference is scope: local session vs. repo-wide enforcement. Hook *scripts* (e.g. `hooks/pre-session-context.sh`) are committed for repo-wide discoverability; the local `settings.json` that wires them into Claude Code sessions is gitignored and set up per-developer.

## Cross-Model Review

### Bidirectional Agent Calls

Both Claude and Codex sessions can invoke each other as specialist reviewers:

| Direction | Script | When to use |
|-----------|--------|-------------|
| Claude → Codex | `bash scripts/codex-review.sh review <branch>` | Second-opinion code review from Codex |
| Claude → Codex | `bash scripts/codex-review.sh audit <path>` | Codex security audit |
| Codex → Claude | `bash scripts/codex-review.sh claude "<prompt>"` | Claude specialist review from Codex sessions |

**Auth requirements:**
- Codex sessions: `OPENAI_API_KEY` or `~/.codex/auth.json` (ChatGPT account, `gpt-5.4` default)
- Claude calls from Codex: `CLAUDE_CODE_OAUTH_TOKEN` in repo `.env` (operator runs `claude setup-token` once, valid 1 year)
- Codex config must inherit the token: `shell_environment_policy.inherit = "all"` in `~/.codex/config.toml`

**Script contract:** Every code repo must have `scripts/codex-review.sh` with at minimum the `review` and `claude` modes. Use `hldpro-governance/scripts/codex-review-template.sh` as the canonical source.

### Weekly Sweep (Codex → Repos)

- Weekly overlord sweep includes Codex CLI (`codex exec review`) as a second-opinion layer
- Codex outputs structured JSON to `~/Developer/hldpro/.codex-ingestion/{repo}/`
- Use `python3 scripts/overlord/codex_ingestion.py generate --repo {repo} --repo-path {path}` to produce `review-{date}.json`
- The primary sweep session cross-references findings against existing docs and validates them
- Use `python3 scripts/overlord/codex_ingestion.py qualify --repo {repo} --repo-path {path}` to produce `qualified-{date}.json` and `backlog-{date}.md`
- The primary sweep session qualifies findings and generates backlog entries in the ingestion folder (`backlog-{date}.md`)
- **Backlog entries are staged, not committed** — they surface during HITL backlog review
- Session start may surface pending backlog with `python3 scripts/overlord/codex_ingestion.py status --repo {repo}`
- User promotes entries to `docs/PROGRESS.md` or `docs/FAIL_FAST_LOG.md` when approved
- Promotion preview or apply path: `python3 scripts/overlord/codex_ingestion.py promote --repo {repo} --repo-path {path} [--finding-id F001] [--apply]`
- Entries tagged `⚠️ CODEX-FLAGGED` / `Source: Codex review` for traceability
- Default helper model is `gpt-5.4` for ChatGPT-account compatibility; pass `--model o3` only when the account supports it
- Graphify-first architecture retrieval is auditable, not assumed. When a governed workflow uses governance graph/wiki artifacts as primary context, log a usage event with `python3 scripts/knowledge_base/log_graphify_usage.py --repo {repo} --task-id {issue-or-task} --task-type {type} --strategy graphify|hybrid --artifact wiki/index.md --artifact graphify-out/GRAPH_REPORT.md --estimated-tokens {n}`.
- Baseline repo-search comparisons should log `--strategy repo-search` to the same append-only event stream so graphify-vs-search adoption and retrieval footprint can be measured over time.
- For fail-fast debugging, the validated graph-guided query pattern is: symptom terms + mechanism terms + likely owner terms (function/workflow/file family). Use graph-guided retrieval first to identify owning files and adjacent components, then confirm those files with bounded repo search.
- For workflow/doc-heavy fail-fast debugging, the validated path is `hybrid`: use graph-guided retrieval for owner/topology hints, then rank bounded workflow/doc artifacts (`.github/workflows/`, `docs/`, `metrics/`, `raw/`) with primary workflow YAML preferred over derivative plan or measurement artifacts.
- Requires one supported Codex auth path in environment:
- `CODEX_AUTH_JSON` for trusted CI/CD runners using a staged `~/.codex/auth.json`
- or `OPENAI_API_KEY` / Codex Connect auth when the CLI supports env-only auth for the runner context
- Sweep should prefer `CODEX_AUTH_JSON` over `OPENAI_API_KEY` when both are present, then skip gracefully if neither is configured

## Completion Verification Protocol — ENFORCED

**Before claiming any cross-repo or governance task as "done":**

1. **Artifact verification**: For every file the plan says to create, run `git show HEAD:<path>` on the target branch to confirm it exists in the commit (not just on disk).
2. **Standards sweep**: Run `~/.claude/agents/verify-completion.md` against all affected repos in isolated worktrees. It checks every item in this STANDARDS.md and reports PASS/FAIL per repo without mutating shared checkouts.
3. **PR verification**: If the plan says "create PR", confirm the PR exists (`gh pr view`), is on the correct base branch, and CI is running.
4. **Specialist verification**: If repo governance required specialist agents/subagents for the task, verify the session used equivalent specialists. Codex may satisfy this with spawned Codex subagents/personas mapped from repo-local definitions; do not waive the requirement just because the repo uses Claude-era agent naming.
5. **No hedging**: Do not use "if it exists" language for required files. If STANDARDS.md says a file is required, it must exist — create it if missing.
6. **Session summary must match reality**: Before writing a session summary to memory, re-verify each claim. "Built" means merged to main or PR passing CI. "Created" means committed and pushed. "Planned" means neither.
7. **PDCA/R Adjust + Review must close the loop**: If verification or review surfaces another required action, test, cleanup, or control improvement, do not leave it implicit. Either:
   - fold it into the current slice before closing, when it is part of the same acceptance path, or
   - create/update the governing GitHub issue and roadmap mirror entry before closing, so the follow-up is issue-backed and visible.
8. **Do not stop at "works now" if the acceptance path still has an unverified step**: If another validation run, rollout step, or policy update is required to make the outcome durable, it must be completed in the current slice or recorded as explicit follow-up before the task is marked done.

**Failure to verify = the task is not complete.** A plan step without artifact verification stays "in progress."

## Fail-Fast Loop Closure

Repos with automated test/heal cycles must close the full failure → diagnosis → pattern → prevention loop:

- **Live log access** (repos with `test-nightly.yml`): Watcher agent must query live runtime logs (Supabase Management API `/logs/explorer` or equivalent), not just static output files. The watcher needs access to edge function errors, webhook payloads, and workflow execution history to diagnose failures without manual log cross-referencing.
- **Automated pattern write-back** (repos with `operator_context`): After a novel failure is identified and the operator confirms a fix, the watcher must write the failure pattern back to `operator_context` automatically (via `memory-writer` edge function, `context_type: failure_pattern`). Manual pattern entry breaks the loop — `heal.py` only benefits from patterns that are persisted before the next run.
- **Gate failure surfacing** (repos using `governance-check.yml`): PR gate failures must write a `context_type: system_event` row to `operator_context` so the morning briefing surfaces them. GitHub Actions `::error::` annotations alone are insufficient — they require the operator to check GitHub notifications.

**Verification**: The `overlord-sweep` agent checks that repos with `test-nightly.yml` have a watcher agent with a Bash tool call containing a log query endpoint, and that `operator_context` tables have `failure_pattern` rows less than 7 days old.

## GitHub Enterprise Configuration (2026-04-05)

Org-level settings applied to NIBARGERB-HLDPRO:

### Security (all repos)
- **Secret scanning**: enabled — detects leaked API keys, tokens, credentials in commits
- **Push protection**: enabled — blocks pushes containing secrets before they reach the repo
- **Dependabot alerts**: enabled — CVE tracking for all dependencies
- **Dependabot security updates**: enabled — auto-PRs for vulnerable dependencies
- **Dependency graph**: enabled — required for Dependabot
- **Web commit signoff**: required

### Branch Protection (org-level rulesets)
- **Protect main branches** (all repos except ASC-Evaluator): no deletion, no force-push, require PR
- **Protect develop branches** (all repos except ASC-Evaluator, hldpro-governance): no deletion, no force-push

### Requires Web UI Setup
- **Verified domains**: `hldpro.com`, `ascsurvey.com`, `hldpro.dev` — add at github.com/organizations/NIBARGERB-HLDPRO/settings/domains
- **2FA requirement**: enable at github.com/organizations/NIBARGERB-HLDPRO/settings/security
- **CodeQL code scanning**: enable at github.com/organizations/NIBARGERB-HLDPRO/settings/security_products

## Society of Minds — Model Routing Charter (2026-04-14)

Activity → model routing is codified as a society-of-minds role charter with enforced handoff protocols. Every intent has a CI-verifiable enforcement artifact — no orphan rules.

### Tiers

| Tier | Role | Primary | Fallback 1 | Fallback 2 | Floor |
|---|---|---|---|---|---|
| 1 | **Dual Planner — required pair** | Claude: `claude-opus-4-6` **AND** Codex: `gpt-5.4` @ `model_reasoning_effort=high` | Claude → `claude-sonnet-4-6`; Codex → `gpt-5.3-codex-spark` @ `high` | Codex only → `gpt-5.3-codex-spark` @ `medium` | Claude: no Haiku for planning. Codex: no below-spark for planning. Both unavailable → halt. |
| 2 | Worker (coder) | `gpt-5.3-codex-spark` @ `high` | `gpt-5.3-codex-spark` @ `medium` | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (local warm daemon) → **Windows Ollama** (`http://172.17.227.49:11434`, `qwen2.5-coder:7b`) → `claude-sonnet-4-6` (cost-flagged). Routed via `scripts/windows-ollama/decide.sh`; PII halts routing per invariant #8; all calls audited per invariant #10. | — |
| 3 | Reviewer (code) | `claude-sonnet-4-6` | `claude-haiku-4-5` (review quality flagged) | — | — |
| 3 | Reviewer (non-code long-form) | `gpt-5.4` @ `medium` | `gpt-5.4` @ `low` | `claude-sonnet-4-6` | — |
| 4 | Gate / verifier | `claude-haiku-4-5-20251001` | `claude-sonnet-4-6` (wasteful but safe) | — | — |

### LAM lane (local, Apple M5 — MLX runtime)

LAM is lateral to the tier chain. Never plans (Tier 1), never cross-reviews (independence requires non-local). Used for PII / bulk / embeddings / offline.

| Mind | Model ID | Role | Token cap |
|---|---|---|---|
| M7 Guardrail-LAM | `mlx-community/Qwen3-8B-4bit` | Pre-exec PASS/BLOCK | 64 |
| M4 Worker-LAM | `mlx-community/Qwen3-14B-4bit` | Implementation on local lanes (PII/bulk/offline) | 400 |
| M6 Critic-LAM | `mlx-community/gemma-4-26b-a4b-4bit` (outlines) | Adversarial review | 256 |
| MCP daemon | `mlx-community/Qwen3-1.7B-4bit` (primary) / `mlx-community/Phi-4-mini-instruct-4bit` (reserve) | Intent parsing + packet routing; always-warm, evictable under pressure | 128 |
| Qwen-Coder fallback | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | Tier-2 worker when codex-spark unavailable | 512 |
| Auditor-Claude | `claude-sonnet-4-6` | Manifest-only review for PII, content review for non-PII | — |

Reference runtime: `local-ai-machine/src/inference/mlx_runtime.py`, `LOCAL_LLM_RUNTIME_STRATEGY.md`, `SOCIETY_OF_MINDS_INTEGRATION.md`. No LAM rewrite — the canonical protocol lives in `local-ai-machine`; this standard references it.

### MCP daemon (always-warm local orchestrator)

Hosted in `local-ai-machine/services/som-mcp/`. Single long-running process (boot-start via launchd) that exposes the MCP protocol over stdio to all local Claude / Codex sessions.

**Responsibilities:**
- Intent parsing (fuzzy NL → structured routing decisions)
- Packet handoff (receives, validates structurally against STANDARDS, dispatches next tier)
- Deterministic validator sits behind MCP tools — LLM is used for intent parsing only, never as rule engine
- Local capability endpoints: `lam.probe`, `lam.embed`, `lam.scrub_pii`, `som.log_fallback`, `som.chain`

**Eviction policy (resident-memory budget):**
- M7 Guardrail-LAM: **privileged, always resident** (4.67 GB)
- MCP daemon model: **warm, evictable** — evicted first under memory pressure; reloaded after M6 unloads
- M4 / M6 / Qwen-Coder: on-demand load, unload after work

**Model upgrade stub:** `active` key in `.lam-config.yml mcp` block controls which MCP model loads. Primary `qwen3-1.7b`; flip to `phi-4-mini` when role_scope expands to include reviewer-lam-fallback or routing-error-rate > 5% over 1 week.

**Fallback semantics:**
- Daemon unavailable → halt for arch / standards / PII work
- Daemon unavailable → degraded-mode allowed for implementation work (logged to `raw/model-fallbacks/`)

### Handoff chain (every architecture/standards slice)

```
Tier 1 Dual Planner (opus-4-6 ⇄ gpt-5.4 high)  →  raw/cross-review/YYYY-MM-DD-*.md
                        ↓ dual-signed plan
Tier 2 Worker (gpt-5.3-codex-spark high)        →  diff on PR
                        ↓
Tier 3 Reviewer (sonnet-4-6 for code)           →  approve / changes
                        ↓
Tier 4 Gate (haiku via verify-completion)       →  PASS / FAIL
```

LAM runs out-of-band for its lanes; feeds sanitized outputs into any tier that needs them.

### Hard-rule invariants

1. **No self-approval.** No mind reviews its own output. Drafter, reviewer, and gate identities must be distinct.
2. **No tier skipping.** No merge without Worker → Reviewer → Gate.
3. **Planning floor.** Tier 1 never drops below `claude-sonnet-4-6` (Claude side) or `gpt-5.3-codex-spark` (Codex side). Both unavailable → halt.
4. **PII floor.** Content tagged or detected as PII routes through LAM only. Never sent to cloud reviewers. Violation = security incident.
5. **Cross-family independence.** Tier 1 Planner-Claude and Planner-Codex MUST be different model families (Anthropic + OpenAI). Never both same family.
6. **Local family diversity.** Worker-LAM and Reviewer-LAM MUST be different model families (e.g., Qwen + Gemma).
7. **Fallback is logged.** Every fallback to a lower tier writes a schema-validated entry under `raw/model-fallbacks/YYYY-MM-DD.md`.
8. **Windows-Ollama PII floor.** PII-tagged or PII-detected payloads MUST block Windows host AND Sonnet cloud fallback. Route to LAM only or halt. Before submitting any payload to the Windows host endpoint, payload must pass `pii-patterns.yml` middleware. Fail-closed if patterns unavailable. (Enforced in Sprint 2 via `scripts/windows-ollama/submit.py`; active in Sprint 5.)
9. **Windows-Ollama firewall binding.** The Windows host endpoint MUST NOT be exposed beyond LAN. Requires firewall binding to Mac host IP or explicit trusted subnet allowlist. No public bind or port-forwarding. Separate epic adding Cloudflare Access may extend this; until then, LAN-only via `sase-switch` vEthernet adapter on subnet `172.17.0.0/16`. (Enforced in Sprint 4 via `check-windows-ollama-exposure.yml` CI; active in Sprint 5.)
10. **Windows-Ollama audit.** Every Windows-Ollama call appends to `raw/remote-windows-audit/YYYY-MM-DD.jsonl` with hash-chain + HMAC + daily manifest. Break the chain → CI validator fails; endpoint disabled until rebuilt. (Enforced in Sprint 3 via `check-windows-ollama-audit-schema.yml` CI; active in Sprint 5.)

### Cross-review artifact schema (required for arch/standards PRs)

`raw/cross-review/YYYY-MM-DD-{pr-slug}.md` must begin with YAML frontmatter validated by `require-cross-review.yml`:

```yaml
---
pr_number: <int>
pr_scope: architecture | standards | implementation
drafter:
  role: architect-claude | architect-codex
  model_id: <exact model string>
  model_family: anthropic | openai | local
  signature_date: YYYY-MM-DD
reviewer:
  role: architect-claude | architect-codex
  model_id: <exact model string>
  model_family: anthropic | openai | local
  signature_date: YYYY-MM-DD
  verdict: APPROVED | APPROVED_WITH_CHANGES | REJECTED
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---
```

Validator rejects if: any field missing, `drafter.model_family` == `reviewer.model_family`, `drafter.model_id` == `reviewer.model_id`, `reviewer.verdict` == `REJECTED`, or any `invariants_checked` value is false.

### Enforcement index (CI-verifiable — no orphan rules)

| # | Intent | Enforcement | Halt on fail |
|---|---|---|---|
| 1 | Agent `model:` pin | `check-agent-model-pins.yml` parses frontmatter | PR blocked |
| 2 | Codex calls specify `-m` + reasoning | `check-codex-model-pins.yml` scans scripts/workflows | PR blocked |
| 3 | Cross-review artifact validates schema + invariants | `require-cross-review.yml` schema validator | PR blocked |
| 4 | No-self-approval (distinct identities) | `check-no-self-approval.yml` | PR blocked |
| 5 | Fallback auto-logged + schema-valid | `scripts/model-fallback-log.sh` + `check-fallback-log-schema.yml` | PR blocked if malformed |
| 6 | Fallback rate + M6-vs-Sonnet agreement metrics | `overlord-sweep` weekly | Auto-issue on threshold |
| 7 | Arch on Haiku blocked | `check-arch-tier.yml` + `verify-completion` hard-fail | PR + closeout blocked |
| 8 | PII never leaves machine | `check-pii-routing.yml` + `require-lam-dual-signature.sh` | PR + closeout blocked |
| 9 | LAM family diversity | `check-lam-family-diversity.yml` reads `.lam-config.yml` | PR blocked |
| 10 | LAM availability for PII PRs | `check-lam-availability.yml` runtime probe | PR blocked |
| 11 | CLAUDE.md points to SoT | `check-claude-md-pointer.yml` | PR blocked |
| 12 | Exception register covers deferrals with expiry ≤ 90d | `overlord-sweep` validates; past-expiry auto-opens issue | Sweep issue on breach |
| 13 | Windows-Ollama PII floor (invariant #8) | `scripts/windows-ollama/submit.py` validates PII patterns; `scripts/windows-ollama/decide.sh` routes `PII` to HALT before all ladder steps | PR blocked if PII routes to Windows or cloud |
| 14 | Windows-Ollama firewall binding (invariant #9) | `check-windows-ollama-exposure.yml` CI gate (Sprint 4) asserts no public bind, endpoint still `172.17.227.49:11434` | PR blocked if exposure detected |
| 15 | Windows-Ollama audit enforcement (invariant #10) | `scripts/windows-ollama/verify_audit.py` local validator (Sprint 3); `check-windows-ollama-audit-schema.yml` CI gate (Sprint 4) | PR blocked on chain break, HMAC forgery, or manifest mismatch |
| 16 | Windows-Ollama audit schema validation | `check-windows-ollama-audit-schema.yml` verifies audit chain integrity on PRs touching audit files | PR blocked |
| 17 | Windows-Ollama firewall exposure validation | `check-windows-ollama-exposure.yml` asserts no public bind, endpoint stability (172.17.227.49:11434), Cloudflare stub status | PR blocked |

### Exception register schema

`hldpro-governance/docs/exception-register.md` entries require:
- `rule_id` (e.g., `SOM-PII-001`)
- `repo` (repo where exception applies)
- `deferral_reason` (cites missing artifact or repo-specific blocker)
- `approver` (human, named)
- `expiry_date` (max 90 days from entry)
- `review_cadence` (monthly minimum)

Overlord-sweep auto-opens issues for past-expiry entries.

### Round 1 execution protocol (transitional, until M6 steady-state confidence)

While M6 Critic-LAM's judgment is being calibrated against Sonnet's:
- M6 is primary code/artifact reviewer; Sonnet runs in **shadow (A/B)** mode on the same artifact.
- Both verdicts logged to `raw/ab-review/YYYY-MM-DD-{slug}.md` with `agreement: match | m6_only_findings | sonnet_only_findings | both`.
- **Conservative gate:** if Sonnet REJECTED and M6 APPROVED, Sonnet wins this round; divergence flagged.
- Overlord-sweep reports weekly M6-vs-Sonnet agreement rate. Exit Round 1 when agreement ≥ 90% for 3 consecutive weeks.

## Windows Host Inference (Tier-2 fallback)

A LAN-resident Ollama-served Windows 10 workstation (64 GB RAM, 16 GB VRAM) acts as a Tier-2 Worker fallback when the local Mac is memory-tight AND codex-spark is quota-blocked. The integration was first proven in `local-ai-machine` issue #68 (closed 2026-03-16) for HP critic work via `CRITIC_OLLAMA_URL`; this section promotes it from critic-only to general SoM Tier-2 worker.

### Endpoint

- URL: `http://172.17.227.49:11434` (LAN-only, vEthernet adapter `sase-switch`)
- API: Ollama `/api/generate` (OpenAI-compatible `/v1/` available)
- Pinned operating settings (proven in LAM #68): `keep_alive=15m`, `num_ctx<=4096`, adaptive offload ladder `99 -> 80 -> 60`, call timeout 45000ms

### Pinned model roster

Treat the runbook (`docs/runbooks/windows-ollama-worker.md`) as the source of truth for the live inventory. Charter-relevant baseline:

| Model | Role | VRAM (~Q4) |
|---|---|---|
| `qwen2.5-coder:7b` | SoM Tier-2 Worker (this PR) | ~5 GB |
| `llama3.1:8b` | HP critic (existing, see LAM #68) | ~5 GB |

Operator may pull additional models (e.g. `qwen3:14b-q4_K_M`) — runbook documents the procedure.

### Threat model (delta vs. local)

| Attack | Mitigation |
|---|---|
| PII tunneled in worker prompt | Invariant #13 PII middleware before submit |
| Endpoint exposed to internet | Invariant #14 LAN-only; Cloudflare Tunnel deferred to future epic |
| Audit trail tampering | Invariant #15 hash-chain + HMAC + daily manifest |
| Endpoint asleep / unreachable | Decision script falls through to next ladder rung; WoL deferred to future epic |
| Wrong model routed for prompt | Submission script validates model name against runbook allowlist |

### Future epics (stubbed; not in scope)

- Cloudflare Tunnel exposure for off-LAN access (mirrors Remote MCP Bridge pattern; would require Cloudflare Access invariant)
- Wake-on-LAN provisioning for unattended availability
- Windows host metrics / health check workflow

## Exceptions
- ASC-Evaluator: knowledge repo, exempt from code governance
- Repos may have ADDITIONAL governance beyond this baseline
- HIPAA agents must never be weakened or consolidated away
- Codex subagents/personas may stand in for repo-required Claude agents only when they preserve the same separation of duties and approval boundaries
- Bootstrap exception (`SOM-BOOTSTRAP-001`): the PR introducing the Society of Minds standard cannot self-enforce `require-cross-review.yml` since the workflow is being added in the same PR. Tier 1 cross-review was completed out-of-band via `raw/cross-review/2026-04-14-society-of-minds-charter.md`. Expires on merge of this PR.
