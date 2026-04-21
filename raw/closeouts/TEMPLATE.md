# Stage 6 Closeout
Date: YYYY-MM-DD
Repo: [ai-integration-services | HealthcarePlatform | local-ai-machine | knocktracker | hldpro-governance]
Task ID: [PROGRESS.md entry ID or GitHub issue #]
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made
[One sentence: what was decided or built]

## Pattern Identified
[Optional: recurring pattern this reveals — e.g., "all edge functions calling external APIs need explicit timeout handling"]

## Contradicts Existing
[Optional: does this contradict or update anything in wiki/? Link to the page.]

## Files Changed
[List of key files modified]

## Issue Links
[GitHub epic, slice, PR, and follow-up issue links. Every residual item must have an issue link.]

## Schema / Artifact Version
[Name the schema or artifact contract version used, for example `raw/cross-review` schema v2 or `som-packet` schema v1.]

## Model Identity
[List model IDs, families, roles, and reasoning effort where applicable. For Codex calls, include both `-m <model>` and `model_reasoning_effort` evidence.]

## Review And Gate Identity
[Name reviewer and gate identities, including role, model ID, model family, signature date, and verdict when the artifact requires it.]

Review artifact refs:
- `raw/cross-review/YYYY-MM-DD-<slug>.md` or `N/A - implementation only`

Gate artifact refs:
- `cache/local-ci-gate/reports/YYYYMMDDTHHMMSSZ-<profile>-git/local-ci-*.json` or command result when the report is local-only

## Wired Checks Run
[List the actual workflow/script/test checks wired and run. Do not claim enforcement from documentation alone.]

## Execution Scope / Write Boundary
[When work is delegated to workers, sweep/status writers, or sibling worktrees, name the execution-scope JSON artifact and the `assert_execution_scope.py` command used to prove the checkout root, branch, changed paths, and forbidden roots.]

Structured plan:
- `docs/plans/<issue>-structured-agent-cycle-plan.json`

Execution scope:
- `raw/execution-scopes/YYYY-MM-DD-<issue>-implementation.json`

Handoff package:
- `raw/handoffs/YYYY-MM-DD-<issue>-plan-to-implementation.json`

Handoff lifecycle:
- `Handoff lifecycle: accepted` or `Handoff lifecycle: released`

## Validation Commands
[Commands run for this closeout and PASS/FAIL/SKIP result. Include why any expected check was skipped.]

Validation artifact:
- `raw/validation/YYYY-MM-DD-<issue>.md`

## Tier Evidence Used
[For architecture or standards scope, name the committed artifact that proves the gate model/tier used (for example `raw/cross-review/YYYY-MM-DD-<slug>.md`).]

## Residual Risks / Follow-Up
[Issue-backed residual risks, deferrals, or rollback/fix-forward notes. If none, state "None."]

## Wiki Pages Updated
[List of wiki/ pages this closeout should update. If none exist yet, note what should be created.]

## operator_context Written
[ ] Yes — row ID: [id]
[ ] No — reason: [reason]

## Links To
[Links to related decisions, patterns, or wiki pages]
