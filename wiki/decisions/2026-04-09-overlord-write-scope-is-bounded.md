# Overlord Write Scope Is Bounded

Date: 2026-04-09

## Decision
Overlord agents stay read-only; controlled write-back happens in the closeout path and weekly sweep.

## Why
- Reduces accidental repo mutation
- Keeps knowledge writes attributable and reviewable
- Matches the solo-operator constraints in the implementation plan

## Links
- [Raw conversation seed](../../raw/conversations/2026-04-09-overlord-write-scope.md)
