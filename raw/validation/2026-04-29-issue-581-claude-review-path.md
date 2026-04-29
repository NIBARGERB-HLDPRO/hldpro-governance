# Validation: Issue #581 Governed Claude Review Path

Date: 2026-04-29
Repo: hldpro-governance
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/581

## Scope

This validation artifact records planning and deterministic reproduction
evidence for the failing governed Claude specialist-review path. No
implementation-ready fix has been authorized yet.

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 -m json.tool docs/plans/issue-581-claude-review-path-structured-agent-cycle-plan.json` | PASS | Planning packet JSON parses cleanly. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-581-claude-review-path --require-if-issue-branch` | PENDING | To be rerun after the planning artifacts are staged in this lane. |
| `CLAUDE_CODE_OAUTH_TOKEN=... claude -p "say ok" --model claude-sonnet-4-6 --max-turns 1 --no-session-persistence` | PASS | Base Claude CLI and governed token path are healthy; output was `ok`. |
| `bash scripts/codex-review.sh claude "<bounded packet review prompt>"` via approved downstream wrapper replay | FAIL | Reproduced repeated `Reached max turns` and `idle_timeout` failures through the approved governed review path; no usable review verdict was produced. |

## Findings

- The defect is not base Claude auth or token bootstrap. The governed token and
  direct `claude -p` preflight succeed.
- The failure is inside the approved governed review path contract
  (`scripts/codex-review.sh claude` wrappers / `scripts/codex-review-template.sh`
  / `scripts/cli_session_supervisor.py`) and is therefore a governance-source
  blocker for downstream rollout.
- ASC-Evaluator issue #15 remains correctly blocked until this path can return
  a real alternate-family review artifact.

## Next Step

Land the issue-581 planning packet, then isolate the specific wrapper or
supervisor contract defect before requesting implementation-ready authority.
