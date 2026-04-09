# Phase 1 — Critic Evaluate Diff-Mode PDCA/R

Date: 2026-04-09
Issue: TBD (to be created in local-ai-machine)
Owner: nibargerb
Target Repo: local-ai-machine
Branch: `riskfix/critic-evaluate-diff-mode-20260409`

## Plan

Extend `/v2/critic/evaluate` to accept external diff-mode payloads from consumer repos (HealthcarePlatform, AIS) and create GitHub issues on REJECTED verdicts. This is the first cross-repo integration surface for the critic pipeline.

### Payload Contract (diff-mode)

New fields alongside existing internal pipeline fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `mode` | `"diff"` | yes | Distinguishes from internal pipeline mode |
| `repo` | string | yes | Caller repo identifier, e.g. `"NIBARGERB-HLDPRO/HealthcarePlatform"` |
| `sha` | string | no | Head commit SHA |
| `base_sha` | string | no | Base commit SHA for diff |
| `diff` | string | yes | Unified diff content |
| `prompt_template` | string | no | Caller-specific review prompt |
| `idempotency_key` | header | yes | Already required by existing endpoint |

Backward compatibility: existing internal callers continue unchanged. `mode` field absent = legacy behavior.

### Synthesizer Design

Wraps `generate_stub_bundle.py` (already exists, produces valid 9-artifact run bundles):

1. Call stub generator with fresh `run_id` → get 9 artifacts in valid default shape
2. Overwrite `drift_report.json` with diff-derived content
3. Overwrite `remediation_plan.json` with `prompt_template` shaped into schema
4. Overwrite `mask_attestation.json` with per-caller mask policy
5. Append `diff_mode_intake` event to `audit.jsonl`
6. Return `run_id` for pipeline pickup

~50-80 lines of glue code wrapping the existing stub generator.

### Mask Enforcement Strategy

- 6 existing masks in `masks.json` remain unchanged
- Add `phi_redaction_gate` mask (v1.0.0) with `required_artifacts: ["redaction_attestation.json"]`
- New `caller_mask_policy.json` in `runtime/` maps callers to active mask sets
- HP-App gets `phi_redaction_gate` active → fails until Phase 1.5 ships redactor
- AIS does NOT get `phi_redaction_gate` → passes without redaction
- Gatekeeper stays uniform — caller-awareness lives only in the diff-mode handler

### GitHub Issue Creation on REJECTED

- Uses existing `gh` CLI (v2.89.0, authed via keyring, full repo scope including issues:write)
- Labels: `critic-flagged` + severity label (`critic-critical`/`critic-high`/`critic-medium`/`critic-low`)
- Idempotent: check `gh_issue_url` column in jobs table before creating
- SQL migration: additive nullable `gh_issue_url text` column on `slm_inference_jobs`

### Consumer Interaction

- Polling-default (2-second interval on `/v2/critic/status?job_id=...`)
- Terminal states: `completed`, `failed`, `dead_letter`
- `CRITIC_ENABLED` feature flag in consumer CI for rollback

### PR Structure

Single PR, 8 ordered commits:

