# Issue #231 — End-to-End Autonomous Delivery Pilot PDCA/R

## Plan

Issue #231 pilots the operator experience on a low-risk governance-repo slice. The pilot must demonstrate issue-backed planning, isolated worktree execution, packet queue dry-run behavior, validation evidence, independent review, gate evidence, closeout, PR checks, and a readiness conclusion.

## Do

- Create the #231 structured plan and PDCAR.
- Create a dry-run SoM packet at `raw/packets/2026-04-17-issue-231-e2e-pilot.yml`.
- Create pilot metrics under `metrics/pilot/`.
- Create cross-review, gate, and closeout artifacts.
- Classify `raw/gate/` and `metrics/pilot/` as governance surface.
- Update registry/data dictionary documentation.

## Check

Planned validation:

- `python3 scripts/packet/validate.py raw/packets/2026-04-17-issue-231-e2e-pilot.yml`
- dry-run packet queue transition for the pilot packet
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- governance-surface changed-file validation with `--enforce-governance-surface`
- issue-branch plan validation with `--require-if-issue-branch`
- model pin checks, graphify contract check, and compendium freshness check

## Adjust

The pilot does not grant broader autonomous execution authority. It records readiness evidence and residual risk for a later authority-expansion issue.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-e2e-pilot.md`.
