# GitHub Enterprise Ruleset Recommendations

Prepared: 2026-04-09
Purpose: Convert the verified required-check baseline into an actionable org-admin rollout sequence without hiding current-state drift.

Canonical inputs:
- `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`
- `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`
- `GITHUB_ENTERPRISE_SPRINT1_TASKS.md`

## Current State Snapshot

Org rulesets currently active:
- `14715976` `Protect main branches`
- `14716006` `Protect develop branches`

Current org protections in effect:
- block deletion on `main` and `develop`
- block non-fast-forward pushes on `main` and `develop`
- require pull request on `main`
- no approving-review requirement at the org level yet
- no code-owner review requirement at the org level yet
- no org-level required status checks yet

Observed repo-level overrides:
- `hldpro-governance`: repo ruleset `15241047` `Require Local CI Gate on main` requires `local-ci-gate` on `refs/heads/main`
- `ai-integration-services`: repo ruleset `14283171` `MAIN` adds required checks on `main`, but is missing `critical-tests` from the verified baseline
- `local-ai-machine`: repo ruleset `13152679` `Main branch PR-only policy` requires PR flow and review-thread resolution on `main`, but does not yet encode the standard-code baseline checks
- `HealthcarePlatform`: no repo-level ruleset beyond inherited org rules
- `knocktracker`: no repo-level ruleset beyond inherited org rules

Sprint 1 repo ownership status:
- `ai-integration-services`: `.github/CODEOWNERS` present on `main`
- `HealthcarePlatform`: `.github/CODEOWNERS` merged on `main`
- `knocktracker`: `.github/CODEOWNERS` merged on `main`
- `local-ai-machine`: `.github/CODEOWNERS` merged on `main`
- `ASC-Evaluator`: exempt from first-pass code-governance enforcement

## Rollout Principle

Do not tighten org rulesets until all of the following are true:

1. exact status-check names are verified from live PR data
2. actor-conditional and path-conditional checks are explicitly excluded or tracked as exceptions
3. target repos have committed `CODEOWNERS` where code-owner review is desired
4. repo owners have been notified of enforcement scope and date

## Target Ruleset Structure

Use layered rulesets:

1. Global branch safety baseline
2. Production-critical merge policy
3. Standard-code merge policy
4. Repo-specific overlays only where live behavior demands them

## Stage 0 — Preflight Validation

Before any GitHub UI change:

1. confirm `CODEOWNERS` is merged on the target repo default branch
2. confirm workflow names still match `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`
3. confirm no skipped context is being promoted into a required check
4. confirm any planned deviation is captured in `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`
5. confirm repo owner has acknowledged the staged change window

## Stage 1 — Keep Global Branch Safety, Do Not Expand Yet

Current org rulesets already satisfy this stage:
- PR-only requirement on `main`
- deletion/non-fast-forward protection on `main`
- deletion/non-fast-forward protection on `develop`

No immediate admin change required here.

## Stage 2 — Normalize Repo-Level Drift Before Broader Enforcement

### hldpro-governance

Current state:
- repo-level `Require Local CI Gate on main` ruleset exists
- required check is:
  - `local-ci-gate`
- strict required status checks are enabled

Recommended action:
- keep this repo-specific hardgate in place
- do not promote `local-ci-gate` into a broad org-level required check for repos that do not yet run the governance-owned Local CI Gate workflow

### ai-integration-services

Current drift:
- repo-level `MAIN` ruleset exists
- required checks are:
  - `governance-check / governance-check`
  - `gitleaks`
  - `npm-audit`
  - `typecheck`
- missing:
  - `critical-tests`

Recommended action:
- update the repo-level ruleset to include `critical-tests`, or remove the repo-level ruleset once the org-level production-critical ruleset is ready to replace it

### local-ai-machine

Current drift:
- repo-level `Main branch PR-only policy` exists
- no required checks yet in that repo-level ruleset
- stricter repo workflow contracts still exist for `riskfix/*` lanes

Recommended action:
- keep the repo-level PR-only policy in place for now
- do not fold repo-specific `riskfix/*` contracts into the org baseline
- add the standard-code required checks in a later admin pass only after this repo policy is explicitly accepted

## Stage 3 — Apply Production-Critical Required Checks

Target repos:
- `ai-integration-services`
- `HealthcarePlatform`
- `knocktracker`

### ai-integration-services

Required checks:
- `critical-tests`
- `gitleaks`
- `governance-check / governance-check`
- `npm-audit`
- `typecheck`

### HealthcarePlatform

Required now:
- `actionlint`
- `build`
- `check-migration-order`
- `gitleaks`
- `lint`
- `npm-audit`
- `require-sprint-status-update`
- `schema-dictionary-check`
- `typecheck`
- `unit-tests`

Keep conditional for now:
- `governance-check / governance-check`
- `playwright-gate`

### knocktracker

Required now:
- `actionlint`
- `gitleaks`
- `npm-audit`
- `require-sprint-status-update`
- `validate`
- `validate-pr`

Keep conditional for now:
- `governance-check`

## Stage 4 — Apply Standard-Code Baseline

Target repo:
- `local-ai-machine`

Required now:
- `actionlint`
- `gitleaks`
- `npm-audit`

Keep out of the first org pass:
- `breaker-mcp-contract`
- `airlock-idempotency`
- `contract-check`
- `governance-check`
- `lint-warning-mode`
- `post-closeout`
- `reconcile-control-plane`
- `SASE Gatekeeper`

Reason:
- these are repo-policy, actor-conditional, or path-conditional today

## Stage 5 — Code-Owner Review Enforcement

Do not enable `require_code_owner_review` globally until:
- the repo has a merged `.github/CODEOWNERS`
- owners agree the first-pass coverage is narrow enough
- no repo still needs ownership-map cleanup for obvious hot paths

Recommended order:
1. `ai-integration-services`
2. `HealthcarePlatform`
3. `knocktracker`
4. `local-ai-machine`

## Exception Handling

Every non-baseline rule deferral must be logged in `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`.

Current rollout-critical exceptions already tracked there:
- `ASC-Evaluator` repo exemption
- actor-conditional HealthcarePlatform checks
- actor-conditional knocktracker governance-check
- local-ai-machine repo-level override / standard-code deferral

## Owner Communication Template

Use this notice before any admin change:

```markdown
Subject: GitHub governance rollout for <repo>

Scope:
- repo: <repo>
- branch target: <main|develop>
- planned change date: <YYYY-MM-DD>

Changes:
- <ruleset or required-check update>
- <code-owner review change if applicable>

No-change items:
- no workflow file edits
- no branch rename
- no deploy/secrets changes

Rollback:
- revert the affected ruleset entry in GitHub UI/API
- document the rollback reason in `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md` if the rollback will persist
```

## Rollback Guidance

If a rollout causes merge deadlock:

1. remove or disable the newly added required check from the repo/org ruleset
2. capture the reason as an exception if the rollback will remain in place
3. link the rollback decision to the relevant governance issue
4. reschedule enforcement only after the underlying workflow behavior is fixed

## Definition of Done For This Planning Slice

This rollout pack is complete when:
- the current org and repo ruleset state is documented accurately
- the staged apply order is explicit
- the owner communication template exists
- all known non-baseline deviations are represented in the exception register
