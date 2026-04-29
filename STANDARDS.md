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
- Governance repos and governed session-contract repos must use one canonical bootstrap helper path for session start, not duplicate checklist logic across multiple hook implementations.
- The canonical session-start helper must emit a machine-checkable sentinel proving that the repo session contract, `docs/EXTERNAL_SERVICES_RUNBOOK.md`, and `STANDARDS.md §Society of Minds` were loaded or surfaced for the current session. Missing files must be recorded as warnings in the sentinel output.
- Conventional commits: `feat/fix/docs/chore` with scope
- **Branch naming (all repos):** Use standard SoM prefixes: `feature/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`. Optional `-YYYYMMDD` date suffix is allowed on any prefix.
  - **LAM high-risk lane exception:** `riskfix/<slug>-YYYYMMDD` is the designated prefix for LAM high-risk fixes in `local-ai-machine`. The date suffix is **mandatory** and one PR per lane family is enforced by `breaker-mcp-contract`. This prefix is complementary to, not conflicting with, the standard SoM prefixes — it applies only to the `riskfix/` lane. All other work in LAM (and all work in every other repo) uses the standard SoM prefixes above. See `docs/exception-register.md §SOM-LAM-BRANCH-001` (resolved).
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
- Active issue-lane plans must also capture machine-checkable reviewer identity and handoff/review evidence fields sufficient for validators to reject self-review and evidence-free promotion.
- Issue-driven execution branches (any branch name containing `issue-<number>`, including `issue-*` and `feat/issue-<number>-...`) and risk-fix branches (`riskfix/*`) must have at least one valid issue-matching `*structured-agent-cycle-plan.json` file before execution is governance-ready. Note: `riskfix/<slug>-YYYYMMDD` (with date suffix) is the **required** implementation branch pattern for `local-ai-machine`, enforced by `edge_breaker_mcp_contract.yml`. Other repos accept `riskfix/*` as an optional prefix alongside standard `feat/fix/chore/docs` conventions but do not require it.
- Reusable governance CI validates structured plans through `scripts/overlord/validate_structured_agent_cycle_plan.py`.
- Cross-model review results from `scripts/codex-review.sh claude` belong in `alternate_model_review`.
- `alternate_model_review.required=false` is not a free-text bypass. New active issue-lane plans may omit alternate-family review only with a validator-legal bounded exemption.
- New accepted active issue-lane alternate-family reviews must record `reviewer_model_id` and `reviewer_model_family`, and validators must reject same-family or same-identity alternate-review claims against `plan_author`.
- Once a plan records accepted specialist or alternate-family review, `execution_handoff.review_artifact_refs` must be populated with `raw/cross-review/...` evidence before promotion continues.

### Planner Write-Boundary (Tier 1)
- Tier 1 planner sessions may create planning, review, and handoff artifacts only.
- Planning execution scope must declare this boundary with `execution_mode: planning_only` and `allowed_write_paths`; that allowlist is the authoritative planning write surface.
- Non-planning diffs require accepted pinned-agent handoff evidence (`handoff_evidence.status: accepted`) before merge.
- If planner and implementer are the same model or model family, handoff evidence must include an active exception reference and concrete expiry (`active_exception_ref`, `active_exception_expires_at`).
- CI is authoritative for this boundary (`.github/workflows/governance-check.yml`); local hook output from `hooks/code-write-gate.sh` is warning/early-signal only for planner-boundary drift.

### Lane Claim Gate (Issue Work)
- Every new implementation-ready issue lane must declare ownership in its execution scope with `lane_claim.issue_number`, `lane_claim.claim_ref`, `lane_claim.claimed_by`, and `lane_claim.claimed_at`.
- When `scripts/overlord/assert_execution_scope.py --require-lane-claim` is used, the current branch issue number, `expected_branch` issue number, and `lane_claim.issue_number` must match.
- Follow-up issue creation is a hard stop for the closing session unless the operator explicitly assigns that follow-up lane to the same session or a matching claimed execution scope already exists.
- Planning bootstrap may create PDCAR, structured plan, and execution-scope artifacts for a new issue; implementation changes require the claimed scope first.
- Local CI Gate resolves issue execution scopes by `lane_claim.issue_number`, not filename alone, so stale or cross-issue scope files cannot authorize another lane.

