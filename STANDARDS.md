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
- `.claude/settings.json` PostToolUse matcher must be `"*"` (all tools), NOT `"Bash"` — errors from MCP, Agent, Read, etc. must also trigger the 3-attempt gate
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
- Issue-driven execution branches (`issue-*` and `riskfix/*`) must have at least one valid `*structured-agent-cycle-plan.json` file before execution is governance-ready.
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
| ai-integration-services | SaaS platform (Supabase + Deno + Vite) | Full (hooks + CI + agents) | Full + PentAGI |
| HealthcarePlatform | Monorepo (backend + frontend), HIPAA | Full + HIPAA (zero-fail) | Full + PentAGI + HIPAA |
| local-ai-machine | AI/ML infrastructure | Full (lane-based + session locks) | Baseline |
| knocktracker | Field operations app | Standard (rules + CI) | Baseline |
| ASC-Evaluator | Knowledge repo (no code) | Exempt from code governance | Exempt |

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

## Exceptions
- ASC-Evaluator: knowledge repo, exempt from code governance
- Repos may have ADDITIONAL governance beyond this baseline
- HIPAA agents must never be weakened or consolidated away
- Codex subagents/personas may stand in for repo-required Claude agents only when they preserve the same separation of duties and approval boundaries
