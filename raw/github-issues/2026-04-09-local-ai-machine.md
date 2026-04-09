# GitHub Issues — local-ai-machine
Date: 2026-04-09

## #376: Fix docs progress path casing conflict on macOS
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary
Fix the tracked path-casing conflict between `docs/PROGRESS.md` and `docs/progress.md` so macOS worktrees can close out cleanly.

## Why
- Both paths are tracked with different contents in Git
- On a case-insensitive filesystem, touching one leaves persistent dirty state in the other
- This blocks clean closeout for governance-only lanes such as CODEOWNERS rollout PR #375

## Scope
- normalize the progress file path strategy to one canonical tracked path
- preserve the intended progre
---
## #374: Add CODEOWNERS baseline for GitHub Enterprise Sprint 1
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary
Add a minimal `.github/CODEOWNERS` baseline for GitHub Enterprise Sprint 1.

## Why
- Align local-ai-machine with staged GitHub Enterprise code-owner enforcement
- Keep code ownership explicit for workflows, governance docs, scripts, and core runtime surfaces
- Do not mix branch-protection or ruleset changes into the same lane

## Scope
- add `.github/CODEOWNERS`
- keep first-pass ownership mapping conservative
- update required governance status docs only if repo rules require it

##
---
## #373: Unblock CODEOWNERS lane by restoring Python 3.11 session-lock tooling
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary
Restore the repo-required session lock/startup toolchain so a governed CODEOWNERS lane can be opened safely.

## Current Blocker
The repo requires `scripts/ops/session_lock.py acquire <branch-name>` before work starts, but the current machine only has Python 3.9.6 available as `python3`. The lock script uses Python 3.10+ type syntax and fails before startup can proceed.

## Why This Matters
- `AGENTS.md` requires session lock + isolated worktree startup before edits
- GitHub Enterpris
---
## #369: Doc consistency scaffolding for governance docs
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary
Bring local-ai-machine governance docs into the shared minimum contract without forcing a fake full-schema format.

## Scope
- add or tighten docs/FEATURE_REGISTRY.md
- tighten docs/DATA_DICTIONARY.md metadata/source-of-truth wording
- keep docs/PROGRESS.md as the repo backlog source of truth

## Acceptance Criteria
- FEATURE_REGISTRY exists with required metadata and summary-table contract
- DATA_DICTIONARY has clear source-of-truth metadata
- PROGRESS reflects the scoped doc-consist
---
## #360: Nightly reliability failure: microvm-smoke-nightly (24024202964)
Labels: ops, nightly-failure | Created: 2026-04-06 | Updated: 2026-04-06

Workflow run: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/actions/runs/24024202964
Job: microvm-smoke-nightly
Action required: run microvm smoke triage flow in OPERATIONS_TRIAGE_RUNBOOK.md
---
## #357: Nightly reliability failure: microvm-smoke-nightly (23996946804)
Labels: ops, nightly-failure | Created: 2026-04-05 | Updated: 2026-04-05

Workflow run: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/actions/runs/23996946804
Job: microvm-smoke-nightly
Action required: run microvm smoke triage flow in OPERATIONS_TRIAGE_RUNBOOK.md
---
## #355: Nightly reliability failure: microvm-smoke-nightly (23974260969)
Labels: ops, nightly-failure | Created: 2026-04-04 | Updated: 2026-04-04

Workflow run: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/actions/runs/23974260969
Job: microvm-smoke-nightly
Action required: run microvm smoke triage flow in OPERATIONS_TRIAGE_RUNBOOK.md
---
## #352: Nightly reliability failure: microvm-smoke-nightly (23938502777)
Labels: ops, nightly-failure | Created: 2026-04-03 | Updated: 2026-04-03

Workflow run: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/actions/runs/23938502777
Job: microvm-smoke-nightly
Action required: run microvm smoke triage flow in OPERATIONS_TRIAGE_RUNBOOK.md
---
## #219: Nightly reliability failure: control-plane-and-retention (23105810428)
Labels: ops, nightly-failure | Created: 2026-03-15 | Updated: 2026-03-15

Workflow run: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/actions/runs/23105810428
Job: control-plane-and-retention
Action required: inspect failed step and apply remediation from OPERATIONS_TRIAGE_RUNBOOK.md
---
## #169: Slack HITL async approvals suppressed by follow-up prompt/context mismatch
Labels: none | Created: 2026-03-10 | Updated: 2026-03-10

Title: Slack HITL async approvals suppressed because webhook follow-up prompt omits bridge-parsable HITL context

Summary
The Slack HITL async path is broken after approval handoff because the webhook follow-up prompt builder emits plain `run_id=...`, `step_id=...`, and `pending_action_id=...` lines instead of one of the two HITL context formats accepted by `scripts/control_plane/cli_bridge.ts`.

Impact
- In `SLACK_HITL_BUTTON_MODE=hitl_async`, the CLI bridge suppresses decision buttons when it 
---