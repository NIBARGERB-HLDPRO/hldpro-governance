# Issue #475 — Self-Learning Loop Operational Proof PDCAR

## Plan

The research pass showed the deterministic self-learning code works locally, but operational proof is stale because the scheduled `overlord-sweep` failed before the self-learning report step. The fix must unblock the sweep preflight, refresh the report, create append-only write-back evidence, and convert the failure into a reusable prevention pattern.

## Do

- Fix codex model-pin validation so it ignores stale local worktree mirrors under `var/worktrees/`.
- Align the hldpro-sim provider test with the required pinned Codex invocation contract.
- Add a real `ERROR_PATTERNS.md` pattern for skipped self-learning reports.
- Add an issue-backed self-learning operator-context artifact for the April 2026 sweep-staleness failure.
- Regenerate `metrics/self-learning/latest.json` and `metrics/self-learning/latest.md`.

## Check

Planned validation:

- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 scripts/orchestrator/test_self_learning.py`
- `python3 scripts/orchestrator/test_packet_queue.py`
- `python3 scripts/orchestrator/self_learning.py report --output-json /tmp/issue-475-self-learning.json --output-md /tmp/issue-475-self-learning.md`
- `python3 scripts/orchestrator/self_learning.py report --output-json metrics/self-learning/latest.json --output-md metrics/self-learning/latest.md`
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-475-self-learning-loop-proof-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-475-self-learning-loop-proof-20260421 --changed-files-file <changed-files> --enforce-governance-surface`
- `python3 -m py_compile .github/scripts/check_codex_model_pins.py scripts/orchestrator/self_learning.py scripts/orchestrator/packet_queue.py scripts/overlord/validate_structured_agent_cycle_plan.py`

## Adjust

If local checks pass but remote `overlord-sweep` cannot be manually dispatched in this session, keep the remaining remote run as explicit issue #475 follow-up instead of claiming the scheduled workflow is proven.

## Review

Review evidence will be recorded in `raw/validation/2026-04-21-issue-475-self-learning-loop-proof.md` and the Stage 6 closeout.
