# Urim query Supabase

> 56 nodes · cohesion 0.06

## Key Concepts

- **auth.ts** (18 connections) — `seek-and-ponder/backend/supabase/functions/_shared/auth.ts`
- **index.ts** (15 connections) — `seek-and-ponder/backend/supabase/functions/urim-query/index.ts`
- **error-handler.ts** (14 connections) — `seek-and-ponder/backend/supabase/functions/_shared/error-handler.ts`
- **cors.ts** (13 connections) — `seek-and-ponder/backend/supabase/functions/_shared/cors.ts`
- **getSupabaseServiceClient()** (12 connections) — `seek-and-ponder/backend/supabase/functions/_shared/auth.ts`
- **rate-limiter.ts** (8 connections) — `seek-and-ponder/backend/supabase/functions/_shared/rate-limiter.ts`
- **getCorsHeaders()** (6 connections) — `seek-and-ponder/backend/supabase/functions/_shared/cors.ts`
- **vault.ts** (6 connections) — `seek-and-ponder/backend/supabase/functions/_shared/vault.ts`
- **index.ts** (5 connections) — `seek-and-ponder/backend/supabase/functions/checkout-session/index.ts`
- **index.ts** (5 connections) — `seek-and-ponder/backend/supabase/functions/corpus-search/index.ts`
- **detectScriptureChapterRefs()** (5 connections) — `seek-and-ponder/backend/supabase/functions/urim-query/index.ts`
- **isAllowedOrigin()** (4 connections) — `seek-and-ponder/backend/supabase/functions/_shared/cors.ts`
- **safeHeaders()** (4 connections) — `seek-and-ponder/backend/supabase/functions/_shared/error-handler.ts`
- **index.ts** (4 connections) — `seek-and-ponder/backend/supabase/functions/billing-portal/index.ts`
- **index.ts** (4 connections) — `seek-and-ponder/backend/supabase/functions/ingest-document/index.ts`
- **crypto.ts** (4 connections) — `seek-and-ponder/backend/supabase/functions/_shared/crypto.ts`
- **index.ts** (4 connections) — `seek-and-ponder/backend/supabase/functions/stripe-webhook/index.ts`
- **getSecurityHeaders()** (3 connections) — `seek-and-ponder/backend/supabase/functions/_shared/cors.ts`
- **safeErrorResponse()** (3 connections) — `seek-and-ponder/backend/supabase/functions/_shared/error-handler.ts`
- **sanitizeError()** (3 connections) — `seek-and-ponder/backend/supabase/functions/_shared/error-handler.ts`
- **audit.ts** (3 connections) — `seek-and-ponder/backend/supabase/functions/_shared/audit.ts`
- **input-validator.ts** (3 connections) — `seek-and-ponder/backend/supabase/functions/_shared/input-validator.ts`
- **bookAliases()** (3 connections) — `seek-and-ponder/backend/supabase/functions/urim-query/index.ts`
- **normalizeRefText()** (3 connections) — `seek-and-ponder/backend/supabase/functions/urim-query/index.ts`
- **emitAuditLog()** (2 connections) — `seek-and-ponder/backend/supabase/functions/_shared/audit.ts`
- *... and 31 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `seek-and-ponder/backend/supabase/functions/_shared/audit.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/auth.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/config.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/cors.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/crypto.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/error-handler.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/input-validator.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/notify.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/rate-limiter.ts`
- `seek-and-ponder/backend/supabase/functions/_shared/vault.ts`
- `seek-and-ponder/backend/supabase/functions/billing-portal/index.ts`
- `seek-and-ponder/backend/supabase/functions/checkout-session/index.ts`
- `seek-and-ponder/backend/supabase/functions/corpus-search/index.ts`
- `seek-and-ponder/backend/supabase/functions/ingest-document/index.ts`
- `seek-and-ponder/backend/supabase/functions/send-study-reminder/index.ts`
- `seek-and-ponder/backend/supabase/functions/stripe-webhook/index.ts`
- `seek-and-ponder/backend/supabase/functions/update-interest-graph/index.ts`
- `seek-and-ponder/backend/supabase/functions/urim-query/index.ts`

## Audit Trail

- EXTRACTED: 182 (89%)
- INFERRED: 23 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*