# Stage 6 Closeout
Date: 2026-04-09
Repo: local-ai-machine
Task ID: Phase 1 critic diff-mode (riskfix/critic-evaluate-diff-mode-20260409)
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made
Extend /v2/critic/evaluate with diff-mode for external consumer repos and GitHub issue creation on REJECTED verdicts, using a synthesizer wrapper around the existing stub generator.

## Pattern Identified
External integrations should wrap existing generators (stub/proof bundles) rather than duplicating artifact creation logic. Per-caller policy files in runtime/ keep caller-awareness out of the gatekeeper.

## Contradicts Existing
None — this is additive. The existing internal pipeline flow is unchanged (mode absent = legacy behavior).

## Files Changed
- `generate_stub_bundle.py` — refactored to expose `generate_bundle()` as importable function
- `masks.json` — added `phi_redaction_gate` (7th mask)
- `runtime/caller_mask_policy.json` — new per-caller mask activation policy
- `runtime/sql/036_gh_issue_url.sql` — nullable column migration
- `scripts/edge/diff_mode_synthesizer.py` — new synthesizer wrapping stub generator
- `scripts/edge/critic_api_postgres.py` — mode=diff dispatch branch
- `scripts/edge/critic_issue_creator.py` — new issue creation worker
- `tests/test_diff_mode_contract.py` — 18 contract tests
- `tests/fixtures/diff_mode/sample_diff_payload.json` — test fixture
- `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/SERVICE_REGISTRY.md`, `docs/DATA_DICTIONARY.md`

## Wiki Pages Updated
- wiki/local-ai-machine/ should get an article on the diff-mode critic integration pattern when the next graphify cycle runs

## operator_context Written
[ ] No — reason: operator_context rows are runtime-only; this slice adds code artifacts tracked in governance docs

## Links To
- Phase 0.5 (Cloudflare Tunnel): PR #408 + #409
- Phase 1.5 (PHI redactor): follow-up, not yet started
- Governance PDCAR: docs/plans/phase1-critic-diff-mode-pdcar.md
- Structured plan: docs/plans/phase1-critic-diff-mode-structured-agent-cycle-plan.json
