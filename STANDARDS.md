# HLD Pro — Shared Standards Manifest

> The overlord agent checks every repo against these standards.
> Update this file to change what the overlord enforces.

## Required Files (all code repos)
- `CLAUDE.md` at repo root (or workspace root for monorepos)
- `docs/PROGRESS.md` — feature status tracker (uppercase filename)
- `docs/FEATURE_REGISTRY.md` — detailed feature inventory and readiness matrix
- `docs/FAIL_FAST_LOG.md` — error patterns and resolutions
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

### Branch Isolation (global hook)
- `~/.claude/hooks/branch-switch-guard.sh` — **global PreToolUse hook** that blocks `git checkout <branch>` and `git switch <branch>` in all repos
- Prevents multi-session conflicts where one session's branch switch corrupts another session's working directory
- **Allowed:** `git checkout -- <file>` (file restore), `git checkout .`, `git worktree add`
- **Blocked:** `git checkout <branch>`, `git switch <branch>`, `git checkout -b <branch>`, `git checkout -`
- **Alternative:** Use `EnterWorktree` tool or `git worktree add` for branch work in concurrent sessions
- Configured in `~/.claude/settings.json` PreToolUse hooks (absolute path, not `~`)

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

- Weekly overlord sweep includes Codex CLI (`codex exec review`) as a second-opinion layer
- Codex outputs structured JSON to `~/Developer/hldpro/.codex-ingestion/{repo}/`
- The primary sweep session cross-references findings against existing docs and validates them
- The primary sweep session qualifies findings and generates backlog entries in the ingestion folder (`backlog-{date}.md`)
- **Backlog entries are staged, not committed** — they surface during HITL backlog review
- User promotes entries to `docs/PROGRESS.md` or `docs/FAIL_FAST_LOG.md` when approved
- Entries tagged `⚠️ CODEX-FLAGGED` / `Source: Codex review` for traceability
- Requires `OPENAI_API_KEY` in environment (or Codex Connect auth) — skips gracefully if missing

## Completion Verification Protocol — ENFORCED

**Before claiming any cross-repo or governance task as "done":**

1. **Artifact verification**: For every file the plan says to create, run `git show HEAD:<path>` on the target branch to confirm it exists in the commit (not just on disk).
2. **Standards sweep**: Run `~/.claude/agents/verify-completion.md` against all affected repos in isolated worktrees. It checks every item in this STANDARDS.md and reports PASS/FAIL per repo without mutating shared checkouts.
3. **PR verification**: If the plan says "create PR", confirm the PR exists (`gh pr view`), is on the correct base branch, and CI is running.
4. **Specialist verification**: If repo governance required specialist agents/subagents for the task, verify the session used equivalent specialists. Codex may satisfy this with spawned Codex subagents/personas mapped from repo-local definitions; do not waive the requirement just because the repo uses Claude-era agent naming.
5. **No hedging**: Do not use "if it exists" language for required files. If STANDARDS.md says a file is required, it must exist — create it if missing.
6. **Session summary must match reality**: Before writing a session summary to memory, re-verify each claim. "Built" means merged to main or PR passing CI. "Created" means committed and pushed. "Planned" means neither.

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
