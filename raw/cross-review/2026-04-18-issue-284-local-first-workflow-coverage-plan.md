---
schema_version: v2
pr_number: pending
pr_scope: implementation
drafter:
  role: planner-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-18
reviewer:
  role: subagent-workflow-review
  model_id: subagents-james-pauli
  model_family: openai
  signature_date: 2026-04-18
  verdict: APPROVED_WITH_FOLLOWUP
gate_identity:
  role: governance-gate
  model_id: workflow-local-coverage-validator
  model_family: deterministic
  signature_date: 2026-04-18
invariants_checked:
  issue_backed_scope: true
  planning_before_implementation: true
  local_first_not_ci_replacement: true
  workflow_inventory_complete: true
  no_actions_full_replay_claim: true
  e2e_evidence_required: true
---

# Cross-Review: Issue #284 Local-First Workflow Coverage

## Scope Reviewed

Issue #284 adds a local-first coverage inventory and validator for governance GitHub Actions workflows. The plan does not authorize consumer repo changes or a blanket local replay of scheduled/token-writing Actions jobs.

## Findings

No blocker for implementation.

The plan correctly separates deterministic checks from GitHub-only execution contexts. The required implementation evidence is a validator and tests that fail on inventory drift, not an `act` replay of every workflow.

## Required Follow-Up Before Closeout

- Include every `.github/workflows/*.yml` file in the inventory.
- Make the validator fail if inventory entries reference missing workflows.
- Make deterministic workflows declare at least one local, contract, or script/dry-run coverage command.
- Make GitHub-only workflows declare an explicit exemption rationale.
- Wire the validator into Local CI Gate and an independent GitHub Actions workflow.
- Record real local command output and GitHub Actions run IDs before closing #284.

## Decision

Accepted for implementation on branch `codex/issue-284-local-first-workflow-coverage`.
