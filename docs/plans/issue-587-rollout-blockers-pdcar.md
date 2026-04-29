# Issue #587 PDCAR: Post-#585 Rollout Blockers

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/587
Branch: `issue-587-rollout-blockers`

## Plan

Close the remaining governance-source blockers found in the final post-`#585`
audit so downstream product-repo rollout can resume without another false
"fixed" claim.

The final audit on current `main`, reconciled with the accepted alternate-family
Claude review and the follow-on specialist-agent research, leaves two confirmed
rollout blockers and four bounded source-alignment items that should land in
the same lane:

- `implementation_complete` is still rejected by the handoff schema and
  validator even though the broader governance contract already uses that
  lifecycle state
- `.claude/settings.json` is still omitted from the consumer package contract,
  leaving downstream settings enforcement incomplete
- the session-contract source contract should explicitly align the local-CI
  trigger coverage with the managed consumer package surfaces before rollout
  resumes
- governed Claude review packets should use one canonical packet-transport path
  without ad hoc shell assembly
- governance specialist planner / auditor / QA lanes should be defined as
  tracked packet-backed agents backed by `hldpro-sim` persona resources rather
  than freeform session memory
- those specialist lanes should be hard-gated to accept structured packets and
  return structured packet outputs that validators can bind to review, QA, and
  handoff evidence
- the shared `hldpro-sim` consumer manifest should expose those specialist
  personas so downstream product repos can consume the same governed resources
  after rollout

## Do

Implementation scope for issue `#587`:

- align handoff schema and handoff validator to accept
  `implementation_complete`
- add `.claude/settings.json` to the governance tooling package and consumer
  pull-state managed file contract where the session-contract package requires
  it
- keep the local-CI trigger coverage and the managed consumer package contract
  aligned, with regression proof
- add a canonical packet-transport path for `scripts/codex-review.sh claude`
  so governed review packets do not depend on ad hoc shell interpolation
- hard-gate bidirectional `Codex <> Claude` pinned-agent routing: if Codex is
  primary it must dispatch Claude-owned pinned roles through the governed
  Claude path; if Claude is primary it must dispatch Codex-owned pinned roles
  through the governed Codex path; neither side may absorb the other side's
  pinned role
- hard-gate end-of-change critical specialist auditor assignment so every
  governed code/doc/config change ends with a distinct pinned auditor/QA
  specialist review before merge or closeout
- define tracked governance specialist agents for planner, auditor, and QA
  using shared `hldpro-sim` personas so the same governed specialist resources
  can be deployed downstream
- hard-gate specialist-agent packet contracts so those lanes accept only
  schema-valid structured packets, return only structured packet outputs, and
  expose tracked availability evidence to validators
- replace text-only bidirectional routing assertions with a machine-readable
  dispatch-ownership contract in plan/handoff artifacts so validators can
  reject opposite-family role absorption structurally
- embed the pinned wrapper invocation into that machine-readable dispatch
  contract so sessions do not improvise shell calls: each governed
  opposite-family or specialist lane must declare the required wrapper path,
  packet transport mode, and output artifact contract
- hard-gate pinned-specialist fallback criteria inside that machine-readable
  dispatch contract so unavailable or exhausted specialists can only fall back
  within the same owned model family, only upward through the approved quality
  ladder, with the fallback criteria and artifact logged; cross-family role
  absorption remains forbidden
- add regression coverage for the above

## Check

Before implementation:

- the issue-backed planning packet validates locally
- the packet names the exact rollout blockers and keeps downstream rollout
  paused until they are closed
- specialist review confirms the bounded fix set is sufficient
- alternate-family review is recorded through
  `scripts/codex-review.sh claude` before implementation-ready promotion

After implementation:

- `package-handoff` accepts `implementation_complete`
- consumer contract output requires `.claude/settings.json` where the session
  package requires it
- session-contract trigger coverage and consumer package surfaces stay aligned
  in local proof
- governed Claude review packets are hard-gated to a file-backed packet
  transport path: `scripts/codex-review.sh claude` must pass a packet file path
  into the governed wrapper flow, and inline shell interpolation of packet
  contents must fail closed
- bidirectional `Codex <> Claude` pinned-agent routing is hard-gated in the
  repo contract: Codex-primary lanes must dispatch Claude-owned pinned roles
  through the governed Claude path, Claude-primary lanes must dispatch
  Codex-owned pinned roles through the governed Codex path, and neither side
- every governed code/doc/config change must end with assigned critical
  specialist auditor review by a distinct pinned auditor/QA lane before merge
  or closeout
- tracked governance specialist planner / auditor / QA agents are available
  through `hldpro-sim` resources, are recorded in registry surfaces, and are
  deployable to downstream repos through the shared consumer manifest
- specialist-agent lanes are hard-gated to file-backed packet input and
  structured packet output, with tracked packet transport and availability
  evidence validated from plan and handoff artifacts
- bidirectional `Codex <> Claude` dispatch is enforced by machine-readable
  plan/handoff contract fields and validator checks, not only by required
  contract strings in repo docs
- machine-readable dispatch ownership includes the pinned wrapper id/path for
  each opposite-family or specialist lane, and validators reject ad hoc call
  paths or missing wrapper/output metadata
- machine-readable dispatch ownership includes pinned-specialist fallback
  policy: if a pinned specialist is unavailable or quota-exhausted, fallback
  remains inside the owned family, uses the approved quality-upgrade ladder,
  emits a fallback artifact, and never permits cross-family role absorption
- regression tests and local proof cover each blocker

## Adjust

If alternate-family review says deeper session-contract semantic checks are
still rollout blockers, widen this issue only to the minimum additional source
checks required to clear rollout. Do not resume downstream rollout on the
strength of `#585` plus process memory.

The accepted Claude review did not identify another missing source blocker. The
final specialist audit did identify one remaining structural gap: routing is
still text-gated more than semantically gated. Widen this lane only enough to
encode dispatch ownership in machine-readable plan/handoff fields and validate
it directly, including the approved same-family fallback ladder for pinned
specialists when the primary pinned agent is unavailable or exhausted.

## Review

Do not resume downstream issue `#579` child rollout lanes until issue `#587`
is merged and the final audit blocker set is closed or explicitly reclassified
as non-blocking by issue-backed review.
