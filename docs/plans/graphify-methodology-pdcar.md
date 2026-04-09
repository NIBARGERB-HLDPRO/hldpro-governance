# Graphify Methodology PDCA/R

Date: 2026-04-09
Owner: Governance
Scope: Living Knowledge Base operating model

## Plan

- Make graphify the canonical architecture-memory layer for governed repos.
- Keep graphify outputs in `hldpro-governance` only.
- Add lightweight enforcement so product repos cannot accidentally become graph storage locations.
- Improve community labels so graph output is readable by operators without manual interpretation.
- Keep Obsidian optional as a local reading surface, not the source of truth.

## Do

- Added a shared governance gate that blocks `graphify-out/` changes in product repos.
- Extended the governance graph builder to infer human-readable community labels from dominant paths and symbols.
- Added a machine-readable `community-labels.json` artifact alongside each graph build.
- Documented the operator rule that governance `wiki/` and `graphify-out/` replace ad hoc architecture-memory search.

## Check

- Product repos still keep only pointer/hook changes.
- Governance remains the only tracked home for graph artifacts.
- Community labels now describe likely domains like route helpers, chart audit, admin workspace, or schema tooling instead of raw `Community N`.
- Obsidian is not required for the system to function.

## Adjust

- If a label is still too generic, improve the post-processor heuristics rather than introducing a second source of truth.
- If operators want richer browsing, generate an Obsidian-friendly mirror from governance `wiki/`, but keep governance Git as canonical.
- If a repo needs stronger adoption, add startup/read-order guidance before adding heavier hard gates.

## Review

- graphify/wiki is now the first-pass map for architecture and topology questions.
- `rg`/local code reads remain the exact implementation truth.
- Customer-facing RAG remains a separate product concern and should not be conflated with governance-hosted graphify memory.
