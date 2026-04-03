# HLD Pro — Cross-Repo Dependencies

> Local manifest for overlord agents. Lists shared infrastructure across all repos.

## Shared Supabase Projects

| Project Ref | Repos | Environment | Risk Level |
|-------------|-------|-------------|------------|
| nrkrquddydupkemtixom | HealthcarePlatform, local-ai-machine | Staging/E2E | HIGH — migration in one repo can break the other |
| gyrtvzvazmvwiirnexls | ai-integration-services | Production | LOW — single repo |
| khyadxaiyfdldyuoapyn | ai-integration-services | Staging | LOW — single repo |

## Cross-Repo Edge Function Calls

| Source | Target | Functions Called | Notes |
|--------|--------|----------------|-------|
| local-ai-machine | HealthcarePlatform (nrkrquddydupkemtixom) | evidence/sign-upload, survey endpoints | E2E test pipelines |

## Dependency Rules
- Before merging a migration in HealthcarePlatform: check if local-ai-machine E2E tests still pass
- Before merging a migration in local-ai-machine: check if HealthcarePlatform staging is unaffected
- ai-integration-services is fully isolated — no cross-repo migration risk
