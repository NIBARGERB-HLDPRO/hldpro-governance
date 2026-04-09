# Dispatcher Never Answers Directly

Date: 2026-04-09

## Decision
The governance `CLAUDE.md` acts as a dispatcher only when an overlord agent exists for the task.

## Why
- Preserves the routing model from the source plan
- Forces use of pre-session context reads
- Keeps governance work aligned with the agent contract

## Links
- [Raw conversation seed](../../raw/conversations/2026-04-09-dispatcher-pattern.md)