### Branch Isolation (global hook)
- `~/.claude/hooks/branch-switch-guard.sh` — **global PreToolUse hook** that blocks `git checkout <branch>` and `git switch <branch>` in all repos
- Prevents multi-session conflicts where one session's branch switch corrupts another session's working directory
- **Allowed:** `git checkout -- <file>` (file restore), `git checkout .`, non-issue `git worktree add`
- **Blocked:** `git checkout <branch>`, `git switch <branch>`, `git checkout -b <branch>`, `git checkout -`
- **Issue worktree guard:** `git worktree add -b issue-*` must include either `HLDPRO_LANE_CLAIM_BOOTSTRAP=1` for planning-bootstrap work or `HLDPRO_LANE_CLAIM_SCOPE=<scope.json>` pointing to an execution scope whose `lane_claim.issue_number` matches the issue branch.
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

### Secret Provisioning UX
- Missing-secret and deploy-preflight diagnostics must list required variable names only. They must not print secret values, partial values, token prefixes, raw phone numbers, signed URLs, Authorization headers, generated env file contents, or screenshots containing credentials.
- Operator guidance must route credential setup through approved provisioning surfaces:
  - `hldpro-governance/.env.shared` as the gitignored local SSOT for operator-managed local credentials
  - `scripts/bootstrap-repo-env.sh` generated repo-local env files, which remain ignored generated artifacts
  - provider dashboards or vaults for provider-owned secret rotation
  - GitHub Actions secrets or vars for CI-only credentials
- Tooling, runbooks, issue bodies, PR descriptions, validation artifacts, and CI logs must not instruct operators to paste credential values into inline shell commands. This includes shell export assignments for secret variables, `launchctl setenv` with secret values, and pipelines that send literal values into `gh secret set`.
- Missing-secret messages should use the canonical pattern documented in `docs/ENV_REGISTRY.md`: report the missing variable names, identify the approved provisioning surface, and ask the operator to rerun the appropriate bootstrap or provider/CI configuration step.
- Evidence for secret provisioning must be value-free. Valid evidence includes variable names, command exit status, redacted dry-run output, file paths to ignored/generated env targets, provider surface names, GitHub secret names, and issue links.

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

`docs/governed_repos.json` is the executable source of truth for governed repository membership, lifecycle status, governance status, subsystem participation, and issue-backed classification. This table is a human summary and is validated so repo names cannot silently drift from the registry.

| Repo | Type | Governance Tier | Security Tier |
|------|------|-----------------|---------------|
| hldpro-governance | Meta-governance repo (scripts + CI + agents) | Governance-owner (see note below) | Baseline |
| ai-integration-services | SaaS platform (Supabase + Deno + Vite) | Full (hooks + CI + agents) | Full + PentAGI |
| HealthcarePlatform | Monorepo (backend + frontend), HIPAA | Full + HIPAA (zero-fail) | Full + PentAGI + HIPAA |
| local-ai-machine | AI/ML infrastructure | Full (lane-based + session locks) | Baseline |
| knocktracker | Field operations app | Standard (rules + CI) | Baseline |
| seek-and-ponder | Faith AI product repo | Full | Full + PentAGI |
| EmailAssistant | Municipal email assistant | Full, adoption blocked pending EmailAssistant#1 | Full + PentAGI |
| Stampede | Phase0 product repo | Standard | Baseline |
| ASC-Evaluator | Knowledge repo (no code) | Exempt from code governance | Exempt |

> **hldpro-governance hook path note:** Product repos store hooks under `.claude/hooks/` (local-only, gitignored). hldpro-governance stores its committed hooks under `hooks/` at repo root (checked in, enforced repo-wide). Both satisfy the Required Governance hook contract — the difference is scope: local session vs. repo-wide enforcement. Hook *scripts* (e.g. `hooks/pre-session-context.sh`) are committed for repo-wide discoverability; the local `settings.json` that wires them into Claude Code sessions is gitignored and set up per-developer.

For `hldpro-governance`, `scripts/session_bootstrap_contract.py` is the
canonical session-start implementation path. `hooks/pre-session-context.sh` and
any `.claude/hooks/pre-session-context.sh` compatibility wrapper must call that
helper instead of maintaining separate bootstrap logic.

## Cross-Model Review

### Bidirectional Agent Calls

Both Claude and Codex sessions can invoke each other as specialist reviewers:

| Direction | Script | When to use |
|-----------|--------|-------------|
| Claude → Codex | `bash scripts/codex-review.sh review <branch>` | Second-opinion code review from Codex |
| Claude → Codex | `bash scripts/codex-review.sh audit <path>` | Codex security audit |
| Codex → Claude | `bash scripts/codex-review.sh claude <packet-file>` | Claude alternate-family review from Codex sessions |

