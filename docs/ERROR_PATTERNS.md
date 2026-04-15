# ERROR_PATTERNS

Reusable solutions to recurring governance failures. See `docs/schemas/error-patterns.schema.md` for the canonical schema.

## Contributing

When a pattern emerges from one or more incidents in `FAIL_FAST_LOG.md`, document it here following the schema:

1. Create a new `## pattern-id` section (kebab-case name, e.g., `overlord-sweep-stale-checkout`)
2. Fill in: Symptom, Root Cause, Detection, Resolution Playbook, Instances
3. Optional: Prevention (can be empty for Phase 1)
4. Reference the pattern in your `FAIL_FAST_LOG.md` entries

See `docs/schemas/error-patterns.schema.md` for examples and detailed field semantics.

## Phase 1 Stub

This file is a stub placeholder during Phase 1. Patterns will be populated in Phase 2 as incidents occur and are logged in `FAIL_FAST_LOG.md`.
