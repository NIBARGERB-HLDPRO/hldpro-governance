# PDCAR — Issue #561: sim-runner Deployer Path + Shared Persona Path Fix
Date: 2026-04-22
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/561

## Problem

`agents/sim-runner.md` documents two incorrect paths for hldpro-sim setup:

1. **Step 1 (install check):** Falls back to `pip install hldpro-sim==0.1.0` (PyPI), which does not exist — hldpro-sim is a private governance package, not a public PyPI release. This would cause an immediate install failure for any operator following the agent's instructions.

2. **Step 3 (persona resolution):** The shared-persona fallback path is `packages/hldpro-sim/personas/<persona_id>.json`. This path references the governance repo's *source* directory, not the *deployed* location in the consumer repo. The deployer (`scripts/deployer/deploy-hldpro-sim.sh`) places managed personas at `sim-personas/shared/` in the consumer repo — not at `packages/hldpro-sim/personas/`.

Additionally, `docs/agents-adoption-guide.md` lists the sim-runner prerequisite as `hldpro-sim installed: python3 -c "import hldprosim" passes` with no reference to how to actually install it in a consumer repo, leaving the deployer undiscoverable.

## Design

Two surgical edits to `agents/sim-runner.md`:
- Replace Step 1's PyPI fallback block with a deployer-first check: verify `.hldpro/hldpro-sim.json` exists; if absent, run `deploy-hldpro-sim.sh`. This aligns the agent with the actual install contract defined in `docs/hldpro-sim-consumer-pull-state.json`.
- Fix Step 3's shared fallback path from `packages/hldpro-sim/personas/` to `sim-personas/shared/`, which is where `deploy-hldpro-sim.sh` copies managed personas (line 49: `PERSONAS_DEST="$CONSUMER/sim-personas/shared"`).

One addition to `docs/agents-adoption-guide.md`:
- Add an "Installation" subsection to the `### sim-runner` block documenting the canonical deployer command, the two artifacts to commit (`.hldpro/hldpro-sim.json` and `sim-personas/shared/`), and the `pinned_sha` verification step.

No changes to the deployer script itself — it is correct.

## Constraints

- Edits must be surgical: only the affected steps in sim-runner.md, only the sim-runner block in the adoption guide.
- No changes to `scripts/deployer/deploy-hldpro-sim.sh`, `docs/hldpro-sim-consumer-pull-state.json`, or `packages/hldpro-sim/`.
- The Step 4 `PersonaLoader(shared_dir=pathlib.Path("packages/hldpro-sim/personas"))` reference in the Python invocation pattern is a follow-on concern (a code change, not a documentation fix) — deferred to a separate issue.
- Branch based on `issue-559-five-new-agents-20260422` (not origin/main) since these files were introduced in PR #560.

## Acceptance Criteria

1. `agents/sim-runner.md` Step 1: no reference to `pip install hldpro-sim==0.1.0` or PyPI; deployer check is the canonical path.
2. `agents/sim-runner.md` Step 3: shared fallback is `sim-personas/shared/<persona_id>.json`.
3. `docs/agents-adoption-guide.md` sim-runner block: deployer command, `.hldpro/hldpro-sim.json` commit requirement, `sim-personas/shared/` commit requirement, and `pinned_sha` verification step are all documented.
4. Structured plan validator passes: `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-561-sim-runner-deployer-path-20260422` returns PASS.
5. Commit is clean: only the six files in the execution scope's `allowed_write_paths` are modified.

## Risks

- **Persona path mismatch in Step 4 Python snippet:** The `PersonaLoader(shared_dir=...)` argument in Step 4 still points to the old governance-source path. This is out of scope but should be tracked — a consumer running Step 4 verbatim will hit a FileNotFoundError if the directory does not exist. Mitigation: document as a known follow-on (separate issue).
- **Consumer repos with old sim-runner cached:** Operators using a cached copy of `sim-runner.md` from before this fix will still see the stale paths. Mitigation: the adoption guide update makes the deployer the prominent entry point, reducing reliance on the agent's internal Step 1 text.
