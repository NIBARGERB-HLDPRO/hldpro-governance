## Preflight

Run this first and include the full command output in your session notes:

```bash
bash scripts/codex-preflight.sh --log
```

Do not start the issue slice until preflight completes with PASS.

## Worktree discipline (HARD GATE)

Create and verify worktrees exactly as below before any commit:

```bash
cd ~/Developer/HLDPRO/<repo>
git fetch origin main
git worktree add -b <branch-name> /tmp/<worktree-name> origin/main
cd /tmp/<worktree-name>
git log --oneline origin/main..HEAD   # HARD GATE: must be empty before first commit
```

If `git log --oneline origin/main..HEAD` shows any lines, HALT and re-create the worktree from a fresh `origin/main`.

## Non-destructive editing

For committed JSON settings (`.claude/settings.json`), use JSON-merge updates only; never overwrite the file wholesale.
For `.gitignore`, apply minimal surgical patches that preserve existing generated lines.
For CLAUDE.md-style docs, use append-only updates at the end of the file unless a full rewrite is explicitly requested.

Use issue #154 as prior art for this exact edit discipline and audit trail.

## Diff scope cap

Per-sprint `file_paths` are enforced. Do not modify anything outside the current sprint's declared files.
If `git diff --name-only origin/main..HEAD` shows a fourth file, immediately HALT and report the violation.

## No push / no gh

Codex-spark is a local executor with no remote network operations in this environment.
Do not run `git push`, do not call `gh` for remote ops, and do not open PRs.
See `feedback_codex_spark_no_network.md`.

## Structured agent cycle plan (REQUIRED for governance surface writes)

Any sprint that writes to a governance surface (OVERLORD_BACKLOG.md, docs/plans/, raw/, wiki/, hooks/, scripts/overlord/, .github/workflows/, etc.) MUST produce a `docs/plans/issue-<N>-<slug>-structured-agent-cycle-plan.json` file BEFORE the first governance surface write.

The plan is validated by `scripts/overlord/validate_structured_agent_cycle_plan.py`. Required top-level fields:

```json
{
  "session_id": "session-YYYYMMDD-issue-<N>-<slug>",
  "issue_number": <N>,
  "objective": "...",
  "tier": "...",
  "scope_boundary": "...",
  "out_of_scope": "...",
  "research_summary": "...",
  "research_artifacts": [],
  "sprints": [
    {
      "sprint_id": "sprint-1",
      "objective": "...",
      "files": ["path/to/file.ext"]
    }
  ],
  "specialist_reviews": [],
  "alternate_model_review": { "required": false, "reason": "..." },
  "execution_handoff": {
    "execution_mode": "implementation_ready",
    "ready_at": "YYYY-MM-DDTHH:MM:SSZ"
  },
  "material_deviation_rules": [],
  "approved": true,
  "approved_by": "session-agent-<model>",
  "approved_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

`execution_mode` must be one of: `implementation_ready`, `implementation_complete`.

## Execution scope (REQUIRED for all implementation work)

Every implementation sprint requires `raw/execution-scopes/YYYY-MM-DD-issue-<N>-<slug>-implementation.json`. The CI gate (`local_ci_gate.py`) auto-discovers this file by glob `*issue-<N>*implementation*.json`.

**Critical fields that are commonly missed:**

```json
{
  "expected_execution_root": "{repo_root}",
  "expected_branch": "issue-<N>-<slug>-YYYYMMDD",
  "allowed_write_paths": [
    "docs/plans/issue-<N>-<slug>-structured-agent-cycle-plan.json",
    "raw/execution-scopes/YYYY-MM-DD-issue-<N>-<slug>-implementation.json",
    "graphify-out/GRAPH_REPORT.md",
    "graphify-out/graph.json",
    "... all other files this sprint touches ..."
  ],
  "forbidden_roots": [
    "/Users/<user>/Developer/HLDPRO/hldpro-governance"
  ],
  "execution_mode": "implementation_ready",
  "lane_claim": {
    "issue_number": <N>,
    "claim_ref": "https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/<N>",
    "claimed_by": "session-agent-<model>",
    "claimed_at": "YYYY-MM-DDTHH:MM:SSZ"
  },
  "handoff_evidence": {
    "status": "accepted",
    "planner_model": "<model-id>",
    "implementer_model": "<model-id>",
    "accepted_at": "YYYY-MM-DDTHH:MM:SSZ",
    "evidence_paths": ["docs/plans/issue-<N>-<slug>-structured-agent-cycle-plan.json"],
    "active_exception_ref": null,
    "active_exception_expires_at": null
  }
}
```

**Do not omit:**
- `lane_claim` — required by `assert_execution_scope.py --require-lane-claim` (wired into CI gate)
- `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` in `allowed_write_paths` — the graphify hook auto-commits these on every commit; omitting them causes the planner-boundary check to fail

## Report format

At each handoff, include:

- branch name
- worktree path
- `git log --oneline origin/main..HEAD`
- `git diff --name-only origin/main..HEAD`
- blockers (if any)

## Example usage

Issue #154 — Pre-session hook standardization

- Branch: `issue-154-pre-session-hook`
- Worktree: `/tmp/issue-154-pre-session-hook`
- Start command:

```bash
cd ~/Developer/HLDPRO/hldpro-governance
git fetch origin main
git worktree add -b issue-154-pre-session-hook /tmp/issue-154-pre-session-hook origin/main
cd /tmp/issue-154-pre-session-hook
git log --oneline origin/main..HEAD
```

- Verified log: `<empty>`
- H2 sections written: Preflight, Worktree discipline, Non-destructive editing, Diff scope cap, No push / no gh, Report format
- 1st sprint files: `agents/pre-session.md`, `agents/pre-session-hook.md`
- 2nd sprint file: `docs/templates/codex-spark-dispatch-brief.md`
- 3rd sprint file: `docs/agents.md`
- Reported blockers: none
- Diff scope after completion: exactly the files declared by each sprint
