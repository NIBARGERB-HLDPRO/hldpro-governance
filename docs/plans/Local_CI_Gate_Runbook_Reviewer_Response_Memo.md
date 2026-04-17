# Reviewer Response Memo — Local CI Gate Runbook

**Date:** April 17, 2026
**Subject artifact:** `HLD_Pro_Local_CI_Gate_Runbook.md` (v1.4, revised April 17, 2026)
**Author:** Benji
**Reviewer feedback received:** Two rounds, April 17, 2026

---

## Artifact Mismatch Note

The first reviewer pass inspected a different artifact — the local-governance-preflight zip — not the `HLD_Pro_Local_CI_Gate_Runbook.md` under discussion. The reviewer's second pass acknowledged this and scoped the remaining feedback to the correct artifact.

This memo captures what transferred, what did not, and the adjustments to be applied. The runbook itself has not been modified at the time of this memo; the five edits enumerated in §5 will be applied in a single revision pass following memo approval.

---

## 1. Accepted

The following points apply to the Local CI Gate Runbook and are being incorporated.

| # | Point | Source section in runbook |
|---|---|---|
| A1 | CI authority language is under-emphasized; operators could misread "local gate passed" as "CI will pass" | §1 Epic; §8 Phase 3.4 QUICKREF |
| A2 | Phase 6.5 verdict log lines ("skipping") can be misread as a pass signal when zero specs ran | §11 Phase 6.5 |
| A3 | Issue creation must precede backlog/planning artifacts; runbook currently has no issue number | §5 Phase 0 (new 0.0 slice) |
| A4 | Baseline artifacts (tracked) and per-run reports (gitignored) need explicit separation to prevent future gitignore-vs-evidence conflict | §15 Appendix A |
| A5 | A single `--full` user-facing override is warranted so operators can force full-suite replay without changing resolver logic | §11 Phase 6.5 |

---

## 2. Not Applicable

The following reviewer points applied to the local-governance-preflight artifact, not to this runbook. They are recorded here so a future reviewer does not re-raise them as unresolved.

| # | Reviewer point | Why it doesn't apply |
|---|---|---|
| N1 | Workflow YAML replay misses inline logic in `governance-check.yml` | This runbook does not replay workflow YAML. Tier 1 governance invokes `./scripts/governance-check.sh` directly; whatever logic exists lives in the shell script, not in YAML heredocs. §4 explicitly rejects `act`/workflow-replay for this reason. |
| N2 | Drift test is too narrow; workflow check registry misses bash checks, inline Python, non-standard names | This runbook has no check registry. The selective-testing resolver maps source files to Playwright specs via convention plus `@covers` annotation. It is not a governance-check registry and does not claim to cover every CI surface. |
| N3 | LAM availability check adds noise to deterministic core | This runbook has no LAM check. LAM-related governance lives elsewhere. |

---

## 3. Refinements Adopted

The reviewer's second-pass refinements are cleaner than the initial drafting and are adopted verbatim where they improve clarity.

**3.1 Log-line phrasing (Phase 6.5).** The reviewer's suggested lines replace the original "skipping" / "PASS for matched specs" phrasing:

- No matches: `LOCAL CHECK: no mapped Playwright specs for this diff. Matched specs: 0. This is not a full-suite replay; CI remains authoritative.`
- Subset match: `LOCAL CHECK: matched Playwright specs passed: N. This is not a full-suite replay.`
- Fallback full suite: `LOCAL CHECK: full Playwright suite required by fallback trigger: <reason>.`

**Rationale:** avoids using "PASS" when zero specs ran; includes the CI-authoritative disclaimer redundantly on every log line so quoting any single line in a later review preserves the context.

**3.2 `--full` override only (no three-mode split).** The runbook does not add `--mode=changed` / `--mode=standard` / `--mode=full` as user-facing modes. The resolver remains three-state internally (skip / subset / FULL_SUITE). A single `--full` escape lever is added to the `test:e2e:*` npm scripts so an operator can force the full suite without editing the resolver.

**Rationale:** the fallback triggers in Phase 6.3 already make the default conservative — any `src/lib/`, migration, or config change forces the full suite. Adding a mode matrix on top duplicates that logic in the CLI layer.

---

## 4. Scope Boundary Reaffirmed

Two points from the reviewer's feedback warrant explicit statement in the runbook, not just in this memo:

- **CI remains authoritative.** The local gate is an upstream filter that reduces avoidable failures; it never replaces required CI. This sentence is added verbatim to §1 (Epic) and to the QUICKREF section created in Phase 3.4.
- **The runbook is not a full CI replay.** Phase 6 selective testing covers Playwright only. Vitest, migration validation, and deno checks run in Tier 2 regardless of diff shape. Governance, lint, type, and secret checks run in Tier 1 regardless of diff shape. No claim of CI equivalence is made at any tier.
- **Any report from Phase 6 must identify whether it ran zero specs, a subset, or the full suite.** This closes the loop between the CI-authority principle and the resolver's actual reporting behavior; it is reflected in the log-line phrasing in §3.1 and enforced by the verdict strings in Phase 6.5.

---

## 5. Edits To Be Applied to Runbook

The following five edits will be applied to `HLD_Pro_Local_CI_Gate_Runbook.md` in a single revision pass following approval of this memo:

| Edit | Section | Change |
|---|---|---|
| E1 | §1 Epic (opening) | Insert "CI remains authoritative" principle as a bolded line beneath the success metric |
| E2 | §5 Phase 0 | Add new micro-slice 0.0 covering issue creation, milestone assignment, and backlog row seeding before any other work begins |
| E3 | §11 Phase 6.5 | Replace log-line strings with reviewer's phrasing (§3.1 above); add `--full` script variant |
| E4 | §15 Appendix A | Add "Artifacts vs Reports" subsection distinguishing tracked baselines from gitignored per-run reports |
| E5 | §8 Phase 3.4 QUICKREF content | Append "CI remains authoritative" line to the QUICKREF section content |

The revision banner at the top of the runbook will be updated to note this memo's date and the five edits.

---

## 6. Decisions Not Revisited

The following earlier architectural decisions (§4 of runbook) are not reopened by this review:

- Choice of lefthook over husky
- Rejection of `act` for workflow replay
- Use of convention + `@covers` annotation over explicit manifest
- `git push --no-verify` as documented escape hatch
- Chromium-only browser matrix for pre-push

No reviewer feedback challenged these and they remain as stated.

---

## 7. Open Items After This Memo

Items still pending, for the record:

- Issue creation (tracked as new Phase 0.0 in the runbook)
- Baseline timing capture (Phase 6.1) — blocks the cap-limit numbers in the baseline summary doc
- Supabase-target confirmation for Playwright (local vs. dedicated cloud test project) — open decision in §13

None of these block planning approval; they remain execution-phase gates.

---

**End of memo.**
