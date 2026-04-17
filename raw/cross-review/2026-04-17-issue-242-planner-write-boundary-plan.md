---
schema_version: v2
pr_number: TBD
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-17
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-17
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: verify-completion
  model_id: gpt-5.3-codex
  model_family: openai
  signature_date: 2026-04-17
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Issue #242 Planner Write-Boundary Plan Review

## Source Review

Prior Claude alternate-family review for the #241/#242 split returned `APPROVED_WITH_CHANGES` and required five changes before #242 implementation:

- define the planning-artifact allowlist;
- define an exception mechanism;
- add warning-to-strict transition behavior;
- specify minimal handoff evidence;
- ensure hook/PR enforcement and implementer briefs require handoff.

Current Claude review of this #242 planning package also returned `APPROVED_WITH_CHANGES`.

Required change status:

- Cross-review frontmatter: resolved in this artifact.
- Execution-scope username path: verified already correct as `/Users/bennibarger/...` in `raw/execution-scopes/2026-04-17-issue-242-planner-write-boundary-planning.json`.
- PDCAR test-list reconciliation: resolved by aligning the PDCAR Do section to the seven required test cases below.

## Research-Agent Findings

Enforcement-map research found that #226 already provides a governance-surface branch gate through `validate_structured_agent_cycle_plan.py`, `governance-check.yml`, and `code-write-gate.sh`. That gate requires issue-specific plans and implementation-ready handoff for governance-surface changes, but it does not yet enforce the planner/non-planning file boundary with accepted pinned-agent evidence.

Minimal-design research recommended putting #242 in `assert_execution_scope.py`, not the structured-plan schema. The execution-scope artifact already owns root, branch, forbidden-root, and allowed-write-path declarations, so it is the natural place to add optional `execution_mode` and `handoff_evidence`.

Audit research found the process-control gap: planner/non-planning boundaries were prose rules. The old local hook blocked only new code files and allowed edits to existing files and docs/config/data paths, so planner sessions could still produce non-planning diffs before a CI path tied the diff to issue-backed handoff evidence.

## Accepted Plan

Implement #242 as a file-scope execution-boundary gate:

- planning-only execution scopes may change only `allowed_write_paths`;
- non-planning execution scopes require accepted pinned-agent handoff evidence;
- same-model or same-family planner/implementer handoff requires an active exception with expiry;
- CI is strict and authoritative;
- local hooks warn for this boundary and keep existing new-code routing behavior;
- historical structured plans remain compatible.

## Required Tests

- planning-only diff inside `allowed_write_paths` passes;
- planning-only diff outside `allowed_write_paths` fails;
- non-planning diff without handoff evidence fails;
- accepted pinned-agent handoff passes;
- planner-model implementer handoff fails without active exception;
- active exception with expiry passes;
- diff-mode and dirty-tree modes share path normalization rules.
