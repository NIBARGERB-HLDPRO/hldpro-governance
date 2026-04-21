# HLDPRO — Environment Variable Registry

**Version:** 2026-04-16
**Owner:** Operator (nibarger.ben@gmail.com)
**SSOT file:** `hldpro-governance/.env.shared` (gitignored — never commit)
**Bootstrap:** `bash scripts/bootstrap-repo-env.sh <repo> [target-path]`

All operator credentials live in `.env.shared`. Repo-local `.env.local` files are **generated artifacts** — never edited by hand. Re-run bootstrap to refresh.

---

## Quick Start

```bash
# Seed HP staging backend (main tree or before running apply-option3-hosted.mjs)
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh hp-staging

# Seed an HP worktree
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh hp-worktree \
  ~/Developer/HLDPRO/HealthcarePlatform/.claude/worktrees/<slug>/backend/.env.local

# Dry-run (redacted preview without writing)
DRY_RUN=1 bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh hp-staging

# Seed Seek and Ponder staging/local env
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh seek
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh seek-local

# Seed Stampede market-data env
bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh stampede
```

---

## Supabase Project Map

| Logical Name | Project Ref | URL | Used By |
|---|---|---|---|
| hp-staging | `nrkrquddydupkemtixom` | `https://nrkrquddydupkemtixom.supabase.co` | HealthcarePlatform (staging) |
| hp-production | `arvqikuzplxuqnkbxodh` | `https://arvqikuzplxuqnkbxodh.supabase.co` | HealthcarePlatform (prod) |
| hldpro-staging | `khyadxaiyfdldyuoapyn` | `https://khyadxaiyfdldyuoapyn.supabase.co` | Cross-repo staging / AIS staging ref |
| ai-integration-services | `gyrtvzvazmvwiirnexls` | `https://gyrtvzvazmvwiirnexls.supabase.co` | ai-integration-services |
| apex-doorknocking | `kfcqyijmuuafflpjepwr` | `https://kfcqyijmuuafflpjepwr.supabase.co` | knocktracker |
| seek-and-ponder | `ajeyrcllfxwneozmywhg` | `https://ajeyrcllfxwneozmywhg.supabase.co` | Seek and Ponder (staging) |

### Key naming convention in `.env.shared`

| Prefix | Project |
|---|---|
| `HP_STAGING_SUPABASE_*` | hp-staging |
| `HP_PROD_SUPABASE_*` | hp-production |
| `HLDPRO_STAGING_SUPABASE_*` | hldpro-staging |
| `AIS_SUPABASE_*` | ai-integration-services |
| `DK_SUPABASE_*` | apex-doorknocking |
| `SEEK_STAGING_SUPABASE_*` | seek-and-ponder staging |
| `SEEK_LOCAL_SUPABASE_*` | seek-and-ponder local dev |

---

## Key → Repo Mapping

### Cross-repo (all repos receive these)

| Key in `.env.shared` | Repo-native name | Description |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code CLI auth (operator Max sub) |
| `ANTHROPIC_API_KEY` | `ANTHROPIC_API_KEY` | Anthropic Messages API |
| `OPENAI_API_KEY` | `OPENAI_LOCAL_AI_MACHINE` | OpenAI project key |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub PAT (repo+workflow+admin:org) |
| `GOVERNANCE_GITHUB_TOKEN` | `GOVERNANCE_GITHUB_TOKEN` | Same token, governance-scoped alias |
| `SUPABASE_ACCESS_TOKEN` | `SUPABASE_ACCESS_TOKEN` | Supabase management API (personal) |

### HealthcarePlatform (hp-staging target)

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `HP_STAGING_SUPABASE_URL` | `SUPABASE_URL` + `VITE_SUPABASE_URL` | Backend + frontend |
| `HP_STAGING_SUPABASE_ANON_KEY` | `SUPABASE_ANON_KEY` + `VITE_SUPABASE_ANON_KEY` | |
| `HP_STAGING_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_ROLE_KEY` | Backend test scripts only |
| `HP_STAGING_SUPABASE_PUBLISHABLE_KEY` | — | Modern key format; use in new code |
| `ELEVENLABS_API_KEY` | `ELEVENLABS_API_KEY` | Training media voiceover |
| `STRIPE_SECRET_KEY` | `STRIPE_SECRET_KEY` | Billing |
| `RESEND_API_KEY` | `RESEND_API_KEY` | Email |
| `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` | same | SMS/voice |

