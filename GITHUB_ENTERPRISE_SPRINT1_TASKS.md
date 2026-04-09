# GitHub Enterprise Sprint 1 Tasks

Prepared: 2026-04-09
Scope: Branch-governance baseline for first-wave repos
Canonical parent docs:
- `OVERLORD_BACKLOG.md`
- `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`
- `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`

## Sprint 1 Outcomes

1. Ensure first-wave repos have committed `.github/CODEOWNERS`.
2. Confirm current required-check names before any org ruleset change.
3. Keep actor-conditional and path-conditional checks out of the first enforcement pass.
4. Establish the exception path before tighter rulesets.

## Current Inventory

### CODEOWNERS Status

- `ai-integration-services`: merged on default branch
- `HealthcarePlatform`: merged on default branch
- `knocktracker`: merged on default branch
- `local-ai-machine`: merged on default branch
- `ASC-Evaluator`: exempt from Sprint 1 repo enforcement

### Execution Notes

- Sprint 1 repo ownership rollout is complete for the first-wave governed repos.
- Default-branch inspection remains the source of truth; stale draft lanes are not governance truth once default-branch state is verified.
- `local-ai-machine` governance-only lanes now use the repo's `riskfix/*` branch family when repo policy requires it.
- Live required-check verification is recorded in `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`.

## Repo Task Breakdown

## ai-integration-services

Status:
- complete for Sprint 1 CODEOWNERS

Notes:
- `.github/CODEOWNERS` already exists on `main`

## HealthcarePlatform

Status:
- complete

Target ownership areas:
- `.github/`
- `backend/`
- `frontend/`
- `scripts/`
- governance/security docs

Acceptance Criteria:
- `.github/CODEOWNERS` exists on `main`
- ownership covers workflows, backend, frontend, docs, and scripts
- no ruleset or branch-protection changes are mixed into the same repo lane

## knocktracker

Status:
- complete

Target ownership areas:
- `.github/`
- `app/`
- `src/`
- `components/`
- `contexts/`
- `hooks/`
- `lib/`
- `supabase/`
- `tests/`
- `scripts/`
- governance docs

Acceptance Criteria:
- `.github/CODEOWNERS` exists on `main`
- repo lane contains minimal ownership changes only
- no ruleset or workflow behavior changes are mixed into the same repo lane

## local-ai-machine

Status:
- complete

Target ownership areas:
- `.github/`
- `scripts/`
- `src/`
- `runtime/`
- `integrations/`
- `supabase/`
- `tests/`
- `clients/`
- `tools/`
- governance docs

Acceptance Criteria:
- `.github/CODEOWNERS` exists on `main`
- repo lane uses the repo's accepted branch-family/workflow policy
- no ruleset or workflow behavior changes are mixed into the same repo lane

## Governance Repo Tasks

1. Keep this task file aligned to the real default-branch state, not old draft PR assumptions.
2. Keep the required-check baseline and ruleset recommendation docs in sync with repo rollout truth.
3. Route any repo-specific blockers into repo issues/PRs rather than hiding them inside governance-only notes.

## Follow-On Sequencing

1. Reconfirm default-branch coverage when rulesets or ownership maps change materially.
2. Use the merged Sprint 1 state as the gate for future ruleset tightening.
3. Track future enforcement changes through issue-backed rollout slices instead of reopening Sprint 1.
