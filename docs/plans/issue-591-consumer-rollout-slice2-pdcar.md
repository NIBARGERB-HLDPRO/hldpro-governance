# PDCAR: Issue #591 Consumer Rollout — Slice 2 (Repair + Completion)

Date: 2026-05-03
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/591
Branch: `issue-591-consumer-rollout-slice2-20260503`
Slice: 2 of 2 (Slice 1 = planning lane via PR #593, merged 2026-04-29)

## Plan

Advance #591 to full completion by repairing all critical failures from the verifier run, resolving
warnings, and executing Stage 6 closeout. Consumer repo changes (file additions, package upgrades)
are out-of-scope for this governance lane — they require repo-native PRs dispatched separately.
This lane owns governance-side artifacts: consumer pull-state records, sub-issue creation, and
final epic closeout.

### Verifier Status at Slice 2 Start (0/7 passing)

Critical failures:
- **Stampede**: `.hldpro/governance-tooling.json` present but 8 managed-file markers missing
- **knocktracker**: PR #190 merged but `.hldpro/governance-tooling.json` missing from remote HEAD
- **HealthcarePlatform**: No consumer record — never rolled out
- **ASC-Evaluator**: No consumer record — exemption status unclear

Warnings:
- **ai-integration-services**: consumer_repo path mismatch in pull-state record
- **local-ai-machine**: Package version stale (0.1.0-contract vs target 0.2.0-ssot-bootstrap)
- **seek-and-ponder**: 3 local override warnings

### Acceptance Criteria

- Sub-issues opened for all not-yet-started consumer repos (HealthcarePlatform, local-ai-machine,
  seek-and-ponder local-overrides, ASC-Evaluator).
- Governance-side consumer pull-state records accurate for all 7 consumers.
- Verifier replay achieves 7/7 passing (after consumer repo PRs are merged).
- Stage 6 closeout artifact present at `raw/closeouts/2026-05-03-issue-591-consumer-rollout-slice2.md`.
- OVERLORD_BACKLOG.md updated to reflect completed state.
- Governing GitHub issue #591 closed.

## Do

### Phase 1: Fix Critical Failures (Governance-side)

**1a. Stampede — 8 missing managed-file markers**
- Root cause: PR adopting `.hldpro/governance-tooling.json` did not include all required managed
  surface entries. The managed-file list in the governance package schema lists 8 surfaces; Stampede
  only has the tooling.json shell without the surface entries.
- Action (dispatcher): Open Stampede repo issue referencing #591. Dispatch worker to add the 8
  missing managed surface entries to `.hldpro/governance-tooling.json` and open a Stampede PR.
- Governance lane: Update `docs/governance-consumer-pull-state.json` Stampede record to reflect
  pending-repair state with the sub-issue ref.

**1b. knocktracker — governance-tooling.json missing from remote**
- Root cause: PR #190 (knocktracker) was merged but the `.hldpro/governance-tooling.json` file
  was not part of the merge, or the verifier is reading a stale remote HEAD ref.
- Action (dispatcher): Verify knocktracker remote HEAD via `gh api`. If file is genuinely absent,
  open knocktracker issue and dispatch repair PR. If stale read, re-run verifier against fresh HEAD.
- Governance lane: Update knocktracker consumer record with verification timestamp + repair ref.

**1c. HealthcarePlatform — never rolled out**
- Sub-issue: "feat(#591): Roll out research specialist surfaces to HealthcarePlatform"
- Action (dispatcher): After sub-issue is open, dispatch HealthcarePlatform worker to adopt
  governance package at 0.2.0-ssot-bootstrap and add the required managed surfaces.
- Governance lane: Create initial consumer pull-state record for HealthcarePlatform.

**1d. ASC-Evaluator — exemption status unclear**
- Investigation: Check OVERLORD_BACKLOG.md and any existing exemption artifacts for ASC-Evaluator.
  Determine if it holds a governance exemption, is a deferred rollout, or is simply unstarted.
- If unstarted: Sub-issue "feat(#591): Roll out research specialist surfaces to ASC-Evaluator"
- If exempted: Document exemption basis in consumer pull-state record with exemption_ref.
- Governance lane: Update consumer pull-state record to reflect determined status.

### Phase 2: Resolve Warnings

**2a. ai-integration-services — consumer_repo path mismatch**
- Inspect current `docs/governance-consumer-pull-state.json` AIS entry.
- Correct the `consumer_repo` path value to match the actual AIS repo path on disk.
- This is a governance-side fix only — no consumer repo PR needed.

**2b. local-ai-machine — package version stale**
- Sub-issue: "feat(#591): Roll out research specialist surfaces to local-ai-machine"
  (upgrade from 0.1.0-contract to 0.2.0-ssot-bootstrap)
- Governance lane: Update LAM consumer record with target version and sub-issue ref.

**2c. seek-and-ponder — 3 local override warnings**
- Sub-issue: "feat(#591): Roll out research specialist surfaces to seek-and-ponder (resolve local
  overrides)"
- Investigate override keys in seek-and-ponder's managed surfaces. Determine if overrides are
  intentional (require exemption notation) or stale (require removal via seek-and-ponder PR).
- Governance lane: Update seek-and-ponder consumer record with override disposition.

### Phase 3: Verifier Replay

- After all consumer repo PRs are merged and governance-side records updated, run:
  `python3 scripts/verify_governance_consumer.py --all` from a fresh origin/main worktree.
- Gate: must achieve 7/7 passing. Document replay output in
  `raw/validation/2026-05-03-issue-591-consumer-rollout-slice2.md`.
- If any repo still fails: create a targeted repair sub-issue and do not proceed to Phase 4.

### Phase 4: Stage 6 Closeout for #591 Epic

1. Fill `raw/closeouts/2026-05-03-issue-591-consumer-rollout-slice2.md` from
   `raw/closeouts/TEMPLATE.md`.
2. Run `hooks/closeout-hook.sh raw/closeouts/2026-05-03-issue-591-consumer-rollout-slice2.md`.
3. Update `OVERLORD_BACKLOG.md`: mark #591 DONE with evidence paths.
4. Close GitHub issue #591 via `gh issue close 591 --repo NIBARGERB-HLDPRO/hldpro-governance`.
5. Verify GRAPH_REPORT.md reflects the completed state on next graph refresh.

## Check

- All 4 sub-issues opened (or confirmed pre-existing) with refs recorded here.
- `docs/governance-consumer-pull-state.json` updated for all 7 consumers.
- Execution scope file present and valid JSON.
- PDCAR plan present and matches this document.
- Verifier replay 7/7 (Phase 3 gate).
- Closeout hook exit 0 (Phase 4 gate).

## Adjust

_To be filled during execution — record any scope creep, unexpected failures, or absorbed repairs._

