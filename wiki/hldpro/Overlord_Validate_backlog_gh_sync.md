# Overlord Validate backlog gh sync

> 10 nodes · cohesion 0.29

## Key Concepts

- **validate_backlog_gh_sync.py** (5 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **main()** (5 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **check_github_issue()** (3 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **find_planned_table()** (3 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **parse_columns()** (3 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **resolve_issue_number()** (3 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **Return (header_line_index, list_of_data_lines) for the ## Planned table.** (1 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **Split a markdown table row into a dict keyed by header column names.     Returns** (1 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **Extract a #NNN from the cell value.     Returns the integer issue number, or Non** (1 connections) — `scripts/overlord/validate_backlog_gh_sync.py`
- **Call GitHub API to verify issue exists and is open.     Returns (ok: bool, title** (1 connections) — `scripts/overlord/validate_backlog_gh_sync.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `scripts/overlord/validate_backlog_gh_sync.py`

## Audit Trail

- EXTRACTED: 18 (69%)
- INFERRED: 8 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*