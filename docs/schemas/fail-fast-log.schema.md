# FAIL_FAST_LOG.md Canonical Schema

All governed repos use this schema for `docs/FAIL_FAST_LOG.md`. Entries are logged chronologically as a Markdown table.

## Table Format

```
| Date | Category | Severity | Error | Root Cause | Resolution | Related Pattern |
|------|----------|----------|-------|-----------|------------|-----------------|
| YYYY-MM-DD | String | CRITICAL/ERROR/WARN | Brief description | Root cause analysis | Action taken | Link or pattern ID |
```

## Column Definitions

| Column | Semantics | Example |
|--------|-----------|---------|
| **Date** | ISO 8601 date of incident discovery | 2026-04-15 |
| **Category** | Broad failure domain: `CI`, `Runtime`, `Data`, `Auth`, `Dependency`, `Config`, `Deploy`, `Infra`, `Other` | CI |
| **Severity** | Incident severity: `CRITICAL` (prod down), `ERROR` (feature broken), `WARN` (degraded) | ERROR |
| **Error** | Short description of the symptom (1-15 words) | GitHub Actions Node 20 deprecated |
| **Root Cause** | Why it happened (2-5 words) | Actions runner default outdated |
| **Resolution** | How it was fixed (1-5 words) | Upgraded checkout to v6 |
| **Related Pattern** | Link to corresponding entry in `docs/ERROR_PATTERNS.md` or pattern ID | `github-actions-deprecation` |

## Entry Rules

1. **Chronological order**: newer entries at the top, oldest at the bottom
2. **One issue per row**: Do not collapse multiple failures into one entry
3. **Pattern linkage**: Every entry MUST reference an existing pattern in `ERROR_PATTERNS.md` (even if pattern is stub); use format `[pattern-id](../)` or bare pattern ID
4. **Exact timestamps**: Date is discovery/report date, not resolution date
5. **Plain markdown tables only**: No HTML, no multiline cells (use `;` to separate if needed)
6. **Character limits**: 
   - Error: ≤80 chars
   - Root Cause: ≤60 chars
   - Resolution: ≤50 chars
7. **No PII**: Scrub before logging

## Legacy entries

If a repo's existing FAIL_FAST_LOG.md has entries in a different format, add this frontmatter to the file:

```markdown
---
legacy: true
---

# FAIL_FAST_LOG

[... existing entries in old format ...]
```

New entries MUST use the canonical table format below the legacy block. During Phase 1–2 migrations, legacy entries are grandfathered. A future phase may migrate them; do not mix formats in new rows.

## Example

```markdown
| Date | Category | Severity | Error | Root Cause | Resolution | Related Pattern |
|------|----------|----------|-------|-----------|------------|-----------------|
| 2026-04-15 | CI | ERROR | GitHub Actions Node 20 deprecated | Actions runner default outdated | Upgraded checkout to v6 | github-actions-deprecation |
| 2026-04-14 | Runtime | WARN | Auth token expiry not cached | Session TTL mismatch | Added 30min buffer logic | token-expiry-race |
```

## CI Validation

The `check-fail-fast-schema.yml` workflow validates every PR touching this file:
- Parses the Markdown table
- Ensures each row has exactly 7 columns
- Validates date format (YYYY-MM-DD)
- Enforces category is one of: CI, Runtime, Data, Auth, Dependency, Config, Deploy, Infra, Other
- Enforces severity is one of: CRITICAL, ERROR, WARN
- Checks character limits
- Verifies pattern reference exists in ERROR_PATTERNS.md
- Reports errors with line numbers

Workflow fails on any violation; PR cannot merge until fixed.
