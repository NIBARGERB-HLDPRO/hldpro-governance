# Governance Path Repair Findings

Date: 2026-04-17
Repo: hldpro-governance
Issue: [#223](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/223)
Status: PLANNING_ONLY
Subject: Compendium work sequencing break and repair path

## Purpose

This note preserves the process finding behind issue #223. The org governance
compendium work began as implementation-first work in the shared main checkout.
That violated the repo's governance path for cross-repo governance/tooling
changes.

This file is a planning artifact only. It does not approve, complete, or
retroactively bless the existing draft diff.

## Workspace State At Finding

The shared checkout contained implementation-first changes for the compendium
work:

- `.github/workflows/overlord-sweep.yml`
- `agents/overlord-sweep.md`
- `docs/DATA_DICTIONARY.md`
- `docs/FEATURE_REGISTRY.md`
- `docs/SERVICE_REGISTRY.md`
- `docs/ORG_GOVERNANCE_COMPENDIUM.md`
- `docs/plans/org-governance-compendium-pdcar.md`
- `scripts/overlord/build_org_governance_compendium.py`

The checkout was also on `main...origin/main` with local commits and uncommitted
changes. That is a risk condition for governance work because branch/worktree
isolation should happen before implementation.

## Primary Finding

The compendium request was cross-repo governance/tooling work, not a small
deterministic local edit.

The correct path was:

1. Classify the request as cross-repo governance/tooling work.
2. Create or identify the governing GitHub issue first.
3. Add the work to the repo execution tracker or backlog with acceptance
   criteria.
4. Produce the canonical structured JSON plan.
5. Record specialist review and alternate-family review in the plan.
6. Decompose into slices, microsprints, and acceptance criteria.
7. Only then implement the generator, generated markdown, sweep integration,
   and registry updates.

The actual path inverted this order. Implementation happened first, and a
Markdown PDCAR companion was created after implementation had already started.

## Rule Evidence

- `STANDARDS.md`: backlog-first workflow requires plan and acceptance criteria
  before implementation.
- `STANDARDS.md`: GitHub Issues are canonical for governance work.
- `STANDARDS.md`: structured JSON is the canonical execution-plan artifact.
- `README.md`: JSON is canonical; Markdown is optional companion context.
- `docs/schemas/structured-agent-cycle-plan.schema.json`: requires issue
  number, sprints, reviews, execution handoff, approval metadata, and material
  deviation rules.
- `scripts/overlord/validate_structured_agent_cycle_plan.py`: validates the
  canonical plan fields.

## Missing Or Late Artifacts

At the time of the finding:

- No GitHub issue existed for the compendium work.
- No canonical `*structured-agent-cycle-plan.json` existed for the compendium
  work.
- The only plan artifact was Markdown:
  `docs/plans/org-governance-compendium-pdcar.md`.
- No alternate-family review was recorded before execution.

The Markdown PDCAR may still be useful as companion context, but it is not the
canonical source of truth.

## Mechanical Control Gap

The current structured-plan validator has a bypass lane.

The validator only hard-requires a structured plan when
`--require-if-issue-branch` is used and the branch starts with `issue-` or
`riskfix/`. Because the compendium work happened in the shared main checkout,
the strongest mechanical gate did not fire.

That does not make the work compliant. It means the repo lacks a sufficient
guard for governance-surface edits made from the wrong branch or checkout.

## Root Cause

The root cause has two parts:

1. Classification failure: cross-repo governance artifact work was treated like
   bounded deterministic tooling.
2. Sequencing failure: research findings were used as implementation input
   instead of plan-review input.

The compendium work touched org-level documentation, weekly sweep behavior,
governance registries, and index/compendium surfaces. That belongs on the
architecture/standards handoff chain with dual planning and review boundaries.

## Repair Path

Treat the existing compendium diff as an unapproved working draft.

The compliant repair path is:

1. Freeze the current draft.
2. Inventory exactly what files changed and what behavior changed.
3. Create or identify the governing GitHub issue.
4. Add the work to the execution tracker or backlog with acceptance criteria.
5. Write the canonical `*structured-agent-cycle-plan.json`.
6. Record specialist review and alternate-family review.
7. Decompose into slices and microsprints.
8. Decide whether the existing diff satisfies the approved plan or needs
   rework.
9. Only then continue implementation, cleanup, commit, or discard.

The existing draft can be salvaged, but only after it is brought under an
approved plan in an isolated worktree.

## Suggested Validator Improvement

The structured plan gate should be strengthened so governance-surface edits
cannot bypass planning by happening on `main` or on a non-issue branch.

Potential behavior:

- If changed files touch governance, standards, sweep, registry, architecture,
  or closeout surfaces, require a structured plan regardless of branch name.
- If such changes happen on `main`, hard-fail or require an explicit documented
  exception.
- If `docs/plans/*.md` exists for governed work without a matching canonical
  JSON plan, warn or fail depending on scope.
- If implementation files exist before issue/plan metadata, fail the closeout
  gate.

Candidate governance-surface paths:

- `CLAUDE.md`
- `STANDARDS.md`
- `README.md`
- `agents/`
- `.github/workflows/`
- `docs/FEATURE_REGISTRY.md`
- `docs/SERVICE_REGISTRY.md`
- `docs/DATA_DICTIONARY.md`
- `docs/ORG_GOVERNANCE_COMPENDIUM.md`
- `docs/schemas/`
- `scripts/overlord/`
- `scripts/knowledge_base/`
- `OVERLORD_BACKLOG.md`
- `docs/PROGRESS.md`
- `wiki/`
- `raw/closeouts/`
- `raw/cross-review/`

## Next Compliant Action

Planning remains the next action.

Do not continue implementing the compendium, sweep integration, or registry
updates until the governing issue, canonical structured JSON plan, reviews, and
acceptance criteria exist.

When implementation resumes, use an isolated issue worktree and an
execution-scope/write-boundary artifact so changes do not land in the wrong
checkout.
