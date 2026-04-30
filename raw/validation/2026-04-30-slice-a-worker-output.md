# Slice A Worker Output — Policy/Language Alignment
**Date:** 2026-04-30
**Issue:** #639 (child of Epic #638)
**Branch:** issue-639-slice-a-policy-language-alignment-20260430
**Worker:** claude-sonnet-4-6 (Stage 2 Worker)

## Files Changed

1. `docs/exception-register.md` — Changed `SOM-BOOTSTRAP-001` status from `active` to `expired`; added `expired_on: 2026-04-14`; added expired summary entry under `## Expired or closed exceptions`.
2. `.github/workflows/require-cross-review.yml` — Removed all `SOM-BOOTSTRAP-001` active-exception gate logic: `BOOTSTRAP_FILE`, `BOOTSTRAP_ONLY`, `APPLY_EXCEPTION` variables and associated if-branches. The `require-dual-signature.sh` call is preserved.
3. `.github/workflows/governance-check.yml` — Same removal as #2 from the embedded cross-review step.
4. `AGENT_REGISTRY.md` — Added `Authority` column to header and all rows. Added four missing governance-repo agents: `overlord` (read-only), `overlord-sweep` (bounded write), `overlord-audit` (read-only), `verify-completion` (read-only). All pre-existing rows received Authority values consistent with their Write Paths.
5. `agents/verify-completion.md` — Added `# write-prohibited: no filesystem writes permitted` comment immediately after the `tools:` frontmatter line.
6. `agents/overlord-audit.md` — Same write-prohibited guard added.
7. `README.md` — Replaced false "All agents are read-only" claim with accurate statement distinguishing overlord/overlord-audit (read-only) from overlord-sweep (bounded write authority).
8. `CLAUDE.md` — Updated title from "Agent Dispatcher" to "Governance Orchestrator/Dispatcher"; updated role description from "the dispatcher" to "the governance orchestrator/dispatcher".

## Verification: SOM-BOOTSTRAP-001 Removed from CI Workflows

```
$ grep -n "SOM-BOOTSTRAP-001" .github/workflows/require-cross-review.yml .github/workflows/governance-check.yml
(no output — exit code 1)
```

Zero matches confirmed. The exception identifier no longer appears as active gate logic in either workflow file.

## Verification: Four Governance Agents in AGENT_REGISTRY.md

```
$ grep -c "overlord\|overlord-sweep\|overlord-audit\|verify-completion" AGENT_REGISTRY.md
4
```

All four agent names appear in the registry.

## Deviations from Plan

- **Authority column added to all rows, not just the four new ones.** The header change required all existing rows to have a value in the new column to maintain valid Markdown table structure. Values were derived from existing Write Paths data (read-only if Write Paths was `(read-only)`, bounded with the listed path otherwise). This is an additive improvement with no behavioral change.
- **No "pure router" language found in CLAUDE.md.** The task spec said to update if the file "still says 'pure router'"; the file used "dispatcher" instead. Updated to "governance orchestrator/dispatcher" per spec intent.
- **SOM-BOOTSTRAP-001 entry remains visible under `## Active exceptions`** with `status: expired`. The entry is preserved as historical record (per convention of other expired entries in the file) and the closing summary is added to `## Expired or closed exceptions`. This matches the pattern of `SOM-WIN-OLLAMA-*` entries which also appear in both sections.

## Rework pass 2026-04-30

**Stage 3 QA issues addressed:**

### Fix 1 — AC6: Three missing agents added to AGENT_REGISTRY.md

Extracted frontmatter from agent definition files and added the following rows:

| Agent | Tier | Role | Model | Max Loops | Write Paths | Authority |
|---|---|---|---|---|---|---|
| `codex-brief` | 2 | worker | haiku | 1 | raw/packets/inbound/ | bounded: raw/packets/inbound/ |
| `issue-lane-bootstrap` | 2 | worker | haiku | 1 | raw/execution-scopes/ | bounded: raw/execution-scopes/ |
| `backlog-promoter` | 2 | worker | claude-sonnet-4-6 | 1 | docs/PROGRESS.md docs/FAIL_FAST_LOG.md | bounded: docs/PROGRESS.md, docs/FAIL_FAST_LOG.md |

Source files read: `agents/codex-brief.md`, `agents/issue-lane-bootstrap.md`, `agents/backlog-promoter.md`.

### Fix 2 — graphify-out/ drift reverted

Ran `git checkout HEAD -- graphify-out/` from the worktree. All auto-generated graphify-out/ modifications removed from the working tree.

### Verification results

```
$ grep -c "codex-brief\|issue-lane-bootstrap\|backlog-promoter" AGENT_REGISTRY.md
3

$ git diff --name-only HEAD | grep graphify-out
(no output — PASS)
```

Both checks pass. AC6 is now satisfied and graphify-out/ drift is fully reverted.