### ai-integration-services

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `AIS_SUPABASE_URL` | `SUPABASE_URL` + `VITE_SUPABASE_URL` | |
| `AIS_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_ROLE_KEY` | |
| `AIS_SUPABASE_DB_PASSWORD` | `SUPABASE_DB_PASSWORD` | |
| `HLDPRO_STAGING_SUPABASE_URL` | `STAGING_SUPABASE_URL` | Cross-env staging ref |
| `N8N_*` | `N8N_*` | All n8n vars |
| `CALCOM_*` | `CALCOM_*` | All Cal.com vars |
| `TWILIO_*` | `TWILIO_*` | All Twilio vars |
| `STRIPE_*` | `STRIPE_*` | All Stripe vars + price IDs |
| `CLOUDFLARE_*` | `CLOUDFLARE_*` | AIS-scoped tokens |
| `VERCEL_*` | `VERCEL_*` | |

### local-ai-machine

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `CLOUDFLARE_MASTER_OPS_TOKEN` | `CLOUDFLARE_MASTER_OPS_TOKEN` | Tunnel + Access management |
| `CLOUDFLARE_ACCOUNT_ID` | `CLOUDFLARE_ACCOUNT_ID` | |
| `CLOUDFLARE_ZONE_ID` | `CLOUDFLARE_ZONE_ID` | |
| `CLOUDFLARE_TUNNEL_ID` | `CLOUDFLARE_TUNNEL_ID` | |
| `CF_TEAM_DOMAIN` | `CF_TEAM_DOMAIN` | JWT validation |
| `CF_ACCESS_AUD_TAG` | `CF_ACCESS_AUD_TAG` | JWT validation |
| `SOM_MCP_URL` | `SOM_MCP_URL` | Remote MCP Cloudflare endpoint |
| `SOM_MCP_TOKEN` / `SOM_REMOTE_MCP_JWT` | same | Signed inner JWT for the Remote MCP Stage B/C bridge |
| `SOM_MCP_PROTOCOL` / `SOM_MCP_CALL_PATH` | same | Bridge protocol selector and call path for live Remote MCP |
| `SOM_MCP_USER_AGENT` | `SOM_MCP_USER_AGENT` | Stable operator client user-agent for Cloudflare edge policy compatibility |
| `SOM_REMOTE_MCP_AUTH_HMAC_KEY` | `SOM_REMOTE_MCP_AUTH_HMAC_KEY` | Local bridge JWT verification key |
| `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` | `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` | Remote MCP audit HMAC key |
| `SOM_REMOTE_MCP_AUDIENCE` / `SOM_REMOTE_MCP_ROTATION_VERSION` | same | Inner JWT audience and rotation marker |
| `CF_ACCESS_CLIENT_ID` / `CF_ACCESS_CLIENT_SECRET` | same | Cloudflare Access service-token client credentials |
| `CF_ACCESS_SERVICE_TOKEN_ID` / `CF_ACCESS_SERVICE_TOKEN_NAME` | same | Service-token inventory metadata; not a substitute for the secret |
| `SOM_OPERATOR_INBOUND_QUEUE_ROOT` / `SOM_OPERATOR_INBOUND_SESSION_ID` | same | HITL relay receive preflight queue root and target session id |
| `SLACK_BOT_USER_OAUTH_TOKEN` / `SLACK_CODEX_CHANNEL_ID` / `SLACK_CHANNEL_ID` / `SLACK_E2E_CHANNEL_ID` | same | Operator notification and HITL Slack routing for local-ai-machine tooling |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_API_SID` / `TWILIO_SECONDARY_AUTH_TOKEN` | same | SMS fallback provider credentials for operator notification routing |
| `SOM_TWILIO_FROM_NUMBER` | `SOM_TWILIO_FROM_NUMBER` | Dedicated SoM HITL SMS sender for local-ai-machine approval/reply routing; do not reuse the AIS/Alex or customer-demo sender as the production approval route |
| `TWILIO_FROM_NUMBER` / `TWILIO_SMS_FROM` | same | Generic Twilio sender aliases for compatibility and diagnostics; production SoM HITL approval routing must prefer `SOM_TWILIO_FROM_NUMBER` |
| `TWILIO_TEST_CONSUMER_NUMBER` / `OPERATOR_SMS_PHONE` / `SOM_OPERATOR_SMS_PHONE` | same | Operator SMS destination values for tests and SoM/HITL notification routing |

### knocktracker

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `DK_SUPABASE_URL` | `SUPABASE_URL` + `VITE_SUPABASE_URL` | apex-doorknocking project |
| `DK_SUPABASE_ANON_KEY` | `SUPABASE_ANON_KEY` + `VITE_SUPABASE_ANON_KEY` | |
| `DK_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_ROLE_KEY` | |

### seek-and-ponder

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `SEEK_STAGING_SUPABASE_URL` | `SUPABASE_URL` + `SEEK_STAGING_SUPABASE_URL` | Default `seek` target writes staging as the active Supabase project |
| `SEEK_STAGING_SUPABASE_ANON_KEY` | `SUPABASE_ANON_KEY` + `SEEK_STAGING_SUPABASE_ANON_KEY` | Browser/client staging anon key |
| `SEEK_STAGING_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_ROLE_KEY` + `SEEK_STAGING_SUPABASE_SERVICE_ROLE_KEY` | Server-side staging writes and e2e seeding only |
| `SEEK_STAGING_SUPABASE_PROJECT_REF` | same | Supabase deploy target ref |
| `SEEK_LOCAL_SUPABASE_URL` / `SEEK_LOCAL_SUPABASE_ANON_KEY` / `SEEK_LOCAL_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_*` via `seek-local` | Local Supabase target for repo-local dev and tests |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | same | Hosted embedding and LLM providers |
| `SUPABASE_ACCESS_TOKEN` | same | Supabase management/deploy CLI |
| `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` | same | Billing integration |
| `RESEND_API_KEY` | same | Email delivery |
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` | same | Google SSO |

