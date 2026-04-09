# Graphify Governance Improvements PDCA/R

Date: 2026-04-09
Issue: `TBD before implementation; create or reopen the execution issue before claiming this slice complete`
Scope: `hldpro-governance` only
Branch: `feat/graphify-pdcar`

## Contract

- source of truth for the org repo registry: `README.md` `## Governed Repositories`
- source of truth for executable graph refresh targets in this system: a governance-tracked manifest file created in the implementation slice and consumed by the workflow, closeout hook, and contract tests
- product repos are out of scope for this slice; no product-repo pointer/hook edits are required here
- primary artifact layout for governed repo graphs: `graphify-out/<repo>/` and `wiki/<repo>/`
- root `graphify-out/` role after this slice: org-level aggregate or explicit compatibility-pointer surface only, never the primary home for a single governed repo
- when runtime/docs disagree, the runtime contract wins first:
  - builder + workflow + hook behavior
  - then governance docs are updated to match that enforced contract

## Plan

- re-baseline the governance-hosted graphify operating model against the implementation that actually exists today
- remove AIS-only assumptions from the weekly/slice update path so approved governed repos can be refreshed consistently under `graphify-out/<repo>/` and `wiki/<repo>/`
- eliminate the current root-vs-repo-scoped output ambiguity so AIS does not exist as two competing graph sources inside governance
- close the current drift between issue/backlog/wiki/index/feature-registry claims and the graph coverage that is actually present on disk
- remove machine-specific path leakage from canonical graph/wiki artifacts so outputs stay portable and reviewable
- define artifact and verification expectations for graphify updates so governance can prove usefulness and correctness instead of assuming them

## Do

- inventory the current graphify runtime path in governance:
  - `scripts/knowledge_base/build_graph.py`
  - `.github/workflows/overlord-sweep.yml`
  - `hooks/closeout-hook.sh`
  - `wiki/index.md`
  - `OVERLORD_BACKLOG.md`
  - `docs/FEATURE_REGISTRY.md`
- normalize graph storage shape so governance uses explicit per-repo destinations for governed repo graphs and wiki output, instead of mixing root `graphify-out/` usage with per-repo subfolders
- create a machine-checkable governance manifest for graph refresh targets, including at minimum:
  - repo slug
  - local checkout path used by automation
  - output path under `graphify-out/`
  - wiki path under `wiki/`
  - enabled/disabled status for scheduled refresh
- migrate current AIS root artifacts so they become either:
  - org-level aggregate outputs, or
  - explicit compatibility pointers during the migration window,
  but not a second competing primary AIS graph home
- update the weekly graph refresh path to iterate through the manifest-defined target list and stage the full affected artifact set, including:
  - `GRAPH_REPORT.md`
  - `graph.json`
  - `community-labels.json`
  - `.graphify_summary.json`
  - generated wiki changes
- align the closeout hook with the same governance-hosted multi-repo model so Stage 6 does not silently rebuild AIS-only output when the knowledge base is meant to cover multiple governed repos
- add a post-build normalization/validation layer for governance graph artifacts so updates can detect or reject:
  - absolute machine/worktree path leakage
  - generic `Community N` labels above an accepted threshold
  - missing summary artifacts
  - mismatched output roots
- reconcile governance status mirrors with actual tracked issue state so `OVERLORD_BACKLOG.md`, phase PDCA/R docs, and the knowledge index do not claim mutually incompatible graphify status
- refresh governance documentation to match the real state of graph coverage and the real runtime path:
  - `wiki/index.md`
  - `OVERLORD_BACKLOG.md`
  - `docs/FEATURE_REGISTRY.md`
  - graphify methodology/phase notes as needed
- add bounded enforcement for the graphify governance path, limited in this slice to:
  - governance-side contract tests
  - builder/workflow/hook assertions needed to keep the layout and artifact contract stable
  and not broader product-repo policy changes
- add lightweight contract coverage for the graphify governance path so future changes cannot silently reintroduce:
  - AIS-only assumptions
  - incomplete artifact staging
  - stale coverage claims

## Check

- the weekly sweep can describe exactly which governed repos are graphified and which are not, with that answer matching `graphify-out/` and `wiki/` on disk
- workflow, closeout hook, and contract tests all read the same manifest-defined graph refresh target set
- graph refresh logic writes only to governance-hosted locations and never requires tracked `graphify-out/` output in product repos
- generated summaries/wiki output no longer embed stale absolute worktree paths as canonical references
- a graph update stages the full artifact set required to understand and review the change, not just a partial report/json pair
- `wiki/index.md`, `OVERLORD_BACKLOG.md`, and `docs/FEATURE_REGISTRY.md` no longer disagree about graphify coverage or next-phase status
- issue-backed roadmap state matches actual GitHub issue state for graphify phases and follow-on work
- the closeout-triggered graph refresh path matches the same storage/runtime assumptions as the weekly sweep path
- AIS no longer has two competing graph homes inside governance without an explicit documented reason
- merge gates for the implementation slice are explicit and reproducible:
  - `python3 scripts/knowledge_base/build_graph.py --source <repo> --output graphify-out/<repo> --wiki-dir wiki/<repo> --no-html` succeeds for the repo(s) selected in the slice
  - contract tests for graphify governance pass, covering:
    - manifest-defined graph target usage
    - workflow/hook layout consistency
    - artifact staging completeness
    - doc/runtime consistency for graph coverage claims
  - `git show HEAD:<path>` succeeds for each required created/updated governance artifact
  - no tracked product-repo `graphify-out/` artifacts are introduced as part of the slice

## Adjust

- if full multi-repo weekly refresh is too heavy for one slice, land the governance manifest + contract enforcement first, then add remaining repo refresh lanes as explicit issue-backed follow-up work
- if generated wiki/graph output is too noisy, tighten repo selection and artifact acceptance rules before changing labeling heuristics again
- if root `graphify-out/` must remain for org-level aggregate output, document that role explicitly, keep it non-primary for per-repo graphs, and issue-back any remaining migration work before closure
- if coverage claims cannot be made truthful immediately because repo graphs do not yet exist, downgrade docs/backlog status instead of overstating completion
- if label-quality validation cannot be given a numeric threshold in the implementation slice, drop it from the merge gate and keep that work issue-backed rather than enforcing a subjective rule

## Review

- graphify should remain governance-hosted architecture memory, not become an ambiguous mix of per-repo local outputs and governance copies
- the next increment should optimize for operator trust:
  - accurate coverage claims
  - predictable artifact locations
  - reproducible update paths
  - reviewable graph/wiki diffs
- retrieval-quality experiments and token-impact measurement remain adjacent but separate concerns; they should build on a stable governance refresh contract rather than substitute for one
