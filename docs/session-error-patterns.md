# Session Error Patterns

Documented failure patterns from governed Claude sessions. Consult before debugging CI or hook failures.

## Pattern: GitHub API commits do not trigger pull_request: synchronize

**Symptom**: Commits pushed via GitHub Contents API (PUT to /contents/<path>) appear on the remote branch but do not trigger `pull_request: synchronize` events. CI runs remain stale from previous git-pushed commits.

**Root cause**: GitHub Actions `pull_request: synchronize` events are only fired by commits pushed via the git protocol (SSH/HTTPS). The Contents API creates commits at the storage layer without emitting a synchronize event.

**Fix**: Always follow GitHub Contents API commits with a `git push` from the local worktree:
```bash
git -C <worktree> fetch origin
git -C <worktree> reset --hard origin/<branch>
git -C <worktree> commit --allow-empty -m "ci: trigger CI after API commits"
git -C <worktree> push
```
Or use `gh workflow run <workflow>.yml --ref <branch>` to manually dispatch specific workflows.

## Pattern: schema-guard.sh fires from session worktree, not cd target

**Symptom**: `schema-guard.sh` blocks a write command even though a valid, recent plan exists at the path you are targeting. The plan mtime check reads the WRONG worktree.

**Root cause**: `hooks/schema-guard.sh` and `hooks/code-write-gate.sh` compute `GIT_ROOT` from the session worktree root at the time the hook fires -- not from the `cd` target in the bash command. If you `cd` into another worktree path and run a script, the hook fires against the original session worktree, where no recent plan may exist.

**Fix**: Use GitHub Contents API for writes targeting a different worktree. Or open a fresh session with the target worktree as root.

## Pattern: CI startup_failure with no job logs

**Symptom**: `CI` workflow shows `startup_failure` with no job-level logs. Governance checks (governance-check, require-cross-review, check-arch-tier) never run.

**Root cause**: `ci.yml` calls reusable workflows with `base_sha`/`head_sha` inputs. If the reusable workflow `workflow_call:` trigger block does not declare these inputs, GitHub Actions rejects the call at parse time with a startup failure.

**Fix**: Ensure all reusable workflows called by `ci.yml` declare matching `inputs:` in their `workflow_call:` trigger. When creating a branch before a `ci.yml` update, cherry-pick or rebase to pick up the input declarations.

## Pattern: Same-family self-approval block

**Symptom**: `governance-surface-planning` fails with "same-family reviewer cannot accept". Plan has `specialist_reviews[N].status: "accepted"` where reviewer is same model family as plan author.

**Root cause**: The governance gate distinguishes `"accepted"` (cross-family validation) from `"complete"` (same-family review). Only cross-family reviewers can set `accepted`.

**Fix**: Set `specialist_reviews[N].status: "complete"` for same-family reviewers. Use `alternate_model_review` block for the cross-family review (or document the exception with `cross_family_path_unavailable: true`).