**Auth requirements:**
- Codex sessions: `OPENAI_API_KEY` or `~/.codex/auth.json` (ChatGPT account, `gpt-5.4` default)
- Claude calls from Codex: use the canonical bootstrap command `bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh <repo>` so the repo wrapper's generated env surface contains `CLAUDE_CODE_OAUTH_TOKEN`; do not hand-source tokens
- `scripts/codex-review.sh claude` is the SSOT packet-review path. The packet must be supplied as a self-contained file path, and the governance wrapper runs Claude in `bypassPermissions` mode by default with no tool access unless the execution scope explicitly enables `CLAUDE_REVIEW_ALLOWED_TOOLS`. This keeps the default path read-only in practice while avoiding plan-mode turn churn. Bounded packet reviews default to `claude-opus-4-6`; execution scopes may override `CLAUDE_REVIEW_MODEL` and `CLAUDE_REVIEW_MAX_TURNS` when a different Claude reviewer or a larger packet is explicitly approved.
- Codex config must inherit the token: `shell_environment_policy.inherit = "all"` in `~/.codex/config.toml`
- Primary-session dispatch is hard-gated in both directions. If Codex is primary, it must dispatch Claude-owned pinned roles through the governed Claude path. If Claude is primary, it must dispatch Codex-owned pinned roles through the governed Codex path. Neither side may absorb the other side's pinned role.
- Every governed code/doc/config change must end with a distinct pinned auditor or QA specialist review before merge or closeout.
- Declared specialist-agent lanes are packet-backed contracts. Structured plans and package handoffs must bind agent identity, packet input, packet output, transport mode, and availability evidence; validators remain authoritative over acceptance.
- `sim-runner` availability is governed by tracked agent surfaces plus `docs/hldpro-sim-consumer-pull-state.json`; do not treat ad hoc local installs or undeclared personas as validator-legal availability evidence.
- Governance specialist planner, auditor, and QA lanes must run through `python3 scripts/packet/run_specialist_packet.py --packet <packet-file> --persona-id <persona-id>`. They are Codex-side specialist lanes backed by tracked `hldpro-sim` personas and do not replace the pinned Claude alternate-family review lane.

**Script contract:** Every code repo must have `scripts/codex-review.sh` with at minimum the `review` and `claude` modes. `scripts/codex-review.sh` is the only operator-facing path. Use `hldpro-governance/scripts/codex-review-template.sh` only as the shared implementation source behind that wrapper. `claude` mode must consume a packet file path, not ad hoc shell-built prompt text.

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

## §DA — Delegation and Agent Authority
<!-- Added: April 2026 — multi-repo agent governance -->

### Agent Tier Model

Claude-native agents (`.claude/agents/`) operate above SoM's execution worker layer.
They route, gate, and report. They do not replace SoM workers for code execution.

| Tier | Class | Examples | Scope |
|------|-------|----------|-------|
| 0 | Cross-repo supervisor | overlord-sweep | All repos |
| 1 | Repo supervisor | hldpro-watcher | Single repo |
| 2 | Worker/reviewer | migration-validator, closeout-writer | Task-scoped |

### Relationship to §Society of Minds

SoM defines the **execution** worker ladder in §Society of Minds (Tier 2). The Worker fallback chain is defined there; `gpt-5.4` is not a Worker fallback model and is used only outside Worker execution.

Claude-native Tier 2 agents define the **quality gate** layer:
```
Orchestrator → Tier 2 agent (validates/reviews) → SoM worker (implements) → Tier 2 agent (reports) → Orchestrator
```

For repos without SoM workers: Tier 2 agents are the execution layer for their registered scope.

### Delegation Rule (all repos)

Orchestrator ROUTES and VERIFIES. Does NOT implement tasks owned by a Tier 2 agent.
If the orchestrator begins a task in the table below: STOP, spawn the agent, wait for report.

| Task Type | Owner | Model |
|-----------|-------|-------|
| Migration validation | migration-validator | Sonnet |
| Edge function review | edge-fn-reviewer | Sonnet |
| Schema consistency | schema-reviewer | Sonnet |
| Test writing | test-writer | Sonnet |
| Diagram generation | diagram-writer | Sonnet |
| Documentation | docs-writer | Sonnet |
| Repo health aggregation | hldpro-watcher / LAM equivalent | Sonnet |
| Cross-repo health | overlord-sweep | Sonnet |

### Delegation Gate Enforcement

