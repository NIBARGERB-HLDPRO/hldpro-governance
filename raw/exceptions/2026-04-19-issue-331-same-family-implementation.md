# Same-Family Implementation Exception: Issue 331

Issue: NIBARGERB-HLDPRO/hldpro-governance#331  
Date: 2026-04-19  
Expires: 2026-04-26T00:00:00Z

## Exception

The same Codex/OpenAI model family may perform planning and implementation for this small no-HITL governance registry slice.

## Rationale

The implementation is expected to be a constrained registry disposition and generated/evidence artifact update. The downstream memory bootstrap has already been completed and validated in `seek-and-ponder#23`; governance code already derives memory integrity participation from the registry flag.

## Compensating Controls

- Issue-backed PDCAR and structured plan.
- Explicit execution scopes for planning and implementation.
- Subagent registry/memory review by Hubble.
- Attempt alternate-family review if Claude CLI is available before final merge.
- Deterministic final e2e gate covering registry validation, memory integrity, graphify target reconciliation, compendium check, issue staleness, backlog sync, and closeout hook.

## Scope Limit

This exception does not authorize script, workflow, product repo, or downstream memory content changes. If those become necessary, create a scope expansion or a new issue.
