---
schema_version: v2
pr_number: pre-pr
pr_scope: standards
drafter:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-28
reviewer:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-28
  verdict: APPROVED_WITH_CHANGES
gate_identity:
  role: deterministic-local-gate
  model_id: hldpro-local-ci
  model_family: deterministic
  signature_date: 2026-04-28
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

# Cross-Review - Issue #575 Thin Session-Contract Adapter Rollout

## Review Subject

Planning-only rollout packet for propagating the issue-573 governance
session-bootstrap contract into governed consumer repos using thin `CLAUDE.md`
/ `CODEX.md` adapter files. The packet defines rollout wave ordering,
thin-adapter acceptance criteria, and governance-source SSOT conflict
reconciliation requirements. Reviewed artifacts: PDCAR, structured agent cycle
plan, execution scope, and handoff packet.

## Verdict

**APPROVED_WITH_CHANGES**

The packet correctly identifies the three governance-source SSOT conflicts that
must be resolved before downstream rollout, correctly gates consumer repo
execution on that reconciliation, maintains planning-only scope with
appropriate write-path constraints, and preserves cross-family review
independence. However, three changes are required before acceptance.

## Findings

### Correctly Blocked: SSOT Reconciliation Gate

The packet establishes a hard gate on downstream rollout through three
reinforcing mechanisms:

1. **PDCAR Adjust clause**: "If the governance repo itself still exposes
   multiple 'correct' review or bootstrap entrypoints, stop consumer rollout
   and fix the source contract first."
2. **Material deviation rule #1**: "If governance-source docs still expose
   multiple 'correct' operator entrypoints, stop downstream rollout and fix the
   source contract first."
3. **Handoff acceptance criterion #1**: "The rollout plan first reconciles
   governance-source SSOT conflicts so policy, runbook, and implementation do
   not present multiple operator-facing paths."

These three mechanisms are consistent and enforceable. A downstream
consumer-repo execution slice cannot pass acceptance if the governance source
still presents conflicting entrypoints.

### Conflict Identification Accuracy

The three SSOT conflicts identified by the specialist subagent audits are
confirmed accurate against the current source:

| Conflict | Evidence |
|----------|----------|
| Review path: `STANDARDS.md` Cross-Model Review declares `scripts/codex-review.sh` wrapper as canonical, but `scripts/codex-review-template.sh` directly exposes `scripts/cli_session_supervisor.py` as a callable subprocess path | `scripts/codex-review-template.sh` invokes `python3 "$REPO_ROOT/scripts/cli_session_supervisor.py"` with full parameter surface |
| Bootstrap path: session-start is split across `CLAUDE.md`, `hooks/pre-session-context.sh`, `.claude/settings.json`, `docs/ENV_REGISTRY.md`, and `scripts/bootstrap-repo-env.sh` multi-root search | `scripts/bootstrap-repo-env.sh` walks parent directories seeking `.env.shared`; `STANDARDS.md` declares `scripts/session_bootstrap_contract.py` as canonical |
| Thin-consumer ownership: `docs/governance-tooling-package.json` describes `shared_governance_package_with_thin_repo_adapter`, while `STANDARDS.md` Required Governance reads as if every consumer repo directly owns hook/wrapper/review surfaces | `STANDARDS.md` lists hooks as repo-local requirements without distinguishing managed shims from thick local implementations |

### Planning-Only Scope Enforcement

The execution scope correctly constrains the branch:

- `execution_mode: planning_only`
- `allowed_write_paths` limited to planning, handoff, review, validation, and
  closeout artifacts
- `forbidden_roots` explicitly blocks the primary governance checkout and all
  consumer repos
- No implementation diffs are present or authorized

### Rollout Wave Ordering

The structured plan names a concrete wave order: `local-ai-machine` →
`ai-integration-services` → `seek-and-ponder` → `knocktracker` → `Stampede` →
`HealthcarePlatform` → `ASC-Evaluator`, with `EmailAssistant` excluded until
locally available. This is risk-appropriate given the subagent audit showing
the first four repos are already near-thin, `Stampede` is missing only
`CODEX.md`, and the latter two carry thick local doctrine.

## Required Conditions

The following three changes must be incorporated before the packet is promoted
beyond draft:

### 1. Fix handoff packet `execution_scope_ref` (metadata gap)

`raw/handoffs/2026-04-28-issue-575-thin-session-contract-rollout.json` field
`execution_scope_ref` is `null` despite the execution scope existing at
`raw/execution-scopes/2026-04-28-issue-575-thin-session-contract-rollout-planning.json`.
Set the field to this path. The structured plan's
`execution_handoff.execution_scope_ref` correctly references it, so the handoff
packet must be consistent.

### 2. Resolve ambiguity in handoff acceptance criterion #1

The current wording could be read as requiring the plan artifact itself to
perform code reconciliation, contradicting the planning-only scope. Reword to:

> "The accepted rollout plan declares that governance-source SSOT conflicts
> must be resolved in dedicated child issue(s) before any downstream consumer
> rollout slice executes, and it names the specific conflicts blocking
> rollout."

### 3. Sprint 1 acceptance criteria must name child issue expectations for reconciliation

Sprint 1 acceptance criteria currently state what the plan must declare, but
do not require the plan to name or create the child issues that will perform
the reconciliation. Add an acceptance criterion:

> "The accepted plan names at least one child issue or follow-up branch
> responsible for resolving each identified SSOT conflict before downstream
> rollout begins."

Without this, the reconciliation gate is a stated intent without a traceable
execution path.

## Residual Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Reconciliation child issues are created but never executed, leaving the rollout permanently blocked | Medium | Overlord-sweep should auto-surface stale planned-but-unexecuted reconciliation issues older than 14 days |
| `bootstrap-repo-env.sh` multi-root search may be load-bearing for worktree workflows; removing it without replacement could break current developer UX | Low | The reconciliation slice should audit which callers depend on multi-root search before collapsing to a single canonical path |
| `cli_session_supervisor.py` direct invocation in `codex-review-template.sh` is the only currently-functional cross-model review path; wrapping it may temporarily break the review pipeline if the wrapper doesn't exist yet | Medium | The reconciliation slice must land the wrapper surface and prove it works end-to-end before removing or hiding the direct subprocess path |
| Rollout wave 1 (`local-ai-machine`) depends on LAM's strict `riskfix/` lane conventions; thin-adapter adoption must not weaken those repo-specific lane constraints | Low | `docs/governance-tooling-package.json` non-goals explicitly forbid weakening lane constraints; the thin-adapter contract must preserve profile extensions |