Delegation ownership may be mechanically enforced through a PreToolUse delegation gate.
The gate inspects orchestrator task descriptions for Agent/Task, Bash, and
implementation-scoped Explore attempts, maps them to registered Tier 2 owners,
and blocks or warns when the orchestrator attempts owned work directly.

Implementation rules:
- Deterministic routing rules run first.
- Optional classifier or MCP fallback may run only when deterministic rules are inconclusive.
- High-confidence matches (`>= 0.90`) block for Agent/Task and Bash.
- Medium-confidence matches (`0.70` to `0.89`) warn and log.
- Explore remains warn-only so the orchestrator can still gather routing context.
- Read is never gated.
- Bypass requires an explicit operator-visible `--bypass-delegation-gate` first-token flag and a local governance log entry.
- Unavailable MCP/classifier endpoints fail open to ALLOW and must not block local work.

### Scope Freeze Rule (all repos)

When session has `.claude/current_plan.json` with `approved_scope_paths`:
- Out-of-scope findings → add to BACKLOG, do not act
- governance-check.sh enforces this mechanically

### Max Loop Rule (all repos)

- Tier 2 workers: max-loops: 1 per invocation
- Tier 1 supervisors: max-loops: 3 before HITL checkpoint
- Orchestrator: same failure twice → HALT, update queue

### HALT Conditions (all repos)

Stop and surface to operator:
- CRITICAL from any worker agent
- Tool call blocked by governance-check.sh
- Scope drift detected
- Same error twice in session
- Net-new scope not in current plan

### Upward Reporting Protocol

Each Tier 1 supervisor writes status JSON after every run.
Path: `${GOVERNANCE_REPORTS_PATH:-../hldpro-governance/reports}/<repo>/<date>-status.json`
CI limitation: stdout `[GOVERNANCE-REPORT]` prefix is local debug only — not consumed cross-repo.
Cross-repo CI reporting requires `gh api` write to governance repo.

```json
{
  "repo": "<repo-name>",
  "date": "<YYYY-MM-DD>",
  "overall": "HEALTHY | ATTENTION | ACTION_REQUIRED",
  "criticals": [], "warnings": [], "scope_violations": [],
  "next_action": "<string>"
}
```

### Session Plan Ownership

`.claude/current_plan.json` is owned by the orchestrator only.
Worker and supervisor agents may read it, but may not create or modify it.
Schema: `hldpro-governance/schemas/approved_scope_paths.schema.json`

## Society of Minds — Model Routing Charter (2026-04-14)

Activity → model routing is codified as a society-of-minds role charter with enforced handoff protocols. Every intent has a CI-verifiable enforcement artifact — no orphan rules.

### Governance waterfall

Codex is the primary local orchestrator for governance work. The orchestrator
coordinates handoffs, integrates approved plans, updates local docs and GitHub
issues, and records evidence. Orchestration is not approval authority: the
orchestrator cannot plan, implement, review, and gate the same work.

Session-start enforcement must surface this waterfall before implementation
authority is exercised. The minimum governance session contract is:

1. Load repo `CODEX.md`.
2. Load repo `CLAUDE.md`.
3. Load `docs/PROGRESS.md`.
4. Load `docs/FAIL_FAST_LOG.md`.
5. Load `STANDARDS.md §Society of Minds`.
6. Load `docs/EXTERNAL_SERVICES_RUNBOOK.md`.
7. Surface pending Codex backlog findings if any exist.
8. Record a bootstrap sentinel proving steps 1, 5, and 6 were loaded or surfaced.

| Stage | Role | Primary | Fallback / Constraint |
|---|---|---|---|
| 0 | Orchestrator | Codex session | Coordinates and integrates only; no self-approval. |
| 1A | Planner | `claude-opus-4-6` | `claude-sonnet-4-6` only when Opus is unavailable; fallback must be logged. |
| 1B | Plan reviewer | `gpt-5.4` @ `model_reasoning_effort=high` | `gpt-5.3-codex-spark` may run same-family critical/specialist plan review only when `gpt-5.4` is unavailable; degraded independence must be logged and operator-visible before implementation. |
| 1C | Plan integrator | Codex orchestrator | Combines the accepted plan and review into issue/docs/artifacts; no independent approval authority. |
| 2 | Worker (substantial implementation) | `claude-sonnet-4-6` | Local Qwen worker sublane for bounded low/medium-risk chunks; otherwise halt or escalate intentionally. |
| 2L | Local bounded worker | Qwen local ladder below | Implementation only; never planning, final review, or gate authority. |
| 3 | QA / code review | Appropriate Codex QA model with explicit `-m` and `model_reasoning_effort` | Must be distinct from the Worker. For standards/architecture changes, preserve the Tier 1 cross-review artifact. |
| 3B | Shadow local critic | `mlx-community/gemma-4-26b-a4b-4bit` | A/B measurement only against Codex/Claude QA; non-blocking and cannot approve or reject. |
| 4 | Gate / verifier | deterministic checks + completion verification | Gate identity must be distinct from planner, worker, and QA reviewer. |

