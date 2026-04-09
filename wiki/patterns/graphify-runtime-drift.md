# Graphify Runtime Drift

## Pattern
The source plan can drift from the real upstream graphify runtime in three ways:
- package install succeeds only on Python 3.10+
- git-hook install assumes `.git` is a directory, which breaks in worktrees
- non-interactive repo automation cannot call `graphify . --update` directly because the installed CLI exposes install/query/hook surfaces, not the interactive `/graphify` build flow

## Impact
Bootstrap work appears complete in docs while the actual update loop fails at runtime.

## Current Control
- use Python 3.11 for local install
- install git hooks in the common repo root, not a worktree gitfile path
- run repo-local builder logic from `scripts/knowledge_base/build_graph.py` for hooks and CI

## Links
- [AIS graph report](../../graphify-out/GRAPH_REPORT.md)
