# PDCAR — Issue #632

## Plan

- Parent: `#607`
- Objective: implement the narrow planning-first authority enforcement slice so governed execution is blocked before valid planning authority exists and allowed only after valid planning authority exists.
- Owned surfaces:
  - `scripts/overlord/assert_execution_scope.py`
  - `.github/workflows/governance-check.yml`
  - `tools/local-ci-gate/profiles/hldpro-governance.yml`
  - focused tests under `scripts/overlord/`
  - issue-local artifacts only
- Out of scope:
  - degraded-fallback propagation under `#612`
  - local pre-hook/startup/pretool/root-parity work under `#615`
  - hldpro-sim verifier/drift-gate work under `#614`
  - blocked child `#631` under `#612`
  - broad standards rewrite unless strictly required for this bounded gate

## Do

- Bootstrap the planning packet and execution-scope boundary in the isolated `#632` worktree.
- Define the acceptance contract for:
  - blocked-before-authority behavior
  - allowed-after-authority behavior
  - independent regression/impact proof requirements
- Run structural validators and sanctioned alternate-family planning review before any implementation promotion.

## Check

- Packet validates structurally.
- Owned surfaces are explicit and bounded.
- `#631`, `#612`, `#614`, and `#615` remain external boundaries.
- No implementation starts until planning validation and alternate-family review complete.

## Adjust

- If specialist or alternate-family review finds scope bleed, narrow the lane rather than widening the parent.
- If the sanctioned review wrapper is unavailable, record the blocker honestly and keep the lane planning-only blocked.

## Review

- This lane is only the implementation child for planning-first authority enforcement under `#607`.
- It does not by itself close the full `#607` parent until later bounded proof is returned from implementation.
