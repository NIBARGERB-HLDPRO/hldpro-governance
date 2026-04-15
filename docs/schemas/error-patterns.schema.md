# ERROR_PATTERNS.md Canonical Schema

All governed repos use this schema for `docs/ERROR_PATTERNS.md`. Patterns are reusable solutions to recurring failures.

## Markdown Structure

```markdown
---
[optional: legacy: true]
---

# ERROR_PATTERNS

## {pattern-id}

### Symptom
[Observable failure, user-facing or internal detection; 2-3 sentences]

### Root Cause
[Why the failure occurs; dig into the mechanism; 2-3 sentences]

### Detection
[How to detect this pattern in logs/metrics; specific signals, log keywords, thresholds; bullet list]

### Resolution Playbook
[Step-by-step fix; numbered list; include rollback instructions if applicable]

### Instances
[Dated incidents that matched this pattern; table of Date | Ref (FAIL_FAST_LOG link) | Notes]

### Prevention
[Code, config, or monitoring changes to prevent recurrence; bullet list]

---

## {next-pattern-id}
[... repeat structure ...]
```

## Section Definitions

| Section | Semantics | Required? | Notes |
|---------|-----------|-----------|-------|
| **Symptom** | What the user or operator observes | Yes | Objective, measurable. Example: "CI workflow hangs on macOS runners after 10 min." |
| **Root Cause** | Mechanism of failure (why symptom occurs) | Yes | Dig one level deeper than surface-level description. Explain the causal chain. |
| **Detection** | How to spot this in monitoring/logs without waiting for user report | Yes | Include specific log strings, metrics, error codes. Allow for `null` (undetectable) if honest. |
| **Resolution Playbook** | Numbered steps to resolve (including rollback) | Yes | Executable by on-call engineer. Each step ≤1 sentence. |
| **Instances** | Logged occurrences of this pattern | No (optional) | Historical record. Helps engineers learn from past incidents. |
| **Prevention** | Code/config changes to reduce recurrence | No (optional) | Future work; can be empty or a checklist. |

## Entry Rules

1. **Pattern ID format**: kebab-case, ≤40 chars, descriptive (e.g., `github-actions-node-deprecation`, `plaid-token-expiry-race`, `supabase-connection-pool-exhaustion`)
2. **Symptom**: Observable failure state (not just "something broke")
3. **Root Cause**: Dig into mechanisms; cite code paths, config, or external dependencies
4. **Detection**: Include specific log keywords, metrics thresholds, error codes; allow `null` if undetectable
5. **Playbook**: Numbered steps, each ≤1 sentence; include explicit rollback step if applicable
6. **Instances**: Link to corresponding `FAIL_FAST_LOG.md` entries (format: `[YYYY-MM-DD](../FAIL_FAST_LOG.md)` or just date)
7. **Prevention**: Futuristic or aspirational; OK to leave empty during Phase 1
8. **No code blocks in patterns**: Use pseudocode or bullet points; actual code lives in issues/PRs/code repos

## Legacy patterns

If a repo's existing ERROR_PATTERNS.md uses a different format, add this frontmatter at the top:

```markdown
---
legacy: true
---
```

New patterns MUST use the canonical structure. During Phase 1–2, legacy patterns are grandfathered. A future phase may reformat them.

## Empty (stub) patterns

A pattern section can be minimal during Phase 1 if no pattern history exists yet:

```markdown
## {pattern-id}

### Symptom
[To be populated]

### Root Cause
[To be populated]

### Detection
[To be populated]

### Resolution Playbook
[To be populated]

### Instances
None yet.

### Prevention
[To be determined]
```

Phase 2 activities will populate these sections as incidents occur.

## Example Pattern (full)

```markdown
## github-actions-node-deprecation

### Symptom
CI workflows fail with deprecation warning: "Node.js 20 actions are deprecated and will be removed..." Workflow steps complete but artifact upload or checkout fails intermittently.

### Root Cause
GitHub Actions default runner images deprecated Node.js 20 in favor of Node.js 22. Legacy action versions (e.g., `actions/checkout@v4`) still target Node 20, causing runtime errors on newer runner images.

### Detection
- Log: `Node.js 20 actions are deprecated`
- Workflow step: artifact upload or checkout step marked with orange warning icon
- Timeline: Failures began 2026-04-07 UTC

### Resolution Playbook
1. In your workflow YAML, update all GitHub actions to newer versions.
2. Example: change `actions/checkout@v4` → `actions/checkout@v6`
3. Re-run the failing workflow.
4. If still failing, check runner OS image version in Actions settings; upgrade runner if needed.
5. Rollback: revert action versions to prior commit; re-push.

### Instances
| Date | Incident | Notes |
|------|----------|-------|
| 2026-04-15 | [2026-04-15](../FAIL_FAST_LOG.md) | Fixed by upgrading checkout action |

### Prevention
- Pin action versions explicitly; audit quarterly for EOL
- Run test workflows on new OS images during beta phases
- Subscribe to GitHub Actions blog for deprecation announcements
```

## CI Validation

The `check-fail-fast-schema.yml` workflow validates every PR touching this file:
- Parses the Markdown section structure
- Ensures each pattern has required sections (Symptom, Root Cause, Detection, Resolution Playbook)
- Validates pattern ID format (kebab-case, ≤40 chars)
- Optionally checks that all instances reference existing FAIL_FAST_LOG.md entries
- Reports errors with section names and line numbers

Workflow fails on violations; PR cannot merge until fixed.

## Frontmatter Options

```yaml
---
legacy: true           # Indicates this file predates the canonical schema
version: "1.0"         # Optional schema version (defaults to current)
---
```

All new ERROR_PATTERNS.md files should NOT include version frontmatter in Phase 1. Versioning is reserved for future schema evolution.
