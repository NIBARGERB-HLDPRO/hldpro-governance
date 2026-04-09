# GitHub Enterprise Adoption Plan

Prepared: 2026-04-09
Status: Closed planning slice; future enforcement changes proceed through issue-backed follow-on work and monthly exception review.
Owner: Governance / Platform

Canonical companions:
- `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`
- `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`
- `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`
- `GITHUB_ENTERPRISE_SPRINT1_TASKS.md`
- `OVERLORD_BACKLOG.md`

## Purpose

Provide the current source-of-truth rollout plan for GitHub Enterprise governance across the org, using verified live ruleset state instead of draft assumptions.

## Current State

Org rulesets currently active:
- `14715976` `Protect main branches`
- `14716006` `Protect develop branches`

Repo-level ruleset drift currently present:
- `ai-integration-services`: repo ruleset `14283171` `MAIN`
- `local-ai-machine`: repo ruleset `13152679` `Main branch PR-only policy`
- `HealthcarePlatform`: no repo-specific ruleset beyond inherited org rules
- `knocktracker`: no repo-specific ruleset beyond inherited org rules
- `ASC-Evaluator`: exempt from first-pass code-governance enforcement

Sprint 1 ownership baseline:
- `ai-integration-services`: complete
- `HealthcarePlatform`: complete
- `knocktracker`: complete
- `local-ai-machine`: complete
- `ASC-Evaluator`: exempt

Verified planning pack status:
- required-check baseline is complete and grounded in live PR/workflow evidence
- staged ruleset rollout guidance is complete and current
- exception register is seeded with live deviations and review dates
- Sprint 1 repo ownership rollout is complete

## Adoption Plan Outcome

The GitHub Enterprise planning/adoption slice is complete when:

1. baseline checks are documented from live PR evidence
2. staged rollout guidance exists for org and repo rulesets
3. exceptions are registered with owners, approvers, and review dates
4. Sprint 1 ownership prerequisites are complete or explicitly exempted
5. remaining admin changes are handled as issue-backed follow-on work instead of a permanently open umbrella plan

That condition is now met.

## Remaining Operational Follow-On Work

These are not blockers for closing the adoption-plan slice itself:

1. continue monthly exception review from `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`
2. normalize `ai-integration-services` repo ruleset drift called out in `EX-2026-05`
3. apply future ruleset tightening only through issue-backed rollout slices using the verified baseline and exception register

## Operating Rules

1. Do not reopen a generic enterprise-adoption umbrella issue for routine admin changes.
2. Any new enforcement change must reference:
   - `GITHUB_ENTERPRISE_REQUIRED_CHECK_BASELINE.md`
   - `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`
   - `GITHUB_ENTERPRISE_EXCEPTION_REGISTER.md`
3. If live GitHub state drifts from this pack, open or update a specific issue and reflect the change in `OVERLORD_BACKLOG.md`.
