# Issue #629 PDCAR: Fallback-Log Schema And Workflow Parity

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/629
Parent: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/612
Branch: `issue-629-fallback-log-parity-20260430`

## Plan

Produce the canonical planning-only packet for governance issue `#629`, the
second narrow implementation child under `#612`.

This child exists because `#625` closed only the execution-scope field
enforcement slice for degraded same-family fallback evidence. `#629`
therefore owns only fallback-log schema/workflow parity for the same proof
chain. It must not absorb execution-scope enforcement, local-hook children
already closed under `#615`, planning-authority workflow work, or downstream
verifier work.

Mandatory intake for this lane includes:

- `docs/PROGRESS.md`
- issue `#612` and its later routing comments
- merged child issue `#625`
- parent governance umbrella `#615`
- the current fallback-log parity surfaces:
  - `.github/scripts/check_fallback_log_schema.py`
  - `scripts/model-fallback-log.sh`
  - `.github/workflows/check-fallback-log-schema.yml`
- adjacent proof consumers for grounding only:
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/packet/validate.py`
  - `scripts/orchestrator/packet_queue.py`

## Do

Planning-only scope for issue `#629`:

- record the canonical structured plan, planning execution scope, handoff,
  review packet, cross-review, and validation artifacts
- define the bounded governance-owned implementation surface for:
  - `.github/scripts/check_fallback_log_schema.py`
  - `scripts/model-fallback-log.sh`
  - `.github/workflows/check-fallback-log-schema.yml`
  - focused tests for those two surfaces
- define the canonical fallback-log reason contract later implementation must
  enforce so the writer and checker agree, while explicitly grandfathering
  historical fallback logs outside the PR diff
- define the degraded-fallback fallback-log content contract that later
  implementation must enforce so it matches the stricter same-family proof
  semantics already required by `#625`
- define the exact positive and negative fallback-log proof cases later
  implementation must return
- keep execution-scope field enforcement out of scope:
  - `docs/schemas/execution-scope.schema.json`
  - `scripts/overlord/assert_execution_scope.py`
  - `scripts/overlord/test_assert_execution_scope.py`
- keep broader validator/workflow or packet-routing work out of scope:
  - `scripts/overlord/validate_handoff_package.py`
  - `scripts/orchestrator/packet_queue.py`
  - `scripts/packet/validate.py`
  - `.github/workflows/governance-check.yml`
- keep issue `#607` planning-authority enforcement and issue `#614`
  downstream verifier work out of scope

## Check

The packet is acceptable only if it:

- stays planning-only and does not patch scripts, tests, or workflows in this
  lane
- keeps ownership bounded to fallback-log schema/workflow parity only
- explicitly records why this child exists:
  `#625` closed execution-scope enforcement first, so `#629` takes the next
  narrow fallback-log parity slice
- names the exact required positive proof case:
  a degraded same-family fallback log passes only when the writer emits and
  the checker accepts the same machine-checkable parity fields and valid
  content
- names the exact negative proof cases:
  fail closed when required fallback-log fields are missing, blank, generic,
  semantically inconsistent with degraded-fallback expectations, or otherwise
  malformed
- explicitly resolves the writer/checker reason-contract mismatch and states
  whether legacy historical logs outside the PR diff are grandfathered
- requires regression proof that non-degraded or unrelated fallback-log flows
  still pass unchanged
- requires workflow proof that the reusable fallback-log schema gate still
  blocks an invalid changed fallback log and still passes a valid changed
  fallback log
- does not collapse into execution-scope rework, local-hook children, or
  broader handoff/review-routing enforcement

Planning validation commands:

- `python3 -m json.tool docs/plans/issue-629-fallback-log-parity-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-30-issue-629-fallback-log-parity-planning.json`
- `python3 -m json.tool raw/handoffs/2026-04-30-issue-629-fallback-log-parity.json`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-629-fallback-log-parity-20260430 --require-if-issue-branch`
- `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-629-fallback-log-parity.json`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-30-issue-629-fallback-log-parity-plan.md`
- `git diff --check`

## Adjust

If the lane drifts into `assert_execution_scope.py`, execution-scope schema or
tests, stop and keep that work closed under `#625`.

If the lane starts editing hook/startup/root-parity surfaces already merged
under `#615`, stop and keep `#629` bounded to fallback-log parity only.

If the lane starts editing broader packet-routing, handoff, or workflow
surfaces beyond the existing fallback-log schema gate, stop and route that
work back to a later `#612` child.

If the governed alternate-family review path is unavailable in this clean
worktree, record that as a real blocker rather than using same-family
substitutes.

## Review

Required before completion:

- governed alternate-family specialist review through the sanctioned review
  wrapper path
- local orchestration check that the packet remains planning-only and issue
  bounded
- deterministic validator pass on the packet artifacts

Issue `#629` does not authorize implementation by itself. It establishes only
the planning packet and implementation-readiness gate for the fallback-log
parity child of `#612`.

Required closure proof for the later implementation lane:

- explicit planning decision for this lane:
  the concrete reason schema and validity rules are deferred to the later
  implementation lane, but that lane must resolve them before closure and may
  not leave the writer/checker mismatch ambiguous

- positive proof that degraded same-family fallback logs pass only when the
  required parity fields are present and semantically valid
- positive proof classes:
  - writer pass on a valid invocation
  - checker pass on one valid changed fallback file
  - checker pass on a valid multi-block append file
- negative proof for each named failure class:
  - missing required field
  - blank required field
  - generic placeholder content
  - semantically inconsistent degraded-fallback metadata
  - malformed or invalid reason/value combinations
- workflow proof that missing PR context remains a skip case rather than a
  false local failure
- regression proof that unrelated or valid fallback-log paths still pass
- regression proof that valid repo-local fallback artifacts still remain
  acceptable to downstream packet/PR consumers
- a validation artifact with one passing fixture and the expected fail output
  for each negative fixture
