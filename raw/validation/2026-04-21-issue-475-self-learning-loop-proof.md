# Validation — Issue #475 Self-Learning Loop Operational Proof

Date: 2026-04-21
Repo: hldpro-governance
Branch: `issue-475-self-learning-loop-proof-20260421`
Worktree: `/Users/bennibarger/Developer/HLDPRO/hldpro-governance/var/worktrees/issue-475-self-learning-loop-proof`

## Scope

Issue #475 closes the local operational proof gap found in the self-learning loop research pass:

- `overlord-sweep` was blocked before self-learning report generation.
- `metrics/self-learning/latest.*` was stale at 2026-04-17.
- no tracked `raw/operator-context/self-learning/*` evidence existed.
- `docs/ERROR_PATTERNS.md` was still a stub.

## Changes Validated

| Area | Evidence |
|---|---|
| Codex model-pin scanner no longer treats stale local worktree mirrors as authoritative source | `.github/scripts/check_codex_model_pins.py` excludes `var/worktrees/` |
| hldpro-sim Codex provider emits required model reasoning pin | `packages/hldpro-sim/hldprosim/providers.py` includes `-c model_reasoning_effort=<effort>` |
| Provider test proves the pinned invocation contract without creating a false checker positive | `packages/hldpro-sim/tests/test_providers.py` asserts `codex`, `exec`, `-m`, and `model_reasoning_effort` separately |
| Self-learning report refreshed | `metrics/self-learning/latest.json` generated at `2026-04-21T17:35:29Z`, `entry_count: 144`, sources include `error_pattern` and `operator_context` |
| Append-only self-learning write-back evidence exists | `raw/operator-context/self-learning/2026-04-21-issue-475-self-learning-sweep-staleness.md` |
| Reusable prevention pattern exists | `docs/ERROR_PATTERNS.md` includes `## Pattern: overlord-sweep-self-learning-skipped` |
| Stage 6 evidence package validates | `raw/handoffs/2026-04-21-issue-475-self-learning-loop-proof.json`, `raw/packets/2026-04-21-issue-475-self-learning-loop-proof.json`, and `raw/closeouts/2026-04-21-issue-475-self-learning-loop-proof.md` |

## Commands

| Command | Result |
|---|---|
| `python3 .github/scripts/check_codex_model_pins.py` | PASS |
| `python3 scripts/orchestrator/test_self_learning.py` | PASS, 5 tests |
| `/tmp/hldpro-issue-475-venv/bin/python scripts/orchestrator/test_packet_queue.py` | PASS, 13 tests |
| `PYTHONPATH=packages/hldpro-sim /tmp/hldpro-issue-475-venv/bin/python -m pytest packages/hldpro-sim/tests/test_providers.py` | PASS, 8 tests |
| `PYTHONPATH=packages/hldpro-sim /tmp/hldpro-issue-475-venv/bin/python -m pytest packages/hldpro-sim/tests` | PASS, 13 tests |
| `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py` | PASS, 20 tests |
| `python3 -m py_compile .github/scripts/check_codex_model_pins.py packages/hldpro-sim/hldprosim/providers.py scripts/orchestrator/self_learning.py scripts/orchestrator/packet_queue.py scripts/overlord/validate_structured_agent_cycle_plan.py` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-475-self-learning-loop-proof-20260421 --require-if-issue-branch` | PASS, 116 plans |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-475-self-learning-loop-proof-20260421 --changed-files-file <tmp> --enforce-governance-surface` | PASS, 116 plans |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `bash hooks/check-errors.sh` | PASS |
| `python3 scripts/overlord/validate_handoff_package.py raw/handoffs/2026-04-21-issue-475-self-learning-loop-proof.json --root .` | PASS, 1 package |
| `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-475-self-learning-loop-proof.md --root .` | PASS |
| `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json --report-dir cache/local-ci-gate/reports` | PASS |
| `python3 scripts/orchestrator/self_learning.py lookup --query 'overlord sweep self-learning report stale model pins var worktrees' --limit 3` | PASS; top result is `docs/ERROR_PATTERNS.md` pattern `overlord-sweep-self-learning-skipped` |
| `git diff --check` | PASS |

## Dependency Note

System Python is externally managed, so packet and package tests were run from temporary venv `/tmp/hldpro-issue-475-venv` with:

```bash
python3 -m venv /tmp/hldpro-issue-475-venv
/tmp/hldpro-issue-475-venv/bin/python -m pip install -r scripts/packet/requirements.txt pytest pydantic
```

## Remaining Proof Boundary

Local closure is proven. Remote scheduled-sweep closure still requires this branch to be pushed/merged and `overlord-sweep` to run with the updated model-pin checker/provider code. Issue #475 should remain open until that remote run proves the `Build self-learning knowledge report` step is no longer skipped.
