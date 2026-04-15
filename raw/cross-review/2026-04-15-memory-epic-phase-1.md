---
pr_number: 136
pr_scope: standards
drafter: "claude-opus-4-6 + claude-haiku-4-5-20251001 (cross_drafter)"
reviewer: "gpt-5.4 high"
signature_date: "2026-04-15"
verdict: REJECTED
---

**Summary**

PR #136 is not ready as a governance standards PR. The high-level shape is right: it adds canonical schema docs, a reusable workflow, a governance thin caller, an `ERROR_PATTERNS.md` stub, and legacy frontmatter for the existing `FAIL_FAST_LOG.md`. However, the implementation has correctness defects in the validator, internal schema inconsistencies, and scope contamination from orchestration handoff artifacts. Most importantly, `ERROR_PATTERNS` validation is currently broken for real pattern sections because it extracts the wrong heading text, the documented schema examples conflict with the validator’s required `## Pattern: <id>` form, and the PR introduces non-schema handoff files that violate the stated governance-only re-scope.

**Must-fix**

- `docs/schemas/error-patterns.schema.md` is internally inconsistent: the canonical rule says headers must be `## Pattern: <kebab-case-id>`, but the “Example Pattern (full)” uses `## github-actions-node-deprecation` without `Pattern:`. The stub also tells contributors to create `## pattern-id`, which contradicts the schema and validator.

- `ERROR_PATTERNS` validator extracts pattern sections incorrectly. It finds IDs with `^## Pattern: ([\w-]+)$`, but then searches with `content.find(f"## {pattern_id}")`. For a valid section like `## Pattern: foo`, that search fails because the actual text is `## Pattern: foo`, not `## foo`. As written, required subsection validation is silently skipped for every valid pattern.

- Pattern ID validation claims “kebab-case” but accepts underscores because it uses `[\w-]+`. It should reject `_` and likely enforce something like `^[a-z0-9]+(?:-[a-z0-9]+)*$`.

- The reusable workflow defines `SCHEMA_PATH` and accepts `schema_fail_fast_path` / `schema_patterns_path`, but it never reads or validates either schema file. That means the schema inputs are cosmetic and schema presence/consistency is not actually enforced.

- `FAIL_FAST_LOG` schema says every entry MUST reference an existing pattern in `ERROR_PATTERNS.md`, and the CI Validation section says the workflow verifies pattern references. The validator does not check related-pattern existence at all. Either implement that check or weaken the schema text for Phase 1.

- `FAIL_FAST_LOG` docs use `Related Pattern` as the column name, while the validator accepts a header containing `Date` and `Category` only, then assigns the seventh column to `pattern`. The error message says the expected header is `Pattern`, not `Related Pattern`. Pick one canonical column name and enforce it.

- `ERROR_PATTERNS.md` stub is not aligned with the canonical schema. It gives contributor instructions for `## pattern-id`, not `## Pattern: pattern-id`, and lists `Instances` as required even though the schema says optional.

- Legacy marker detection is inconsistent. `FAIL_FAST_LOG` uses a frontmatter parser fallback, while `ERROR_PATTERNS` treats any occurrence of `legacy: true` anywhere in the file as legacy. That can false-skip validation if the phrase appears in documentation or examples.

- The workflow’s `pull_request.paths` only includes `.github/workflows/check-fail-fast-*.yml`; changes to `docs/schemas/*.md` do not trigger validation. For a standards PR, schema changes must trigger the check.

- Scope discipline is violated by adding `raw/handoff/2026-04-15-memory-epic-halt-phase-1.md` and `raw/handoff/2026-04-15-memory-epic-orchestration-handoff.md`. These are orchestration/process artifacts, not canonical schema, validator, thin caller, stub, or legacy-grandfathering changes. They also contain claims about caller repos and prior orchestration state, which conflicts with the “governance-only after 2026-04-15 re-scope” boundary.

- The added handoff file `raw/handoff/2026-04-15-memory-epic-orchestration-handoff.md` asserts broader cross-repo completion and mentions caller PRs. That is directly out of scope for this re-scoped PR and should be removed or moved to the appropriate issue/artifact outside this standards PR.

**Nice-to-have**

- Move the inline Python validator into a committed script, for example under `scripts/validate_fail_fast_schema.py`, and have the workflow call it. The current heredoc is hard to test locally and falls short of the stated “reusable Python validator” deliverable.

- Add at least one positive and one negative fixture for both schemas so future reviewers can verify the validator without relying on GitHub Actions behavior.

- Use deterministic ordering in error messages for valid category sets; printing a Python set can produce noisy diffs/logs.

- Consider validating real calendar dates with `datetime.date.fromisoformat`, not just `YYYY-MM-DD` shape.

**Notes**

The workflow caller itself correctly uses a relative reusable workflow reference, not an `@main` circular reference. The pinned action versions satisfy the requested `actions/checkout@v6` and `actions/setup-python@v5` check, and both workflows set `permissions: contents: read`.

The pattern-heading regex does satisfy the narrow requirement of matching only `## Pattern: <id>` and not boilerplate headings like `## Contributing`. The problem is downstream section extraction and the schema/stub examples contradicting that rule.

No enforcement-index changes are present in the diff, which is correct for this PR’s stated scope. The rejection is based on validator correctness, schema consistency, and out-of-scope artifacts, not on missing caller-repo changes.