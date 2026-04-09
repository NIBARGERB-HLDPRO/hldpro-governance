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
- `HealthcarePlatform`: missing on `main`; tracked by issue `#737`
- `knocktracker`: missing on `main`; dormant draft PR `#143` exists from issue `#142`
- `local-ai-machine`: missing on `main`; dormant draft PR `#375` exists from issue `#374`
- `ASC-Evaluator`: exempt from Sprint 1 repo enforcement

### Execution Notes

- `ai-integration-services` no longer needs Sprint 1 repo work.
- `HealthcarePlatform` had no repo issue or lane at all before this refresh; the older governance assumption that CODEOWNERS had already landed there was stale.
- `knocktracker` and `local-ai-machine` both have older draft lanes, but default-branch inspection remains the source of truth until `.github/CODEOWNERS` is merged.
- `local-ai-machine` now expects governance-only lanes to use a `riskfix/*` branch family, so the old `lane/*` CODEOWNERS PR is not the clean final merge path.
- Live required-check verification is recorded in `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`.

## Repo Task Breakdown

## ai-integration-services

Status:
- complete for Sprint 1 CODEOWNERS

Notes:
- `.github/CODEOWNERS` already exists on `main`

## HealthcarePlatform

Status:
- active rollout required

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
- active rollout required

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
- active rollout required

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

1. Merge remaining first-wave repo CODEOWNERS lanes.
2. Reconfirm default-branch coverage.
3. Use that merged state as the gate for `#40` staged ruleset rollout.
