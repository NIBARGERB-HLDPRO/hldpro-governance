# Cross-Review — Issue #530 Pages Deploy Wrangler Flag

## Scope Review

The issue is a narrow compatibility fix. Wrangler 4.x rejects `--non-interactive` for `wrangler pages deploy`, and the gate already sets `CI=true` in the child process environment.

## Findings

- The deploy command can drop `--non-interactive` without changing required env checks, build flow, approval gating, pre-deploy hooks, or evidence emission.
- The focused test should assert `--non-interactive` is absent and `CI=true` remains present.
- Runbook and GOV-029 wording must stop claiming the removed flag is used.

## Decision

Accepted. No alternate model review is required for this one-flag compatibility fix because it does not change architecture, policy, or downstream repo behavior.
