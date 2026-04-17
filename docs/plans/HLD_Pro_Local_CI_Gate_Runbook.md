# HLD Pro — Local CI Gate Implementation Runbook

**Version target:** v1.4 (quality-of-life, ships alongside current bug sprint)
**Prepared:** April 17, 2026
**Revised:** April 17, 2026 — (1) Added Phase 6 (Selective Playwright Testing); Phase 3.2 (`@slow` tagging) superseded and removed. (2) Applied reviewer-response memo edits E1–E5: CI-authority principle (§1), Phase 0.0 issue creation, Phase 6.5 verdict-line phrasing and full-suite override clarification, Appendix A "Artifacts vs Reports" subsection, QUICKREF CI-authority line. (3) Added hldpro-governance target-repo implementation overlay for issue #253. (4) Added alternate-model review follow-up: governance-profile micro-slices and explicit deployer safety contract.
**Issue number:** #253
**Target repo:** `hldpro-governance`
**Paired memo:** `Local_CI_Gate_Runbook_Reviewer_Response_Memo.md`
**Owner:** Benji (solo)
**Estimated effort:** 6–8 hours across 2–3 sittings
**Dependencies:** None blocking; `preflight-probe` agent already exists

---

## Revision Note (April 17, 2026)

**Revision 1 — Phase 6 added:** Phase 3.2 originally proposed tagging slow tests with `@slow` and excluding them from pre-push. That approach is **superseded by Phase 6 — Selective Playwright Testing by Diff**, which runs only the specs whose covered source files actually changed. Running a broken-but-unrelated test fast is still wasted work; not running it at all is the right answer.

**Revision 2 — Reviewer memo edits applied:** Five targeted edits applied per `Local_CI_Gate_Runbook_Reviewer_Response_Memo.md`:
- **E1** — §1 Epic: added "CI remains authoritative" principle beneath success metric
- **E2** — §5 Phase 0: added new micro-slice 0.0 covering GitHub issue creation, milestone assignment, and backlog row seeding before any implementation work
- **E3** — §11 Phase 6.5: replaced resolver log-line strings with precise verdict phrasing; clarified the full-suite script as the single user-facing override
- **E4** — §15 Appendix A: added "Artifacts vs Reports" subsection distinguishing tracked baselines, gitignored per-run reports, and closeout evidence
- **E5** — §8 Phase 3.4 QUICKREF content: appended "CI remains authoritative" line

**Revision 3 — org-level toolkit target:** Issue #253 targets `hldpro-governance` as the source-of-truth repository for reusable local CI gate tooling. Consumer repos should pull/deploy this toolkit through thin shims instead of recreating the logic. The first implementation PR should build the governance-owned toolkit and a governance-repo profile; product-repo Playwright selective testing remains a reusable downstream profile, not hand-copied per repo.

**Revision 4 — implementation handoff tightened:** Alternate-model review approved the plan with follow-up changes. §1.1 now includes governance-profile implementation micro-slices and a Local CI Gate deployer contract so the next implementation PR does not need to infer those details from the downstream Playwright profile or the graphify helper analogy.

**Migration from the old approach:** If you already started Phase 3.2 tagging, the `@slow` tags cause no harm — they're simply ignored. Do not add new ones. The `@covers` annotation described in Phase 6 replaces `@slow` as the authoring metadata that matters.

**Why:** See chat history on April 17 — selective testing eliminates the need for a slow/fast split because a diff that doesn't touch a slow test's pages won't run that test at all. Keeping both creates two overlapping mental models.

---

## Table of Contents

