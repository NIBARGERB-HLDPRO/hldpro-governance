# PDCAR: Cloudflare Pages Direct Upload Deploy Gate (Epic #467)

Date: 2026-04-21
Planning branch: `issue-468-pages-deploy-pdcar-20260421`
Repo: `hldpro-governance`
Status: PLANNING — pending gpt-5.4 alternate-model review
GitHub epic: [#467](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/467)
Planning issue: [#468](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/468)

## Problem

`seek-and-ponder` is deployed to Cloudflare Pages using the **Direct Upload** delivery
model (Pages project config: `Git Provider: No`). Because there is no Cloudflare-side
git integration, merging to `main` does **not** auto-deploy. The live Pages project is
currently ~21 commits behind `main` (last successful deployment from `b27b931`, latest
main at `311d5db`). A cluster of recent PRs (#157-#162) that include web bundle changes
and `persona-respond` edge-function changes are merged on `main` but are **not live in
production**.

Additional failure modes that have been observed or are latent:

- **Frontend deployed before function** — frontend that expects a new `persona-respond`
  contract can reach a stale function if the function is not redeployed first, producing
  silent contract mismatches.
- **Domain parity drift** — apex (`seekandponder.com`) vs `www.` vs `*.pages.dev` can
  serve different deployments when only one target is updated.
- **No governance reuse** — any future Direct Upload Pages project will hit the same
  class of bugs because no org-level primitive exists for this deploy pattern.
- **Inventory blind spot** — we do not know which other governed repos use Direct Upload
  Pages; the problem is assumed seek-only but has never been verified.

## Context

The governance org owns reusable delivery gates for cross-repo concerns that are not
safe to implement per-repo (`governance-check.yml`, `local-ci-gate`, the consumer
verifier, the governance tooling deployer, and the `hldpro-sim` package pattern are
precedents).

The Cloudflare Pages **Direct Upload** path is distinct from the `Git Provider: Yes`
path because:

1. The deploy step must be invoked **by CI or by an operator**, not by Cloudflare.
2. Secrets (Cloudflare API token, account id, project name) must be held in the
   **consumer** repo's environment — governance never sees them.
3. The proof that a merge went live can only come from a post-deploy **freshness +
   domain parity** check that reads the public Pages surface and compares it to the
   latest consumer commit.

Child issues (all open) decompose the epic:

- #468 (this issue): Opus PDCAR + structured plan + planning execution scope
  (planning only; no implementation).
- #469: Reusable governance **Pages Direct Upload deploy gate** — gate implementation
  lives in this repo.
- #470: Governance **freshness + domain parity verifier** — verifier implementation
  lives in this repo.
- #471: **Seek first-consumer adoption proof** — governance child that tracks the
  downstream seek-and-ponder adoption (downstream seek issue #163).
- #472: **Direct Upload Pages inventory rollout** — governance chore that enumerates
  every governed repo running Pages in Direct Upload mode and tracks adoption.

Downstream seek-and-ponder issue: **#163** (adopt the governance Pages deploy gate
and verifier as the first consumer proof).

## Plan

Five sprints, one per child issue. Implementation only starts after `gpt-5.4
@ model_reasoning_effort=high` accepts this plan.

### Sprint 1 — Planning package (this issue #468, planning only)

Produce the canonical PDCAR (this doc), structured JSON plan validated against
`docs/schemas/structured-agent-cycle-plan.schema.json`, and the `planning_only`
execution scope that limits writes to the planning artifacts. Commit on
`issue-468-pages-deploy-pdcar-20260421`. Orchestrator will run the gpt-5.4 review
after this commit; no PR is opened by the planner.

### Sprint 2 — Reusable governance Pages Direct Upload deploy gate (#469)

Deliver a governance-owned Python gate, test-covered, with a consumer contract schema:

- `scripts/pages-deploy/pages_deploy_gate.py` — the gate entrypoint. Reads a consumer
  config (`pages-deploy.config.json`), plans the deploy, enforces the
  **function-before-frontend** ordering (any edge functions declared in the consumer
  config deploy before the static bundle), fails closed if credentials are missing,
  and **never logs token values** (only token presence/absence and redacted hashes).
- `scripts/pages-deploy/tests/test_pages_deploy_gate.py` — test suite covering
  ordering, missing-creds fail-closed, secret-redaction proof, dry-run mode, and
  non-zero exit on any step failure.
- `docs/schemas/pages-deploy-consumer.schema.json` — JSON Schema for the consumer
  config the gate consumes (project name, build output dir, edge function list +
  deploy order, domain list for parity check, dry-run flag).
- Documentation row in `STANDARDS.md` + `docs/runbooks/` entry.

Gate is invoked from consumer CI (e.g., GitHub Actions in seek-and-ponder) with the
consumer's own Cloudflare token; governance holds no secrets.

### Sprint 3 — Pages deployment freshness + domain parity verifier (#470)

Deliver the verifier that proves a deploy landed and serves consistent content across
all declared domains:

- `scripts/pages-deploy/pages_deploy_verifier.py` — compares the latest consumer
  `main` commit (or tag) against each configured domain, reports freshness delta in
  commits + time, and fails if any domain disagrees on the served deployment id.
- `scripts/pages-deploy/tests/test_pages_deploy_verifier.py` — stub HTTP fixtures,
  drift-detection coverage, domain-parity disagreement coverage.
- Freshness threshold and parity rule declared in the consumer config (Sprint 2
  schema extended as needed).
- Verifier is safe to run post-deploy, nightly, and on-demand. It must read **only
  public surface data** (no Cloudflare API token required for the base freshness
  probe; API reads are opt-in for richer diagnostics).

### Sprint 4 — Seek first-consumer adoption + live proof (#471 + seek-and-ponder #163)

Seek-and-ponder is the first consumer and the live proof that the gate works:

- Governance child #471 records the adoption plan, the seek branch/PR, and the live
  evidence paths back into `raw/validation/`.
- Downstream seek-and-ponder #163 lands:
  - `pages-deploy.config.json` at the seek repo root, validating against
    `docs/schemas/pages-deploy-consumer.schema.json`.
  - `scripts/deploy-pages.sh` — thin wrapper that invokes the governance gate via
    the managed distribution path (or a pinned copy where the governance package is
    not yet distributed).
  - CI change: `main` merge triggers `deploy-pages.sh`, then
    `pages_deploy_verifier.py`.
  - Live proof artifact: catching up the production Pages project to current `main`
    and verifying `seekandponder.com`, `www.seekandponder.com`, and the `*.pages.dev`
    preview all serve the same latest commit id.
- Governance-side evidence: `raw/validation/2026-04-21-issue-471-seek-first-consumer.md`.

### Sprint 5 — Direct Upload Pages inventory rollout (#472)

Lowest-priority cleanup sprint:

- `scripts/pages-deploy/inventory_direct_upload_projects.py` — enumerates governed
  repos, queries each for a `pages-deploy.config.json` or equivalent marker, and
  reports which projects are Direct Upload vs Git Provider.
- Adds any discovered Direct Upload consumers to the adoption backlog (one governance
  issue per discovered consumer), following the per-repo adoption pattern.
- Updates `docs/governed_repos.json` or the appropriate registry with a
  `pages_deploy_mode` field.

## Scope

**In scope (epic #467):**
- Reusable Pages Direct Upload deploy gate owned by `hldpro-governance`.
- Freshness + domain parity verifier owned by `hldpro-governance`.
- Consumer config schema at `docs/schemas/pages-deploy-consumer.schema.json`.
- Seek-and-ponder as first consumer proof.
- Inventory of other Direct Upload Pages consumers across governed repos.
- Documentation + runbook entries.

**Out of scope (epic #467):**
- Cloudflare Workers (non-Pages) deploy patterns.
- Vercel, Netlify, S3, or other non-Cloudflare static hosts.
- Changing any Cloudflare Pages project's delivery model (e.g., flipping a project
  from Direct Upload to Git Provider) — that is a per-consumer decision, not a
  governance mandate.
- Rewriting seek-and-ponder's web bundle build or `persona-respond` source logic.
- Any governance write into downstream repos. The planner may **read** seek-and-ponder
  to understand its deploy shape; it may not write there. Downstream edits happen via
  seek-and-ponder #163 on a lane claimed inside that repo.

## Do

1. Sprint 1 (this issue #468): commit PDCAR + structured plan + planning execution
   scope + backlog row. Push branch. Orchestrator runs gpt-5.4 review.
2. Sprint 2 (#469): implement gate + schema + tests; PR; CI green; merge.
3. Sprint 3 (#470): implement verifier + tests; PR; CI green; merge.
4. Sprint 4 (#471 + seek-and-ponder #163): governance adoption record first;
   downstream seek PR second; live deploy + verifier evidence captured in
   `raw/validation/`.
5. Sprint 5 (#472): inventory script; any new adoption issues filed; backlog updated.

## Check

```bash
# Sprint 1 — structured plan validates against schema
python3 -c "import json,jsonschema; jsonschema.validate(\
  json.load(open('docs/plans/issue-467-pages-deploy-gate-structured-plan.json')), \
  json.load(open('docs/schemas/structured-agent-cycle-plan.schema.json')))" && echo VALID

# Sprint 1 — execution scope validates and matches lane
python3 scripts/overlord/assert_execution_scope.py \
  --scope raw/execution-scopes/2026-04-21-issue-468-planning-only.json \
  --require-lane-claim

# Sprint 1 — backlog/GH alignment
python3 scripts/overlord/check_overlord_backlog_github_alignment.py

# Sprint 2/3 — gate + verifier tests (added by those sprints)
python3 -m pytest scripts/pages-deploy/tests/ -q

# Sprint 4 — live proof
# (run inside seek-and-ponder after its PR merges)
#   bash scripts/deploy-pages.sh
#   python3 scripts/pages-deploy/pages_deploy_verifier.py --config pages-deploy.config.json

# Sprint 5 — inventory
python3 scripts/pages-deploy/inventory_direct_upload_projects.py \
  --output raw/validation/2026-04-21-issue-472-direct-upload-inventory.md
```

## Adjust

### Material deviation rules (apply to every sprint)

1. **Emergency deploys.** If production is broken and the gate is the only path out,
   the operator may bypass the gate **only** by setting an explicit
   `PAGES_DEPLOY_EMERGENCY_BYPASS=1` env var and recording the bypass in
   `raw/validation/` with the reason, the operator, and a follow-up governance issue
   opened **before** the next merge. Silent bypass is not allowed.
2. **Missing credentials.** Gate must fail closed with a human-readable message when
   the Cloudflare API token, account id, or project name is absent. It must never
   attempt to deploy with partial credentials and must never log the values of the
   credentials it did find.
3. **Stale consumer checkouts.** The verifier must refuse to run against a consumer
   working tree that is not fast-forward-equal to the configured upstream; a stale
   checkout will otherwise produce false parity failures. Required evidence: fetch
   remote, compare HEAD, exit non-zero if behind.
4. **Downstream repo edits from governance.** This planning lane must not write into
   seek-and-ponder or any other consumer repo. Any seek-side change is the
   responsibility of seek-and-ponder issue #163 under its own lane claim. If Sprint 4
   discovers a required downstream change that cannot wait for issue #163, a separate
   seek-and-ponder issue must be opened before any write.
5. **No-secret evidence.** Validation artifacts must never include token values,
   signed URLs that embed tokens, or raw `Authorization` headers. Redaction is
   mandatory; test coverage in Sprint 2 must assert redaction.
6. **Sprint expansion.** If an implementation sprint discovers work that does not fit
   the sprint's acceptance criteria, either finish it inside the sprint's governing
   issue or open a new governance issue before closing the sprint. No silent scope
   widening.

## Review

- **Primary planner (Tier 1):** `claude-opus-4-6`.
- **Alternate-model review (required):** `gpt-5.4 @ model_reasoning_effort=high`.
  Orchestrator schedules the review after this commit. Implementation on Sprint 2+
  does not begin until the review is `accepted` or `accepted_with_followup`.
- **Architecture flag:** This epic introduces a new governance surface
  (`scripts/pages-deploy/`) and a new consumer-config schema. A dual-signed
  cross-review artifact under `raw/cross-review/` is required **at the Sprint 2 PR**
  per `STANDARDS.md` Society of Minds.
- **Specialist reviews recorded in the structured plan:** Opus planner (this role)
  and an infrastructure-delivery reviewer focused on Direct Upload pitfalls.

## Handoff

On gpt-5.4 acceptance, orchestrator opens the PR for this planning branch and, on
merge, fires implementation lanes for #469 / #470 / #471 / #472 in that order with
separate worktrees, separate lane claims, and separate execution scopes. No lane
fires until its predecessor's acceptance criteria are met.
