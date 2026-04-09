# Decision: Governance CLAUDE Is Dispatcher-Only
Date: 2026-04-09
Source: Claude.ai session
Session URL: internal-session

## Context
Governance requests were drifting between direct answers and agent delegation, which undermined the planned operating model.

## Decision Made
`hldpro-governance/CLAUDE.md` is a pure dispatcher and must not answer directly when an overlord agent covers the task.

## Rationale
The dispatcher pattern keeps routing behavior explicit and makes pre-session knowledge-base reads part of the governance contract.

## Links To
- [wiki/decisions/2026-04-09-dispatcher-never-answers-directly.md](../../wiki/decisions/2026-04-09-dispatcher-never-answers-directly.md)
