# GitHub Enterprise Ruleset Recommendations

Prepared: 2026-04-09
Purpose: Translate the verified required-check baseline into staged org-ruleset recommendations without applying any GitHub settings yet.

Canonical inputs:
- `OVERLORD_BACKLOG.md`
- `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`

## Rollout Principle

Do not tighten org rulesets until all of the following are true:

1. exact status-check names are verified from live PR data
2. actor-conditional and path-conditional checks are explicitly excluded or reworked
3. target repos have merged `CODEOWNERS` where code-owner enforcement is desired
4. repo owners have been notified of the enforcement date

## Recommended Ruleset Structure

Use layered rulesets rather than one giant org-wide rule:

1. Global branch safety baseline
2. Production-critical merge policy
3. Standard-code merge policy
4. Repo-specific overlays only where required

## Ruleset 1: Global Branch Safety Baseline

Target:
- all non-exempt repositories
- branches: `main`, `develop`

Recommended protections:
- block force pushes
- block branch deletion
- require pull request before merge
- require conversation resolution before merge

Do not require status checks in this baseline.

Purpose:
- establish universal branch safety without breaking repos that still carry conditional check behavior

## Ruleset 2: Production-Critical Merge Policy

Target repos:
- `ai-integration-services`
- `HealthcarePlatform`
- `knocktracker`

Recommended protections:
- require pull request before merge
- require at least 1 approving review
- require code-owner review once `CODEOWNERS` is merged
- require only the stable baseline checks from `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`

### Recommended Required Checks by Repo

#### ai-integration-services

- `critical-tests`
- `gitleaks`
- `governance-check / governance-check`
- `npm-audit`
- `typecheck`

#### HealthcarePlatform

Require now:
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

Do not require yet:
- `governance-check / governance-check`
- `playwright-gate`

Reason:
- both are intentionally actor-conditional today

#### knocktracker

Require now:
- `actionlint`
- `gitleaks`
- `npm-audit`
- `require-sprint-status-update`
- `validate`
- `validate-pr`

Do not require yet:
- `governance-check`

Reason:
- it intentionally skips Dependabot PRs today

## Ruleset 3: Standard-Code Merge Policy

Target repos:
- `local-ai-machine`

Recommended protections:
- require pull request before merge
- require at least 1 approving review
- require code-owner review once `CODEOWNERS` is merged
- require only stable always-on checks in the first pass

Require now:
- `actionlint`
- `gitleaks`
- `npm-audit`

Do not require yet:
- `breaker-mcp-contract`
- `airlock-idempotency`
- `contract-check`
- `governance-check`
- `lint-warning-mode`
- `post-closeout`
- `reconcile-control-plane`
- `SASE Gatekeeper`

Reason:
- these checks are branch-policy, actor-conditional, or path-conditional today

## Repo Exemption Handling

### ASC-Evaluator

Recommended treatment:
- exempt from required-check and code-owner enforcement
- branch safety rules may still be applied if desired, but no code-governance baseline is necessary

## Pre-Apply Checklist

Before an admin touches the GitHub UI:

1. confirm target repo has merged `CODEOWNERS` if code-owner review is being enabled
2. confirm current workflow names still match the baseline document
3. confirm no skipped contexts are being marked required
4. confirm repo owner has acknowledged the enforcement date
5. confirm open PRs will not be surprised by an immediate policy flip

## Staged Application Order

1. Apply Global Branch Safety Baseline only
2. Apply `ai-integration-services` required checks
3. Apply `HealthcarePlatform` stable checks only
4. Apply `knocktracker` stable checks only
5. Apply `local-ai-machine` stable checks only
6. Revisit actor-conditional and path-conditional checks after workflow-policy cleanup

## Review Gates Before Promotion of Conditional Checks

Promote a conditional check only when all are true:

- it runs for the relevant common PR class consistently
- it is not skipped for legitimate bot or maintenance PRs unless a separate bot policy exists
- it has acceptable flake rate
- it materially protects merge quality

## Known Risks

- requiring skipped checks can deadlock merges
- branch-family contract checks can block bot PRs even when code quality is otherwise acceptable
- tightening rules mid-PR can surprise active branches

## Mitigations

- only require stable live contexts
- keep first enforcement pass conservative
- announce the change before applying it
- re-verify check names immediately before applying the ruleset
