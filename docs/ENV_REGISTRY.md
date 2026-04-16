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

# Dry-run (print without writing)
DRY_RUN=1 bash ~/Developer/HLDPRO/hldpro-governance/scripts/bootstrap-repo-env.sh hp-staging
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

### Key naming convention in `.env.shared`

| Prefix | Project |
|---|---|
| `HP_STAGING_SUPABASE_*` | hp-staging |
| `HP_PROD_SUPABASE_*` | hp-production |
| `HLDPRO_STAGING_SUPABASE_*` | hldpro-staging |
| `AIS_SUPABASE_*` | ai-integration-services |
| `DK_SUPABASE_*` | apex-doorknocking |

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

### knocktracker

| Key in `.env.shared` | Repo-native name | Notes |
|---|---|---|
| `DK_SUPABASE_URL` | `SUPABASE_URL` + `VITE_SUPABASE_URL` | apex-doorknocking project |
| `DK_SUPABASE_ANON_KEY` | `SUPABASE_ANON_KEY` + `VITE_SUPABASE_ANON_KEY` | |
| `DK_SUPABASE_SERVICE_ROLE_KEY` | `SUPABASE_SERVICE_ROLE_KEY` | |

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
