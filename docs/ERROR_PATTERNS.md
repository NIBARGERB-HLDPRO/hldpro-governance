# ERROR_PATTERNS

Reusable solutions to recurring governance failures. See `docs/schemas/error-patterns.schema.md` for the canonical schema.

## Contributing

When a pattern emerges from one or more incidents in `FAIL_FAST_LOG.md`, document it here following the schema:

1. Create a new `## Pattern: <kebab-case-id>` section (kebab-case name, e.g., `overlord-sweep-stale-checkout`)
2. Fill in: Symptom, Root Cause, Detection, Resolution Playbook, Instances
3. Optional: Prevention (can be empty for Phase 1)
4. Reference the pattern in your `FAIL_FAST_LOG.md` entries

See `docs/schemas/error-patterns.schema.md` for examples and detailed field semantics.

## Pattern: overlord-sweep-self-learning-skipped

**Symptom:** `metrics/self-learning/latest.json` remains stale even after new closeouts, fail-fast entries, or operator-context records land.

**Root Cause:** A pre-sweep gate fails before `.github/workflows/overlord-sweep.yml` reaches the `Build self-learning knowledge report` step. In the April 2026 instances, `check_codex_model_pins.py` first scanned both an authoritative hldpro-sim provider invocation missing `model_reasoning_effort` and stale local worktree mirrors under `var/worktrees/**`; after that was fixed, `memory_integrity.py` assumed operator-local Claude memory files existed on GitHub-hosted runners. Both failures stopped self-learning report generation before it could refresh.

**Detection:** Compare `metrics/self-learning/latest.json.generated_at` to current governance activity. Also inspect the latest `Overlord Sweep -- Weekly Cross-Repo Audit` GitHub Actions run and confirm whether `Build self-learning knowledge report` ran or was skipped.

**Resolution Playbook:** Fix the upstream pre-sweep blocker first, then regenerate the self-learning report locally and let the next scheduled or manual sweep prove remote persistence. If stale worktree mirrors are the failure source, exclude local worktree roots from repo-authoritative scanners rather than editing copied artifacts. If a runner lacks operator-local memory sources, keep local strict validation as the default and make the runner skip explicit so local-only state cannot block the self-learning report.

**Instances:**
- 2026-04-20: GitHub Actions run `24674456168` failed at `Validate codex and agent model pins`, so self-learning report generation was skipped.
- 2026-04-21: Issue #475 records the operational proof gap and refreshes self-learning metrics from the current corpus.
- 2026-04-21: GitHub Actions run `24738583207` cleared cross-repo checkouts and model-pin validation, then failed at `Memory integrity audit` because GitHub-hosted runners do not have operator-home Claude memory files mounted.

**Prevention:** Keep workflow preflight scanners scoped to authoritative repo files, add local validation for `self_learning.py report`, require at least one issue-backed `raw/operator-context/self-learning/` artifact when closing a self-learning loop gap, and keep local-only audit surfaces from blocking repo-generated self-learning metrics in GitHub-hosted runners.

## Pattern: hook-command-classification-drift

### Symptom
Read-only operator commands fail before execution with `schema-guard: BLOCKED: Bash file write detected` even though the command only compares values inside quoted `awk` or `jq` expressions. Separately, commands that should be treated as high-risk session mutations, such as force pushes, remain policy-only unless an operator notices them manually.

### Root Cause
Hook code classified shell commands with independent raw-string regexes instead of one shared command-intent classifier. The regexes did not distinguish quoted comparison operators from shell redirects, branch matching saw heredoc bodies as executable command text, and the local branch/worktree guard had no force-push detector.

### Detection
- Log: `schema-guard: BLOCKED: Bash file write detected` followed by a target fragment from a quoted comparison.
- Log: blocked target text containing snippets such as `for = 0`, `> 1`, or `0)po`.
- Review signal: `git push -f`, `git push --force`, `git push --force-with-lease`, or `git push origin +...` appears in session output without a local hook block.

### Resolution Playbook
1. Add or update a focused regression in `scripts/overlord/test_check_plan_preflight.py` for the misclassified read-only command.
2. Route Bash write-target detection through `scripts/overlord/check_plan_preflight.py` instead of adding another regex to `hooks/schema-guard.sh`.
3. Add hook-level fixture coverage in `scripts/overlord/test_schema_guard_hook.py`.
4. If branch matching is involved, strip heredoc bodies before matching executable segments in `hooks/branch-switch-guard.sh`.
5. If the command mutates remote history, block the force flag or `+` refspec in `hooks/branch-switch-guard.sh`.
6. Roll back by reverting the hook/classifier change and disabling only the new failing regression if the shared classifier blocks legitimate writes incorrectly.

