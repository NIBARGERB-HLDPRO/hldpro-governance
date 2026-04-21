# Pages Deploy Rollback Runbook

## List Deployments

```bash
wrangler pages deployments list --project-name <name>
```

## Roll Back

```bash
wrangler pages deployments rollback <deployment-id> --project-name <name>
```

## Dashboard

In the Cloudflare dashboard, open Pages → project → Deployments tab.

Supabase edge function rollback is separate. Use the Supabase dashboard or `supabase functions deploy --version`.
