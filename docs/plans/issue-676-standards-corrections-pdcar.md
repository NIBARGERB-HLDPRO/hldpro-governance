# PDCAR: Issue #676 — fix(standards): 6 STANDARDS.md drift/conflict corrections

Date: 2026-05-03
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/676
Branch: `issue-676-standards-corrections-20260503`

## Plan

Apply 6 targeted surgical corrections to STANDARDS.md to resolve drift and
conflicts accumulated since the April 2026 SoM charter update. Each fix is
self-contained; none introduces new policy, only clarifies or corrects existing
text.

Acceptance criteria:

- Fix 1: Schema-guard section documents approved Stampede doc schema exceptions.
- Fix 2: Branch naming section lists feat/ as approved alias and references origin/main (not origin/develop).
- Fix 3: Stale review-contract table row removed or updated to reflect current model roster.
- Fix 4: Baseline Security heading explicitly lists Stampede in scope.
- Fix 5: Hook gate rule carries a scope qualifier limiting it to hldpro-governance and consumer-pull-enrolled repos.
- Fix 6: Structured plan requirement section carries a scope note specifying which repo types and workflows must produce the artifact.

## Do

### Fix 1 — Stampede doc schema exceptions

The schema-guard CI check enforces a canonical JSON structure for governance
artifacts. Stampede deliberately uses a different shape for its planning JSON
documents. The exceptions are approved and should be documented in STANDARDS.md
so that future schema-guard contributors do not inadvertently close the gap.

### Fix 2 — Branch naming: feat/ alias and origin/develop to origin/main

STANDARDS.md branch naming section references origin/develop as the base branch
for feature work. The org migrated to origin/main in 2025. Additionally, feat/
is an accepted alias for feature/ in all governed repos but is not listed.

### Fix 3 — Stale review contract row

The review contract table contains a row referencing a model or workflow
superseded by the April 2026 SoM Model Routing Charter update. That row is
either removed or updated to reflect the current active roster.

### Fix 4 — Baseline Security heading missing Stampede

The Baseline Security section lists governed repos in scope but omits Stampede,
which was enrolled in Q1 2026. The heading is updated to include it.

### Fix 5 — Hook gate scope qualifier

The hook gate rule as written applies unconditionally to all HLDPRO repos. The
intent is to scope it only to hldpro-governance itself and consumer repos that
have completed the consumer-pull governance tooling adoption. A scope qualifier
sentence is added.

### Fix 6 — Structured plan scope note

The structured plan requirement is ambiguous about which repo types must produce
the artifact. A scope note is added specifying: hldpro-governance issue branches,
Codex orchestrated slices, and governed consumer repo implementations. Non-issue
hotfix branches and documentation-only PRs are explicitly excluded.

## Check

- STANDARDS.md content audit: all 6 fixes present, no unrelated changes.
- JSON lint on execution scope and structured plan.
- Governance surface validator passes on STANDARDS.md change.
`git diff origin/main..HEAD` shows only expected files.

## Adjust

Pending implementation.

## Review

Pending implementation.