### Local worker ladder

Local workers conserve paid token usage on bounded implementation work. They do
not replace the planning, QA, or gate roles.

| Order | Model | Role | Constraints |
|---|---|---|---|
| 1 | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | Micro-worker | Tiny patches, tests, mechanical edits. Do not use for full-file regeneration above the issue #105 safe limit. |
| 2 | `mlx-community/Qwen3-14B-4bit` | Standard local worker | Moderate bounded implementation and structured-output work. |
| 3 | `mlx-community/Qwen3.6-35B-A3B-4bit` | Large local worker | On-demand only; one large local model loaded at a time; use when memory headroom is available. |
| 4 | Halt or deliberate cloud escalation | `claude-sonnet-4-6` | Escalation is an explicit routing decision, not an automatic fallback. |

### LAM lane (local, Apple M5 — MLX runtime)

LAM is lateral to the tier chain. Never plans (Tier 1), never cross-reviews (independence requires non-local). Used for PII / bulk / embeddings / offline.

| Mind | Model ID | Role | Token cap |
|---|---|---|---|
| M7 Guardrail-LAM | `mlx-community/Qwen3-8B-4bit` | Pre-exec PASS/BLOCK | 64 |
| M4 Worker-LAM | `mlx-community/Qwen3-14B-4bit` | Implementation on local lanes (PII/bulk/offline) | 400 |
| M5 Large Worker-LAM | `mlx-community/Qwen3.6-35B-A3B-4bit` | On-demand larger local implementation | 512 |
| M6 Shadow-Critic-LAM | `mlx-community/gemma-4-26b-a4b-4bit` (outlines) | A/B shadow critique only | 256 |
| MCP daemon | `mlx-community/Qwen3-1.7B-4bit` (primary) / `mlx-community/Phi-4-mini-instruct-4bit` (reserve) | Intent parsing + packet routing; always-warm, evictable under pressure | 128 |
| Qwen-Coder micro-worker | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | Bounded local implementation chunks | 512 |
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
- M4 / M5 / M6 / Qwen-Coder: on-demand load, unload after work

**Model upgrade stub:** `active` key in `.lam-config.yml mcp` block controls which MCP model loads. Primary `qwen3-1.7b`; flip to `phi-4-mini` when role_scope expands to include reviewer-lam-fallback or routing-error-rate > 5% over 1 week.

**Fallback semantics:**
- Daemon unavailable → halt for arch / standards / PII work
- Daemon unavailable → degraded-mode allowed for implementation work (logged to `raw/model-fallbacks/`)

### Handoff chain (every architecture/standards slice)

```
Codex orchestrator                                 →  issue/docs/artifact coordination
                        ↓
Planner-Claude (opus-4-6)                          →  plan
                        ↓
Plan reviewer-Codex (gpt-5.4 high)                →  raw/cross-review/YYYY-MM-DD-*.md
                        ↓
Codex orchestrator                                 →  integrated plan + GH issue/docs
                        ↓
Worker-Claude (sonnet-4-6) or bounded Qwen worker  →  diff on PR
                        ↓
Codex QA                                           →  approve / changes
                        ↓
Gate / deterministic verifier                      →  PASS / FAIL
```

LAM runs out-of-band for its lanes; feeds sanitized outputs into any tier that needs them.

### Handoff package artifacts

Every model/agent handoff that crosses planning, implementation, QA, or gate
authority must have a structured package view. The package does not replace
the existing plan, execution scope, packet, validation, review, or closeout
artifacts; it binds them so the receiver can verify the exact acceptance
criteria and evidence before accepting the handoff.

Canonical schema: `docs/schemas/package-handoff.schema.json`

Canonical location: `raw/handoffs/YYYY-MM-DD-issue-<n>-<stage>.json`

