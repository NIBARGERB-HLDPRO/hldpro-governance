# Phase 4 — HealthcarePlatform Graphify PDCA(R)

Date: 2026-04-09
Owner: Benji / Codex
Repo Pair: `hldpro-governance` + `HealthcarePlatform`
Phase: 4 of the Living Knowledge Base rollout
Status: In Progress

## Plan

Goal:
- Add `HealthcarePlatform` to the Living Knowledge Base as the second governed repo in graphify scope.
- Keep governance as the knowledge home.
- Mirror the Phase 1 AIS pattern: product repo gets read-only pointers + graphify hook integration, governance stores the graph outputs and wiki references.

Approved scope:
- Full HealthcarePlatform repo.
- No HIPAA/BAA documents are stored in the repo.
- No sensitive data is expected in repo contents.
- Governance outputs may be stored in `hldpro-governance`.

Execution rules:
- Work on isolated clean branches/worktrees only.
- Do not push graphify output into `HealthcarePlatform`.
- Keep `hldpro-governance` as the only tracked home for `graphify-out/`.

Success criteria:
- A current HealthcarePlatform graph build exists in governance.
- Governance wiki/index references HealthcarePlatform as an approved graphified repo.
- HealthcarePlatform `CLAUDE.md` and `.claude/settings.json` point at governance in the same pattern as AIS.
- Phase 4 decisions and follow-up notes are documented in governance.

## Do

1. Baseline
- Create isolated worktrees for governance and HealthcarePlatform.
- Confirm current Living Knowledge Base Phase 4 source-plan baseline.

2. HealthcarePlatform graph build
- Run graphify on the full HealthcarePlatform repo from its isolated worktree.
- Prefer the repo root as the target.
- Generate graph outputs including `GRAPH_REPORT.md`, `graph.json`, and `graph.html` if available.

3. Governance capture
- Copy the HealthcarePlatform graph outputs into a dedicated governance path under `graphify-out/healthcareplatform/`.
- Do not overwrite AIS outputs.
- Add or refresh governance wiki/index references for the new repo.

4. Product repo pointer alignment
- Update `HealthcarePlatform/CLAUDE.md` so architecture questions point to governance graph/report paths.
- Update `HealthcarePlatform/.claude/settings.json` to include the graphify PreToolUse hook, preserving existing repo hooks.

5. Governance documentation
- Update the Living Knowledge Base plan note to reflect the explicit approval for full-repo HP scope.
- Add a short decision record or plan note if the existing source plan still says “code only”.

## Check

Operational checks:
- `graphify` completes successfully on HealthcarePlatform.
- Governance contains:
  - `graphify-out/healthcareplatform/GRAPH_REPORT.md`
  - `graphify-out/healthcareplatform/graph.json`
  - `graphify-out/healthcareplatform/graph.html` when produced
- `wiki/index.md` names HealthcarePlatform in knowledge coverage.
- `HealthcarePlatform/CLAUDE.md` contains a governance graph/report pointer.
- `HealthcarePlatform/.claude/settings.json` contains a graphify hook entry without removing existing governance hooks.

Quality checks:
- No generated graph artifacts are committed to HealthcarePlatform.
- Governance remains the source of truth.
- No unrelated repo churn is introduced.

## Act

If graphify output is useful and clean:
- Keep the Phase 4 pattern and use it for later governed repos.

If graphify output is too noisy:
- Narrow with explicit excludes for generated/vendor directories and rerun.

If HealthcarePlatform pointer integration conflicts with existing hooks:
- Merge graphify hook entries conservatively rather than reinstalling blindly.

## Review

Review questions:
- Are the HealthcarePlatform god nodes and communities meaningful enough to aid Stage 1 research?
- Does the governance wiki/index now make cross-repo navigation clearer?
- Is the HP pointer pattern identical enough to AIS to stay maintainable?
- Should Phase 5 reuse the same per-repo subfolder pattern under governance `graphify-out/`?

Follow-on candidates:
- add HealthcarePlatform wiki stub/community article updates
- add a governance closeout for this Phase 4 adoption
- extend the weekly sweep to reference multiple governed graph outputs rather than AIS only