0. **Stub generator refactor** — extract `main()` body into importable `generate_bundle(run_id, base_dir)` function in `generate_stub_bundle.py`, keeping `if __name__ == "__main__"` as thin wrapper
1. **Mask addition** — `phi_redaction_gate` in `masks.json` + `caller_mask_policy.json` in `runtime/`
2. **SQL migration** — `gh_issue_url` column on `slm_inference_jobs`
3. **Diff-mode synthesizer** — `scripts/edge/diff_mode_synthesizer.py` calling `generate_bundle()` from refactored stub generator
4. **Handler dispatch** — `mode=diff` routing in `critic_api_postgres.py`, inserted BEFORE `apply_token_budget` (line ~2667) to skip internal pipeline prompt assembly
5. **Issue creation worker** — `scripts/edge/critic_issue_creator.py` using `subprocess.run([...], shell=False)` for `gh` CLI (no shell interpolation)
6. **Contract tests + fixtures** — `tests/test_diff_mode_contract.py` + fixtures
7. **Governance docs** — `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, `docs/SERVICE_REGISTRY.md`

### Security Guards (from Codex review)

- `MAX_DIFF_BYTES = 524288` (512 KB) — reject oversized diffs at handler level with 413
- `gh issue create` args passed as list to `subprocess.run(shell=False)` — no f-string/shell interpolation of `repo` field
- `repo` field validated against allowlist pattern `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`

### Dependencies (all verified)

- Phase 0.5 (Cloudflare Tunnel) ✅ DONE (PR #408 + #409)
- `generate_stub_bundle.py` exists at repo root ✅
- `test_mask_policy_contract.py` exists at `scripts/ops/` ✅
- `gh` CLI authed with full repo scope ✅

## Do

### Sprint 1: Foundation (mask + migration + synthesizer)

**Tasks:**
1. Add `phi_redaction_gate` mask to `masks.json`
2. Create `runtime/caller_mask_policy.json` with HP-App and AIS caller profiles
3. Add SQL migration `036_gh_issue_url.sql` to `runtime/sql/`
4. Create `scripts/edge/diff_mode_synthesizer.py`:
   - Import and call `generate_stub_bundle` with fresh run_id
   - Overwrite `drift_report.json` with diff payload content
   - Overwrite `remediation_plan.json` with prompt_template
   - Overwrite `mask_attestation.json` per caller_mask_policy
   - Append `diff_mode_intake` audit event

**Acceptance:**
- `masks.json` has 7 masks, `phi_redaction_gate` requires `redaction_attestation.json`
- `caller_mask_policy.json` maps HP-App → phi gate active, AIS → phi gate inactive
- Migration is additive (nullable column), backward compatible
- Synthesizer produces valid 9-artifact bundle with diff-derived overrides
- Existing `test_mask_policy_contract.py` still passes

### Sprint 2: Handler + issue creation + tests

**Tasks:**
1. Add `mode=diff` dispatch in `critic_api_postgres.py` `do_POST()`:
   - Check `payload.get("mode") == "diff"`
   - Validate required diff-mode fields (`repo`, `diff`)
   - Call synthesizer to produce run bundle
   - Enqueue job with synthesized payload
2. Create `scripts/edge/critic_issue_creator.py`:
   - Called by worker on REJECTED verdict
   - Check `gh_issue_url` column for idempotency
   - Create issue via `gh issue create` with labels
   - Update job record with `gh_issue_url`
3. Create `tests/test_diff_mode_contract.py`:
   - Test synthesizer produces valid bundle
   - Test diff-mode payload validation (required fields)
   - Test issue creation idempotency
   - Test caller mask policy resolution
4. Add test fixtures under `tests/fixtures/diff_mode/`

**Acceptance:**
- `/v2/critic/evaluate` with `mode: "diff"` returns 202 with job_id
- Legacy calls (no `mode` field) continue working unchanged
- REJECTED verdict triggers `gh issue create` with correct labels
- Duplicate idempotency_key does not create duplicate issue
- All contract tests pass

### Sprint 3: Governance docs

**Tasks:**
1. Update `docs/PROGRESS.md` with Phase 1 entry
2. Update `docs/FEATURE_REGISTRY.md` with diff-mode feature
3. Update `docs/SERVICE_REGISTRY.md` with new endpoints/scripts
4. Update `docs/DATA_DICTIONARY.md` with migration column

**Acceptance:**
- Doc co-staging requirements met for all changed source files
- Feature registry reflects diff-mode as `alpha`

## Check

Verification targets (automated, no HITL):

1. `python -m pytest tests/test_diff_mode_contract.py -v` — all pass
2. `python scripts/ops/test_mask_policy_contract.py` — still passes with 7th mask
3. `python -c "import json; json.load(open('masks.json'))"` — valid JSON
4. `python -c "import json; json.load(open('runtime/caller_mask_policy.json'))"` — valid JSON
5. `psql` or sqlite check: migration applies cleanly, column exists, nullable
6. Synthesizer dry-run: produces 9 artifacts in `var/runs/<run_id>/`
7. `gh auth status` confirms issue creation permissions

## Adjust

Potential adjustments discovered during Check:

- If `generate_stub_bundle.py` import path needs `sys.path` manipulation, fix in synthesizer
- If `gh` CLI auth scope is insufficient for cross-repo issue creation, document the gap and create follow-up issue
- If existing mask contract tests break due to mask count assumptions, update expected counts
- If `proof_bundle_schema.json` requires `redaction_attestation.json` globally (not just per-mask), the schema needs conditional update — issue-back rather than breaking existing flows

## Review

This slice is complete when:

1. Single PR merged to `develop` in local-ai-machine
2. All 7 commits present and ordered
3. Existing tests unbroken
4. New contract tests passing
5. `masks.json` has 7 masks
6. `caller_mask_policy.json` exists in `runtime/`
7. Migration `036_gh_issue_url.sql` exists and is additive
8. Diff-mode synthesizer produces valid bundles
9. Issue creation is idempotent on `gh_issue_url` column
10. Governance docs updated per co-staging rules

**Follow-up work (NOT in this slice):**
- Phase 1.5: PHI redactor producing `redaction_attestation.json` (HP-App blocked until then)
- Consumer CI integration (`CRITIC_ENABLED` flag wiring in HP-App/AIS)
- SSE streaming for diff-mode jobs (polling-only in Phase 1)
