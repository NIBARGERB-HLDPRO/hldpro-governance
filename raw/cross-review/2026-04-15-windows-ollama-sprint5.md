---
pr_number: 123
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-15
co_drafters:
  - role: worker-claude-fallback
    model_id: claude-sonnet-4-6
    model_family: anthropic
    signature_date: 2026-04-15
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  model_reasoning_effort: high
  signature_date: 2026-04-15
  verdict: REJECTED
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: false
  cross_family_independence: true
---

**Summary**
Verdict: **REJECTED**.

PR #123 activated the Windows-Ollama Tier-2 rung in the merged code, but the live controls do not satisfy the charter. The blocking failures are in PII preservation, Tier-2 ladder ordering, fallback logging, exception closure evidence, and test coverage.

I verified merged HEAD is `1e76b202b682d2de7fa9b794171cf2e27a50f4cd`. `test_decide.sh` passes 8/8, `test_integration.sh` correctly exits `77` when the Windows host is unreachable, and `bash -n` passes for the new shell scripts. Those results do not cover the failing paths below.

**Must-Fix**
1. PII-detected payloads can route to Windows or cloud. [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):55 parses only YAML list lines matching `^  - `, but [pii_patterns.yml](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/pii_patterns.yml):7 stores patterns under `regex:` keys. Direct probes routed `jane@example.com` to `WINDOWS` and `SSN: 123-45-6789` to `CLOUD`. This violates [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/STANDARDS.md):331 and [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/STANDARDS.md):335.

2. `decide.sh` fails open when patterns are unavailable or the script is run outside repo root. [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):53 uses a repo-relative path and [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):63 returns “no PII” if the file is absent. The charter requires fail-closed when patterns are unavailable.

3. The Tier-2 ladder skips `gpt-5.3-codex-spark @ medium`. [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/STANDARDS.md):271 defines high spark, then medium spark, then local daemon, then Windows, then Sonnet. [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):85 has only one `--codex-spark-status`; when it is not `ok`, routing jumps straight to local/Windows/cloud. The runbook repeats the same skip at [windows-ollama-worker.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/docs/runbooks/windows-ollama-worker.md):84.

4. Global invariant #7 regresses: fallbacks are not logged. [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/STANDARDS.md):334 requires every fallback to write `raw/model-fallbacks`. `decide.sh` only prints stderr decision logs at [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):88, [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):95, [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):102, and [decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/decide.sh):108; it never calls [model-fallback-log.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/model-fallback-log.sh):1.

5. Exception closures are not earned. PII-001 is false because `decide.sh` fails PII detection. DISABLED-001 is false because the active routing logic is unsafe and skips a ladder rung. AUDIT-001 is at least overstated: [test_integration.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/tests/test_integration.sh):3 claims `decide.sh -> submit.py -> audit.py`, but the script only calls `decide.sh` at [test_integration.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/tests/test_integration.sh):16.

6. Audit HMAC enforcement is not fully live in CI. [verify_audit.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/verify_audit.py):61 reads `SOM_WINDOWS_AUDIT_HMAC_KEY`, but [verify_audit.py](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/verify_audit.py):62 skips HMAC verification if unset. The CI workflow at [check-windows-ollama-audit-schema.yml](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/.github/workflows/check-windows-ollama-audit-schema.yml):28 runs the verifier without setting that key. The closure text at [exception-register.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/docs/exception-register.md):97 says HMAC validation is live; as merged, that is conditional, not enforced.

7. The claimed 8-case matrix does not exercise every decision path. [test_decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/tests/test_decide.sh):50 covers explicit `--pii-flag yes`, but no inline PII, no `--prompt-file`, no missing-pattern fail-closed case, no medium spark rung, and no fallback logging assertion. The “empty pii-flag” case at [test_decide.sh](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/scripts/windows-ollama/tests/test_decide.sh):68 actually passes `"no"`.

8. STANDARDS references a missing PII CI gate. [STANDARDS.md](/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-sprint5-posthoc/STANDARDS.md):385 names `.github/workflows/check-windows-ollama-pii-submission.yml`, but no such workflow exists in the merged workspace. That leaves the enforcement index with an orphan rule.

**Nice-to-Have**
- Replace the shell YAML scraping in `decide.sh` with a shared parser or call into the same PII detection code path as `submit.py`.
- Split the decision output into destination plus reason/rung, so `CLOUD` can distinguish spark-high, spark-medium, and Sonnet cost fallback.
- Rename the runbook’s “activation requires” section to “activation acceptance evidence” and fix `decision.sh` to `decide.sh`.

**Notes**
- The STANDARDS Tier-2 cell is textually activated and references `decide.sh`; that part is genuine.
- The runbook no longer has “NOT APPROVED” blocker language, but it now overclaims enforcement.
- Exit `77` in `test_integration.sh` is correct for LAN-dependent smoke tests: not silent pass, not hard fail.
- This post-hoc artifact intentionally carries `verdict: REJECTED` and `pii_floor: false`; it should not be treated as a passing `require-cross-review.yml` artifact.