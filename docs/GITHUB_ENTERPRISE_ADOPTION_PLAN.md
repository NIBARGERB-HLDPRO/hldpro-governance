# GitHub Enterprise Adoption Plan

Prepared: 2026-04-07
Owner: Governance / Platform
Scope: Org-wide GitHub Enterprise rollout for HLD Pro repositories

## Purpose

Use GitHub Enterprise as an enforced governance, security, and delivery control plane across HLD Pro repos, not just as upgraded hosting with extra toggles enabled.

This plan lives in `hldpro-governance` because the majority of the work is org-wide:

- rulesets
- security baselines
- reusable workflows
- actions policy
- audit logging
- repo metadata taxonomy
- exception handling

Product repos should only carry repo-local implementation details such as `CODEOWNERS`, repo-specific workflow changes, and documented exceptions.

## Current State

### Already in place

- Secret scanning
- Push protection
- Dependabot alerts
- Dependabot security updates
- Dependency graph
- Org rulesets protecting `main` and `develop`

These were captured in [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/hldpro-governance/STANDARDS.md).

### Gaps still to close

- No `CODEOWNERS` baseline across first-wave repos
- No documented org-wide required-check baseline
- No visible repo settings-as-code baseline
- No documented GHAS rollout plan by repo class
- No org-level actions allowlist and SHA-pinning program
- No audit log streaming integration documented here
- No custom repository property taxonomy
- No operating cadence for reviewing GitHub governance posture

## Goals

1. Prevent unsafe merges to protected branches.
2. Standardize code security controls across production repos.
3. Reduce GitHub Actions supply-chain risk.
4. Improve auditability for vendor diligence, incident response, and compliance work.
5. Keep repo-specific deviation small and explicit.

## Program Success Criteria

The program is considered successful when all of the following are true:

- 100% of first-wave repos have committed `CODEOWNERS` and enforced protected-branch review requirements.
- 100% of active non-exempt code repos are covered by baseline rulesets.
- 100% of first-wave repos are attached to an approved security baseline within 60 days of Sprint 2 completion.
- 100% of active repos have an assigned `owner_team` repository property.
- Critical security findings have a named owner and are triaged within 1 business day.
- No production deploy is blocked for more than 1 business day due to missing break-glass or exception handling.
- Exceptions and suppressions have an owner, rationale, expiry/review date, and monthly review coverage.

## Non-Goals

- Rebuilding existing CI from scratch
- Forcing every feature into one sprint
- Adopting EMU unless the org has a real identity-lifecycle need

## Repo Classes

### First-Wave Repos

- `ai-integration-services`
- `HealthcarePlatform`
- `knocktracker`
- `local-ai-machine`

### Exempt / Different Treatment

- `ASC-Evaluator`
  - knowledge repo
  - exempt from most code-governance requirements

## Required-Check Classes

These classes determine the minimum blocking checks for protected branches:

- `production-critical`
  - customer-facing, deployable, or integration-heavy repos
- `standard-code`
  - active internal code repos without direct production blast radius
- `knowledge-exempt`
  - documentation or evaluation repos exempt from most code governance

Initial mapping:

- `ai-integration-services` -> `production-critical`
- `HealthcarePlatform` -> `production-critical`
- `knocktracker` -> `production-critical`
- `local-ai-machine` -> `standard-code`
- `ASC-Evaluator` -> `knowledge-exempt`

## Workstreams

### 1. Branch and Merge Governance

- rulesets
- required checks
- code owner review
- merge queue decision

### 2. Code Security

- GHAS licensing confirmation
- security configuration baseline
- code scanning / CodeQL
- dependency review and alert ownership

### 3. Actions Security

- actions inventory
- approved source policy
- SHA pinning
- reusable workflow centralization
- environment protections
- artifact attestation decision

### 4. Audit and Reporting

- audit log streaming
- custom repository properties
- monthly governance review
- KPI tracking

## Sprint Plan

## Sprint 1: Branch Governance Baseline

