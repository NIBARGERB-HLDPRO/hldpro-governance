# Pages Deploy Gate Runbook

## Invocation

```bash
python3 scripts/pages-deploy/pages_deploy_gate.py --config <path> [--dry-run]
```

## Required Environment

- `CLOUDFLARE_API_TOKEN`: Cloudflare token with Cloudflare Pages: Edit plus account-level access.
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare account id for the Pages project.
- `PAGES_DEPLOY_APPROVED=1`: Required for non-dry-run deployment.

Missing-secret diagnostics list variable names only. Provision Cloudflare Pages credentials through `hldpro-governance/.env.shared` plus bootstrap for local runs, or through GitHub Actions secrets for CI. Values are intentionally not accepted in prompts, copied into inline shell commands, or printed in logs. This runbook implements the Secret Provisioning UX contract from `docs/ENV_REGISTRY.md` and remains scoped to the Cloudflare Pages direct-upload deploy gate tracked by #467.

## Deploy Flow

The gate runs deployment in two phases:

1. `pre_deploy.command` runs first. Use this phase for dependent deploy work such as Supabase edge function deploys.
2. `wrangler pages deploy` uploads the built Pages artifact with `CI=true` in the child environment. The gate does not pass `--non-interactive`; Wrangler 4.x removed that flag and treats it as an unknown argument.

## Config Schema

Consumer config must follow `docs/schemas/pages-deploy-consumer.schema.json`.
