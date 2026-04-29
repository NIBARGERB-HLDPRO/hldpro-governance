# Issue #589 PDCAR: Governed Research Specialists

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/589
Branch: `issue-589-research-specialists`

## Plan

Close the remaining governance-source gap around research work by defining two
governed research specialist lanes and the downstream rollout model needed to
push those org-level governance changes safely into consumer repos.

Specialist research confirmed the current governance source already has
packet-backed planner, auditor, QA, and sim-runner surfaces, but it still
lacks first-class governed specialists for:

- local repo / workspace discovery
- web / external-source discovery

The same research also confirmed a second gap: even if those specialist lanes
are added at governance source, downstream product repos still need a clear
package-managed versus repo-specific rollout model so the new specialist
contract can be adopted without ad hoc copying or central overreach.

## Do

Implementation scope for issue `#589`:

- define a governed `local-repo researcher` specialist lane as a bounded,
  read-only research surface for graphify/docs/repo-search discovery
- define a governed `web/external researcher` specialist lane as a bounded,
  read-only research surface for public-web, live system, vendor/runtime, or
  temporally unstable questions that local governed sources cannot answer
- pin both research specialists to tracked hldpro-sim personas, tracked agent
  definitions, file-backed packet input, and structured output artifacts
- hard-gate source attribution for the web/external lane so output must include
  source URL or endpoint, source title/domain/system, retrieval timestamp, why
  external lookup was needed, and claim-to-source mapping
- extend validator-visible packet contracts so plans and handoffs can prove
  which research lane was used and where the resulting evidence artifact lives
- define the safest downstream rollout model for these org-level changes:
  package-managed surfaces versus repo-specific issue-backed PR work, required
  proof, and what remains report-only from the consumer side
- add regression coverage and local proof for the above

## Check

Before implementation:

- the issue-backed planning packet validates locally
- acceptance criteria are phrased as hard gates, not recommendations
- specialist research confirms both the specialist-lane design and the
  downstream rollout model are correctly bounded
- alternate-family review is recorded through the governed
  `scripts/codex-review.sh claude` path before implementation-ready promotion
- if the governed Claude packet path fails closed, the lane must stay
  `planning_only` and record the failure evidence plus the blocking governance
  dependency rather than treating the review as complete
- if the blocking governance dependency is still open, the next execution step
  is to advance that dependency rather than widening issue `#589` into
  cross-issue transport repair work

After implementation:

- tracked local-repo and web/external research specialists exist as
  packet-backed, hldpro-sim-backed governance lanes
- plans and handoffs can declare which research specialist lane was used and
  validators can prove the packet/output contract
- web/external research evidence is machine-checkable for attribution fields
- governance package/deployer/verifier surfaces clearly distinguish:
  package-managed consumer changes, repo-specific issue-backed rollout work,
  and report-only central GitHub state
- downstream rollout guidance is SSOT and strong enough to avoid ad hoc repo
  copying
- regression tests and local proof cover each new contract surface

## Adjust

If the web/external lane needs tighter allow/deny rules than existing
STANDARDS/runbook language can express, widen this issue only enough to make
that boundary machine-checkable. Do not leave the lane governed only by prose.

If downstream rollout requires a new managed consumer surface beyond the
current package contract, add it here only when the deployer, verifier, and
rollback semantics can all be updated in the same slice.

The prior governance-source dependency on the packet-transport fix is now
resolved on `main`. Issue `#589` can move into implementation-ready scope
without reopening transport work in this branch.

The accepted review raised one metadata cleanup item only: remove the duplicate
`next_execution_step` key in the structured plan before promotion so JSON
parsers cannot silently discard the earlier value.

## Review

Do not claim the research-specialist contract is rollout-ready until both of
these are true:

- governance source has the research specialists, validators, and attribution
  contract wired
- the downstream rollout model is explicit about what can be package-managed
  versus what must remain repo-specific and issue-backed
