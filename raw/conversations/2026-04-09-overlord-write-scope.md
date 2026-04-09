# Decision: Overlord Agents Stay Read-Only
Date: 2026-04-09
Source: Claude.ai session
Session URL: internal-session

## Context
Adding a knowledge base increased the temptation to let many agents mutate governance state directly.

## Decision Made
The overlord agents remain read-only; only the controlled weekly sweep and closeout/write-back path mutate wiki or graph artifacts.

## Rationale
This keeps write scope bounded for a solo operator and makes automated changes easier to audit.

## Links To
- [wiki/decisions/2026-04-09-overlord-write-scope-is-bounded.md](../../wiki/decisions/2026-04-09-overlord-write-scope-is-bounded.md)