Required lifecycle links:
- GitHub issue number and optional parent epic number.
- Source role and destination role.
- Structured plan reference.
- Lifecycle-state transitions are hard-gated:
  - `planned` / `planning_only` may defer populated review refs only until the
    required review actually happens.
  - Promotion to `implementation_ready` requires accepted review evidence and
    populated review refs.
  - Continuing handoffs from `implementation_ready` onward require populated
    handoff and gate evidence where the lifecycle validator expects it.
- Execution-scope reference for implementation-ready or later states.
- Packet reference for dispatch/validation-ready or later states.
- Acceptance criteria with verification references.
- Validation commands.
- Review and gate artifact references when required by risk/surface.
- Closeout reference for accepted/released/archived states.

Execution scopes are schema-backed by
`docs/schemas/execution-scope.schema.json` and remain enforced by
`scripts/overlord/assert_execution_scope.py`.

### Hard-rule invariants

1. **No self-approval.** No mind reviews its own output. Drafter, reviewer, and gate identities must be distinct.
2. **No tier skipping.** No merge without Planner → Plan Review → Worker → QA → Gate.
3. **Planning floor.** Planning never drops below `claude-sonnet-4-6` on the Claude side or `gpt-5.3-codex-spark` on the OpenAI side. `gpt-5.3-codex-spark` is a plan-review fallback/specialist critic only when `gpt-5.4` is unavailable, and the degraded same-family review state must be logged. Both planning families unavailable → halt.
4. **PII floor.** Content tagged or detected as PII routes through LAM only. Never sent to cloud reviewers. Violation = security incident.
5. **Cross-family independence.** Tier 1 Planner-Claude and Planner-Codex MUST be different model families (Anthropic + OpenAI). Never both same family.
6. **Local family diversity.** Local Qwen workers and Gemma shadow critique must remain separate roles. Gemma output is A/B evidence only until a later issue explicitly promotes it.
7. **Fallback is logged.** Every fallback to a lower tier writes a schema-validated entry under `raw/model-fallbacks/YYYY-MM-DD.md`.
8. **Windows-Ollama off-ladder.** Windows Ollama is not an active governance waterfall fallback. Historical Windows tooling may remain for archived validation or separately approved experiments, but it is not a Worker fallback and must not be selected by SoM routing.
9. **Gemma non-authority.** `mlx-community/gemma-4-26b-a4b-4bit` may produce A/B shadow critique only. Its findings can inform follow-up work but cannot block, approve, or satisfy QA/gate requirements.
10. **Local worker bounded scope.** Qwen local workers may write only within an approved execution scope, with explicit file/task bounds and downstream QA/gate evidence.
11. **Remote MCP stdio-only boundary.** Remote-origin packets MUST NOT invoke stdio-only tools. `lam.scrub_pii` remains stdio-only; remote bridge dispatchers must refuse it and any future stdio-only tool before local MCP execution.
12. **Remote MCP server-authoritative origin.** Remote HTTP transport MUST overwrite client-supplied `origin` after Cloudflare Access and inner-token validation. Client-supplied local origins are ignored and audited as spoof attempts.
13. **Remote MCP PII middleware.** Every remote-exposed tool call MUST pass application-layer PII middleware before dispatch. PII matches, missing PII patterns, malformed PII patterns, schema violations, and payload-size violations fail closed.
14. **Remote MCP Cloudflare Access identity.** Remote calls require Cloudflare Access outer identity plus an inner bridge token. Anonymous principals and unauthenticated tunnel access are forbidden.
15. **Remote MCP audit.** Every accepted or rejected remote MCP call appends to `raw/remote-mcp-audit/YYYY-MM-DD.jsonl` with sequence, prev-hash, args HMAC, entry HMAC, and daily manifest. Chain or manifest failure disables the remote endpoint until operator trust is rebuilt.

### Remote MCP Bridge

Issue [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109) governs the Cloud -> Local MCP Bridge. The bridge may expose only a bounded remote subset of the local Society-of-Minds MCP daemon through authenticated HTTPS. It is operator-CLI infrastructure, not a SaaS surface.

**Transport and identity**

- Cloudflare Tunnel (`cloudflared`) is the only approved off-LAN transport.
- Cloudflare Access is mandatory. Requests without verified Access identity are rejected before bridge-token evaluation.
- The bridge also requires an inner bearer/JWT token with issuer, audience, subject, expiry, not-before, jti, kid, rotation version, and explicit tool scope.
- Token rotation bumps `rotation_version`; lower-version tokens are refused on the next validation.
- If `cloudflared` or the HTTP bridge is down, remote access fails closed. The local stdio MCP path continues without unauthenticated network fallback.

