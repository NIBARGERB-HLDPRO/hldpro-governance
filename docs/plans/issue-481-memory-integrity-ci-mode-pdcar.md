# Issue 481 PDCAR: Memory Integrity CI Mode

Issue: NIBARGERB-HLDPRO/hldpro-governance#481  
Date: 2026-04-21

## Plan

The manual Overlord Sweep proof for issue #475 cleared cross-repo checkout and model-pin validation, but GitHub Actions run `24738583207` failed at `Memory integrity audit` because the runner does not have operator-local Claude memory files under `~/.claude/projects/...`.

Expected implementation:

- Keep `scripts/overlord/memory_integrity.py` strict by default for operator machines.
- Add an explicit CI/runner mode for missing operator-home memory sources.
- Wire the weekly sweep to use that explicit mode so `Build self-learning knowledge report` is no longer blocked by local-only memory state.
- Add focused regression tests for strict missing-memory failure and CI-mode skip behavior.
- Record the failure pattern in governance fail-fast/self-learning docs.

## Do

1. Create a bounded issue branch and execution scope for #481.
2. Add the memory-integrity option, workflow call, tests, and issue-backed docs.
3. Validate locally with focused unit tests, strict local memory audit, runner-mode missing-memory audit, and temp self-learning report generation.
4. Publish a PR, wait for CI, merge, and re-run the Overlord Sweep.

## Check

Acceptance criteria:

- `python3 scripts/overlord/memory_integrity.py` remains strict locally and passes against the operator memory files on this machine.
- `python3 scripts/overlord/memory_integrity.py --memory-root /tmp/definitely-missing-hldpro-memory-root --allow-missing` exits 0 and prints explicit `SKIP` notices.
- `python3 -m unittest scripts.overlord.test_memory_integrity scripts.orchestrator.test_self_learning` passes.
- `python3 scripts/orchestrator/self_learning.py report --output-json /tmp/issue-481-self-learning.json --output-md /tmp/issue-481-self-learning.md` passes.
- The next manual Overlord Sweep reaches `Build self-learning knowledge report`.

## Act

If the sweep still fails before self-learning, inspect the failed step, add or update a GitHub issue with concrete acceptance criteria, and loop again before claiming the cross-repo self-learning gap is closed.

## Reflect

This slice separates repo-generated self-learning metrics from operator-local memory files. The long-term memory snapshot/source-of-truth question remains issue-backed if CI needs to validate memory contents without mounting operator home state.
