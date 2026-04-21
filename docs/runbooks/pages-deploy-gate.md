# Pages Deploy Gate Runbook

## Invocation

Run from the consumer repository root:

```bash
python3 scripts/pages-deploy/pages_deploy_gate.py --config pages-deploy.config.json
```

Dry-run skips approval, build, Pages limit checks, and deploy:

```bash
python3 scripts/pages-deploy/pages_deploy_gate.py --config pages-deploy.config.json --dry-run
```

## Required Environment

- `CLOUDFLARE_API_TOKEN`: Cloudflare API token with Cloudflare Pages: Edit permission at the account level.
- `CLOUDFLARE_ACCOUNT_ID`: Cloudflare account id for the Pages project.
- `PAGES_DEPLOY_APPROVED=1`: Required for non-dry-run deploys.

Do not place secret values in the config file. Put only environment variable names in `required_env`.

## Two-Phase Deploy Order

1. Validate config and preflight local tooling, required environment, approval, and Wrangler version.
2. Run the optional `pre_deploy.command`, build the app, validate the artifact directory and Pages limits, then run `wrangler pages deploy`.

The gate fails closed before deploy if any preflight, hook, build, stale-artifact, or Pages limit check fails.

## Config Schema

Consumer config shape is defined in `docs/schemas/pages-deploy-consumer.schema.json`.