Duration: 2 weeks
Priority: Highest

### Objectives

- Make branch protection enforceable and reviewable across first-wave repos.
- Introduce clear ownership for sensitive paths.

### Scope

1. Add `CODEOWNERS` to first-wave repos.
2. Define required-check baseline by repo tier.
3. Review org rulesets for `main` and `develop`.
4. Require code-owner review on critical paths where appropriate.
5. Validate push protection and secret scanning on one controlled test.
6. Define exception process for governance and security policy deviations.
7. Publish sprint communication plan for affected repo owners before enforcement begins.

### Deliverables

- `CODEOWNERS` PRs for first-wave repos
- required-check matrix by required-check class and repo
- branch governance runbook
- push protection validation record
- exception register template
- Sprint 1 communication notice and enforcement date

### Acceptance Criteria

- each first-wave repo has a committed `CODEOWNERS`
- `main` blocks direct pushes on all non-exempt code repos
- required checks are written down and reflect actual workflow names
- at least one protected-repo test confirms push protection behavior
- exception process exists with owner, storage location, approval authority, and review cadence
- repo owners receive notice of enforcement scope and start date before rules tighten

### Risks

- code owner coverage is too broad and slows reviews
- flaky checks become blocking without cleanup

### Mitigations

- start with critical path ownership only
- exclude known flaky checks from blocking status until stabilized

## Sprint 2: Advanced Security Rollout

Duration: 2 weeks
Priority: High

### Objectives

- Move from mixed custom controls to a platform-native code security baseline.

### Scope

1. Confirm GHAS licensing and active entitlement.
2. Create shared security configuration for production repos.
3. Enable code scanning / CodeQL on supported first-wave repos.
4. Standardize dependency review on PRs.
5. Define triage ownership and severity SLA.
6. Build actions inventory for active repos as a prerequisite for Sprint 3 enforcement.
7. Publish sprint communication plan for changes to security workflows and alert handling.

### Deliverables

- GHAS entitlement decision record
- security baseline configuration
- first-wave repo rollout tracker
- alert triage playbook
- actions inventory for active repos
- Sprint 2 communication notice and enforcement date

### Acceptance Criteria

- first-wave repos are mapped to a baseline security configuration
- supported repos show code scanning results in GitHub
- dependency review runs on dependency-changing PRs
- severity SLA exists for critical/high/medium findings
- actions inventory exists and identifies third-party actions needing approval or pinning before Sprint 3
- repo owners receive notice of workflow-impacting changes before enforcement begins

### Risks

- code scanning produces initial noise
- unsupported stacks need exception handling

### Mitigations

- phase rollout by repo class
- document suppressions and exceptions with owner and review date

## Sprint 3: Actions Hardening

Duration: 2 weeks
Priority: High

### Objectives

- Reduce workflow supply-chain risk and centralize trusted automation.
- Enforce action policy only after Sprint 2 action inventory is complete.

### Scope

1. Use the Sprint 2 actions inventory to classify all third-party action usage in active repos.
2. Define approved action sources.
3. Require commit SHA pinning where practical.
4. Centralize reusable workflows in governance-owned repos.
5. Review production environment protections.
6. Add break-glass procedure for policy-caused deployment blockage.
7. Decide on artifact attestation rollout.
8. Publish sprint communication plan before policy enforcement.

### Deliverables

- action inventory
- approved-actions policy
- pinning exception register
- reusable workflow ownership map
- environment protection review
- break-glass runbook
- Sprint 3 communication notice and enforcement date

### Acceptance Criteria

- all active repos are inventoried for action usage
- non-approved actions are removed or exception-documented
- external actions are pinned or tracked for remediation
- production deploy environments are reviewed and protected where needed
- break-glass runbook exists, identifies approvers, and is tested on a non-production scenario before hard enforcement
- repo owners receive notice of action restrictions before enforcement begins

### Risks

- action restrictions can break existing pipelines
- pinning requires cleanup effort

### Mitigations

- run audit first, enforce second
- define break-glass process for production incidents

