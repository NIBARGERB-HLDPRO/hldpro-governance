# Magic link jwt Supabase

> 45 nodes · cohesion 0.07

## Key Concepts

- **index.ts** (19 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **magic-link-jwt.ts** (19 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **tryReadEnvSecret()** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- **intake-validator.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **index.ts** (7 connections) — `ai-integration-services/backend/supabase/functions/magic-link-session-fetch/index.ts`
- **isObject()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **validateAgainstSchema()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **generateEmbedding()** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/embeddings.ts`
- **createTrialCoupon()** (5 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **sendDenySms()** (5 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **schemaMatches()** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **responseJson()** (4 connections) — `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- **sendReviewSms()** (4 connections) — `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- **signMagicLink()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **verifyMagicLink()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **resolveTwilioFrom()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **reviewPhone()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- **schemaMatchesType()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **base64UrlDecodeToBytes()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **base64UrlDecodeToString()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **base64UrlEncode()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **base64UrlEncodeString()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **hmacSha256()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- **hashEmbedding()** (2 connections) — `ai-integration-services/backend/supabase/functions/_shared/embeddings.ts`
- **generateEmbeddings()** (2 connections) — `ai-integration-services/backend/supabase/functions/brain-ingest/index.ts`
- *... and 20 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/embeddings.ts`
- `ai-integration-services/backend/supabase/functions/_shared/intake-validator.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- `ai-integration-services/backend/supabase/functions/_shared/magic-link-jwt.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- `ai-integration-services/backend/supabase/functions/brain-ingest/index.ts`
- `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- `ai-integration-services/backend/supabase/functions/magic-link-session-fetch/index.ts`

## Audit Trail

- EXTRACTED: 142 (82%)
- INFERRED: 31 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*