**Remote tool allowlist**

| Tool | Remote | Boundary |
|---|---:|---|
| `som.ping` | yes | Health only; no user payload. |
| `som.handoff` | yes | PII middleware scans all string fields; server stamps origin. |
| `som.chain` | yes | Packet-id lookups only; no free text. |
| `som.log_fallback` | yes | Structured fields only; PII middleware and rate limit apply. |
| `lam.probe` | yes | Runtime status only; no prompt payload. |
| `lam.embed` | yes | PII middleware, schema allowlist, size limit, and rate limit apply. |
| `lam.scrub_pii` | no | Stdio-only because it necessarily accepts PII-bearing input. |

**Application-layer controls**

- Remote dispatchers validate strict JSON schema per tool and reject unexpected fields.
- PII scanning uses the shared LAM PII pattern set before dispatch. Missing or malformed patterns reject all remote calls.
- Rate limits are keyed by stable principal (`sub`), not token material, and run before tool dispatch.
- HTTP transport overwrites `origin` after authentication. Client origin values are never authoritative.
- Error responses must not echo user payloads.

**Audit contract**

Remote MCP audit files live under `raw/remote-mcp-audit/`. Each JSONL entry contains `ts`, `seq`, `prev_hash`, `principal`, `session_jti`, `tool`, `args_hmac`, `status`, `reject_reason`, `latency_ms`, and `entry_hmac`. Daily manifests record first hash, last hash, entry count, and file SHA-256. `scripts/remote-mcp/verify_audit.py` and `.github/workflows/check-remote-mcp-audit-schema.yml` are the governance-owned verifier surfaces for this contract.

**Stage boundaries**

- Stage A (`hldpro-governance`): standards, runbook, thin client contract, audit verifier, CI workflow, local tests, validation, and closeout.
- Stage B+C (`local-ai-machine`): HTTP server, auth, PII middleware, rate limit, audit writer, launchd/tunnel scripts, and negative security tests.
- Stage D: remote smoke and security tests from a second machine.
- Issue #109 remains open until downstream implementation and remote e2e proof complete.

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

Validator rejects if: any required field missing, `drafter.model_family` == `reviewer.model_family`, `drafter.model_id` == `reviewer.model_id`, `reviewer.verdict` == `REJECTED`, any `invariants_checked` value is false, and for `schema_version: v2+`, `gate_identity` must be present with a distinct non-empty `model_id`.

### Enforcement index (CI-verifiable — no orphan rules)

| # | Intent | Enforcement | Halt on fail |
|---|---|---|---|
| 1 | Agent `model:` pin | `check-agent-model-pins.yml` parses frontmatter | PR blocked |
| 2 | Codex calls specify `-m` + reasoning | `check-codex-model-pins.yml` scans scripts/workflows | PR blocked |
| 3 | Cross-review artifact validates schema + invariants | `require-cross-review.yml` schema validator | PR blocked |
| 4 | No-self-approval (distinct identities) | `check-no-self-approval.yml` | PR blocked |
| 5 | Fallback auto-logged + schema-valid | `scripts/model-fallback-log.sh` + `check-fallback-log-schema.yml` | PR blocked if malformed |
| 6 | Fallback rate + Gemma-vs-Codex/Claude A/B agreement metrics | `overlord-sweep` weekly | Auto-issue on threshold |
| 7 | Arch on Haiku blocked | `check-arch-tier.yml` checks PR-scoped raw `raw/cross-review/` artifacts and rejects schema v2+ gates using Haiku | PR + closeout blocked |
| 8 | PII never leaves machine | `check-pii-routing.yml` + `require-lam-dual-signature.sh` | PR + closeout blocked |
| 9 | LAM family diversity | `check-lam-family-diversity.yml` reads `.lam-config.yml` | PR blocked |
| 10 | LAM availability for PII PRs | `check-lam-availability.yml` runtime probe | PR blocked |
| 11 | CLAUDE.md points to SoT | `check-claude-md-pointer.yml` | PR blocked |
| 12 | Exception register covers deferrals with expiry ≤ 90d | `overlord-sweep` validates; past-expiry auto-opens issue | Sweep issue on breach |
| 13 | Windows-Ollama remains off active SoM routing | `STANDARDS.md` + runtime inventory tests assert Windows is deprecated/off-ladder | PR blocked if active Worker fallback language returns |
| 14 | Local Qwen worker ladder present | `.lam-config.yml` + `scripts/lam/runtime_inventory.py` tests | PR blocked if Qwen2.5/Qwen3-14B/Qwen3.6 worker roles drift |
| 15 | Gemma shadow-only status | `.lam-config.yml` + `scripts/lam/runtime_inventory.py` tests | PR blocked if Gemma is promoted to authoritative reviewer without a new issue |
| 16 | Codex plan-review fallback floor | `check-codex-model-pins.yml` and cross-review schema | PR blocked if Codex calls omit `-m` or `model_reasoning_effort` |
| 17 | Worker/QA separation | PR template, execution scope, and no-self-approval checks | PR blocked when evidence collapses worker, reviewer, and gate identities |
| 18 | Remote MCP stdio-only boundary | `STANDARDS.md` allowlist + downstream `local-ai-machine` bridge tests; Stage A client exposes no `lam.scrub_pii` helper | PR blocked once downstream bridge lands |
| 19 | Remote MCP server-authoritative origin | Stage A client omits origin authority; downstream HTTP bridge must overwrite origin and test spoofed local origin | PR blocked once downstream bridge lands |
| 20 | Remote MCP PII middleware | `docs/runbooks/remote-mcp-bridge.md` + downstream PII middleware tests using shared patterns | PR blocked once downstream bridge lands |
| 21 | Remote MCP Access identity | `docs/runbooks/remote-mcp-bridge.md` requires Cloudflare Access + inner token; downstream auth tests must reject anonymous calls | PR blocked once downstream bridge lands |
| 22 | Remote MCP audit validation | `scripts/remote-mcp/verify_audit.py` + `check-remote-mcp-audit-schema.yml` validate hash chain, HMAC, and daily manifest | PR blocked if malformed |

