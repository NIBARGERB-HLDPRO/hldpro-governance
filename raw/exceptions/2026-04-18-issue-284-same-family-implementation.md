# Exception: Issue #284 Same-Family Implementation

## Exception

- ID: `SOM-ISSUE-284-SAME-FAMILY-IMPLEMENTATION`
- Issue: #284
- Scope: local-first workflow coverage inventory, validator, tests, Local CI Gate wiring, and evidence artifacts
- Reason: the same Codex session is carrying the issue from planning through implementation under explicit operator instruction to loop E2E with no HITL.
- Mitigation: subagent review is used for repository-rule and workflow-classification checks, and deterministic local/GitHub Actions tests are required before closeout.
- Expires: 2026-04-19T18:30:00Z

This exception does not authorize consumer repo edits, ruleset changes, or bypassing CI.
