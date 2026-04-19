# Issue #313 Registry Surface Review

Date: 2026-04-19
Reviewer: Codex subagent `James`
Scope: Read-only registry surface reconciliation review for hldpro-governance#313.

## Verdict

Accepted with follow-up applied.

## Findings

- Medium: `scripts/overlord/validate_registry_surfaces.py` duplicated registry subsystem membership as hard-coded expected sets. Fixed by removing the second allowlist and validating registry-derived subsystem selections without naming repo membership outside `docs/governed_repos.json`.
- Low: `README.md` still said "Three workflows" in a section that now lists more workflow-backed surfaces. Fixed by changing the heading text to "Key workflows".
