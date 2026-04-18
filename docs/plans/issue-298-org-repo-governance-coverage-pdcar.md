# Issue #298 - Org-Wide Active Repository Governance Coverage PDCA/R

## Plan

Issue #298 makes active repository coverage an explicit org-governance contract.
The current governance surface covers six canonical repos, while live GitHub
inventory on 2026-04-18 shows eight active repos:

- `hldpro-governance`
- `ai-integration-services`
- `HealthcarePlatform`
- `knocktracker`
- `ASC-Evaluator`
- `local-ai-machine`
- `seek-and-ponder`
- `EmailAssistant`

The governance gap is not just that `seek-and-ponder` and `EmailAssistant` are
missing from a table. The deeper issue is that a repo can be active in the org
while absent from `docs/governed_repos.json`, sweep scope, graphify targets,
raw issue feeds, metrics, memory integrity, Codex ingestion, compendium
generation, and final closeout verification.

Policy target:

- Every active org repo must be represented in `docs/governed_repos.json`.
- Exemption is a registry classification, not absence from the registry.
- Lifecycle and exemption classifications must become machine-checkable in the
  registry schema and validator, not prose-only notes.
- Duplicate repo lists must be generated from, validated against, or explicitly
  reconciled with the registry.
- Epic closeout requires live end-to-end proof that GitHub org inventory and
  governance coverage agree.

## Do

Implementation should run as child issue-backed slices under epic #298.

### Slice 1 - Inventory Drift Detector

- Add a validator that compares live `NIBARGERB-HLDPRO` repo inventory with
  `docs/governed_repos.json`.
- Extend `docs/schemas/governed-repos.schema.json` and registry validation so
  active, archived, exempt, limited-scope, and adoption-blocked states are
  explicit fields. Exempt or adoption-blocked rows must carry owner, rationale,
  review date, and linked issue evidence.
- Include fixture-backed tests so Local CI can run without network.
- Add weekly sweep surfacing first.
- Promote to CI enforcement only after known current gaps are classified.

### Slice 2 - `seek-and-ponder` Intake

- Classify governance tier and security tier.
- Add `seek-and-ponder` to `docs/governed_repos.json`.
- Reconcile graphify, wiki, raw feed, metrics, memory, Codex ingestion, and
  compendium subsystem flags.
- Validate existing `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, and governance docs.
- Create downstream issue/scope before any `seek-and-ponder` repo writes.

### Slice 3 - `EmailAssistant` Discovery

- Clone or inspect default branch in an isolated worktree.
- Identify stack, data sensitivity, CI, and existing governance docs.
- Classify tier before adoption.
- Add registry coverage or create an issue-backed blocker with rationale.

### Slice 4 - Registry-Driven Surface Reconciliation

- Reconcile `README.md`, `STANDARDS.md`, `docs/graphify_targets.json`, sweep,
  nightly cleanup, raw-feed sync, metrics, compendium, memory integrity, and
  Codex ingestion selection.
- Validate org ruleset applicability, default branch, branch protection, and
  required-check coverage for newly included active repos.
- Replace hardcoded lists where practical.
- Where GitHub Actions checkout mechanics force explicit entries, add
  validation so the explicit list cannot drift silently.

### Slice 5 - Final E2E Closeout Gate

- Run live org inventory against registry.
- Run registry schema validation.
- Run graphify target reconciliation.
- Run sweep/metrics/compendium/raw-feed selection validation.
- Run branch protection, default branch, org ruleset, and required-check
  validation for newly included repos.
- Run a named e2e command matrix so closeout proof is reproducible rather than
  scattered.
- Run baseline governance checks against newly included repos or cite accepted
  issue-backed deferrals.
- Create closeout and update #298 only after the e2e gate passes.

## Check

Planning package validation:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- Planner-boundary validation with changed-file evidence for issue #298.
- `python3 scripts/overlord/validate_backlog_gh_sync.py`

Implementation validation expected across child slices:

- Registry schema validation for `docs/governed_repos.json`.
- Live org drift detector against GitHub inventory.
- Offline fixture tests for missing active repo and archived/exempt repo cases.
- Graphify target reconciliation against registry graphify-enabled repos.
- Sweep selection simulation or registry-backed sweep smoke test.
- Compendium generation check against the expanded registry.
- Branch/ruleset/default-branch/required-check validation for newly included
  active repos.
- Baseline governance checks for `seek-and-ponder`.
- EmailAssistant classification evidence.

Final e2e command matrix must include, at minimum:

- live org inventory drift command
- registry schema/classification validator
- graphify target reconciliation
- sweep selection simulation or registry-backed sweep smoke
- compendium generation/check
- raw-feed selection check
- memory-integrity selection check
- Codex-ingestion selection check
- branch protection/default-branch/org-ruleset/required-check validation
- baseline governance checks for newly included repos

Final e2e acceptance:

- GitHub org inventory and `docs/governed_repos.json` agree on every active
  repo, or every difference has an accepted issue-backed classification.
- `seek-and-ponder` is governed or explicitly deferred by linked issue.
- `EmailAssistant` is classified and governed or explicitly deferred by linked
  issue.
- Registry classification fields validate for all active, archived, exempt,
  limited-scope, and adoption-blocked repos.
- Graphify, sweep, metrics, compendium, raw-feed, memory-integrity, and
  Codex-ingestion selection paths are registry-driven or guarded against drift.
- Branch protection, default branch, org ruleset applicability, and required
  checks validate for newly included active repos or have linked deferrals.
- Closeout includes exact command output, issue links, and accepted deferrals.

## Adjust

If another active repo appears during implementation, absorb it into #298 if it
is part of the same coverage gap. If it is materially different, create a child
classification issue before closeout.

If `seek-and-ponder` or `EmailAssistant` requires downstream edits, stop and
create repo-local issues and execution scopes before writing there.

If live GitHub inventory is unavailable in CI, keep a fixture-backed local test
for deterministic coverage and run the live check in weekly sweep with a clear
degraded-mode report.

If a workflow cannot consume the registry directly because `actions/checkout`
requires static entries, keep the explicit checkout block but add a validator
that fails when a sweep-enabled registry repo lacks a matching checkout step.

If alternate-family review is unavailable during planning, do not mark it as
accepted. Implementation PRs that change standards, schema semantics, registry
enforcement, or org-wide workflow behavior must add the required cross-family
review artifact before merge.

## Review

Review should focus on whether the plan eliminates silent blind spots:

- Can an active org repo exist without a registry row?
- Are exempt repos still visible to governance?
- Will hardcoded workflow repo lists drift without detection?
- Are `seek-and-ponder` and `EmailAssistant` handled through classification
  rather than assumptions?
- Are registry classifications enforceable by schema and tests?
- Are branch protection, default branch, ruleset, and required-check controls
  covered for newly included active repos?
- Is there a concrete e2e command matrix for closeout proof?
- Is final e2e evidence required before #298 can close?

This epic is not complete until the final e2e closeout gate passes and #298 has
links to the validation evidence.
