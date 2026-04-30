# Validation: Issue #623 Mutation-Time Pre-Tool Hardening

Date: 2026-04-30
Repo: hldpro-governance
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/623
Branch: `issue-623-mutation-pretool-hardening-20260430`

## Scope

This validation artifact records the bounded implementation slice for the local
mutation-time pre-tool fail-closed path under parent issue `#615`.

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 -m unittest scripts.overlord.test_check_plan_preflight -v` | PASS | Canonical `docs/plans/*structured-agent-cycle-plan.json` evidence, expanded Bash mutation detection, and read-only allow cases all pass. |
| `python3 -m unittest scripts.overlord.test_schema_guard_hook -v` | PASS | Schema-guard now fails closed on missing helper, malformed payload, unknown decision, and still allows read-only Bash analysis. |
| `/opt/homebrew/bin/python3.11 -m pytest scripts/orchestrator/test_delegation_hook.py -q` | PASS | Mutation hook path covers `Write`/`Edit`/`MultiEdit`, malformed/missing payload failure, and in-scope allow cases. |
| `bash -n hooks/code-write-gate.sh` | PASS | Hook shell syntax valid after fail-closed mutation-path changes. |
| `bash -n hooks/schema-guard.sh` | PASS | Hook shell syntax valid after fail-closed helper-decision changes. |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-30-issue-623-mutation-pretool-hardening-implementation.json --require-lane-claim` | PASS | Implementation scope matches declared root, branch, write paths, and forbidden roots. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-623-mutation-pretool-hardening-20260430 --require-if-issue-branch` | PASS | Structured plan validates after implementation promotion. |
| `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-623-plan-to-implementation.json` | PASS | Implementation-ready handoff validates. |
| `bash scripts/codex-review.sh claude raw/packets/2026-04-30-issue-623-claude-review-packet.md` | PASS | Sanctioned alternate-family implementation review returned `accepted` and was normalized to `docs/codex-reviews/2026-04-30-issue-623-claude.md`. |
| `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS | Local CI Gate verdict `PASS` after reconciling the canonical backlog mirror and sanctioned review wrapper outputs inside the implementation scope. |
| `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-30-issue-623-mutation-pretool-hardening.md --root .` | PASS | Stage 6 closeout evidence validates after implementation-phase reviewer and gate identities were reconciled. |
| `git diff --check` | PASS | Diff hygiene remains clean after final issue-local artifact updates. |

## Proof Matrix

| Surface / Case | Result | Evidence |
|---|---|---|
| `.claude/settings.json` wires `Edit` and `MultiEdit` to `code-write-gate.sh` | PASS | Added `PreToolUse` matchers for `Edit` and `MultiEdit` with the same hook command as `Write`. |
| `hooks/code-write-gate.sh` allows compliant in-scope `Edit` with implementation-ready evidence | PASS | Direct transcript: `Edit` payload targeting `hooks/code-write-gate.sh` returned `RC 0`, empty stdout, empty stderr. |
| `hooks/code-write-gate.sh` hard-blocks malformed or incomplete mutation payloads | PASS | Direct transcript: `MultiEdit` payload without `file_path` returned `RC 2` with `{\"decision\":\"block\",\"reason\":\"FAIL: missing file_path for mutation tool 'MultiEdit'\"}`. |
| `hooks/schema-guard.sh` allows read-only Bash analysis | PASS | Direct transcript: `git status --short` returned `RC 0`, empty stdout, empty stderr. |
| `hooks/schema-guard.sh` hard-blocks helper-missing condition | PASS | Direct transcript in temp repo without helper returned `RC 2` and `schema-guard: FAIL: missing helper scripts/overlord/check_plan_preflight.py`. |
| `scripts/overlord/check_plan_preflight.py` blocks indeterminate in-place mutation verbs | PASS | Direct transcript: `sed -i -e 's/old/new/'` returned `decision=block`, `target_path=<indeterminate bash write: sed -i>`, and `PLAN_GATE_BLOCKED: missing_recent_plan`. |
| Expanded Bash mutation detection (`sed -i`, `perl -pi`, `cp`, read-only `sed -n` / `perl -ne`) | PASS | Covered by `scripts.overlord.test_check_plan_preflight` passing 17 tests. |
| Fail-closed helper/decision behavior on schema path | PASS | Covered by `scripts.overlord.test_schema_guard_hook` passing 12 tests. |
| Fail-closed mutation payload behavior on write hook path | PASS | Covered by `scripts/orchestrator/test_delegation_hook.py` passing 13 tests. |

## Findings

- Issue `#623` stays bounded to `.claude/settings.json`,
  `OVERLORD_BACKLOG.md`, `hooks/code-write-gate.sh`, `hooks/schema-guard.sh`,
  `scripts/overlord/check_plan_preflight.py`, focused tests, required
  governance doc co-staging, and issue-local artifacts only.
- Canonical plan evidence now comes from `docs/plans/*structured-agent-cycle-plan.json`
  rather than `.claude/plans`.
- Canonical backlog-gate parity was restored by moving closed sibling issue
  `#621` out of the active `OVERLORD_BACKLOG.md` table and recording live
  issue `#623` there without reopening `#621` hook ownership.
- Named Bash mutation forms now include in-place and copy/move style writes in
  addition to redirects, `tee`, heredocs, and Python file-write detection.
- `Edit`, `MultiEdit`, missing `file_path`, malformed payloads, helper-missing
  conditions, parse failures, and unknown decisions now fail closed on the
  owned local mutation path.
- The governed commit hook regenerated `graphify-out/graph.json` and
  `graphify-out/GRAPH_REPORT.md`, and those generated outputs were kept inside
  the bounded implementation packet instead of being ignored as out-of-scope
  drift.
- Sanctioned review wrapper outputs were normalized to the issue-scoped Claude
  review artifact and approved CLI session-event evidence under
  `raw/cli-session-events/2026-04-30/`.
- `#617`, `#621`, `#607`, `#612`, and `#614` remain explicit external
  boundaries; no sibling-lane surfaces were edited.
