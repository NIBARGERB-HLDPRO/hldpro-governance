# GitHub Enterprise Required Check Baseline

Prepared: 2026-04-09
Purpose: Record live status-check behavior on first-wave governed repos so rulesets use exact stable contexts instead of stale assumptions or workflow filenames.

Canonical companions:
- `OVERLORD_BACKLOG.md`
- `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`

## Verification Method

Sources:
- `gh pr checks <number> -R <owner>/<repo>`
- direct inspection of repo-local `.github/workflows/`

Verification date:
- 2026-04-09

Policy rule used for this pass:
- `Required now` means stable on common human-authored PRs and not intentionally actor- or path-conditional.
- `Conditional` means intentionally skipped for a meaningful PR class and therefore not safe as an org-wide required check yet.
- `Repo-policy only` means a repo-specific contract that may be valuable locally but should not be promoted into the first org baseline.

## Verified Live Check Contexts

## ai-integration-services

PR sampled:
- `#808` to `main`

Observed checks:
- `critical-tests`
- `gitleaks`
- `governance-check / governance-check`
- `npm-audit`
- `typecheck`

Required now:
- `critical-tests`
- `gitleaks`
- `governance-check / governance-check`
- `npm-audit`
- `typecheck`

Notes:
- Governance-check is always on for PRs in this repo, so it remains baseline-safe.

## HealthcarePlatform

PRs sampled:
- `#734` to `develop`
- `#718` to `main`

Observed stable checks:
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

Observed conditional checks:
- `governance-check / governance-check`
- `playwright-gate`

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

Conditional:
- `governance-check / governance-check`
- `playwright-gate`

Notes:
- `build` is no longer pending. It is always on in `ci-core.yml` and is safe for the baseline.
- `playwright-gate` is intentionally skipped for Dependabot because it requires smoke-auth secrets.
- `governance-check` is also actor-conditional in this repo, so it should not be org-required until bot policy or workflow behavior changes.

## knocktracker

PRs sampled:
- `#144` to `main`
- `#141` to `main`

Observed stable checks:
- `actionlint`
- `gitleaks`
- `npm-audit`
- `require-sprint-status-update`
- `validate`
- `validate-pr`

Observed conditional checks:
- `governance-check`

Required now:
- `actionlint`
- `gitleaks`
- `npm-audit`
- `require-sprint-status-update`
- `validate`
- `validate-pr`

Conditional:
- `governance-check`

Notes:
- The earlier skip-behavior question is resolved. `governance-check` intentionally skips `dependabot[bot]` PRs in `.github/workflows/governance.yml`.
- Do not require `governance-check` in org rulesets until the repo either stops skipping bot PRs or adopts a separate bot-safe enforcement policy.

## local-ai-machine

PRs sampled:
- `#378` to `main`
- `#372` to `main`

Observed stable checks:
- `actionlint`
- `gitleaks`
- `npm-audit`

Observed repo-policy or specialized checks:
- `breaker-mcp-contract`

Observed conditional checks:
- `airlock-idempotency`
- `contract-check`
- `governance-check`
- `lint-warning-mode`
- `post-closeout`
- `reconcile-control-plane`
- `SASE Gatekeeper`

Required now:
- `actionlint`
- `gitleaks`
- `npm-audit`

Repo-policy only:
- `breaker-mcp-contract`

Conditional:
- `airlock-idempotency`
- `contract-check`
- `governance-check`
- `lint-warning-mode`
- `post-closeout`
- `reconcile-control-plane`
- `SASE Gatekeeper`

Notes:
- The specialized-check question is resolved. `breaker-mcp-contract` is not a safe org baseline check because it enforces the repo's `riskfix/*` branch-family contract and fails on common bot PRs.
- `airlock-idempotency` and `lint-warning-mode` are path-triggered and should stay conditional overlays.
- `governance-check` is actor-conditional for Dependabot here as well.

## Ruleset Guidance

1. Only use exact live status-check names in org rulesets.
2. Do not require checks that intentionally skip for Dependabot or other common PR classes.
3. Treat path-triggered and lane-policy checks as repo overlays, not org baseline checks.
4. Re-verify check names and skip semantics any time a workflow or job is renamed.

## Resolved Follow-Up Decisions

1. knocktracker `governance-check` remains conditional because the skip behavior is intentional.
2. local-ai-machine specialized checks remain repo-specific or conditional and should not be part of the first org baseline.
3. HealthcarePlatform `build` is baseline-safe now; `playwright-gate` remains conditional.
