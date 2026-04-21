# Issue #432 Validation: SoM Waterfall Routing

Issue: [#432](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/432)
Branch: `issue-432-som-waterfall-routing-20260421`

## Scope

Update the governance source of truth for model routing: Codex orchestrates, Opus plans, GPT-5.4 high reviews plans with Spark only as logged same-family fallback/specialist critique, Sonnet implements, Codex QA reviews, Qwen handles bounded local worker chunks, Gemma stays A/B shadow-only, and Windows Ollama is off the active governance waterfall.

## Downstream Follow-Ups

- local-ai-machine: https://github.com/NIBARGERB-HLDPRO/local-ai-machine/issues/506
- ai-integration-services: https://github.com/NIBARGERB-HLDPRO/ai-integration-services/issues/1207
- HealthcarePlatform: https://github.com/NIBARGERB-HLDPRO/HealthcarePlatform/issues/1441
- ASC-Evaluator: https://github.com/NIBARGERB-HLDPRO/ASC-Evaluator/issues/9
- seek-and-ponder: https://github.com/NIBARGERB-HLDPRO/seek-and-ponder/issues/145
- Stampede: https://github.com/NIBARGERB-HLDPRO/Stampede/issues/97

## Validation

Passed before closeout:

- `python3 -m json.tool docs/plans/issue-432-structured-agent-cycle-plan.json`
- `python3 -m json.tool raw/execution-scopes/2026-04-21-issue-432-som-waterfall-routing-implementation.json`
- `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-21-issue-432-som-waterfall-routing.md`
- `python3 .github/scripts/check_lam_family_diversity.py`
- `python3 scripts/lam/test_runtime_inventory.py`
- `bash scripts/windows-ollama/tests/test_decide.sh`
- `bash scripts/windows-ollama/tests/test_integration.sh`
- `python3 scripts/orchestrator/test_delegation_hook.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-432-som-waterfall-routing-20260421 --require-if-issue-branch`
- `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-432-som-waterfall-routing-implementation.json --require-lane-claim`
- `python3 -m py_compile scripts/lam/runtime_inventory.py .github/scripts/check_lam_family_diversity.py`
- `python3.11 scripts/packet/test_validate.py`
- `python3.11 scripts/orchestrator/test_packet_queue.py`
- `python3.11 scripts/overlord/test_validate_structured_agent_cycle_plan.py`
- `python3.11 scripts/overlord/test_assert_execution_scope.py`
- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json`
- `hooks/closeout-hook.sh raw/closeouts/2026-04-21-issue-432-som-waterfall-routing.md`
- `git diff --check`

## Notes

`assert_execution_scope.py` passed with warnings for declared dirty sibling roots in active parallel lanes. The broader packet tests were run with `python3.11` because the default Homebrew `python3` is Python 3.14 and lacks the repo's packet `jsonschema` dependency. The first Local CI Gate run caught closed issue #430 in an active backlog row; this slice moved #430 to completed history, and the final Local CI Gate run passed. The closeout hook refreshed graph/wiki outputs and skipped memory-writer consolidation because credentials were not configured. Historical raw fallback and closeout artifacts still contain prior Spark/Windows routing records by design; current live standards, runbooks, tests, and guardrails now supersede those records.
