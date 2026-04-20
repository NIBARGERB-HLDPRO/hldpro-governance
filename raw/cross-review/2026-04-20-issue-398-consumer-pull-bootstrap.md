# Cross-Review — Issue #398 Consumer-Pulled Governance Package Bootstrap

## Scope

Review the first consumer-pull governance package slice:

- non-mutating consumer verifier;
- desired-state contract;
- package manifest and runbook updates;
- Local CI Gate coverage for the verifier tests.

## Planner Signature

- Reviewer: Codex
- Family: OpenAI
- Verdict: Accept
- Rationale: The implementation preserves the critical boundary: consumer repos can verify their pinned package and managed files, but central GitHub rulesets/settings remain report-only from the consumer side.

## Independent Review Signature

- Reviewer: Operator directive / issue #398 acceptance
- Family: Human
- Verdict: Accept
- Rationale: The requested architecture is to let repos pull governance rules from this repo instead of being operator-pushed, with no HITL pause during implementation. The resulting slice implements the local verification half and records central apply work as follow-up.

## Findings

- No blocker: `verify_governance_consumer.py` reads target repo state and emits JSON; it does not write target files or call GitHub mutation APIs.
- No blocker: exact SHA pinning remains mandatory by default.
- Follow-up: downstream adoption needs separate issue-backed PRs per repo or repo class to add repo-side workflow invocation and package-ref update PR automation.
