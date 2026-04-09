# Decision: Governance Repo Is the Knowledge Home
Date: 2026-04-09
Source: Claude.ai session
Session URL: internal-session

## Context
The Living Knowledge Base needed one canonical location so graph artifacts, wiki pages, closeouts, and raw feeds would not fragment across governed repos.

## Decision Made
All tracked knowledge-base infrastructure lives in `hldpro-governance`; product repos get read-only pointers and local runtime hooks only.

## Rationale
This keeps the memory layer centralized, avoids duplicated graph artifacts across repos, and makes weekly sweep write-back controllable from one governance surface.

## Links To
- [wiki/decisions/2026-04-09-governance-is-knowledge-home.md](../../wiki/decisions/2026-04-09-governance-is-knowledge-home.md)
