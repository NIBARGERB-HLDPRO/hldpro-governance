# hldpro-governance — Feature Registry

**Last Updated:** 2026-04-06
**Scope:** Shared governance standards, reusable CI enforcement, and cross-repo audit agents.

---

## Status Taxonomy

| Implementation Status | Meaning |
|---|---|
| `COMPLETE` | Built and in active use |
| `IN_PROGRESS` | Actively being changed or expanded |
| `PLANNED` | Intended but not yet implemented |

| Readiness | Meaning |
|---|---|
| `REQUIRED` | Expected baseline for governed repos |
| `OPS_READY` | Ready for operational use by repo maintainers |
| `INTERNAL_ONLY` | Internal tooling, not a repo baseline |

---

## Summary Table

| Feature ID | Domain | Feature | Status | Readiness |
|---|---|---|---|---|
| GOV-001 | STANDARDS | Shared standards manifest in `STANDARDS.md` | COMPLETE | REQUIRED |
| GOV-002 | CI_ENFORCEMENT | Reusable GitHub governance workflow | COMPLETE | REQUIRED |
| GOV-003 | AGENT_AUDIT | Overlord audit agents (`overlord`, `overlord-sweep`, `overlord-audit`) | COMPLETE | OPS_READY |
| GOV-004 | COMPLETION_VERIFICATION | `verify-completion` agent and artifact verification protocol | COMPLETE | OPS_READY |
| GOV-005 | BACKLOG_CONTROL | Cross-repo backlog coordination in `OVERLORD_BACKLOG.md` | COMPLETE | OPS_READY |
| GOV-006 | FEATURE_REGISTRY_POLICY | Feature-registry requirement and co-staging enforcement | IN_PROGRESS | REQUIRED |

---

## Domain Notes

### STANDARDS

| Feature ID | Notes |
|---|---|
| GOV-001 | Defines the baseline governance contract for all HLDPRO code repos, including hooks, CI, security tiers, and verification rules. |

### CI_ENFORCEMENT

| Feature ID | Notes |
|---|---|
| GOV-002 | Reusable workflow enforces doc co-staging, placeholder scans, migration documentation, and other shared merge gates. |
| GOV-006 | Current rollout adds `docs/FEATURE_REGISTRY.md` as a governed artifact and blocks stale code-only changes when the registry is not updated. |

### AGENT_AUDIT

| Feature ID | Notes |
|---|---|
| GOV-003 | Agent set performs repo sweeps, standards audits, and backlog-quality checks across the portfolio. |
| GOV-004 | Completion verifier exists to prevent false “done” claims by checking artifacts, PR state, and standards compliance. |

### BACKLOG_CONTROL

| Feature ID | Notes |
|---|---|
| GOV-005 | `OVERLORD_BACKLOG.md` tracks cross-repo governance work; per-repo execution details stay in each repo’s `docs/PROGRESS.md`. |
