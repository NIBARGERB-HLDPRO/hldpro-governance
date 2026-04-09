# Decision: Graphify AIS First
Date: 2026-04-09
Source: Claude.ai session
Session URL: internal-session

## Context
The plan covered multiple governed repos, but the first production graph needed to maximize value quickly while avoiding HIPAA/privacy ambiguity.

## Decision Made
The initial graphify run targets `ai-integration-services` only.

## Rationale
AIS has the highest architectural complexity and daily cognitive load, while HealthcarePlatform remains gated on the HIPAA documentation extraction boundary.

## Links To
- [wiki/decisions/2026-04-09-graphify-on-ais-first.md](../../wiki/decisions/2026-04-09-graphify-on-ais-first.md)
