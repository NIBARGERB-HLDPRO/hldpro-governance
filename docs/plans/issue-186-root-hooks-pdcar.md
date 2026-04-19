# PDCAR - Issue #186 Root-Level Enforcement Hooks

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/186
Branch: `fix/issue-186-root-hooks`

## Plan

Add the three missing repo-root local governance hook entrypoints named in issue #186:

- `hooks/governance-check.sh`
- `hooks/backlog-check.sh`
- `hooks/check-errors.sh`

Keep the slice narrow. The hooks should expose local smokeable entrypoints over existing governance enforcement logic rather than introducing a separate policy engine.

## Do

- Add portable root resolution that works from the repo root and nested working directories.
- Wire `governance-check.sh` to structured-plan validation, governance-surface changed-file validation, backlog alignment, and whitespace checking.
- Wire `backlog-check.sh` to the existing `OVERLORD_BACKLOG.md` to GitHub issue alignment validator.
- Wire `check-errors.sh` to the same minimal FAIL_FAST_LOG and ERROR_PATTERNS schema contract used by the reusable workflow.
- Mark all three scripts executable.
- Record structured plan, execution scope, validation, and Stage 6 closeout artifacts.
- Update local progress/backlog mirrors.

## Check

Required checks:

- `bash -n` on all three hook scripts.
- Executable-bit check for all three hook scripts.
- Root smoke tests for all three hooks.
- Nested-directory smoke tests for all three hooks.
- Structured-plan and execution-scope JSON validation.
- Governance-surface plan gate against the changed-file set.
- Execution-scope assertion against the changed-file set.
- Backlog alignment.
- Local CI Gate.
- Stage 6 closeout hook.

## Adjust

If a hook requires broader policy than already exists in this repo, create a follow-up issue rather than expanding #186. If smoke testing exposes an existing validator blocker unrelated to these hooks, record the blocker and keep the implementation scoped to root hook availability.

## Review Notes

The root hook names are local entrypoints. They do not replace the reusable GitHub workflows; they make the same enforcement surfaces discoverable and executable from this repository's tracked `hooks/` directory.
