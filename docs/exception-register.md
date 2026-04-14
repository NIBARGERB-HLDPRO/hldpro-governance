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

## Expired or closed exceptions

_(none)_
