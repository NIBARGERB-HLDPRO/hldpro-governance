# GitHub Enterprise Exception Register

Prepared: 2026-04-09
Owner: Governance / Platform
Canonical policy:
- `GITHUB_ENTERPRISE_ADOPTION_PLAN.md`
- `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md`

## Purpose

Track approved GitHub governance exceptions in one place, with real owners and a real monthly review cadence.

## Operating Rules

- Every exception must have an owner.
- Every exception must have an approver.
- Every exception must have a review or expiry date.
- Expired exceptions must be closed or renewed explicitly.
- Open exceptions are reviewed in the monthly GitHub governance review.

## Approval Authority

- Platform approves workflow, branch-policy, required-check, and codeowners exceptions.
- Security approves security-control suppressions or deferrals.
- Engineering leadership approves any production-risk exception lasting longer than 30 days.

Current solo-operator mapping:
- Platform approver: `nibargerb`
- Security approver: `nibargerb`
- Engineering leadership approver: `nibargerb`

## Review Cadence

- cadence: monthly
- standing window: first Monday of each month
- timezone: America/Chicago
- required outputs:
  - close, renew, or re-date every open exception
  - assign owners and due dates for unresolved drift
  - link any continued exception to a live issue or decision record

## Exception Log

| ID | Repo | Policy Area | Exception Summary | Owner | Approver | Opened | Review/Expiry | Status | Mitigation | Decision Ref |
|----|------|-------------|-------------------|-------|----------|--------|---------------|--------|------------|--------------|
| EX-2026-01 | ASC-Evaluator | required-checks | Exempt from first-pass CODEOWNERS and required-check enforcement because the repo is knowledge-exempt and low-risk relative to production code repos | nibargerb | nibargerb | 2026-04-09 | 2026-05-04 | approved | Keep only the org branch-safety baseline; do not apply code-governance rules until the repo classification changes | `GITHUB_ENTERPRISE_RULESET_RECOMMENDATIONS.md` |
| EX-2026-02 | HealthcarePlatform | required-checks | Keep `governance-check / governance-check` and `playwright-gate` out of the first org required-check pass because both are actor-conditional today | nibargerb | nibargerb | 2026-04-09 | 2026-05-04 | approved | Use the verified stable baseline only; revisit after workflow-policy cleanup and stable CI evidence | Issue [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40) |
| EX-2026-03 | knocktracker | required-checks | Keep `governance-check` out of the first org required-check pass because it intentionally skips Dependabot PRs today | nibargerb | nibargerb | 2026-04-09 | 2026-05-04 | approved | Require only the stable validated checks until bot-policy behavior changes | Issue [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40) |
| EX-2026-04 | local-ai-machine | required-checks | Keep repo-specific `riskfix/*` and specialized checks out of the first org baseline; maintain repo-level PR-only override separately | nibargerb | nibargerb | 2026-04-09 | 2026-05-04 | approved | Apply only the standard-code baseline checks at org level when ready; keep repo-specific workflow contracts local | Issues [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40), [#42](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/42) |
| EX-2026-05 | ai-integration-services | required-checks | Temporary repo-level ruleset drift: current `MAIN` ruleset omits `critical-tests` from the verified production-critical baseline | nibargerb | nibargerb | 2026-04-09 | 2026-05-04 | proposed | Update or replace the repo-level ruleset before broader org enforcement so AIS matches the canonical baseline | Issue [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40) |

## Policy Area Values

- `branch-protection`
- `required-checks`
- `codeowners`
- `actions-policy`
- `sha-pinning`
- `security-configuration`
- `code-scanning`
- `secret-scanning`
- `environment-protection`
- `other`

## Status Values

- `proposed`
- `approved`
- `expired`
- `closed`

## Entry Template

| ID | Repo | Policy Area | Exception Summary | Owner | Approver | Opened | Review/Expiry | Status | Mitigation | Decision Ref |
|----|------|-------------|-------------------|-------|----------|--------|---------------|--------|------------|--------------|
| EX-YYYY-NN | repo-name | required-checks | Short description of the exception | team/person | team/person | YYYY-MM-DD | YYYY-MM-DD | proposed | Temporary mitigation while exception remains open | Link to decision log or issue |
