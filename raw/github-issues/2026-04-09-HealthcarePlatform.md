# GitHub Issues — HealthcarePlatform
Date: 2026-04-09

## #711: Chart Audit validation corpus and route/test harness hardening
Labels: none | Created: 2026-04-09

Parent epic: #706
Source draft PR: #704

## Scope
- PHI validation corpus
- pilot DON review fixtures
- route coverage contract tests
- service/frontend harness additions that support chart-audit verification

## Acceptance Criteria
- Validation fixtures and route/test harness work are isolated from product-feature scope.
- PHI-safe synthetic data assumptions are documented and verifiable.
- Test additions materially support the chart-audit rollout without hiding product defects inside test-only
---
## #710: Chart Audit Phase 3: QAPI feed, trends, and PIP triggers
Labels: none | Created: 2026-04-09

Parent epic: #706
Source draft PR: #704

## Scope
- qapi_findings and trend-data schema
- QAPI feed from chart audit findings
- corrective-action/PIP stub trigger path
- notification integration for audit-driven CAPA flow

## Acceptance Criteria
- QAPI and corrective-action behavior is independently reviewable.
- Verification covers data creation, notification emission, and tenant isolation.
- No Phase 3 merge depends on unverified Phase 4 portfolio work.

---
## #709: Chart Audit Phase 4: portfolio, benchmarking, and scheduling
Labels: none | Created: 2026-04-09

Parent epic: #706
Source draft PR: #704

## Scope
- consultant/enterprise portfolio views
- anonymized peer benchmarking
- schedule/cadence management
- tier-gated route and UI behavior for cross-facility access

## Acceptance Criteria
- Portfolio and scheduling UI are isolated from core ingestion/QAPI logic.
- Verification covers tier-gated access and PHI-safe benchmarking presentation.
- Route additions and frontend affordances are tested independently.

---
## #708: Chart Audit Phase 2: FHIR and CCD structured intake
Labels: none | Created: 2026-04-09

Parent epic: #706
Source draft PR: #704

## Scope
- FHIR R4 bundle parser
- CCD/C-CDA parser
- format detection and structured ingest path integration

## Acceptance Criteria
- Structured-intake parser work is isolated from core Phase 1 ingestion.
- Verification proves FHIR and CCD paths map into the governed audit record shape.
- Parser behavior is covered by bounded tests and PHI-safe fixtures.

---
## #707: Chart Audit Phase 1: core schema, RLS, ingestion, and reporting
Labels: none | Created: 2026-04-09

Parent epic: #706
Source draft PR: #704

## Scope
- chart audit schema and RLS
- edge function ingest/process/report endpoints
- PHI scrubber and rule engine baseline
- batch/dashboard core UI and service wiring needed for Phase 1 flow

## Acceptance Criteria
- Scope is reduced to the minimum viable Phase 1 slice.
- Migrations, RLS, and edge function changes are issue-backed and independently reviewable.
- Verification covers schema/RLS, edge routes, and the core frontend batch/report path.
- Re
---
## #706: Epic: Governed intake and decomposition for Chart Audit / QAPI module
Labels: none | Created: 2026-04-09

## Summary
Draft PR #704 contains a large multi-phase Chart Audit / QAPI implementation intended for `main`, but it is not currently issue-backed and is too large to move through the repo's governed issue lane flow as a single unit.

This issue converts that draft into a tracked epic so the work can be reviewed, split, verified, and merged under the structured agent cycle and issue-governance rules now active in this repo.

## Source
- Draft PR: #704 `feat: AI Chart Auditor — QAPI Integration (P
---