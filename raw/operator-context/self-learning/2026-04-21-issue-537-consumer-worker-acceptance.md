# Self-Learning: Issue #537 Consumer Worker Acceptance

## Pattern

`consumer-worker-acceptance-evidence-gap`

## Trigger

Worker output can touch consumer-managed governance surfaces while the existing consumer verifier catches drift only after acceptance, or only when the operator remembers to run it. A typoed `--governance-root`, malformed `local_overrides`, or stale reusable workflow SHA must fail before a handoff can be marked accepted.

## Correction

- Resolve consumer verifier defaults from the supplied `--governance-root`.
- Require `verify_governance_consumer.py` validation commands and evidence refs for accepted handoffs touching consumer-managed paths.
- Normalize handoff evidence refs through safe repo-relative validation before Worker route approval.
- Keep stale workflow SHA mismatch and malformed `local_overrides` as direct regression fixtures.

## Retrieval Hints

- Search `consumer-worker-acceptance-evidence-gap` when a Worker handoff has consumer-managed files but no verifier command.
- Search `verify_governance_consumer.py` when downstream `.hldpro` records, reusable workflow refs, or `local_overrides` are involved.
- Search `handoff_evidence.evidence_paths` when Worker route approval is blocked by invalid evidence refs.
