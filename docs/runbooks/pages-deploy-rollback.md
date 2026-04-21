# Pages Deploy Rollback Runbook

List recent deployments:

```bash
wrangler pages deployments list --project-name <name>
```

Rollback a deployment:

```bash
wrangler pages deployments rollback <deployment-id> --project-name <name>
```

Cloudflare dashboard path: Workers & Pages -> Pages -> `<project-name>` -> Deployments.

Supabase function rollback is separate from Cloudflare Pages rollback and must be handled through the Supabase deployment path for the affected project.
