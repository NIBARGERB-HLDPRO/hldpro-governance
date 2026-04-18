# Exception: Issue #292 Same-Family Deployer Slice

## Exception

- ID: `SOM-ISSUE-292-SAME-FAMILY-DEPLOYER`
- Issue: #292
- Parent epic: #288
- Scope: package-level governance tooling deployer, deployer tests, contract/runbook updates, Local CI Gate profile wiring, status mirrors, and closeout evidence
- Reason: the operator instructed the current Codex lane to continue through the issue-backed implementation loop, and no callable alternate-family review tool is available in this session.
- Mitigation: subagent review, real temporary git repo e2e tests, compatibility shim tests, execution-scope preflight, structured-plan validation, Local CI Gate, and GitHub Actions are required before merge.
- Expires: 2026-04-19T22:27:43Z

This exception does not authorize downstream repo edits, final downstream e2e proof claims, or bypassing CI.
