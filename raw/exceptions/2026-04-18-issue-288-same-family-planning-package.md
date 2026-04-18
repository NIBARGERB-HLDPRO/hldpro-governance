# Exception: Issue #288 Same-Family Planning Package

## Exception

- ID: `SOM-ISSUE-288-SAME-FAMILY-PLANNING-PACKAGE`
- Issue: #288
- Scope: planning artifacts, review artifact, execution scope, backlog mirror, and progress mirror for the org governance tooling distribution epic
- Reason: the operator instructed the current Codex session to proceed end to end, and no callable alternate-family review tool is available in this lane.
- Mitigation: subagent review, deterministic plan validation, execution-scope preflight, backlog alignment, Local CI Gate, and GitHub Actions are required before merge.
- Expires: 2026-04-19T19:30:00Z

This exception does not authorize shared tooling code changes, downstream repo edits, or bypassing CI. Implementation slices must obtain fresh review evidence or a separately scoped exception.