### Exception register schema

`hldpro-governance/docs/exception-register.md` entries require:
- `rule_id` (e.g., `SOM-PII-001`)
- `repo` (repo where exception applies)
- `deferral_reason` (cites missing artifact or repo-specific blocker)
- `approver` (human, named)
- `expiry_date` (max 90 days from entry)
- `review_cadence` (monthly minimum)

Overlord-sweep auto-opens issues for past-expiry entries.

### Gemma A/B shadow protocol

Gemma is being measured against Codex/Claude QA before any authority decision:
- Gemma runs in **shadow (A/B)** mode only.
- Authoritative QA remains Codex or Claude per the approved waterfall.
- Verdicts are logged to `raw/ab-review/YYYY-MM-DD-{slug}.md` with `agreement: match | gemma_only_findings | cloud_only_findings | both | conflict`.
- Conservative gate: cloud QA and deterministic gates win every conflict.
- Overlord-sweep reports weekly Gemma agreement/usefulness rates. Promotion requires a separate issue, explicit acceptance criteria, and updated enforcement.

## Windows Host Inference (deprecated / off-ladder)

A LAN-resident Ollama-served Windows workstation was previously evaluated as a
Tier-2 fallback. As of issue #432, Windows Ollama is **not** an active
governance waterfall fallback. Existing scripts, audit verifiers, and runbooks
remain historical/deprecated surfaces until a separate issue removes or
repurposes them.

### Endpoint

- URL: `http://172.17.227.49:11434` (LAN-only, vEthernet adapter `sase-switch`)
- API: Ollama `/api/generate` (OpenAI-compatible `/v1/` available)
- Pinned operating settings (proven in LAM #68): `keep_alive=15m`, `num_ctx<=4096`, adaptive offload ladder `99 -> 80 -> 60`, call timeout 45000ms

### Pinned model roster

Treat the runbook (`docs/runbooks/windows-ollama-worker.md`) as a historical
inventory reference, not an active routing source. Deprecated roster:

| Model | Role | VRAM (~Q4) |
|---|---|---|
| `qwen2.5-coder:7b` | Deprecated Windows worker experiment | ~5 GB |
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
- Windows host metrics / health check workflow and direct hardware telemetry capture

## Exceptions
- ASC-Evaluator: knowledge repo, exempt from code governance
- Repos may have ADDITIONAL governance beyond this baseline
- HIPAA agents must never be weakened or consolidated away
- Codex subagents/personas may stand in for repo-required Claude agents only when they preserve the same separation of duties and approval boundaries
- Bootstrap exception (`SOM-BOOTSTRAP-001`): the PR introducing the Society of Minds standard cannot self-enforce `require-cross-review.yml` since the workflow is being added in the same PR. Tier 1 cross-review was completed out-of-band via `raw/cross-review/2026-04-14-society-of-minds-charter.md`. Expires on merge of this PR.
