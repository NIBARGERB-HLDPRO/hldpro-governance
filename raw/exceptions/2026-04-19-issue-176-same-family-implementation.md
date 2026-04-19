# Same-Family Implementation Exception: Issue 176

Issue: NIBARGERB-HLDPRO/hldpro-governance#176  
Date: 2026-04-19  
Expires: 2026-04-26T00:00:00Z

## Exception

The same Codex/OpenAI model family may perform planning and implementation for this small no-HITL governance documentation reconciliation.

## Rationale

The slice is constrained to documenting the observed live compatibility between ASC-Evaluator's existing Governance Gate workflow and its knowledge-repo code-governance exemption. The downstream workflow is already green on `master`, so the implementation does not modify product code or reusable workflow logic.

## Compensating Controls

- Issue-backed PDCAR and structured plan.
- Explicit execution scope for implementation.
- Read-only ASC-Evaluator workflow and GitHub Actions evidence.
- Governance Local CI Gate and GitHub PR checks before merge.
- Stage 6 closeout before #176 is closed.

## Scope Limit

This exception does not authorize downstream ASC-Evaluator writes, reusable workflow changes, ruleset changes, or bypassing CI.
