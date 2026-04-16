# Compendium Index -- hldpro-governance

> Quick-reference index for [COMPENDIUM.md](./COMPENDIUM.md)

---

## Document Sections

| Section | Location in COMPENDIUM.md | Description |
|---------|--------------------------|-------------|
| [Product Narrative & Gap Analysis](#part-1) | Part 1 | What the repo does, the 9-step governance loop, status of each step, and gap inventory |
| [Repo File Compendium](#part-2) | Part 2 | Every file with one-line description, organized by directory |
| [Architecture Summary](#part-3) | Part 3 | System components and technology |
| [Current Backlog](#part-4) | Part 4 | Active planned work from OVERLORD_BACKLOG.md |

---

## Governance Loop Steps (Narrative)

| # | Step | Status | Compendium Section |
|---|------|--------|--------------------|
| 1 | Standards Manifest | DONE | Part 1, Step 1 |
| 2 | Governed Repository Portfolio | DONE (2 repos have placeholder docs) | Part 1, Step 2 |
| 3 | Claude Agent System | DONE | Part 1, Step 3 |
| 4 | CI Enforcement | DONE (Codex auth fragile) | Part 1, Step 4 |
| 5 | Global Hooks | DONE | Part 1, Step 5 |
| 6 | Codex Integration | DONE (auth fragile in CI) | Part 1, Step 6 |
| 7 | Living Knowledge Base | Phases 1-5 DONE; 6-8 PLANNED | Part 1, Step 7 |
| 8 | GitHub Enterprise Config | Sprint 1 DONE; Sprints 2-4 PLANNED | Part 1, Step 8 |
| 9 | Effectiveness Metrics | DONE | Part 1, Step 9 |

---

## Top 9 Gaps

| # | Gap | Section |
|---|-----|---------|
| 1 | knocktracker + local-ai-machine not graphified | Part 1, Gap Table |
| 2 | Codex CLI CI auth fragility | Part 1, Gap Table |
| 3 | GitHub Enterprise Sprints 2-4 not started | Part 1, Gap Table |
| 4 | knocktracker/local-ai-machine placeholder docs | Part 1, Gap Table |
| 5 | No auto-remediation in agents | Part 1, Gap Table |
| 6 | Neo4j graph push (Phase 7) | Part 1, Gap Table |
| 7 | Nightly cleanup timezone policy | Part 1, Gap Table |
| 8 | No metrics trend analysis | Part 1, Gap Table |
| 9 | Qwen3-32B fine-tune (Phase 8) | Part 1, Gap Table |

---

## File Directory Index

| Directory | File Count | Compendium Table |
|-----------|-----------|------------------|
| Root files | 6 | Root Files |
| GitHub Enterprise docs | 5 | GitHub Enterprise Documents |
| `agents/` | 4 | Agents |
| `hooks/` | 2 | Hooks |
| `.github/workflows/` | 4 | CI Workflows |
| `scripts/` | 6 | Scripts |
| `metrics/` | 5 | Metrics |
| `docs/` | 2 | Documentation |
| `docs/plans/` | 11 | Plans |
| `raw/` | 12 | Raw Feeds |
| `wiki/` | 619 | Wiki (auto-generated + curated) |
| `graphify-out/` | varies | Generated Artifacts |

---

## Key Files by Role

### If you want to understand...

| Topic | Start here |
|-------|-----------|
| What this repo does | `README.md` |
| What standards are enforced | `STANDARDS.md` |
| What work is planned | `OVERLORD_BACKLOG.md` |
| Cross-repo dependencies | `DEPENDENCIES.md` |
| Agent behavior | `agents/overlord.md`, `agents/overlord-sweep.md` |
| How CI governance works | `.github/workflows/governance-check.yml` |
| How Codex reviews work | `scripts/overlord/codex_ingestion.py`, `scripts/overlord/README.md` |
| How the knowledge base works | `docs/plans/living-knowledge-base-implementation-plan.md`, `wiki/index.md` |
| GitHub Enterprise roadmap | `GITHUB_ENTERPRISE_ADOPTION_PLAN.md` |
| Past errors and resolutions | `docs/FAIL_FAST_LOG.md` |
| Feature inventory | `docs/FEATURE_REGISTRY.md` |
| Effectiveness metrics | `metrics/effectiveness-baseline/latest.md` |
| Architectural decisions | `wiki/decisions/` |
| Branch safety mechanism | `hooks/branch-switch-guard.sh` |
| Closeout process | `hooks/closeout-hook.sh`, `raw/closeouts/TEMPLATE.md` |

---

## Governed Repos Quick Reference

| Repo | Governance Tier | Security Tier | Graphified? |
|------|-----------------|---------------|-------------|
| ai-integration-services | Full | Full + PentAGI | Yes (1883 nodes) |
| HealthcarePlatform | Full + HIPAA | Full + PentAGI + HIPAA | Yes (1549 nodes) |
| local-ai-machine | Full | Baseline | No (Phase 6) |
| knocktracker | Standard | Baseline | No (Phase 6) |
| ASC-Evaluator | Exempt | Exempt | Yes (pointer pattern) |
