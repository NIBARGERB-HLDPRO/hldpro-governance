# Pages Deploy Gate Runbook

## Invocation

```bash
python3 scripts/pages-deploy/pages_deploy_gate.py --config <path> [--dry-run]
```

## Required Environment

- `CLOUDFLARE_API_TOKEN`: Cloudflare token with Cloudflare Pages: Edit plus account-level access.
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare account id for the Pages project.
- `PAGES_DEPLOY_APPROVED=1`: Required for non-dry-run deployment.

## Deploy Flow

The gate runs deployment in two phases:

1. `pre_deploy.command` runs first. Use this phase for dependent deploy work such as Supabase edge function deploys.
2. `wrangler pages deploy` uploads the built Pages artifact with CI and non-interactive flags.

## Config Schema

Consumer config must follow `docs/schemas/pages-deploy-consumer.schema.json`.