### Stampede

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` | same | Brokerage/market data integration |
| `ALPHA_VANTAGE_API_KEY` | same | Market data fallback |
| `POLYGON_API_KEY` | same | Generated from `POLYGON_API_KEY` when present, otherwise `MASSIVE_API_KEY` compatibility value |
| `MASSIVE_API_KEY` | same | Massive market-data API key |
| `MASSIVE_FLATFILES_BASE_URL` / `MASSIVE_FLATFILES_BUCKET` | same | Massive flatfiles endpoint and bucket |
| `MASSIVE_FLATFILES_ACCESS_KEY_ID` / `MASSIVE_FLATFILES_SECRET_ACCESS_KEY` | same | Massive flatfiles object-store credentials |
| `INTRINIO_API_KEY` | same | Optional market-data provider key; generated blank when absent from SSOT |
| `TRADIER_PRODUCTION_API_TOKEN` | `TRADIER_API_TOKEN` | Stampede default is production per repo `.env.example`; sandbox key remains in `TRADIER_API_TOKEN` for sandbox callers |
| `TRADIER_ACCOUNT_ID` / `TRADIER_PRODUCTION_BASE_URL` / `TRADIER_PRODUCTION_ENV` | `TRADIER_ACCOUNT_ID` / `TRADIER_BASE_URL` / `TRADIER_ENV` | Tradier account, production endpoint, and environment selector |
| `X_BEARER_TOKEN` | same | Optional X/Twitter bearer token; generated blank when absent from SSOT |

---

## Rotation Procedures

| Service | Cadence | Steps |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Annual (expires 2027-04-09) | `claude setup-token` → update `.env.shared` → run bootstrap for all repos |
| `ANTHROPIC_API_KEY` | As needed | Anthropic Console → API Keys → Rotate → update `.env.shared` |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Annual or on scope change | github.com/settings/tokens → update `.env.shared` |
| `SUPABASE_ACCESS_TOKEN` | Annual | Supabase Dashboard → Account → Access Tokens → update `.env.shared` |
| Supabase JWT keys | At project re-creation | Via management API or dashboard → update `.env.shared` |
| Stripe keys | On compromise | Stripe Dashboard → Developers → API Keys → update `.env.shared` |
| Twilio tokens | On compromise | Twilio Console → update `.env.shared` |
| Cloudflare tokens | Annual or on scope change | Cloudflare Dashboard → My Profile → API Tokens → update `.env.shared` |
| Remote MCP operator keys | On bridge rotation, Cloudflare service-token rotation, or suspected exposure | Generate a new `SOM_REMOTE_MCP_AUTH_HMAC_KEY`, mint a matching `SOM_REMOTE_MCP_JWT`, set `SOM_MCP_TOKEN` to that JWT, create/attach a new Cloudflare Access service token, reload `com.hldpro.remote-mcp-bridge`, run live preflights, then remove the old Access token |

After any rotation in `.env.shared`, re-run bootstrap for affected repos:
```bash
bash scripts/bootstrap-repo-env.sh <repo>
```

---

## TODOs (known gaps)

| Item | Priority |
|---|---|
| `HP_STAGING_SUPABASE_DB_PASSWORD` | Done — reset via management API 2026-04-16 |
| `HP_PROD_SUPABASE_DB_PASSWORD` | Done — reset via management API 2026-04-16 |
| knocktracker `.gitignore` — confirm `.env.local` is gitignored | Medium |
| Automate worktree bootstrap on `WorktreeCreate` hook | Done — `HealthcarePlatform/.claude/hooks/worktree-env-bootstrap.sh` wired to `WorktreeCreate` event 2026-04-16 |

---

## History

| Date | Change |
|---|---|
| 2026-04-16 | Initial registry created. `.env.shared` SSOT established. Bootstrap script written. Consolidates credentials previously scattered across AIS `.env`, LAM `.env`, and HP `frontend/.env.staging`. |