1. [Epic](#epic)
2. [Problem Statement](#problem-statement)
3. [Non-Goals](#non-goals)
4. [Architectural Decisions](#architectural-decisions)
5. [Phase 0 — Upstream Quick Wins (Pre-Work)](#phase-0)
6. [Phase 1 — lefthook Install & Tier 1 Pre-Commit](#phase-1)
7. [Phase 2 — Tier 2 Pre-Push (Fast Checks)](#phase-2)
8. [Phase 3 — Tier 2 Pre-Push (Playwright)](#phase-3)
9. [Phase 4 — Integration with Existing Agents](#phase-4)
10. [Phase 5 — Documentation & Rollout](#phase-5)
11. [Phase 6 — Selective Playwright Testing by Diff](#phase-6)
12. [Rollback Plan](#rollback-plan)
13. [Open Decisions](#open-decisions)
14. [Acceptance Criteria — Epic Level](#epic-acceptance-criteria)
15. [Appendix A — File Manifest](#appendix-a)
16. [Appendix B — Minute Savings Estimate](#appendix-b)
17. [Appendix C — Baseline Timing Capture Script](#appendix-c)

---

## Applicability Note

Issue #253 makes this runbook an org-level toolkit plan. The authoritative implementation path for this PR is §1.1: build the reusable toolkit in `hldpro-governance`, dogfood the governance profile, and deploy thin shims to consumers through later issue-backed rollout slices.

The lefthook, Playwright, Supabase, and `pnpm` details in later phases are retained as a downstream product-repo profile pattern. They must not be implemented directly in `hldpro-governance` unless a later issue first adds that runtime surface to this repo.

## 1. Epic <a name="epic"></a>

**Title:** Local CI Gate — Pre-Push Validation to Replace Redundant GitHub Actions Runs

**Implementation target for issue #253:** `hldpro-governance` as the org-level source of truth for reusable local CI gate tooling.

**Epic goal:** Catch all preventable CI failures on the local machine before `git push` completes, so that GitHub Actions becomes a safety net (rarely-triggered re-run) rather than a primary validation path. Staging (Cloudflare-fronted sites + staged Supabase) remains the post-push eyeball verification layer.

**Success metric:** ≥80% reduction in failed GitHub Actions runs over a 2-week window post-rollout, measured via `gh run list --status failure --limit 50` week-over-week.

**Principle — CI remains authoritative.** The local gate is an upstream filter that reduces avoidable failures; it never replaces required CI. No local result at any tier — skip, subset, or full — should be read as "CI will pass."

**Milestone:** v1.4 (ships as a dev-velocity improvement before CoS v1.5 work begins)

### 1.1 Org-Level Toolkit Implementation Plan

`hldpro-governance` is the implementation target, but its role is not "one more consumer repo." It owns the reusable toolkit that other repos can pull and deploy. Implementation for issue #253 is therefore split into source-tooling and consumer-adoption tracks:

| Track | Status | Purpose |
|---|---|---|
| **Track A — reusable toolkit source** | Issue #253 implementation target | Build the canonical local CI gate runner, profiles, and deployer in `hldpro-governance`. |
| **Track B — governance-repo profile** | Issue #253 implementation target | Dogfood the toolkit against `hldpro-governance` using existing Python/bash governance checks. |
| **Track C — consumer repo rollout** | Follow-up issues | Deploy thin shims into AIS, HealthcarePlatform, local-ai-machine, knocktracker, and any other governed repo. |
| **Track D — Playwright selective testing profile** | Downstream profile | Preserve the Playwright resolver design for repos that already have `package.json`, Playwright config, and `e2e/` tests. |

Toolkit architecture:

- Source directory: `tools/local-ci-gate/` in `hldpro-governance`.
- Runner: `tools/local-ci-gate/bin/hldpro-local-ci` with a Python core for deterministic check orchestration and report generation.
- Profiles: `tools/local-ci-gate/profiles/*.yml` for repo families, starting with `hldpro-governance.yml` and later `vite-supabase-playwright.yml`, `python-governance.yml`, and `knowledge-repo.yml` as needed.
- Deployer: `scripts/overlord/deploy_local_ci_gate.py` that installs or refreshes a thin consumer shim from a pinned governance checkout/ref.
- Consumer shim: a small repo-local command (for example `.hldpro/local-ci.sh` or `.governance/local-ci.sh`) that delegates back to the governance toolkit instead of copying implementation logic.
- Reports: local-only by default, under a gitignored repo-local path; tracked evidence is summarized into closeout artifacts when needed.

Precedent from the service runbook and graphify helper:

- `docs/EXTERNAL_SERVICES_RUNBOOK.md` is already the cross-repo SSOT and explicitly supersedes independently maintained downstream service runbooks. Local CI Gate should follow the same model: governance owns the canonical docs and implementation surface; downstream repos point back or install a shim.
- `scripts/knowledge_base/graphify_hook_helper.py` is the closest tool precedent. It resolves a governed target from a manifest, refuses unsafe output paths, installs managed hooks with a marker, and protects unmanaged local hooks from silent overwrite. The Local CI Gate deployer should copy those safety properties.

Local CI Gate deployer contract:

- Managed marker: every installed shim must include a stable marker such as `# hldpro-governance local-ci gate managed`. The deployer may refresh files containing that marker.
- Valid install targets: repo-local shim paths only, initially `.hldpro/local-ci.sh` or `.governance/local-ci.sh` under the target repo root. The deployer must refuse absolute target paths outside the target repo and must not write generated reports into consumer repo tracked paths.
- Unmanaged overwrite behavior: if the target shim already exists without the managed marker, the deployer refuses by default. Optional `--backup-existing` may rename the old file before install; optional `--force` may overwrite only when explicitly passed and logged.
- Refresh semantics: refresh updates only managed shim content and pinned governance ref/config metadata. It must not mutate consumer test scripts, package files, workflow files, or hooks unless a later issue adds those paths to the explicit contract.
- Dry-run: `resolve` or `dry-run` must print the target repo, profile, shim path, governance source/ref, and planned write set before install.

Governance-repo profile checks should start with the deterministic checks already used by this repo:

- `python3 scripts/overlord/check_overlord_backlog_github_alignment.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .`
- governance-surface validation with `--changed-files-file`
- planner-boundary planning-only classification or `assert_execution_scope.py` when an implementation scope is present
- `git diff --check`
- focused `pytest` targets selected by changed paths where cheap and deterministic
- optional import/compile checks for changed Python scripts

Governance-profile implementation micro-slices for the next PR:

| Slice | Purpose | Acceptance |
|---|---|---|
| **G1 — runner skeleton** | Add `tools/local-ci-gate/bin/hldpro-local-ci` and a Python core that loads a profile, resolves changed files, runs checks, and returns blocker/advisory status. | `--help`, `--dry-run`, and one no-op profile path work without side effects; output states that CI remains authoritative. |
| **G2 — governance profile** | Add `tools/local-ci-gate/profiles/hldpro-governance.yml` with backlog alignment, structured-plan validation, governance-surface validation, planner-boundary checks, diff hygiene, and focused Python checks. | A governance-repo dry run prints the planned checks and a real run can execute the deterministic checks currently used by this repo. |
| **G3 — reporting contract** | Emit local-only machine-readable and human-readable reports under a gitignored local path, with verdict fields that distinguish all-supported checks, changed-file subset, skipped advisory checks, and blockers. | Reports never claim full CI parity and can be summarized into a closeout without tracking per-run files. |
| **G4 — deployer and shim fixture** | Add `scripts/overlord/deploy_local_ci_gate.py` plus a fixture or dry-run target that installs/refreshes only a managed shim. | Dry-run lists the write set; install refuses unmanaged files by default; refresh changes only managed shim content. |
| **G5 — dogfood gate** | Wire the governance profile into the repo workflow as a documented local command before consumer rollout. | The implementation PR records local dogfood evidence, focused tests, and Stage 6 closeout; no consumer repo is modified in the same PR. |

Acceptance for the issue #253 implementation plan:

- The toolkit has one canonical runner and profile system in `hldpro-governance`; consumer repos do not receive bespoke copies of the logic.
- The governance-repo profile exits non-zero on blocker failures and continues far enough to report all deterministic blocker failures it can collect.
- The runner prints whether it ran all supported checks or a changed-file subset; it never claims to be a full CI replay.
- The deployer can install or refresh a thin shim for at least one local test fixture or governed repo dry-run without writing unrelated files.
- Reports, if any, are local-only unless summarized in a tracked closeout artifact.
- No Playwright, Node, Supabase, or lefthook dependency is introduced into `hldpro-governance` itself unless a separate issue proves that surface exists in this repo.
- Consumer-repo rollout remains issue-backed and staged repo-by-repo after the toolkit is dogfooded in governance.

---

## 2. Problem Statement <a name="problem-statement"></a>

- Playwright 60/82 suite, migration validation, `deno check`, and governance-check reviews currently run in GitHub Actions on every push.
- Feature-branch pushes frequently fail on preventable issues (TS errors, lint, missing migrations) that would be caught in <30s locally.
- Each failed Actions run burns minutes; failed Playwright runs are the single largest drain.
- Existing `preflight-probe` agent (Haiku) runs via `package.json &&` chain but is not wired to git, so it only fires when Benji remembers to invoke the test script.

---

## 3. Non-Goals <a name="non-goals"></a>

- **Not replacing GitHub Actions.** CI stays as source of truth; local gate is an upstream filter.
- **Not using `act`.** Full workflow YAML replay in Docker is slower than native for Playwright and drifts from real GitHub runners. See `Architectural Decisions` for rationale.
- **Not adding post-deploy staging tests.** Benji prefers manual spot-check of staged URLs over automated staging suites.
- **Not blocking `--no-verify`.** Escape hatch must exist for emergencies and is documented, not hidden.
- **Not changing the test suite itself.** This epic wraps existing tests; it does not author new ones.

---

## 4. Architectural Decisions <a name="architectural-decisions"></a>

| Decision | Chosen | Rejected | Rationale |
|---|---|---|---|
| Hook runner | **lefthook** | husky | Parallel execution default, single YAML config, no Node runtime overhead on every hook fire |
| Workflow replay | **None (native scripts)** | `act` | `act` is slower than native Playwright, drifts from real runners, solves a problem Benji doesn't have |
| Playwright target | **localhost dev server** | Staged Supabase | Staged Supabase shared state would collide with manual spot-checking; local is the canonical MacBook-first pattern |
| Supabase for tests | **Local (`supabase start`)** | Staged | Isolates test writes from staging data; forces migration chain to be real before push |
| Pre-commit scope | **Staged files only** | Full repo | Sub-5s budget; full repo lint defeats the hook's purpose |
| Browser matrix | **Chromium only** | Full matrix | Feature-branch pushes don't need Firefox/WebKit parity; full matrix reserved for nightly CI if ever added |
| Escape hatch | **`git push --no-verify` documented** | Hidden/blocked | Solo operator must retain ability to bypass in emergencies |
| **Playwright scope** | **Selective by diff (Phase 6)** | Full suite every push, or `@slow` tag split | Only run specs whose covered source files changed; full-suite fallback for shared-code changes |
| **Fail-fast semantics** | **Serial within file, parallel across files** | `--max-failures=1` across whole run | Hard-fail immediately on first failure in a flow; continue other files to surface independent failures |
| **Test→source mapping** | **Convention + `@covers` annotation** | Explicit manifest file | File-name mirror auto-maps most specs; `@covers` JSDoc handles the rest; no central manifest to drift |

---

## 5. Phase 0 — Upstream Quick Wins (Pre-Work) <a name="phase-0"></a>

**Goal:** Capture the ~50% minute savings that exist independent of any local hook work. Do this first so we can measure the local gate's incremental value accurately.

**Effort:** 45 min (includes issue creation)
**Dependencies:** None

### Micro-slice 0.0 — Create governing GitHub issue and backlog row

**Purpose:** Under the repo's governance model, no implementation work begins before a tracked issue exists. This slice establishes the issue, milestone, and backlog row so every later phase has a stable reference.

**Steps:**

1. Create GitHub issue in `NIBARGERB-HLDPRO/hldpro-governance`:
   - **Title:** `Local CI gate runbook planning artifacts`
   - **Labels:** `governance`, `documentation`, `priority:next`
   - **Body:** Link to this runbook; paste the Epic section as the description
2. Copy the resulting issue number into the runbook's revision banner (top of file) and into the `OVERLORD_BACKLOG.md` entry referenced by this planning slice.
3. Add a Planned row to `OVERLORD_BACKLOG.md`, referencing the issue number:

   ```markdown
   | Local CI Gate implementation planning for hldpro-governance | [#253](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/253) | MEDIUM | 1-2 | Define the governance-native local gate implementation plan in `docs/plans/HLD_Pro_Local_CI_Gate_Runbook.md`, with Playwright-specific material preserved as downstream pattern only. |
   ```

4. If a planning-only PR is being used to land this runbook, open it now with only the runbook + memo + backlog row; hold all script/config changes for the implementation PR that follows.

**Acceptance criteria:**
- [ ] GitHub issue exists with correct title and labels
- [ ] Issue number is recorded in the runbook revision banner
- [ ] `OVERLORD_BACKLOG.md` contains a Planned row referencing the issue
- [ ] Reviewer-response memo (if any) references the same issue number
- [ ] No implementation work (Phases 0.1 onward) begins until the above are in place

---

### Micro-slice 0.1 — Add concurrency groups to all PR workflows

**File:** `.github/workflows/*.yml` (every workflow triggered by `pull_request` or `push`)

**Change:** Add at top level of each workflow:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Acceptance criteria:**
- [ ] All PR-triggered workflows contain a `concurrency:` block
- [ ] Force-pushing to an open PR cancels the in-flight run (verify once by pushing twice in quick succession)
- [ ] `gh run list` shows `cancelled` status on the superseded run, not `failure`

---

### Micro-slice 0.2 — Audit `paths-ignore` for doc-only changes

**File:** `.github/workflows/*.yml` (Playwright + heavy workflows)

**Change:** Add `paths-ignore` so `.docx`, `.md` (planning docs), and `docs/**` pushes don't trigger Playwright:

```yaml
on:
  pull_request:
    paths-ignore:
      - '**.docx'
      - 'docs/**'
      - '*.md'
      - 'BACKLOG.md'
      - 'QUICKREF.md'
```

**Acceptance criteria:**
- [ ] Pushing a commit that only touches `.docx` or planning `.md` files does not trigger Playwright workflow
- [ ] `gh run list` after such a push shows zero new Playwright runs
- [ ] Code-only pushes still trigger Playwright normally

---

### Micro-slice 0.3 — Verify Playwright runs headless + chromium-only in CI

**File:** `playwright.config.ts` and/or `.github/workflows/playwright.yml`

**Change:** Confirm `headless: true` and CI projects limited to chromium. If the CI matrix currently runs multiple browsers, reduce to chromium-only for PRs.

**Acceptance criteria:**
- [ ] `playwright.config.ts` has `headless: true` as default
- [ ] CI matrix contains only `chromium` project (or a single-project run)
- [ ] Full browser matrix, if needed, is gated behind manual `workflow_dispatch` or nightly schedule

---

## 6. Phase 1 — lefthook Install & Tier 1 Pre-Commit <a name="phase-1"></a>

**Goal:** Sub-5-second pre-commit gate that catches lint, type, secret leaks, and governance violations on staged files.

**Effort:** 1 hour
**Dependencies:** Phase 0 complete (not strictly required, but clean baseline matters for measurement)

### Micro-slice 1.1 — Install lefthook

**Commands:**

```bash
pnpm add -D lefthook
npx lefthook install
```

**Acceptance criteria:**
- [ ] `lefthook` appears in `devDependencies` of `package.json`
- [ ] `.git/hooks/pre-commit` and `.git/hooks/pre-push` exist and reference lefthook
- [ ] `npx lefthook version` prints version without error

---

### Micro-slice 1.2 — Create `lefthook.yml` with pre-commit jobs

**File:** `lefthook.yml` (repo root)

**Content:**

```yaml
# HLD Pro — Local CI Gate
# Docs: see HLD_Pro_Local_CI_Gate_Runbook.md

pre-commit:
  parallel: true
  commands:
    governance:
      run: ./scripts/governance-check.sh {staged_files}
      glob: "*.{ts,tsx,js,jsx,sql,sh,md}"
      stage_fixed: false

    eslint:
      glob: "*.{ts,tsx,js,jsx}"
      run: pnpm eslint --cache --max-warnings=0 {staged_files}
      stage_fixed: true

    tsc:
      glob: "*.{ts,tsx}"
      run: pnpm tsc-files --noEmit {staged_files}

    gitleaks:
      run: gitleaks protect --staged --redact --no-banner
```

**Install `tsc-files` helper:**

```bash
pnpm add -D tsc-files
```

**Acceptance criteria:**
- [ ] `git commit` with a lint error in a staged TS file is blocked with clear error
- [ ] `git commit` with a hardcoded API key in staged diff is blocked by gitleaks
- [ ] `git commit` on a `.docx`-only change runs zero commands (globs don't match) and completes in <1s
- [ ] All four pre-commit commands run in parallel (timestamps in verbose output overlap)
- [ ] Total pre-commit time on typical 3-file staged change is <5s

---

### Micro-slice 1.3 — Verify governance-check.sh is git-compatible

**File:** `scripts/governance-check.sh`

**Check:** The script currently runs as a PreToolUse hook inside Claude Code. Confirm it:
1. Accepts a file list as `$@` or reads from stdin
2. Exits 0 on pass, non-zero on fail
3. Produces human-readable output (not JSON-only)

**If incompatible:** Wrap existing logic in a thin adapter `scripts/governance-check-git.sh` that translates git file arguments into the format the existing script expects.

**Acceptance criteria:**
- [ ] `./scripts/governance-check.sh <file.ts>` exits 0 for a compliant file
- [ ] Same command exits non-zero with clear error for a violating file
- [ ] Script runs in <2s on a 5-file staged set

---

## 7. Phase 2 — Tier 2 Pre-Push (Fast Checks) <a name="phase-2"></a>

**Goal:** 30–90s pre-push gate that catches Vitest failures, migration errors, edge function issues, and build breakage — **without** Playwright yet.

**Effort:** 1.5 hours
**Dependencies:** Phase 1 complete

### Micro-slice 2.1 — Add pre-push block to `lefthook.yml`

**File:** `lefthook.yml` (append)

**Content:**

```yaml
pre-push:
  parallel: true
  commands:
    preflight-probe:
      run: pnpm preflight
      # Invokes the existing Haiku preflight-probe agent

    vitest-changed:
      run: pnpm vitest run --changed origin/main --passWithNoTests

    migration-lint:
      glob: "supabase/migrations/*.sql"
      run: |
        pnpm supabase db lint --local
        pnpm run validate:migrations

    deno-check:
      glob: "supabase/functions/**/*.ts"
      run: |
        deno lint {push_files}
        deno check {push_files}

    vite-build:
      run: pnpm build
      # Catches TS errors CI would catch, plus bundling failures
```

**Acceptance criteria:**
- [ ] `git push` with a failing Vitest test on a changed file is blocked
- [ ] `git push` with an invalid SQL migration is blocked with lint error
- [ ] `git push` with a `deno check` error in an edge function is blocked
- [ ] `git push` with a broken Vite build is blocked
- [ ] Push of a docs-only change runs only `preflight-probe` + `vite-build` and completes in <30s
- [ ] Full Tier 2 run on a typical 10-file code change completes in <90s
- [ ] `git push --no-verify` bypasses all pre-push commands (escape hatch works)

---

### Micro-slice 2.2 — Wire `pnpm preflight` script

**File:** `package.json`

**Change:** Ensure `preflight` script invokes the existing `preflight-probe` agent:

```json
{
  "scripts": {
    "preflight": "claude-code agent run preflight-probe --ci-mode"
  }
}
```

**Acceptance criteria:**
- [ ] `pnpm preflight` executes the `preflight-probe` agent with no interactive prompts
- [ ] Agent exits 0 on clean repo state, non-zero on blocking issues
- [ ] Output is terse (one-line status per check) to avoid log spam on every push

---

### Micro-slice 2.3 — Add migration validator script

**File:** `scripts/validate-migrations.sh` (new)

**Content:** Thin wrapper around the existing `migration-validator` agent:

```bash
#!/usr/bin/env bash
set -euo pipefail

CHANGED_MIGRATIONS=$(git diff --name-only origin/main...HEAD -- 'supabase/migrations/*.sql')

if [ -z "$CHANGED_MIGRATIONS" ]; then
  echo "No migration changes; skipping validator."
  exit 0
fi

echo "Validating migrations: $CHANGED_MIGRATIONS"
claude-code agent run migration-validator --files "$CHANGED_MIGRATIONS" --ci-mode
```

**Update `package.json`:**

```json
{
  "scripts": {
    "validate:migrations": "bash scripts/validate-migrations.sh"
  }
}
```

**Acceptance criteria:**
- [ ] Running `pnpm validate:migrations` with no migration changes exits 0 in <1s
- [ ] With a valid new migration, exits 0 after agent review
- [ ] With an invalid migration (e.g., missing down migration, unsafe DDL), exits non-zero with agent report
- [ ] Script is idempotent across multiple runs

---

## 8. Phase 3 — Tier 2 Pre-Push (Playwright) <a name="phase-3"></a>

**Goal:** Add Playwright 60/82 suite to pre-push gate against local dev server + local Supabase. This is the biggest minute-saver and the highest-risk phase for introducing friction.

**Effort:** 2 hours
**Dependencies:** Phase 2 complete, local Supabase environment working

### Micro-slice 3.1 — Configure Playwright `webServer` block

**File:** `playwright.config.ts`

**Change:** Add or verify `webServer` block so Playwright boots `vite dev` automatically:

```typescript
export default defineConfig({
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  use: {
    baseURL: 'http://localhost:5173',
    headless: true,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

**Acceptance criteria:**
- [ ] `pnpm playwright test` with no running dev server starts one automatically
- [ ] Same command with a running dev server reuses it (no port conflict)
- [ ] Startup overhead is ≤10s when server must be booted
- [ ] All 60 passing tests still pass after this change

---

### Micro-slice 3.2 — ~~Tag slow tests with `@slow`~~ **SUPERSEDED by Phase 6**

**Status:** This micro-slice is intentionally left blank. See Phase 6 (Selective Playwright Testing by Diff) for the replacement approach.

**Do not implement `@slow` tagging.** If tags already exist in the repo from an earlier attempt, they are ignored by the new pre-push invocation. Remove them opportunistically during Phase 6.2 when auditing spec files for `@covers` annotations.

---

### Micro-slice 3.3 — Wire Playwright into pre-push (placeholder; finalized in Phase 6)

**File:** `lefthook.yml` (update `pre-push` section)

**Interim content for Phase 3 (full-suite run; superseded by Phase 6.5):**

```yaml
    playwright:
      run: pnpm test:e2e
      # Phase 3: runs full suite. Phase 6.5 replaces this with
      # selective execution via select-playwright-specs.sh.
```

**Add a single `test:e2e` script to `package.json`:**

```json
{
  "scripts": {
    "test:e2e": "playwright test"
  }
}
```

**Acceptance criteria:**
- [ ] `git push` triggers Playwright after all Phase 2 checks complete
- [ ] A broken E2E test blocks the push with clear failure output
- [ ] `git push --no-verify` still bypasses Playwright (escape hatch preserved)
- [ ] This invocation is **replaced** by Phase 6.5 — do not treat it as the final shape

> **Note:** If you are doing Phases 3 and 6 in the same sitting, skip this interim wiring and go straight to Phase 6.5. This micro-slice exists only for operators who want an intermediate checkpoint.

---

### Micro-slice 3.4 — Document local Supabase requirement

**File:** `QUICKREF.md` (append new section)

**Content:**

```markdown
## Local CI Gate — Playwright Requirements

Pre-push Playwright runs against **local Supabase** (`supabase start`) and the local Vite dev server.

**Before pushing for the first time in a session:**
```bash
supabase start          # Boots local Postgres + Supabase stack
pnpm dev                # Optional; Playwright will boot its own if not running
```

**If `supabase start` is not running**, Playwright tests that hit Supabase will fail. Options:
1. Start local Supabase (preferred)
2. Skip with `git push --no-verify` and rely on staging spot-check
3. Open an issue if the Supabase boot requirement becomes chronic friction

**Selective testing:** Pre-push Playwright runs only the specs whose covered source files changed (see Phase 6). To run the full suite manually before a PR, use `pnpm test:e2e:full`.

**CI remains authoritative.** The local gate is an upstream filter that reduces avoidable failures; it never replaces required CI. A green local result — at any tier, matched or full — is not a CI pass.
```

**Acceptance criteria:**
- [ ] `QUICKREF.md` contains the Local CI Gate section
- [ ] Instructions are copy-pasteable and correct
- [ ] No stale references to old test invocation patterns or `@slow` tags
- [ ] The "CI remains authoritative" line is present verbatim in the QUICKREF section

---

## 9. Phase 4 — Integration with Existing Agents <a name="phase-4"></a>

**Goal:** Ensure the local gate complements, rather than duplicates, the existing `.claude/agents/` supervisor ecosystem.

**Effort:** 45 min
**Dependencies:** Phases 1–3 complete

### Micro-slice 4.1 — Update `hldpro-watcher.md` supervisor table

**File:** `.claude/agents/hldpro-watcher.md`

**Change:** Add a row to the supervisor sub-agent table acknowledging the local gate:

| Sub-agent | Trigger | Output target | Notes |
|---|---|---|---|
| (existing rows…) | | | |
| `preflight-probe` | Pre-push (git hook) | stderr | Runs via lefthook; not under watcher supervision |

**Acceptance criteria:**
- [ ] `hldpro-watcher.md` table reflects the new pre-push invocation path
- [ ] Report format section notes that pre-push failures surface via git output, not via watcher briefing

---

### Micro-slice 4.2 — Add `system_event` row on push bypass

**File:** `scripts/log-push-bypass.sh` (new)

**Content:**

```bash
#!/usr/bin/env bash
# Logs --no-verify pushes to operator_context for pattern detection.
# Not a blocker; purely observability.

if [ -n "${GIT_PUSH_NO_VERIFY:-}" ]; then
  curl -s -X POST "$SUPABASE_URL/rest/v1/operator_context" \
    -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "event_type": "system_event",
      "category": "push_bypass",
      "payload": {"branch": "'$(git branch --show-current)'"}
    }' >/dev/null 2>&1 || true
fi
```

**Decision point:** This is optional. Leave as deferred micro-slice unless Benji wants passive telemetry on bypass frequency. If `--no-verify` stays rare, the logging adds noise without value.

**Acceptance criteria (if implemented):**
- [ ] `operator_context` receives a `push_bypass` row when `--no-verify` is used
- [ ] Script fails silently (does not block push) if Supabase is unreachable
- [ ] No PII or diff content is logged — only branch name and timestamp

---

## 10. Phase 5 — Documentation & Rollout <a name="phase-5"></a>

**Goal:** Capture the new workflow in existing governance docs and set a 2-week measurement window.

**Effort:** 30 min
**Dependencies:** All prior phases complete

### Micro-slice 5.1 — Update `CLAUDE.md` with hook expectations

**File:** `CLAUDE.md`

**Change:** Add section under governance rules:

```markdown
## Local CI Gate

All commits and pushes pass through lefthook-managed gates. See `lefthook.yml` and `HLD_Pro_Local_CI_Gate_Runbook.md`.

Do not bypass hooks in agent-driven workflows. `--no-verify` is reserved for operator-level emergencies only.
```

**Acceptance criteria:**
- [ ] `CLAUDE.md` references the runbook and `lefthook.yml`
- [ ] Agent workflows do not include `--no-verify` as a default

---

### Micro-slice 5.2 — Update `BACKLOG.md` milestone mapping

**File:** `BACKLOG.md`

**Change:** Add entry under v1.4:

```markdown
- [x] **Infra: Local CI Gate** — lefthook pre-commit + pre-push, replaces redundant Actions runs
  - `type: infra` `area: dev-velocity` `status: shipped`
  - See: `HLD_Pro_Local_CI_Gate_Runbook.md`
```

**Acceptance criteria:**
- [ ] Entry present in `BACKLOG.md` under v1.4 section
- [ ] Marked shipped after final acceptance criteria checked

---

### Micro-slice 5.3 — Measurement window

**Action:** Record baseline and check at T+14 days.

**Baseline capture commands (run before merging this epic):**

```bash
gh run list --limit 100 --json status,conclusion,workflowName > baseline-ci-runs.json
```

**T+14 days measurement:**

```bash
gh run list --limit 100 --json status,conclusion,workflowName > post-gate-ci-runs.json
# Compare failure rate, total runtime, cancelled count
```

**Acceptance criteria:**
- [ ] Baseline JSON captured and committed to `docs/measurements/` or equivalent
- [ ] T+14 measurement scheduled in BACKLOG or calendar
- [ ] Epic success metric (≥80% reduction in failed runs) evaluated and recorded

---

## 11. Phase 6 — Selective Playwright Testing by Diff <a name="phase-6"></a>

**Goal:** Run only the Playwright specs whose covered source files actually changed in the push. If no specs match, skip Playwright entirely. If the diff touches shared code (libs, edge functions, migrations, build config), fall back to the full suite.

**Effort:** 2–3 hours
**Dependencies:** Phase 3 complete (or skipped; see Phase 3.3 note)

### Why this replaces chunking

Chunking and `@slow` tagging both accept the premise that "the suite must run; it's just a question of *how fast*." Selective testing rejects that premise: **if your diff touches one page, run one spec**. A push that only touches `src/pages/Dashboard.tsx` should trigger `e2e/dashboard.spec.ts` and nothing else, typically completing in under 30 seconds.

### Fail-fast semantics

Three rules govern how failures surface, per decision table in §4:

1. **Serial within a file** — `test.describe.configure({ mode: 'serial' })` means once a test in a flow fails, remaining tests in that file skip. You don't waste time on dependent steps of a broken flow.
2. **Parallel across files** — `fullyParallel: true` at the project level means failure in `dashboard.spec.ts` does not block `billing.spec.ts`. Independent failures surface in the same run.
3. **No `--max-failures`** — the whole selected set runs to completion so you see every independent failure without re-running.

This matches Benji's stated preference: "fail fast and log, then continue path to see if any other failures unrelated."

---

### Micro-slice 6.1 — Capture baseline timing

**Purpose:** Produce the numbers that cap-limit decisions and success metrics reference.

**File:** `scripts/capture-playwright-baseline.sh` (new)

**Content:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Captures per-file wall time for the full Playwright suite.
# Run once before Phase 6 to establish baseline.

mkdir -p docs/measurements

pnpm playwright test \
  --reporter=json \
  --output=.playwright-baseline-artifacts \
  > docs/measurements/playwright-baseline-raw.json

node scripts/summarize-playwright-baseline.mjs \
  docs/measurements/playwright-baseline-raw.json \
  > docs/measurements/playwright-baseline-summary.md

echo "Baseline written to docs/measurements/playwright-baseline-summary.md"
```

**File:** `scripts/summarize-playwright-baseline.mjs` (new) — see Appendix C for full source.

**Summary produces:**

| Metric | Value |
|---|---|
| Total wall time (full suite) | _filled by script_ |
| Number of spec files | _filled_ |
| p50 wall time per file | _filled_ |
| p75 wall time per file | _filled_ |
| p95 wall time per file | _filled_ |
| Slowest spec | _filled_ |
| Files >3 min wall time | _filled_ |

**Cap limits** for new spec files (enforced advisorily, see 6.6):
- **Soft cap:** p75 of current suite × 1.25, rounded to nearest 30s
- **Hard cap:** p95 of current suite × 1.25, rounded to nearest 30s
- If the computed soft cap is <90s, floor at 90s (no benefit chasing sub-minute specs)
- If the computed hard cap is >240s, cap at 240s (anything larger should be split)

**Acceptance criteria:**
- [ ] `docs/measurements/playwright-baseline-summary.md` exists and contains real numbers
- [ ] Summary includes p50/p75/p95 per-file wall times
- [ ] Computed soft and hard caps are recorded in the summary
- [ ] Baseline raw JSON is committed for future comparison

---

### Micro-slice 6.2 — Audit specs for `@covers` coverage

**Purpose:** Every existing `e2e/*.spec.ts` must either follow the file-name mirror convention or declare `@covers`. Ambiguous specs force the full-suite fallback, which defeats the point.

**Convention rule:** `e2e/<feature>.spec.ts` auto-maps to `src/pages/<Feature>.tsx` and `src/pages/<Feature>/*.tsx` (PascalCase → kebab-case).

**Example convention match:**
- `e2e/dashboard.spec.ts` → `src/pages/Dashboard.tsx` (auto-mapped, no annotation needed)

**Example `@covers` annotation (multi-page or non-conventional name):**

```typescript
/**
 * @covers src/pages/Leads.tsx
 * @covers src/components/LeadTable.tsx
 * @covers src/lib/lead-scoring.ts
 */
import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });
test.describe('Leads CRM', () => {
  test('loads lead list', async ({ page }) => { /* ... */ });
  test('creates new lead', async ({ page }) => { /* ... */ });
});
```

**Audit step:** For each existing spec, check if convention match exists. If not, add `@covers`. Any spec that genuinely cannot map to source files (rare — e.g., health-check specs) gets `@covers *`.

Resolver rule for `@covers *`: include that spec for any code diff unless a full-suite fallback has already triggered. `@covers *` does **not** mean "run the entire suite"; it means "this spec is globally relevant and should be included in selective runs whenever source code changed."

**Acceptance criteria:**
- [ ] Every `e2e/**/*.spec.ts` file matches by convention OR contains `@covers`
- [ ] Any `@covers *` spec is included for any source-code diff and does not by itself force `FULL_SUITE`
- [ ] A grep audit (`grep -L '@covers' e2e/**/*.spec.ts | xargs -I{} test -f src/pages/$(basename {} .spec.ts | sed ...)`) produces zero unmatched, un-annotated files
- [ ] Every `describe` block in a multi-flow spec file has `test.describe.configure({ mode: 'serial' })` OR a comment explaining why parallel-within-file is safe

---

### Micro-slice 6.3 — Build the spec resolver

**File:** `scripts/select-playwright-specs.sh` (new)

**CLI contract:**

```bash
scripts/select-playwright-specs.sh [--explain-trigger] [diff-base]
```

- Normal mode prints one of: empty stdout (no mapped specs), `FULL_SUITE`, or a space-separated spec list.
- `--explain-trigger` prints the first fallback reason only, such as `src/lib change`, `migration change`, or `config change`. It prints empty output when no fallback trigger matched.
- `diff-base` defaults to `origin/main`.

**Content:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Given a git diff range, emit a space-separated list of spec files to run.
# Emits "FULL_SUITE" if shared code changed.
# Emits nothing (empty stdout) if no specs match and no fallback triggered.

EXPLAIN_TRIGGER=false
if [ "${1:-}" = "--explain-trigger" ]; then
  EXPLAIN_TRIGGER=true
  shift
fi

DIFF_BASE="${1:-origin/main}"
CHANGED=$(git diff --name-only "$DIFF_BASE"...HEAD)

if [ -z "$CHANGED" ]; then
  exit 0
fi

# Triggers for full-suite fallback
FULL_SUITE_PATTERNS=(
  'src/lib/'
  'supabase/functions/'
  'supabase/migrations/'
  'package.json'
  'pnpm-lock.yaml'
  'vite.config.'
  'playwright.config.'
  'tailwind.config.'
  'tsconfig'
)

for pattern in "${FULL_SUITE_PATTERNS[@]}"; do
  if echo "$CHANGED" | grep -q "$pattern"; then
    if [ "$EXPLAIN_TRIGGER" = true ]; then
      case "$pattern" in
        'src/lib/') echo "src/lib change" ;;
        'supabase/functions/') echo "edge function change" ;;
        'supabase/migrations/') echo "migration change" ;;
        *) echo "config change" ;;
      esac
      exit 0
    fi
    echo "FULL_SUITE"
    exit 0
  fi
done

if [ "$EXPLAIN_TRIGGER" = true ]; then
  exit 0
fi

# Docs-only — handled by Phase 0 paths-ignore in CI, but belt-and-suspenders here
CODE_CHANGED=$(echo "$CHANGED" | grep -E '\.(ts|tsx|js|jsx|sql|sh)$' || true)
if [ -z "$CODE_CHANGED" ]; then
  exit 0
fi

# Build candidate spec list via convention + @covers
node scripts/resolve-specs.mjs "$CHANGED"
```

**File:** `scripts/resolve-specs.mjs` (new) — see Appendix C for full source.

**Behavior:**
1. Read every `e2e/**/*.spec.ts`
2. For each, extract `@covers` paths; if none, derive from file-name convention
3. Intersect with the changed files set
4. Emit the matched spec paths to stdout

**Acceptance criteria:**
- [ ] `bash scripts/select-playwright-specs.sh origin/main` returns empty when diff contains only docs
- [ ] `bash scripts/select-playwright-specs.sh --explain-trigger origin/main` returns the fallback reason only when a full-suite pattern matches
- [ ] Returns `FULL_SUITE` when diff includes `src/lib/*` or `supabase/migrations/*`
- [ ] Returns a single spec path when diff touches only one mapped page
- [ ] Returns multiple specs when diff spans multiple mapped pages
- [ ] Handles renamed files (git detects rename; resolver uses new path)
- [ ] Completes in <2s on a typical diff

---

### Micro-slice 6.4 — Update `playwright.config.ts` for fail-fast + reporter

**File:** `playwright.config.ts`

**Content:**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,           // Parallel across files
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0, // No retries on local pre-push
  workers: process.env.CI ? 2 : undefined, // Local: auto (cpu count)
  reporter: [
    ['list'],
    ['json', { outputFile: '.playwright-failures.json' }],
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  use: {
    baseURL: 'http://localhost:5173',
    headless: true,
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

**Convention for spec authors:** every `describe` block representing a dependent flow wraps with:

```typescript
test.describe.configure({ mode: 'serial' });
```

This gives per-file fail-fast (first failed test in flow causes remaining to skip) without blocking other files.

**Acceptance criteria:**
- [ ] `playwright.config.ts` matches the structure above
- [ ] Running a broken spec file in isolation shows the failing test + skipped remainder (serial mode working)
- [ ] Running multiple broken spec files shows all failures after the run completes (parallel-across-files working)
- [ ] `.playwright-failures.json` contains structured per-test status after any run
- [ ] Local runs have `retries: 0`; CI runs have `retries: 2`

---

### Micro-slice 6.5 — Wire selective execution into lefthook

**File:** `lefthook.yml` (replace the `playwright:` command from Phase 3.3)

**Content:**

```yaml
    playwright-selective:
      run: |
        SPECS=$(bash scripts/select-playwright-specs.sh origin/main)
        if [ -z "$SPECS" ]; then
          echo "LOCAL CHECK: no mapped Playwright specs for this diff. Matched specs: 0. This is not a full-suite replay; CI remains authoritative."
          exit 0
        elif [ "$SPECS" = "FULL_SUITE" ]; then
          TRIGGER=$(bash scripts/select-playwright-specs.sh --explain-trigger origin/main)
          echo "LOCAL CHECK: full Playwright suite required by fallback trigger: $TRIGGER."
          pnpm playwright test
        else
          COUNT=$(echo "$SPECS" | wc -w | tr -d ' ')
          echo "LOCAL CHECK: running $COUNT matched Playwright specs: $SPECS"
          pnpm playwright test $SPECS
          STATUS=$?
          if [ $STATUS -eq 0 ]; then
            echo "LOCAL CHECK: matched Playwright specs passed: $COUNT. This is not a full-suite replay."
          fi
          exit $STATUS
        fi
```

**Resolver script addition:** `scripts/select-playwright-specs.sh` gains a `--explain-trigger` mode that echoes the first matched fallback pattern (e.g., `src/lib change`, `migration change`, `config change`) without running Playwright. Implementation is a 5-line branch at the top of the script.

**Add three scripts to `package.json`:**

```json
{
  "scripts": {
    "test:e2e": "bash scripts/run-playwright-selective.sh origin/main",
    "test:e2e:full": "pnpm playwright test",
    "test:e2e:selective": "bash scripts/run-playwright-selective.sh origin/main"
  }
}
```

**Wrapper contract:** `scripts/run-playwright-selective.sh [diff-base]` owns the three resolver outcomes:

- empty resolver output: print the zero-match verdict line and exit 0
- `FULL_SUITE`: call `scripts/select-playwright-specs.sh --explain-trigger <diff-base>`, print the fallback-trigger verdict line, then run `pnpm playwright test`
- spec list: run `pnpm playwright test <specs>`, then print the matched-spec verdict line on success

This wrapper prevents `FULL_SUITE` from being passed through `xargs` as if it were a spec path.

**Operator override — full-suite script.** The `test:e2e:full` script is the user-facing override: when an operator wants to force a full-suite replay locally without touching resolver logic, they run `pnpm test:e2e:full`. This is a single escape lever, not a mode matrix; the resolver remains three-state internally (skip / subset / FULL_SUITE).

**Acceptance criteria:**
- [ ] Push with no code changes runs zero Playwright tests and prints the "Matched specs: 0" verdict line verbatim
- [ ] Push touching only `src/pages/Dashboard.tsx` runs only `e2e/dashboard.spec.ts` and prints the "matched Playwright specs passed: N" verdict line on success
- [ ] Push touching `src/lib/utils.ts` runs full suite with the "fallback trigger" verdict line naming the trigger
- [ ] Every verdict line contains either "This is not a full-suite replay" or "full Playwright suite required" — never a bare "PASS" without qualification
- [ ] `pnpm test:e2e:full` runs the full suite regardless of diff state (override works)
- [ ] `pnpm test:e2e` handles empty output, `FULL_SUITE`, and spec-list resolver output through the wrapper; it never passes `FULL_SUITE` to Playwright as a path
- [ ] Failing spec blocks push with clear output
- [ ] Independent failures across two spec files both surface in one run (parallel-across-files confirmed)
- [ ] Total pre-push time on a single-page diff is under 45s (Tier 2 fast + one spec)
- [ ] `git push --no-verify` still bypasses all Playwright work

---

### Micro-slice 6.6 — Update `test-writer` agent spec

**File:** `.claude/agents/test-writer.md`

**Change:** Append a "Selective Testing Rule" section:

```markdown
## Selective Testing Rule (added April 2026)

When authoring new Playwright specs, the test-writer agent MUST:

1. Name the spec file using the file-name mirror convention (`src/pages/Foo.tsx` → `e2e/foo.spec.ts`) OR include a `@covers` JSDoc at the top of the file listing every source file the spec depends on.
2. Wrap any dependent-flow `describe` block with `test.describe.configure({ mode: 'serial' })`.
3. Keep each spec file below the soft cap recorded in `docs/measurements/playwright-baseline-summary.md`. If the test will exceed the soft cap, split it into multiple files by flow.
4. Do NOT use `@slow` tags. That pattern is deprecated; selective testing makes it unnecessary.
5. Verify the resolver picks up the new spec by running `bash scripts/select-playwright-specs.sh origin/main` after adding it — the new spec must appear when its covered source files are in the diff.

Violations block the PR via pre-push resolver failure, not via agent self-check. The hook is the enforcement layer; this rule is the authoring guidance.
```

**Acceptance criteria:**
- [ ] `test-writer.md` contains the Selective Testing Rule section
- [ ] Any new spec the agent produces includes either a convention-matching filename or `@covers` JSDoc
- [ ] Agent does not propose `@slow` tags in new work

---

### Micro-slice 6.7 — Create standalone rule doc

**File:** `docs/rules/PLAYWRIGHT_SELECTIVE_TESTING.md` (new)

**Content:** A ~1-page reference doc covering:
- The three resolver outcomes (skip / subset / full fallback)
- The convention and `@covers` annotation syntax
- The fail-fast model (serial within file, parallel across files, no max-failures)
- How to run selectively manually (`pnpm test:e2e:selective`)
- How to regenerate baseline timing
- Cap limits from the baseline summary
- Link back to this runbook as implementation source

**Acceptance criteria:**
- [ ] `docs/rules/PLAYWRIGHT_SELECTIVE_TESTING.md` exists
- [ ] Document is <2 pages, reads as reference not tutorial
- [ ] Links to baseline summary, runbook, and `test-writer.md`
- [ ] No duplicated content from this runbook — pointers only

---

### Micro-slice 6.8 — Add pointer in `CLAUDE.md`

**File:** `CLAUDE.md`

**Change:** Append one paragraph under the Local CI Gate section created in Phase 5.1:

```markdown
### Playwright Selective Testing

Pre-push Playwright runs only the specs whose covered source files changed in the diff. See `docs/rules/PLAYWRIGHT_SELECTIVE_TESTING.md` for the authoring rule and `scripts/select-playwright-specs.sh` for the resolver. Do not propose `@slow` tags or full-suite-always patterns in new work.
```

**Acceptance criteria:**
- [ ] `CLAUDE.md` contains the pointer paragraph
- [ ] Paragraph is under the Local CI Gate section, not a duplicate top-level section
- [ ] Links resolve in rendered markdown

---

## 12. Rollback Plan <a name="rollback-plan"></a>

If the local gate introduces chronic friction (Benji bypasses it more than occasionally, or push latency exceeds 5 minutes consistently):

1. **First mitigation — resolver tuning:** If selective testing triggers `FULL_SUITE` too often, audit the patterns in `select-playwright-specs.sh` — `src/lib/` changes may not actually affect all pages. Tighten the fallback triggers before demoting Playwright.
2. **Second mitigation:** Demote Playwright from pre-push to a manual `pnpm test:e2e:selective` ritual before PR merge. Keep Tier 1 + Phase 2 fast checks active.
3. **Third mitigation:** Split `lefthook.yml` into `lefthook-fast.yml` (always on) and `lefthook-full.yml` (opt-in via env var). Source fast by default.
4. **Full rollback:** `npx lefthook uninstall && pnpm remove lefthook tsc-files` — hooks removed, CI returns to sole-validator role. Selective-testing scripts remain in the repo as dead code; delete if desired.

No database migrations, no schema changes, no production code paths affected. Rollback is non-destructive.

---

## 13. Open Decisions <a name="open-decisions"></a>

| Decision | Default | Alternative | Owner |
|---|---|---|---|
| Supabase target for Playwright | Local (`supabase start`) | Dedicated cloud test project | Benji — confirm during Phase 3 |
| Log `--no-verify` bypasses? | No | Yes, via `operator_context` | Benji — decide during Phase 4 |
| Add `post-merge` hook to pull latest deps? | No | Yes, auto `pnpm install` | Benji — decide if dep drift becomes issue |
| CI workflow minute budget alert | None | Slack alert at 75% monthly | Benji — v1.5 optional add |
| Selective-testing full-suite trigger list | `src/lib/`, edge functions, migrations, config | Tighter or looser | Benji — tune in Phase 6.3 after first week |
| Soft/hard cap enforcement | Advisory (doc in `test-writer.md`) | Hard block via governance-check.sh | Benji — promote to hard block if specs drift |

---

## 14. Epic Acceptance Criteria <a name="epic-acceptance-criteria"></a>

The epic is **done** when:

- [ ] lefthook installed and `lefthook.yml` committed at repo root
- [ ] Tier 1 pre-commit gate catches lint, type, secret, and governance errors on staged files in <5s
- [ ] Tier 2 pre-push gate catches Vitest, migration, deno, and build errors in <90s (excluding Playwright)
- [ ] Playwright baseline timing captured in `docs/measurements/playwright-baseline-summary.md`
- [ ] Every `e2e/**/*.spec.ts` file either matches the file-name convention or contains `@covers` annotation
- [ ] `scripts/select-playwright-specs.sh` correctly returns skip / subset / FULL_SUITE for representative diff scenarios
- [ ] `playwright.config.ts` has `fullyParallel: true`, `retries: 0` locally, JSON reporter, no `--max-failures`
- [ ] Push touching one mapped page completes pre-push Playwright in <45s
- [ ] Push touching `src/lib/*` or migrations runs full suite with clear log message
- [ ] Docs-only push runs zero Playwright tests
- [ ] `git push --no-verify` escape hatch documented in `QUICKREF.md` and works
- [ ] Phase 0 workflow concurrency groups live on all PR workflows
- [ ] `CLAUDE.md` references the gate; `docs/rules/PLAYWRIGHT_SELECTIVE_TESTING.md` exists; `BACKLOG.md` has shipped entry under v1.4
- [ ] `test-writer.md` agent spec contains the Selective Testing Rule
- [ ] Baseline CI failure rate captured in `docs/measurements/`
- [ ] T+14 measurement shows ≥80% reduction in failed GitHub Actions runs
- [ ] Benji has run a full dev cycle (commit → push → staging spot-check) with the gate active and confirms no chronic friction

---

## 15. Appendix A — File Manifest <a name="appendix-a"></a>

**New files:**

- `lefthook.yml`
- `scripts/validate-migrations.sh`
- `scripts/log-push-bypass.sh` *(optional, Phase 4.2)*
- `scripts/capture-playwright-baseline.sh` *(Phase 6.1)*
- `scripts/summarize-playwright-baseline.mjs` *(Phase 6.1)*
- `scripts/select-playwright-specs.sh` *(Phase 6.3)*
- `scripts/resolve-specs.mjs` *(Phase 6.3)*
- `docs/measurements/baseline-ci-runs.json`
- `docs/measurements/playwright-baseline-raw.json` *(Phase 6.1)*
- `docs/measurements/playwright-baseline-summary.md` *(Phase 6.1)*
- `docs/rules/PLAYWRIGHT_SELECTIVE_TESTING.md` *(Phase 6.7)*

**Modified files:**

- `package.json` (scripts + devDependencies: `lefthook`, `tsc-files`)
- `playwright.config.ts` (webServer + reporter + fullyParallel + retries — Phase 6.4)
- `e2e/**/*.spec.ts` (`@covers` annotations where convention doesn't apply + `test.describe.configure({ mode: 'serial' })` on dependent flows — Phase 6.2)
- `scripts/governance-check.sh` (git-arg compatibility, if needed)
- `.github/workflows/*.yml` (concurrency + paths-ignore — Phase 0)
- `CLAUDE.md` (Local CI Gate section + Playwright selective testing pointer)
- `QUICKREF.md` (Playwright requirements section, references selective testing)
- `BACKLOG.md` (v1.4 shipped entry)
- `.claude/agents/hldpro-watcher.md` (supervisor table row)
- `.claude/agents/test-writer.md` (Selective Testing Rule section — Phase 6.6)

**Unchanged (explicitly out of scope):**

- Test suite logic (only annotations added; no test behavior modified)
- Supabase migrations
- Edge function implementations
- Reseller tier RLS policies

---

### Artifacts vs Reports — Tracking Rules

To prevent future gitignore-vs-evidence conflict, files produced by this epic fall into three explicit categories:

| Category | Tracked? | Example paths | Purpose |
|---|---|---|---|
| **Baseline artifacts** | Tracked (committed once per measurement cycle) | `docs/measurements/baseline-ci-runs.json`, `docs/measurements/playwright-baseline-raw.json`, `docs/measurements/playwright-baseline-summary.md` | Evidence for cap limits, success-metric comparisons, and governance review |
| **Per-run reports** | Gitignored | `.playwright-failures.json`, `.playwright-baseline-artifacts/`, any local run output | Ephemeral per-push output; not suitable for governance trail |
| **Closeout evidence** | Tracked (inside the closeout artifact itself) | Summaries or selected excerpts copied into the v1.4 closeout doc | When a specific report matters for review, it is summarized or excerpted into a tracked closeout, not committed raw |

**Rules:**

- `.gitignore` entries for per-run reports are added in Phase 1 alongside lefthook install. Candidates: `.playwright-failures.json`, `.playwright-baseline-artifacts/`, `playwright-report/`, `test-results/`.
- Baseline artifacts are regenerated at discrete cycles (start of epic, start of v1.5 CoS work, any suite-scale change). Between cycles they are read-only reference.
- If a per-run report is cited in a PR or closeout, the relevant excerpt is copied into the tracked artifact at citation time. The raw report file is never committed retroactively.
- This category list is the authoritative answer to "why is this file tracked/ignored?" Future additions to the epic's output surface must be placed into one of these three categories explicitly.

---

## 16. Appendix B — Minute Savings Estimate <a name="appendix-b"></a>

Rough model, based on a solo operator with ~30 pushes/week and the current 60/82 Playwright suite on GitHub-hosted runners. **Revised to reflect Phase 6 selective testing.**

| Source | Current minutes/week | Post-gate minutes/week | Savings |
|---|---|---|---|
| Successful Playwright runs (CI) | ~90 min (30 pushes × 3 min) | ~90 min (CI still runs full suite) | 0 |
| Failed Playwright runs caught by local gate | ~60 min (10 failures × 6 min fail+retry) | ~0 min | 60 min |
| Concurrency cancellations (Phase 0) | N/A | Cancels ~15 min/week superseded runs | 15 min |
| Docs-only PRs triggering Playwright (Phase 0) | ~20 min/week | ~0 min | 20 min |
| **Local pre-push time (Phase 6 selective)** | N/A — no local gate | ~15 min/week total (avg 30s × 30 pushes) instead of ~90 min (3 min × 30) if always full suite | 75 min of local time saved vs. naive full-suite pre-push |
| **Total estimated CI savings** | | | **~95 min/week** |
| **Total estimated local time saved** | | | **~75 min/week vs. naive pre-push** |

At GitHub's billing rate for private repo Linux runners (~$0.008/min), that's **~$3/week or ~$150/year** in direct CI cost. The larger win is the local 75 min/week — without selective testing, every push costs 3 minutes of Benji's attention waiting on the full suite. With Phase 6, most pushes cost 30 seconds.

The non-monetary value — keeping the "CI is green" signal trustworthy and not burning operator attention on unrelated test runs — is larger than the dollar figure.

---

## 17. Appendix C — Baseline Timing Capture Script <a name="appendix-c"></a>

### `scripts/summarize-playwright-baseline.mjs`

```javascript
#!/usr/bin/env node
// Reads Playwright's JSON reporter output and produces a markdown summary
// with p50/p75/p95 per-file wall times and computed cap limits.

import fs from 'node:fs';

const [, , inputPath] = process.argv;
if (!inputPath) {
  console.error('Usage: node summarize-playwright-baseline.mjs <raw.json>');
  process.exit(1);
}

const raw = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

// Aggregate per-file duration from Playwright's suite tree
const fileDurations = new Map();
function walk(suite) {
  if (suite.file) {
    const existing = fileDurations.get(suite.file) || 0;
    const specDurations = (suite.specs || []).reduce((acc, s) => {
      return acc + (s.tests || []).reduce((a, t) =>
        a + (t.results || []).reduce((x, r) => x + (r.duration || 0), 0), 0);
    }, 0);
    fileDurations.set(suite.file, existing + specDurations);
  }
  (suite.suites || []).forEach(walk);
}
(raw.suites || []).forEach(walk);

const durations = [...fileDurations.values()].sort((a, b) => a - b);
const totalMs = durations.reduce((a, b) => a + b, 0);

function percentile(arr, p) {
  if (arr.length === 0) return 0;
  const idx = Math.floor(arr.length * p);
  return arr[Math.min(idx, arr.length - 1)];
}

const p50 = percentile(durations, 0.5);
const p75 = percentile(durations, 0.75);
const p95 = percentile(durations, 0.95);

const roundTo30s = (ms) => Math.round(ms / 30_000) * 30_000;
const softCapMs = Math.max(90_000, roundTo30s(p75 * 1.25));
const hardCapMs = Math.min(240_000, roundTo30s(p95 * 1.25));

const slowest = [...fileDurations.entries()].sort((a, b) => b[1] - a[1])[0];
const over3min = [...fileDurations.entries()].filter(([, ms]) => ms > 180_000);

const fmt = (ms) => `${(ms / 1000).toFixed(1)}s`;

console.log(`# Playwright Baseline Timing Summary

Generated: ${new Date().toISOString()}
Source: ${inputPath}

| Metric | Value |
|---|---|
| Total wall time (full suite, sum of per-file) | ${fmt(totalMs)} |
| Number of spec files | ${durations.length} |
| p50 wall time per file | ${fmt(p50)} |
| p75 wall time per file | ${fmt(p75)} |
| p95 wall time per file | ${fmt(p95)} |
| Slowest spec | ${slowest ? `${slowest[0]} (${fmt(slowest[1])})` : 'n/a'} |
| Files >3 min wall time | ${over3min.length} |

## Cap limits for new spec files

- **Soft cap:** ${fmt(softCapMs)}  (p75 × 1.25, floored at 90s)
- **Hard cap:** ${fmt(hardCapMs)}  (p95 × 1.25, capped at 240s)

New specs exceeding soft cap should be split by flow. Specs exceeding hard cap must be split.

## Per-file durations

${[...fileDurations.entries()].sort((a, b) => b[1] - a[1])
  .map(([f, ms]) => `- ${f}: ${fmt(ms)}`).join('\n')}
`);
```

### `scripts/resolve-specs.mjs`

```javascript
#!/usr/bin/env node
// Given a newline-separated list of changed files on stdin (or as argv),
// emit the spec file paths whose @covers or convention match.

import fs from 'node:fs';
import path from 'node:path';
import { globSync } from 'glob';

const changed = (process.argv[2] || fs.readFileSync(0, 'utf8'))
  .split('\n').map(s => s.trim()).filter(Boolean);

const specFiles = globSync('e2e/**/*.spec.ts');
const matched = new Set();

// Convention: e2e/foo.spec.ts → src/pages/Foo.tsx, src/pages/Foo/**
function conventionTargets(specPath) {
  const base = path.basename(specPath, '.spec.ts');
  const pascal = base.charAt(0).toUpperCase() + base.slice(1);
  return [
    `src/pages/${pascal}.tsx`,
    `src/pages/${pascal}/`,
  ];
}

// @covers annotation: /** @covers src/foo.ts */
function coversTargets(specPath) {
  const text = fs.readFileSync(specPath, 'utf8');
  const matches = [...text.matchAll(/@covers\s+([^\s*]+)/g)];
  return matches.map(m => m[1]);
}

for (const spec of specFiles) {
  const covers = coversTargets(spec);
  const targets = covers.length > 0 ? covers : conventionTargets(spec);

  if (targets.includes('*')) {
    matched.add(spec); // wildcard always matches
    continue;
  }

  for (const target of targets) {
    if (changed.some(c => c === target || c.startsWith(target))) {
      matched.add(spec);
      break;
    }
  }
}

console.log([...matched].join(' '));
```

**Notes:**

- `glob` package already in repo (used by Vite). If not, `pnpm add -D glob`.
- Resolver exits 0 and emits empty stdout when no specs match — the lefthook wrapper handles the skip message.
- Intentionally simple: no caching, no memoization. Runs in <1s on 60-file suite; premature optimization is a trap here.


---

**End of runbook.**
