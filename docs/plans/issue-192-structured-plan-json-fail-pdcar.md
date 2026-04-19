# Issue #192 - Structured Plan JSON Failure Contract PDCA/R

## Plan

Issue #192 fixes a CI/operator feedback bug in `scripts/overlord/validate_structured_agent_cycle_plan.py`: malformed `*structured-agent-cycle-plan.json` files currently raise a raw Python traceback instead of the validator's structured `FAIL ...` output.

Scope stays narrow:

- Replace unsafe plan JSON loading with a safe loader that records `FAIL <path>: could not parse JSON: ...`.
- Ensure malformed plans are skipped for semantic validation after the parse failure is recorded.
- Cover both full-repo validation and governance-surface matching-plan lookup, since both paths load plan JSON.
- Preserve valid-plan behavior.
- Record issue-backed validation, execution-scope, and closeout evidence.

Out of scope:

- Changing the structured plan schema.
- Reworking governance-surface matching semantics.
- Fixing unrelated open issues surfaced by existing backlog/progress mirrors.

## Do

Implementation adds `_load_json_safe(path, root, failures)` and routes both `_matching_plan_payloads` and the main validation loop through it. The helper catches `json.JSONDecodeError` and `OSError`, appends a structured failure with a repo-relative path when possible, and returns `None` so the caller skips object-level validation for unreadable JSON.

Focused tests prove:

- malformed plan JSON returns exit code 1;
- output starts with `FAIL docs/plans/...: could not parse JSON: ...`;
- no traceback is emitted;
- malformed JSON during governance-surface matching does not crash;
- valid existing behavior still passes.

## Check

Acceptance criteria:

- Malformed JSON file produces structured `FAIL <path>: could not parse JSON: ...` output.
- Malformed JSON exits `1`, not an unhandled traceback path.
- Valid JSON still validates normally.
- Existing focused tests continue to pass.
- Final e2e AC: run the validator against a temp malformed plan and against the full repo plan set, then run execution-scope and Local CI gates.

## Adjust

If the parser encounters multiple malformed plan files, each should produce its own structured failure. Do not short-circuit after the first parse failure because CI should list all unreadable plan artifacts in one run.

## Review

Reviewer focus:

- No remaining unsafe `_load_json` path.
- Failure output is structured and operator-readable.
- Regression tests exercise both parse paths.
- Scope stays limited to the validator, tests, and governance evidence.
