# Society of Minds — Exception Register

Prepared: 2026-04-14
Canonical standard: [`STANDARDS.md §Society of Minds`](../STANDARDS.md)

## Purpose

Track approved deferrals of the Society of Minds routing standard per rule, repo, and expiry. Enforced by `overlord-sweep` — past-expiry entries auto-open issues.

## Entry schema (required fields)

- `rule_id` — stable identifier, format `SOM-<AREA>-<NNN>` (e.g. `SOM-PII-001`, `SOM-BOOTSTRAP-001`)
- `repo` — repository where the exception applies
- `deferral_reason` — must cite the missing enforcement artifact or repo-specific blocker
- `approver` — human name (solo-operator: `nibargerb`)
- `approval_date` — `YYYY-MM-DD`
- `expiry_date` — `YYYY-MM-DD` (maximum 90 days from approval_date)
- `review_cadence` — `monthly` minimum
- `status` — `active` | `expired` | `renewed` | `closed`

## Approval authority

- Standards / routing exceptions: `nibargerb` (Platform + Engineering leadership — solo operator mapping)
- All exceptions beyond 90 days require a fresh approval (not a renewal)

## Active exceptions

### `SOM-BOOTSTRAP-001` — Society of Minds bootstrap PR cannot self-enforce `require-cross-review.yml`

- **rule_id:** `SOM-BOOTSTRAP-001`
- **repo:** `hldpro-governance`
- **deferral_reason:** The PR that introduces the Society of Minds charter and the `require-cross-review.yml` reusable workflow is adding the workflow in the same PR — the workflow cannot validate its own introducing PR. Tier 1 cross-review was completed out-of-band via `raw/cross-review/2026-04-14-society-of-minds-charter.md` (Architect-Claude `claude-opus-4-6` drafter + Architect-Codex `gpt-5.4 high` reviewer, verdict `APPROVED_WITH_CHANGES` with all 6 required changes resolved in the revised plan).
- **approver:** `nibargerb`
- **approval_date:** 2026-04-14
- **expiry_date:** 2026-04-21 (expires on merge of the introducing PR — short expiry because the exception evaporates the moment the workflow it supersedes is live)
- **review_cadence:** monthly
- **status:** `active`

### `SOM-EXEMPT-ASC-001` — ASC-Evaluator knowledge repo exempt from code governance CI

- **rule_id:** `SOM-EXEMPT-ASC-001`
- **repo:** `ASC-Evaluator`
- **deferral_reason:** ASC-Evaluator is explicitly exempt from HLD Pro code governance per `STANDARDS.md §Exceptions` ("ASC-Evaluator: knowledge repo, exempt from code governance"). It has no `.github/workflows/` infrastructure and consists primarily of knowledge artifacts. Society of Minds adoption is limited to a `CLAUDE.md §Society of Minds — Model Routing (SoT pointer)` block; no CI workflows are wired.
- **approver:** `nibargerb`
- **approval_date:** 2026-04-14
- **expiry_date:** 2026-07-14 (90-day review — at which point either re-approve or evaluate whether the repo has grown into code-governance scope)
- **review_cadence:** monthly
- **status:** `active`

### `SOM-ASC-CI-001` — ASC-Evaluator governance-check fails on knowledge repo