## Sprint 4: Audit, Metadata, and Operating Rhythm

Duration: 2 weeks
Priority: Medium

### Objectives

- Make GitHub governance observable and sustainable.

### Scope

1. Stream GitHub audit logs to the approved destination.
2. Define and apply custom repository properties.
3. Create monthly governance review cadence.
4. Define KPI dashboard.
5. Decide on EMU timing.

### Proposed Custom Properties

- `owner_team`
- `system_tier`
- `customer_facing`
- `data_classification`
- `regulated_data`
- `deployment_criticality`

### Controlled Values

- `system_tier`
  - `production-critical`
  - `internal-standard`
  - `low-risk`
  - `exempt`
- `customer_facing`
  - `yes`
  - `no`
- `data_classification`
  - `public`
  - `internal`
  - `confidential`
  - `restricted`
- `regulated_data`
  - `none`
  - `financial`
  - `health`
  - `multiple`
- `deployment_criticality`
  - `high`
  - `medium`
  - `low`

### Deliverables

- audit log streaming setup
- repo property taxonomy
- repo classification sheet
- monthly review checklist
- EMU decision record
- Sprint 4 communication notice for reporting owners

### Acceptance Criteria

- audit stream is active and test-verified
- all active repos have required property values
- monthly governance review has owner, agenda, and KPI set
- EMU is classified as adopt now, later, or not needed
- custom properties use controlled values defined in this plan
- reporting owners receive the monthly review process and KPI definitions

### Risks

- audit sink ownership may sit outside engineering
- custom property values can drift without review discipline
- monthly review can degrade into stale reporting with no decisions

### Mitigations

- assign one accountable owner for audit ingestion before enabling the stream
- review repo property completeness monthly
- require each monthly review to produce owners and due dates for exceptions or drift

## Exception Process

Any exception to GitHub governance or security policy must include:

- policy being bypassed or deferred
- affected repo(s)
- owner
- approver
- business/technical rationale
- mitigation while the exception remains open
- expiry or review date
- decision log reference

Storage:

- tracked in `hldpro-governance` under the governance operating process chosen by the repo owner and platform owner

Approval:

- Platform approves workflow and branch policy exceptions
- Security approves security-control suppressions or deferrals
- Engineering leadership approves any production-risk exception lasting longer than 30 days

Review cadence:

- reviewed monthly in the GitHub governance review

## Cross-Sprint Decision Log Requirements

Each major GitHub Enterprise decision must record:

- decision
- owner
- date
- repos impacted
- risk addressed
- developer experience impact
- rollback plan
- review date

## Success Metrics

- percent of first-wave repos with `CODEOWNERS`
- percent of active repos covered by baseline rulesets
- percent of active repos under security configuration
- number of secret push blocks per month
- median time to triage critical security alerts
- number of third-party action exceptions
- number of repos missing owner metadata
- broken-main incidents per month

## Repo Execution Model

### Governance Repo Responsibilities

- define standards
- maintain rollout plan
- own reusable workflow policy
- own exceptions register
- own audit cadence
- own KPI reporting

### Product Repo Responsibilities

- add `CODEOWNERS`
- wire repo-specific required checks
- document repo-specific exceptions
- fix local workflow drift

## Immediate Next Actions

1. Break Sprint 1 into repo-specific tasks.
2. Add `CODEOWNERS` backlog items for first-wave repos.
3. Build required-check inventory from current workflow names.
4. Confirm GHAS licensing status and capture the result here.
5. Create actions inventory across active repos.
6. Define exception register storage and approvers.
7. Draft break-glass runbook skeleton before Sprint 3 starts.
8. Draft staged ruleset recommendations before any GitHub UI change.

## Definition of Done

This program is complete when:

- first-wave repos have enforced ownership and branch governance
- security controls are standardized and centrally reviewable
- workflow trust is improved by action policy and pinning
- audit evidence is accessible without manual reconstruction
- repo metadata supports governance reporting and policy targeting
