# Issue 62 PDCA/R — Neo4j Runtime Bootstrap

Date: 2026-04-09
Issue: [#62](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/62)
Owner: nibargerb

## Plan

- create a deterministic local Neo4j bootstrap path in governance
- validate that the runtime can start on this machine and answer a Cypher query
- reduce issue `#48` to the actual remaining gate after runtime exists

## Do

- added `scripts/knowledge_base/bootstrap_neo4j.sh`
- used Docker as the local runtime substrate because Docker is already installed and running on this machine
- kept the bootstrap self-contained so it does not depend on a host Neo4j install

## Check

Verification target:
- the bootstrap script starts or resumes a local Neo4j container
- the container accepts a `cypher-shell` query
- the script prints the local HTTP and Bolt endpoints needed for future graph push work

## Adjust

If runtime bootstrap succeeds, issue `#48` should no longer be blocked on missing local infrastructure and should be reclassified only against the remaining milestone gate.

If bootstrap fails, that failure mode becomes the governing blocker and must be captured before closing this issue.

## Review

This slice is complete only if the runtime exists on this machine and the local operator has a deterministic command path to bring it back without re-deriving the setup from scratch.