### Instances
| Date | Incident | Notes |
|------|----------|-------|
| 2026-04-21 | [2026-04-21](FAIL_FAST_LOG.md) | Issue #538 repaired `awk`/`jq` comparison handling, heredoc branch matching, and local force-push blocking. |

### Prevention
- Keep command intent parsing in `scripts/overlord/check_plan_preflight.py` where focused Python tests can cover it.
- Require hook fixture tests for every new shell syntax pattern added to a guard.
- Prefer updating existing guardrails before adding new hook layers.
- Record session-command failures in `docs/FAIL_FAST_LOG.md` and `docs/ERROR_PATTERNS.md` so self-learning lookup can retrieve the correction.

## Pattern: stage6-closeout-passive-gate

### Symptom
Implementation or governance-surface work reaches PR or merge readiness without a Stage 6 closeout artifact. Existing closeout validation appears healthy when run manually, but no gate forces the closeout to exist.

### Root Cause
The closeout hook and validator were local authoring/integrity tools, not merge-presence gates. CI validated handoff packages and closeout contents when closeout paths changed, but it did not require `raw/closeouts/*issue-NNN*.md` for issue-backed implementation or governance-surface diffs.

### Detection
- PR changes implementation/governance-surface paths but has no `raw/closeouts/*issue-NNN*.md` file.
- Session closeout relies on narrative status updates instead of a committed Stage 6 closeout artifact.
- `validate_closeout.py` is never invoked because no closeout file was created.

### Resolution Playbook
1. Add an issue-matching closeout under `raw/closeouts/`.
2. Run `scripts/overlord/validate_closeout.py` against the closeout.
3. If the PR is planning-only, keep changes limited to planning artifacts so the closeout-presence gate can skip it.
4. If implementation files changed, add validation, handoff, execution-scope, and closeout references before merge.
5. Roll back by removing the new enforcement call only if it blocks planning-only PRs after focused regression tests prove the exemption failed.

### Instances
| Date | Incident | Notes |
|------|----------|-------|
| 2026-04-21 | [2026-04-21](FAIL_FAST_LOG.md) | Issue #541 wired Stage 6 closeout presence into reusable governance CI and Local CI. |

### Prevention
- Keep `check_stage6_closeout.py` in the merge path, not only in local hooks.
- Use the existing `validate_closeout.py` for integrity so closeout semantics stay centralized.
- Preserve a tested planning-only exemption to avoid blocking early plan/scope PRs.
- Record closeout gaps in self-learning evidence so future sessions retrieve the merge-gate fix.

## Pattern: session-error-kb-unindexed

### Symptom
Session-specific errors are corrected in chat, PR notes, or one-off validation artifacts, but later sessions rediscover the same flag, path, schema, hook, or merge-flow correction.

### Root Cause
`docs/FAIL_FAST_LOG.md` is the formal ledger and `docs/ERROR_PATTERNS.md` is the canonical pattern catalog, but neither provided a compact operator lookup table for exact session error signatures. The self-learning loop also did not index a dedicated session-error runbook, so packet enrichment could miss recently corrected operational failure modes.

### Detection
- A repeated session error is visible in transcripts but no structured runbook entry exists with signature, category, correction, guardrail, and validation.
- `scripts/orchestrator/self_learning.py report` does not include `session_error_pattern` in indexed sources.
- `scripts/orchestrator/self_learning.py lookup --query '<exact session symptom>'` returns only broad closeout or fail-fast context.

### Resolution Playbook
1. Add or update `docs/runbooks/session-error-patterns.md` using the repeatable entry schema.
2. Keep durable formal incidents in `docs/FAIL_FAST_LOG.md`.
3. Add canonical broad patterns to `docs/ERROR_PATTERNS.md` only when machine-readable lookup or prevention needs a reusable pattern.
4. Ensure `scripts/orchestrator/self_learning.py` indexes the runbook as `session_error_pattern`.
5. Validate with self-learning lookup and report output before closeout.

### Instances
| Date | Incident | Notes |
|------|----------|-------|
| 2026-04-21 | [2026-04-21](FAIL_FAST_LOG.md) | Issue #535 added the session error patterns runbook and indexed it in self-learning reports. |

### Prevention
- Record exact session signatures before they are abstracted into broad runbook prose.
- Prefer extending the existing self-learning source loader over adding a parallel KB service.
- Keep external services runbooks focused on service operation; keep session/tooling errors in this dedicated runbook.
