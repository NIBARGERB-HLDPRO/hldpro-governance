# PDCAR: Org-Wide Always-On Governance Orchestrator

Date: 2026-04-17
Repo: `hldpro-governance`
Branch: `plan/always-on-governance-orchestrator-20260417`
Epic: [#224](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/224)
Related Phase 0 issue: [#223](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/223)
Status: PLANNING_APPROVED_FOR_ISSUE_DECOMPOSITION
Canonical plan: `docs/plans/issue-224-structured-agent-cycle-plan.json`

## Problem

The HLDPRO repos now have enough governance machinery to support an always-on local governance orchestrator, but the current control path is not ready for autonomous execution.

The immediate risks are:

- Repo discovery is duplicated across sweep, graphify, metrics, memory integrity, Codex ingestion, and the draft compendium generator.
- The compendium work in issue #223 exposed a governance sequencing break: implementation started before issue-backed structured planning and alternate-family review.
- The structured-plan validator is strongest only for issue/riskfix branch names, so governance-surface edits can bypass the planning gate when made on the wrong branch.
- Existing SoM daemon and packet concepts exist, but launchd-managed always-on execution should not start until registry, planning, scope, and review gates are deterministic.

## Plan

Build the always-on governance system in phases. Do not start with a daemon. Start by repairing the governance path and establishing a single governed-repo registry, then add local observers, model runtime probes, packet queues, self-learning feedback, and finally an autonomous delivery pilot.

The intended final state is an org-wide governance control plane where the operator can define an outcome, produce a reviewed issue-backed plan, decompose it into phases/microslices/ACs, route it through SoM with local/cloud model roles, and return to tested, reviewed, closeout-ready work.

## Scope

In scope:

- Issue-backed planning for the org-wide governance orchestrator epic.
- Coordination with issue #223 as Phase 0.
- Canonical structured JSON plan and PDCAR companion.
- Specialist and alternate-family review before implementation.
- GitHub phase/slice issues with acceptance criteria.
- A phased implementation design for:
  - compendium/path repair,
  - unified governed-repo registry,
  - planning/scope gatekeeper,
  - read-only always-on observers,
  - local model runtime guardrails,
  - packet queue/orchestrator,
  - self-learning loop,
  - autonomous delivery pilot.

Out of scope for this planning branch:

- Implementing any daemon, launchd service, registry, packet queue, validator, compendium generator, or model runtime change.
- Adopting the dirty shared-main compendium diff.
- Editing local-ai-machine runtime code.
- Relaxing SoM constraints.
- Replacing GitHub Issues as the canonical execution tracker.

## Do

Planning sequence:

1. Create the governing epic issue #224.
2. Create this canonical structured JSON plan and PDCAR companion in a clean isolated worktree.
3. Run Claude review against the written plan.
4. Apply required review changes.
5. Create phase/slice GitHub issues only after review approval.
6. Update this PDCAR and the structured JSON plan with phase/slice issue links.
7. Run plan validation and close with a PR-ready planning package.

Proposed implementation phases after planning approval:

| Phase | Purpose | Issue |
|---|---|---|
| Phase 0 | Governance path repair and compendium decision | #223 |
| Phase 1 | Unified governed-repo registry | #225 |
| Phase 2 | Planning and scope gatekeeper | #226 |
| Phase 3 | Read-only always-on observers | #227 |
| Phase 4 | Local model runtime and guardrail lane | #228 |
| Phase 5 | Packet queue and controlled orchestration | #229 |
| Phase 6 | Self-learning and self-healing loop | #230 |
| Phase 7 | End-to-end autonomous delivery pilot | #231 |

## Check

Planning checks:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name plan/always-on-governance-orchestrator-20260417 --require-if-issue-branch`
- JSON parse of `docs/plans/issue-224-structured-agent-cycle-plan.json`
- Claude review artifact exists before issue decomposition is considered approved.
- GitHub epic #224 links issue #223 and all new phase/slice issues.
- Worktree status remains isolated from the dirty shared main checkout.

Implementation checks will be phase-specific. Minimum expected families:

- Governed repo registry schema validation.
- Structured plan validation for all implementation branches.
- Governance-surface planning-gate tests.
- Execution-scope/wrong-checkout tests.
- launchd plist validation and health-check probes.
- packet schema validation.
- PII routing fail-closed tests.
- SoM no-self-approval and model-pin checks.
- closeout hook and verify-completion evidence before any done state.

## Adjust

Review or implementation must stop and update the plan if:

- Claude review rejects or requires changes.
- Issue #223 must be absorbed as a child of #224 rather than remaining a Phase 0 dependency.
- A phase needs local-ai-machine code changes that require a separate repo issue.
- Any proposed gate relies on LLM judgment instead of deterministic validation.
- The measured local model/runtime state differs from the hardware assumptions.
- Any implementation would touch the dirty shared main checkout.

Known design corrections already applied:

- The daemon is not Phase 1. Registry and planning-gate repair come first.
- Graphify and compendium can route attention, but direct files/issues/validators must prove compliance.
- Filesystem packet queues are preferred initially because they are auditable and fit current repo artifacts; Redis/SQLite can be considered later if file queues become inadequate.
- Default HITL boundary: Phases 0-6 require operator approval at the whole-plan or phase-plan boundary before execution. Phase 7 pilot must define its own microslice-level HALT/approval granularity under review before autonomous execution.
- Windows hardware contract is unresolved: operator reports the retired Windows unit has 64 GB RAM and no VRAM, while `STANDARDS.md` currently documents 64 GB RAM and 16 GB VRAM. Phase 4 must verify and reconcile this before model-placement decisions.

## Review

Required before implementation:

- Claude Opus/Sonnet review of this written plan. Completed for planning readiness on 2026-04-17.
- Alternate-family review is required because this is architecture/standards/governance workflow design.
- Review artifact must be recorded under `raw/cross-review/`. Completed at `raw/cross-review/2026-04-17-always-on-governance-orchestrator-plan.md`.
- Required review changes must be applied before phase/slice issues are treated as implementation-ready. Completed for planning decomposition; implementation remains blocked.

Review decisions:

- Claude Opus 4.6 returned `APPROVED_WITH_CHANGES`.
- Required changes applied: `execution_mode` set to `planning_only`; default HITL boundary added; issue #224 row added to `OVERLORD_BACKLOG.md`; Windows hardware discrepancy made a Phase 4 hard gate.
- Claude Sonnet 4.6 returned `GATE_PASSED` for planning readiness and phase/slice issue creation.
- Phase/slice issues #225-#231 were created only after the gate passed.

Research already completed:

- Codex specialist research agents:
  - Hegel: repo/SoM constraints.
  - Einstein: repo integration/data flow.
  - Euclid: end-to-end orchestration workflow.
- Claude Opus 4.6 planning memo:
  - confirmed multiple-gatekeeper architecture,
  - launchd local runtime model,
  - self-learning feedback loop,
  - Mac/Windows model placement,
  - phased implementation,
  - with the Codex synthesis correction that registry/planning gates precede daemon work.

## Initial Acceptance Criteria

- Issue #224 exists as the governing epic.
- Issue #223 is linked and treated as the separate Phase 0 dependency.
- Canonical structured plan exists and passes validation.
- PDCAR companion exists and does not contradict the JSON plan.
- Claude review artifact exists and required changes are applied.
- Phase/slice issues are created with file ownership, ACs, validation, and closeout expectations.
- No implementation work starts from this planning branch.

## Open Questions For Review

1. Should `projects/<repo_slug>/` be tracked for routing/report artifacts, with only runtime locks ignored?
2. Should the first always-on daemon be read-only only, or may it enqueue packets after approval?
3. Should the default HITL boundary above be tightened further before Phase 7, for example phase approval plus microslice approval for risky repos?
4. What operator notification channel should be first for HALT states: macOS notification, GitHub issue comment, email, Slack, or all?
5. After hardware verification, should Windows remain LAN-only Ollama fallback/batch infrastructure in the first epic, or be expanded into a broader batch worker immediately?
