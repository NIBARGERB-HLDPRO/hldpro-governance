# Cross review evidence

> 25 nodes · cohesion 0.08

## Key Concepts

- **TestCrossReviewViolations** (11 connections) — `tests/test_cross_review_evidence.py`
- **test_cross_review_evidence.py** (4 connections) — `tests/test_cross_review_evidence.py`
- **_load_module()** (3 connections) — `tests/test_cross_review_evidence.py`
- **.test_agent_change_triggers_enforcement()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_agent_registry_change_triggers_enforcement()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_check_ci_workflow_triggers_enforcement()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_empty_diff_passes()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_hook_change_triggers_enforcement()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_new_cross_review_with_planning_only_passes()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_new_cross_review_without_planning_only_fails()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_non_trigger_file_passes_without_evidence()** (2 connections) — `tests/test_cross_review_evidence.py`
- **.test_trigger_without_evidence_fails()** (2 connections) — `tests/test_cross_review_evidence.py`
- **vcre()** (2 connections) — `tests/test_cross_review_evidence.py`
- **Tests for cross-review evidence validation (AC2).  These tests verify that a PR** (1 connections) — `tests/test_cross_review_evidence.py`
- **Changes to agents/*.md must trigger cross-review enforcement.** (1 connections) — `tests/test_cross_review_evidence.py`
- **Changes to hooks/*.sh must trigger cross-review enforcement.** (1 connections) — `tests/test_cross_review_evidence.py`
- **A plain file change (docs/PROGRESS.md) should not trigger enforcement.** (1 connections) — `tests/test_cross_review_evidence.py`
- **An empty diff should pass without violations.** (1 connections) — `tests/test_cross_review_evidence.py`
- **Changes to .github/workflows/check-*.yml must trigger enforcement.** (1 connections) — `tests/test_cross_review_evidence.py`
- **Changes to AGENT_REGISTRY.md must trigger enforcement.** (1 connections) — `tests/test_cross_review_evidence.py`
- **Load validate_cross_review_evidence from the repo scripts directory.** (1 connections) — `tests/test_cross_review_evidence.py`
- **A PR that introduces raw/cross-review/* without PLANNING_ONLY must fail.** (1 connections) — `tests/test_cross_review_evidence.py`
- **Introducing a cross-review artifact without PLANNING_ONLY=true is a violation.** (1 connections) — `tests/test_cross_review_evidence.py`
- **When PLANNING_ONLY=true is set by the caller, trusted-base rule is relaxed.** (1 connections) — `tests/test_cross_review_evidence.py`
- **A trigger file (STANDARDS.md) without any cross-review artifact must fail.** (1 connections) — `tests/test_cross_review_evidence.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `tests/test_cross_review_evidence.py`

## Audit Trail

- EXTRACTED: 48 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*