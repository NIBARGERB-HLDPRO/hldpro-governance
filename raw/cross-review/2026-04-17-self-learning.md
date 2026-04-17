# Cross-Review — Issue #230 Self-Learning and Self-Healing Loop

Date: 2026-04-17
Issue: #230
Reviewer: Claude Opus 4.6
Reviewed worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-230-self-learning-20260417`
Verdict: APPROVED_WITH_REQUIRED_CHANGES
Final disposition: Accepted after required changes

## Scope

Read-only alternate-family review of the #230 self-learning diff:

- `scripts/orchestrator/self_learning.py`
- `scripts/orchestrator/test_self_learning.py`
- packet queue repeated-failure halt
- packet schema `known_failure_context`
- weekly sweep report wiring
- governance-surface classifier update
- registry and data dictionary documentation

## Findings

### F1 — `record_failure` issue number lacked upper bound

Severity: high
Status: resolved

Reviewer finding: `record_failure()` rejected zero and negative issue numbers but did not bound extremely large positive values before placing the issue number in an output filename.

Resolution: added an accepted range of `1..999999` and test coverage for zero and out-of-range issue numbers.

### F2 — PII halt reason could be hidden by repeated-failure halt

Severity: medium
Status: resolved

Reviewer finding: repeated known-failure halt ran before the PII-mode LAM-role halt. A packet with both conditions would still halt, but the audit reason would not surface the PII invariant.

Resolution: moved the PII-mode LAM-role check before repeated known-failure context evaluation and added a precedence regression test.

### F3 — Weekly sweep self-learning report fails the sweep on error

Severity: low advisory
Status: accepted

Resolution: accepted intentionally. A malformed learning corpus means the weekly learning report cannot be trusted, so the sweep should fail rather than silently publish stale or incomplete learning state.

### F4 — Packet enrichment wrote `score` outside schema

Severity: medium
Status: resolved

Reviewer finding: `enrich_packet()` serialized the full `LearningMatch`, including `score`, into `governance.known_failure_context`, but schema items have `additionalProperties: false`.

Resolution: packet enrichment now writes only schema fields: `title`, `summary`, `source_path`, `evidence_paths`, and `repeat_count`. Added a regression assertion that `score` is not injected.

### F5 — Missing test for invalid issue number write-back

Severity: low advisory
Status: resolved

Resolution: added `test_record_failure_rejects_out_of_range_issue_numbers`.

## Accepted Review Notes

The reviewer verified that:

- Self-learning lookup is deterministic and local.
- No model inference, network calls, subprocesses, packet payload execution, `exec`, or `eval` paths exist.
- Injected packet context cites direct source files through `evidence_paths`.
- Graphify and compendium content are used only as attention tokens.
- Novel failure write-back creates new files under `raw/operator-context/self-learning/` and does not overwrite existing files.
- Schema compatibility is preserved because `known_failure_context` is optional.

## Result

All required review changes were applied before closeout validation.
