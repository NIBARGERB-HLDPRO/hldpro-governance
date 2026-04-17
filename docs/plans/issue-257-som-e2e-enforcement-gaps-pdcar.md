# Issue #257 — SoM E2E Enforcement Gaps PDCA/R

## Plan

Issue #257 closes the gap between a packet dry-run passing and the full Society of Minds governance chain being hard-gated end to end.

The current validators prove packet shape, packet queue behavior, structured-plan shape, and execution-scope behavior independently. The broken edge is the integration contract between them:

- A dirty shared checkout on `main` can reach the governance-surface gate before a safe issue-branch execution context exists.
- A packet can name an arbitrary existing file as `governance.execution_scope_ref`; the #231 pilot names a PDCAR Markdown file instead of an execution-scope JSON.
- Current planner-boundary CI would reject the #231 pilot changed-file set because no `raw/execution-scopes/*issue-231*...json` artifact exists.
- Repo-local E2E starts at packet/plan/artifact validation and does not exercise natural-language intent parsing through the MCP daemon in `local-ai-machine/services/som-mcp/`.

The solution is to make the handoff boundaries explicit and mechanically checked:

1. Require packet dispatch scope evidence to be an execution-scope JSON when `execution_scope_ref` is present.
2. Run `assert_execution_scope.py` from packet queue dispatch validation for any packet that declares an execution scope, using the declared validation or changed-file evidence.
3. Add regression tests proving Markdown PDCAR refs are refused as execution-scope refs.
4. Add a local E2E/CI simulation test for the pilot changed-file set so missing issue-specific scopes fail before closeout claims readiness.
5. Define the repo-local boundary for natural-language input: this repo requires a structured packet or MCP handoff artifact from `local-ai-machine`; it does not locally emulate fuzzy intent parsing.

## Do

Implementation should land in a follow-up branch after this planning artifact is reviewed.

Expected implementation files:

- `scripts/orchestrator/packet_queue.py`
- `scripts/orchestrator/test_packet_queue.py`
- `scripts/overlord/validate_structured_agent_cycle_plan.py` or a focused E2E helper if needed
- `scripts/overlord/test_validate_structured_agent_cycle_plan.py` or a new focused E2E test
- `docs/DATA_DICTIONARY.md`
- `docs/FEATURE_REGISTRY.md`
- `raw/execution-scopes/*issue-257*implementation*.json`
- Optional compatibility repair for #231 by adding `raw/execution-scopes/*issue-231*planning*.json` and updating the pilot packet only if the branch scope explicitly authorizes historical artifact repair.

Implementation rules:

- Do not weaken dry-run safety. `dry_run_authorized: true` must never permit live dispatch.
- Do not make PDCAR Markdown an accepted execution-scope substitute.
- Do not require this repo to start or mock the `local-ai-machine` MCP daemon for repo-local validation.
- If cross-repo MCP validation is added, represent it as an explicit handoff artifact or fixture from the canonical MCP repo.

## Check

Required validation for the implementation slice:

- `python3 scripts/packet/validate.py raw/packets/2026-04-17-issue-231-e2e-pilot.yml`
- `python3 scripts/orchestrator/test_packet_queue.py`
- `python3 scripts/packet/test_validate.py`
- `python3 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3 scripts/overlord/test_assert_execution_scope.py`
- `python3 -m py_compile scripts/orchestrator/packet_queue.py scripts/orchestrator/test_packet_queue.py scripts/overlord/validate_structured_agent_cycle_plan.py scripts/overlord/test_validate_structured_agent_cycle_plan.py scripts/overlord/assert_execution_scope.py`

New or updated tests must prove:

- A packet with `governance.execution_scope_ref: docs/plans/*.md` is refused when dispatch validation expects execution-scope evidence.
- A packet with a valid `raw/execution-scopes/*issue-<n>*implementation*.json` ref passes scope validation only when changed files are within `allowed_write_paths`.
- A pilot changed-file set containing planner-boundary files fails when no matching issue-specific execution scope exists.
- A dry-run packet without live dispatch authorization remains dry-run only.
- Repo-local E2E documents that natural-language MCP parsing is an external handoff boundary, not silently skipped local coverage.

## Adjust

If validating the #231 historical packet directly would require changing merged history semantics, do not rewrite the pilot conclusion. Add a compatibility scope artifact and document that #231 was dry-run-only, while #257 makes future packets fail closed.

If packet queue dispatch cannot safely run `assert_execution_scope.py` because it lacks changed-file context, require the packet governance block to reference an explicit changed-file artifact or a structured plan field that can be deterministically converted into changed paths.

If the MCP daemon handoff cannot be tested from this repo without depending on a sibling checkout, add a fixture contract:

- `source_repo: local-ai-machine`
- `source_component: services/som-mcp`
- `handoff_type: intent_to_packet`
- `artifact_ref: <packet or JSON fixture path>`
- `validator: scripts/packet/validate.py`

## Review

The review should focus on integration correctness, not only unit-level green tests:

- Does a passing packet dry-run now imply the packet has valid execution-scope evidence?
- Would current planner-boundary CI accept the same changed-file set the packet claims is authorized?
- Is the repo-local E2E boundary with `local-ai-machine` explicit enough that natural-language input coverage cannot be overstated?
- Are dry-run and live dispatch authorization still separate?

Completion is not valid until the implementation branch has a closeout artifact that cites the new regression tests and the planner-boundary simulation.
