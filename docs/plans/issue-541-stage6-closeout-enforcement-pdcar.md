# Issue #541 PDCAR: Stage 6 Closeout Enforcement

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/541
Epic: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/533
Branch: `issue-541-stage6-closeout-enforcement-v2`

## Plan

Stage 6 closeout validation exists, but closeout presence is not merge-enforced. `hooks/closeout-hook.sh` validates a closeout only after an operator creates and runs it; reusable governance CI and Local CI do not currently require an issue-matching closeout for implementation or governance-surface PRs.

## Do

Add a shared deterministic validator and wire it into existing gates:

- `scripts/overlord/check_stage6_closeout.py`
- `scripts/overlord/test_check_stage6_closeout.py`
- `.github/workflows/governance-check.yml`
- `tools/local-ci-gate/profiles/hldpro-governance.yml`
- progress/feature registry/evidence/closeout artifacts for issue #541

Keep the existing closeout format and validator. Do not create a second closeout system.

## Check

Required validation:

- `python3 scripts/overlord/test_check_stage6_closeout.py`
- `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-541-stage6-closeout-enforcement.md --root .`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-21-issue-541-stage6-closeout-enforcement.json`
- `python3 scripts/overlord/check_stage6_closeout.py --root . --branch-name issue-541-stage6-closeout-enforcement --changed-files-file /tmp/issue-541-changed-files.txt`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-541-stage6-closeout-enforcement --changed-files-file /tmp/issue-541-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-541-stage6-closeout-enforcement-implementation.json --changed-files-file /tmp/issue-541-changed-files.txt --require-lane-claim`

Negative controls must prove:

- implementation/governance-surface changes without a matching closeout fail;
- planning-only changes do not require a closeout;
- valid matching closeout passes;
- invalid matching closeout fails;
- multiple matching closeouts fail.

## Adjust

If the validator is too broad, adjust the planning-only exemption list rather than weakening closeout validation. If downstream rollout needs repo-specific behavior, split that into a consumer rollout sprint after governance proves the contract.

## Review

Closeout must cite the gate wiring, negative controls, and the self-learning record that explains why passive closeout validation was insufficient.
