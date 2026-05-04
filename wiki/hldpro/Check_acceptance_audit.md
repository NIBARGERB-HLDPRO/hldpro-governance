# Check acceptance audit

> 14 nodes · cohesion 0.20

## Key Concepts

- **test_check_acceptance_audit.py** (7 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **run_check()** (7 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **test_audit_dir_exists_but_no_matching_issue()** (3 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **test_no_audit_dir_exits_1()** (3 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **test_non_issue_branch_exempt()** (3 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **test_pass_artifact_present_and_matching()** (3 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **test_planning_only_flag_exempt()** (3 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **Tests for check_acceptance_audit.py — functional acceptance audit CI gate.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **Helper: run check_acceptance_audit.py with given args against a temp audit dir.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **PASS artifact with matching issue_number and overall_verdict=PASS → exits 0.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **Non-existent audit dir → exits 1.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **Audit dir exists but no artifact for the branch issue → exits 1.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **Non-issue branch (e.g. chore/foo) → exits 0 (exempt).** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`
- **planning_only flag → exits 0 regardless of audit artifacts.** (1 connections) — `hldpro-governance/tests/test_check_acceptance_audit.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/tests/test_check_acceptance_audit.py`

## Audit Trail

- EXTRACTED: 26 (72%)
- INFERRED: 10 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*