- **rule_id:** `SOM-ASC-CI-001`
- **repo:** `ASC-Evaluator`
- **deferral_reason:** Pre-existing `governance-check` workflow in ASC-Evaluator requires governance docs (PROGRESS.md, FEATURE_REGISTRY.md, etc.) that this repo is explicitly exempt from per STANDARDS §Exceptions and SOM-EXEMPT-ASC-001. The adoption PR (NIBARGERB-HLDPRO/ASC-Evaluator#4) adds only a CLAUDE.md pointer; the CI failure is unrelated and pre-existing. Blocks merge until reconciled.
- **approver:** `nibargerb`
- **approval_date:** 2026-04-14
- **expiry_date:** 2026-05-14 (30 days)
- **review_cadence:** monthly
- **status:** `active`
- **follow-up:** update ASC-Evaluator's governance.yml workflow to opt out or inherit the exemption

### `SOM-LAM-BRANCH-001` — SoM adoption PRs don't match local-ai-machine riskfix/* branch convention

- **rule_id:** `SOM-LAM-BRANCH-001`
- **repo:** `local-ai-machine`
- **deferral_reason:** `breaker-mcp-contract` workflow requires PR head branch match `riskfix/*`. The Society of Minds adoption uses `chore/adopt-society-of-minds` (PR #431) and `feat/som-mcp-daemon` (PR #432) per standard SoM branch naming. Reconciling the two conventions is out of scope for the adoption. Renaming branches post-facto would force PRs closed and disrupt the audit chain.
- **approver:** `nibargerb`
- **approval_date:** 2026-04-14
- **expiry_date:** 2026-05-14 (30 days)
- **review_cadence:** monthly
- **status:** `resolved`
- **resolution_date:** 2026-04-16
- **resolution:** The two conventions are explicitly complementary, not conflicting. `riskfix/<slug>-YYYYMMDD` is the designated LAM high-risk lane prefix in `local-ai-machine`, governed by LAM-local policy (mandatory date suffix, one PR per lane family enforced by `breaker-mcp-contract`). All other work — including in `local-ai-machine` — uses the standard SoM prefixes (`feature/`, `fix/`, `docs/`, `chore/`). `STANDARDS.md` branch naming rule now documents this explicitly. No ambiguity remains. See hldpro-governance PR #175.
- **closed_by:** `nibargerb`

### `SOM-WIN-OLLAMA-PII-001` — PII middleware enforcement deferred to Sprint 2

- **rule_id:** `SOM-WIN-OLLAMA-PII-001`
- **repo:** hldpro-governance
- **deferral_reason:** Invariant #8 (PII floor) requires `pii-patterns.yml` middleware + `scripts/windows-ollama/submit.py` before Windows-Ollama payloads are accepted. Stage A (this PR) lands standards + runbook only. Submission path + middleware + CI gate land in Sprint 2 (submit.py + PII middleware) and Sprint 4 (CI validator). Windows rung remains disabled until Sprint 5.
- **approver:** nibargerb
- **approval_date:** 2026-04-15
- **expiry_date:** 2026-05-15 (30 days; Stage B Sprint 2 must land before then)
- **review_cadence:** weekly during overlord-sweep
- **status:** CLOSED — Sprint 6 remediation merge (commit refs to be backfilled with actual PR merge SHA)
- **reopen_date:** 2026-04-15
- **reopen_reason:** Sprint 6 remediation revalidates the Windows-Ollama routing and audit controls; temporary reopen for final verification.
- **closure_reason:** PII middleware fully active via Sprint 2 `submit.py` + Sprint 5 `decide.sh` routing gate. All payloads validated against `pii_patterns.yml` before submission. Invariant #8 enforced.
- **reclose_reason:** Re-closed as `CLOSED` during Sprint 6 merge — all PII probes tested and passing (email, SSN, phone all correctly HALT); routing decision tree validated end-to-end.
- **closure_date:** 2026-04-15

### `SOM-WIN-OLLAMA-AUDIT-001` — Audit trail + CI validation deferred to Sprints 3–4

- **rule_id:** `SOM-WIN-OLLAMA-AUDIT-001`
- **repo:** hldpro-governance
- **deferral_reason:** Invariant #10 requires hash-chain audit + HMAC signing + daily manifest + CI schema validator. Stage A lands standards only. Audit writer (`audit.py` + `verify_audit.py`) lands in Sprint 3; CI gate (`check-windows-ollama-audit-schema.yml`) lands in Sprint 4. Windows rung remains disabled until Sprint 5. **Partially closed — CI enforcement live as of Sprint 4; full close deferred to Sprint 5 activation.**
- **approver:** nibargerb
- **approval_date:** 2026-04-15
- **expiry_date:** 2026-05-15 (30 days; Sprint 5 must land activation before then)
- **review_cadence:** weekly during overlord-sweep
- **status:** CLOSED — Sprint 6 remediation merge (commit refs to be backfilled with actual PR merge SHA)
- **reopen_date:** 2026-04-15
- **reopen_reason:** Sprint 6 remediation revalidates exception lifecycle with stronger secret-enforcement controls.
- **closure_reason:** Audit trail fully enforced via Sprint 3 `audit.py` + `verify_audit.py` and Sprint 4 CI gate `check-windows-ollama-audit-schema.yml`. Hash-chain, HMAC, and manifest validation live. Invariant #10 enforced.
- **reclose_reason:** Re-closed as `CLOSED` during Sprint 6 merge — HMAC secret enforcement verified live in CI workflow; audit schema validation confirmed working.
- **closure_date:** 2026-04-15

### `SOM-WIN-OLLAMA-DISABLED-001` — Windows rung documented but disabled during Phase 1

- **rule_id:** `SOM-WIN-OLLAMA-DISABLED-001`
- **repo:** hldpro-governance
- **deferral_reason:** Invariants #8–#10 and enforcement rows 13–15 are documented in Stage A (this PR), but the Windows rung remains **disabled** in the active ladder until all hard controls land. Stage A changes the charter to "documented / disabled until Sprint 5" to prevent accidental use. PII middleware (Sprint 2), audit trail (Sprint 3), CI gates (Sprint 4), and activation gate (Sprint 5) must all pass before the rung is live.
- **approver:** nibargerb
- **approval_date:** 2026-04-15
- **expiry_date:** 2026-05-15 (30 days; Sprint 5 must land activation before then)
- **review_cadence:** weekly during overlord-sweep
- **status:** CLOSED — Sprint 6 remediation merge (commit refs to be backfilled with actual PR merge SHA)
- **reopen_date:** 2026-04-15
- **reopen_reason:** Sprint 6 remediation re-checks the active rung state and related controls.
- **closure_reason:** Windows-Ollama Tier-2 rung now ACTIVE. All three prerequisite controls live (PII middleware Sprint 2, audit trail Sprint 3, CI gates Sprint 4, and routing decision tree Sprint 5). Rung transitions from documented/disabled to active in Tier-2 ladder per STANDARDS.md. Invariants #8–#10 enforced.
- **reclose_reason:** Re-closed as `CLOSED` during Sprint 6 merge — all 8 must-fixes from gpt-5.4 post-hoc review addressed and tested; Tier-2 routing restored to fully functional state.
- **closure_date:** 2026-04-15

## Active exceptions (temporary)

(none currently)

## Expired or closed exceptions

### `SOM-LAM-BRANCH-001` — RESOLVED

Status: resolved 2026-04-16 (hldpro-governance #175). The `riskfix/<slug>-YYYYMMDD` convention and the standard SoM prefixes are now documented as complementary in `STANDARDS.md`. No ambiguity remains; exception retired.

### `SOM-WIN-OLLAMA-PII-001` — CLOSED

Status: closed 2026-04-15. Re-opened during Sprint 6 validation and re-closed after final verification. PII middleware is enforced via Sprint 2 `submit.py` + Sprint 5 `decide.sh` routing gate.

### `SOM-WIN-OLLAMA-AUDIT-001` — CLOSED

Status: closed 2026-04-15. Re-opened during Sprint 6 validation and re-closed after final verification. Audit trail enforced via Sprint 3 writers + Sprint 4 CI gate.

### `SOM-WIN-OLLAMA-DISABLED-001` — CLOSED

Status: closed 2026-04-15. Re-opened during Sprint 6 validation and re-closed after final verification. Rung activated in Sprint 5; transitions from documented/disabled to active.
