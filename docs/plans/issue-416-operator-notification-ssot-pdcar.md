# PDCAR: Issue #416 Operator Notification SSOT Propagation

Date: 2026-04-20
Branch: `issue-416-operator-notification-ssot-20260420`
Issue: [#416](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/416)
Parent: [#109](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/109)

## Plan

Treat `hldpro-governance/.env.shared` as the local vault and single source of truth for operator notification routing. Make the governance bootstrap safely propagate Remote MCP, Slack, Twilio, and operator SMS routing keys into the generated `local-ai-machine/.env` without executing vault values.

## Do

1. Replace shell sourcing of `.env.shared` with data-only parsing and shell-safe export quoting.
2. Extend the `lam` bootstrap target to emit Remote MCP, Cloudflare Access service-token metadata, operator inbound queue, Slack routing, Twilio provider, and operator SMS destination keys.
3. Document the local-ai-machine key mappings in the environment registry.
4. Add a static contract test that prevents reintroducing shell execution of `.env.shared` and verifies the key mappings.
5. Regenerate local-ai-machine `.env` only as an ignored local artifact after code validation.

## Check

- `scripts/bootstrap-repo-env.sh` must not execute `.env.shared` as shell.
- `DRY_RUN=1 bash scripts/bootstrap-repo-env.sh lam` must complete without the prior command-string execution error.
- Generated LAM env output must contain required key names without printing secret values in validation logs.
- `docs/ENV_REGISTRY.md` must document the propagated keys.
- Static contract, shell syntax, structured plan, execution scope, diff whitespace, and final local env presence checks must pass.
- Final AC: GitHub PR checks pass before closeout.

## Adjust

If Slack or SMS provider credentials are absent from `.env.shared`, keep emitting empty generated keys and report the missing source configuration separately. Do not commit local vault values or generated `.env` files.

## Review

Review must verify that the bootstrap treats the vault as data, optional LAM notification keys do not trigger unbound-variable failures, and all validation avoids printing PII, token values, JWTs, or HMAC material.
