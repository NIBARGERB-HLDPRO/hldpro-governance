# Validation: Issue #581 Governed Claude Review Path

Date: 2026-04-29
Repo: hldpro-governance
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/581

## Scope

This validation artifact records the reproduced failure, the governance-owned
contract repair, and the post-fix proof for the governed Claude
specialist-review path.

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 -m json.tool docs/plans/issue-581-claude-review-path-structured-agent-cycle-plan.json` | PASS | Structured plan JSON parses cleanly after promotion to implementation-ready. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-581-claude-review-path --require-if-issue-branch` | PASS | Issue-backed packet remains valid after the scope promotion. |
| `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-29-issue-581-claude-review-path.json` | PASS | Handoff validates with implementation-ready scope and review refs. |
| `CLAUDE_CODE_OAUTH_TOKEN=... claude -p "say ok" --model claude-sonnet-4-6 --max-turns 2 --no-session-persistence` | PASS | Base Claude CLI and governed token path are healthy; output was `ok`. |
| `bash scripts/codex-review.sh claude "<bounded packet review prompt>"` using the pre-fix template defaults | FAIL | Reproduced `Reached max turns` and `idle_timeout` through the approved governed review path; no usable review verdict was produced. |
| `CODEX_REVIEW_DRY_RUN=1 bash scripts/codex-review.sh claude "Review this packet only."` | PASS | Dry-run now reports the SSOT packet-review contract: `claude-opus-4-6`, `bypassPermissions`, `max_turns=8`, `allowed_tools=none`. |
| `bash scripts/codex-review.sh claude "Review this bounded packet only. Goal: validate whether the no-tools packet-review path can return a concise markdown result with Findings and Summary. Proposed change summary: self-contained prompt contract, no tool access by default unless explicitly enabled, claude-opus-4-6 default model, bypassPermissions default mode, max-turns 8 default, silence-timeout 300 default, dry-run reporting of the contract, and matching STANDARDS.md plus EXTERNAL_SERVICES_RUNBOOK.md updates. If there are no blocking issues, say so clearly."` | PASS | Governed wrapper returned a usable markdown review artifact at `docs/codex-reviews/2026-04-29-claude.md`. |
| `uv run pytest scripts/test_codex_fire.py scripts/test_cli_session_supervisor.py` | PASS | Focused regression suite passed: 18 tests green. |
| `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-29-issue-581-claude-review-path.md` | PASS | Cross-review artifact passed dual-signature validation. |
| `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS | Full governance local-CI profile passed. Report: `cache/local-ci-gate/reports/20260429T143716Z-hldpro-governance-git/`. |
| `git diff --check` | PASS | Final whitespace check passed. |

## Findings

- The defect is not base Claude auth or token bootstrap. The governed token and
  direct `claude -p` preflight succeed.
- The failing behavior came from the shared review contract, not the operator
  path name: the previous prompt wording invited repo exploration, the template
  defaulted to tool-capable behavior, and the turn ceiling was too tight for a
  bounded review.
- The repaired contract keeps the same operator-facing wrapper but narrows the
  runtime semantics to self-contained packet review with no tool access by
  default, which is enough to return a usable markdown verdict.
- ASC-Evaluator issue #15 can resume only after this governance-source fix is
  merged and replayed there.

## Next Step

Finalize the focused regression suite, write the reviewed issue-581 artifacts,
then push PR #582 so the governance-source fix can merge before returning to
ASC-Evaluator issue #15.
