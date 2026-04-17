# PDCAR: SoM Enforcement Drift Closure

Date: 2026-04-17
Branch: `fix/som-enforcement-drift-20260417`
Repo: `hldpro-governance`
Status: REVIEWED_ISSUES_OPEN_SLICE_7_REVIEW_CHANGES_APPLIED
Claude review: APPROVED_WITH_CHANGES_APPLIED
GitHub epic: [#214](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/214)

## Problem

The Society of Minds implementation is documented as a hard, deterministic governance system, but the repo still mixes documented, deferred, partially wired, and live-enforced controls. The audit found enforceable gaps that make operators believe the repo is following the charter when several rules are either contradictory, noisy, placeholder-only, or not uniformly triggered.

## Plan

Close the drift as issue-backed slices instead of making broad unreviewed changes. The first pass creates this plan, obtains Claude review, then opens GitHub epic/slice issues with acceptance criteria. Implementation starts only after review and issue creation.

## Scope

In scope:
- Align the SoM Tier 2 worker ladder so `STANDARDS.md`, fallback logs, and workflow behavior describe one policy.
- Fix Codex model/reasoning pin enforcement so it passes on the repo, excludes local/generated worktrees, and still catches real unpinned `codex exec` calls.
- Replace placeholder architecture-tier enforcement with a concrete check or explicitly downgrade the documented claim until enforcement exists.
- Tighten cross-review validation so architecture/standards artifacts bind to the PR and include gate identity where the standard requires it.
- Reconcile packet schema/validator docs with the actual local implementation and create a follow-up for runtime MCP wiring that lives in `local-ai-machine`.
- Refresh operational status docs so active, resolved, and deferred SoM items do not contradict each other.
- Add executable execution-root and write-scope enforcement so SoM delegation cannot write to the wrong checkout or outside a declared slice scope.

Out of scope for this planning slice:
- Implementing code fixes before Claude review.
- Touching user-owned dirty files in the main checkout.
- Changing `local-ai-machine` runtime code directly from this repo.
- Applying GitHub org/ruleset admin changes.

## Do

After Claude approves or amends this plan:
1. Create a GitHub epic issue for SoM enforcement drift closure.
2. Create issue-backed AC slices for each bounded implementation area.
3. Update this plan with created issue links.
4. Assign worker agents to slices with disjoint file ownership.

## Check

Each implementation slice must include its own validation commands. Minimum expected checks:
- `python3 .github/scripts/check_agent_model_pins.py`
- `python3 .github/scripts/check_codex_model_pins.py`
- `python3 .github/scripts/check_lam_family_diversity.py`
- `python3 scripts/packet/test_validate.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name fix/som-enforcement-drift-20260417 --require-if-issue-branch`

For standards or architecture changes, the PR must include a valid `raw/cross-review/YYYY-MM-DD-*.md` artifact and pass `scripts/cross-review/require-dual-signature.sh`.

## Adjust

If Claude review finds a scope problem, split the slice before implementation. If any checker reveals additional drift, either absorb it only when it is part of the same acceptance path or create a follow-up GitHub issue before closeout.

`SOM-BOOTSTRAP-001` expires 2026-04-21. Slice 3 must either land before that date or the exception must be formally extended in `docs/exception-register.md` before expiry.

## Review

Review gate before implementation:
- Claude review of this plan is required.
- Claude review artifact: `raw/cross-review/2026-04-17-som-enforcement-drift-plan.md`.
- Claude Opus gate: `GATE_PASSED`; gate identity is recorded in the v2 review artifact.
- The review must explicitly state whether implementation may start.
- Any requested changes must be applied to this plan before creating worker assignments.
- Claude returned `APPROVED_WITH_CHANGES`; the five required plan changes have been incorporated before GitHub issue creation.

## Proposed GitHub Slices

### Epic: SoM Enforcement Drift Closure

Issue: [#214](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/214)

Acceptance criteria:
- All child slices are linked.
- The plan artifact is committed in repo.
- Claude review is attached or linked.
- Residual deferrals are explicit and issue-backed.

## Worker Assignment Wave 1

Wave 1 uses disjoint file ownership so workers do not collide:

- Slice 1 / issue #215: assigned to Codex worker Feynman.
- Slice 3 / issue #217: assigned to Codex worker Descartes.
- Slice 5 / issue #219: assigned to Codex worker Epicurus.

Queued until Wave 1 is integrated because of overlapping ownership:

- Slice 2 / issue #216: touches `STANDARDS.md`, `docs/PROGRESS.md`, and `docs/FEATURE_REGISTRY.md`.
- Slice 4 / issue #218: touches `STANDARDS.md`.
- Slice 6 / issue #220: touches `docs/PROGRESS.md`, `docs/FEATURE_REGISTRY.md`, and `OVERLORD_BACKLOG.md`.

## Worker Assignment Wave 2 / Ordered Integration

Slices 2, 4, and 6 have been integrated before Slice 7 starts. Slice 7 runs after those slices because its closeout/status needs depend on the final operational-status wording from Slice 6. Slice 7 worker ownership is limited to new enforcement code and its scope artifact; any status or closeout wording updates are final-integrator edits after the checker passes.

## Scope Addendum: Execution Root And Write-Scope Enforcement

The 2026-04-17 implementation exposed a repo-rule gap: worker prompts named the intended worktree, but two workers and one sweep/status write still produced output in the main checkout. This is the same documentation-versus-enforcement failure class as the SoM drift: expected cwd and allowed paths lived in prose, not in executable policy.

This addendum adds a seventh issue-backed slice under epic #214 and keeps it in the same PR because it directly protects the SoM worker/sweep delegation path being fixed here.

### Slice 7: Execution Root And Write-Scope Enforcement

Issue: [#221](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/221)

File ownership:
- `scripts/overlord/assert_execution_scope.py`
- `scripts/overlord/test_assert_execution_scope.py`
- `raw/execution-scopes/2026-04-17-som-enforcement-drift-slice7.json`
- `docs/plans/2026-04-17-som-enforcement-drift-pdcar.md`

Final integrator, not the Slice 7 worker, may update:
- `raw/execution-scopes/2026-04-17-som-enforcement-drift-pr.json`
- `raw/closeouts/TEMPLATE.md`
- `raw/closeouts/2026-04-17-som-enforcement-drift-closeout-loop.md`
- `docs/PROGRESS.md`
- `OVERLORD_BACKLOG.md`

These files are excluded from worker ownership because Slice 4 and Slice 6 already own the closeout/status surfaces. Any updates to them must happen after Slice 7 code validation, as same-PR integration edits.

Acceptance criteria:
- Plans/slices can declare an expected execution root, expected branch, allowed write paths, and forbidden roots.
- A local checker refuses execution when the current checkout root differs from the declared execution root.
- The checker refuses execution when the current branch differs from the declared branch.
- The checker refuses changed files outside declared write paths.
- The checker refuses dirty forbidden roots, so a main checkout cannot silently receive worker/sweep output while a branch worktree is active.
- The checker supports JSON scope files so worker dispatch briefs and closeouts can use the same artifact.
- The checker has a concrete invocation path: worker dispatch briefs must run `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-som-enforcement-drift-slice7.json` before accepting Slice 7 delegated output; final closeout validation must run `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-17-som-enforcement-drift-pr.json` before accepting the full PR. CI coverage for cross-checkout dirtiness is deferred because GitHub Actions cannot inspect a developer's sibling main checkout; CI still runs the unit tests for the checker and can validate in-repo changed-file scope.
- Tests cover wrong root, wrong branch, forbidden-root dirtiness, allowed path changes, and out-of-scope changes.
- Closeout requirements include the execution-scope validation command when work is delegated to workers or sweep/status writers.
- GitHub issue comments for Slice 7 record assignment, implementation, and validation.

## Slice 7 Plan Review

Claude Sonnet reviewed the Slice 7 addendum before issue creation and returned `APPROVED_WITH_CHANGES`. Required changes were:
- Resolve file ownership collisions with Slices 4 and 6.
- Add Slice 7 to an explicit ordered wave.
- Add a concrete invocation path for the checker.

All required changes have been applied above. Review artifact: `raw/cross-review/2026-04-17-som-execution-scope-slice7-plan.md`.

### Slice 1: Codex Model Pin Enforcement

Issue: [#215](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/215)

File ownership:
- `.github/scripts/check_codex_model_pins.py`
- `.github/workflows/overlord-sweep.yml`
- `scripts/codex-review-template.sh`
- `scripts/overlord/codex_ingestion.py`

Acceptance criteria:
- Checker passes locally on a clean worktree.
- Checker ignores `.claude/worktrees/` and generated/local-only directories.
- Checker catches shell and Python-list `codex exec` invocations.
- Checker validates both the `-m <model>` flag and the presence of `model_reasoning_effort` in each real `codex exec` invocation.
- `overlord-sweep.yml` invokes `check_codex_model_pins.py` and `check_agent_model_pins.py`; failures surface as CI errors, not warnings.

### Slice 2: SoM Ladder And Standards Consistency

Issue: [#216](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/216)

File ownership:
- `STANDARDS.md`
- `docs/exception-register.md`
- `docs/PROGRESS.md`
- `docs/FEATURE_REGISTRY.md`

Acceptance criteria:
- Tier 2 fallback ladder is described once without contradiction.
- Any use of `gpt-5.4` as worker fallback is either formally allowed or documented as a violation with an issue-backed correction.
- Resolved exceptions are not presented as active blockers.

### Slice 3: Cross-Review And Gate Identity Enforcement

Issue: [#217](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/217)

File ownership:
- `scripts/cross-review/require-dual-signature.sh`
- `.github/scripts/check_no_self_approval.py`
- `.github/workflows/require-cross-review.yml`
- `.github/workflows/governance-check.yml`
- `raw/cross-review/`

Acceptance criteria:
- Cross-review validation enforces the documented schema fields.
- `require-dual-signature.sh` validates a `gate_identity` field when present.
- Existing historical artifacts that predate the field are exempt via an explicit `schema_version: v1` marker; v2+ artifacts must include the field.
- No-self-approval covers drafter, reviewer, and gate identity for v2+ artifacts.
- Architecture/standards PR triggers are explicit and documented.
- The bootstrap exception cannot silently bypass future non-bootstrap PRs.

### Slice 4: Architecture Tier Enforcement

Issue: [#218](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/218)

File ownership:
- `.github/workflows/check-arch-tier.yml`
- `STANDARDS.md`
- `agents/`
- `raw/closeouts/TEMPLATE.md`

Acceptance criteria:
- Placeholder warning is replaced by a concrete enforcement path, or the standards text is downgraded to match reality.
- Arch-on-Haiku evidence is checkable from committed artifacts.
- Closeout requirements name the artifact that proves the tier used.

### Slice 5: Packet Schema And Runtime Boundary

Issue: [#219](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/219)

File ownership:
- `docs/schemas/README.md`
- `docs/schemas/som-packet.schema.yml`
- `scripts/packet/validate.py`
- `scripts/packet/test_validate.py`
- `raw/closeouts/2026-04-14-packet-schema-stage4.md`
- `raw/closeouts/2026-04-16-som-stage4b.md`

Acceptance criteria:
- Docs match actual validator behavior and CLI support.
- Claims about `schemas/packet-schema.json` and `schemas/packet-validator.py` are reconciled or marked historical.
- Runtime MCP work is clearly assigned to `local-ai-machine`, not implied to live in this repo.
- The slice explicitly chooses one reconciliation path: either implement the three missing invariants (`check_tier_escalation_valid`, `check_local_family_diversity`, `check_fallback_logged`) and bring tests into alignment, or mark the Stage 4 closeout invariant claims as historical overstatement with corrected counts.

### Slice 6: Operational Status And Closeout Loop

Issue: [#220](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/220)

File ownership:
- `docs/PROGRESS.md`
- `docs/FEATURE_REGISTRY.md`
- `OVERLORD_BACKLOG.md`
- `wiki/index.md`
- `raw/closeouts/`

Acceptance criteria:
- Active Planned rows match unresolved SoM work.
- Resolved SoM branch-policy drift no longer appears as a planned blocker.
- Weekly sweep/write-back status reflects the current operational state.
- Closeout records all residual work as issue-backed follow-up.
