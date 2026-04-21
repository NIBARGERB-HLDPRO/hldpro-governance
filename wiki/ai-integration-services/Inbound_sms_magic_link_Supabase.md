# Inbound sms magic link Supabase

> 36 nodes · cohesion 0.09

## Key Concepts

- **index.ts** (15 connections) — `ai-integration-services/backend/supabase/functions/inbound-sms-magic-link/index.ts`
- **oauth-state.ts** (9 connections) — `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- **crypto.ts** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- **twiml-response.ts** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/twiml-response.ts`
- **index.ts** (6 connections) — `ai-integration-services/backend/supabase/functions/sms-inbound/index.ts`
- **twilio-signature.ts** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/twilio-signature.ts`
- **verifyOAuthState()** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- **twimlMessage()** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/twiml-response.ts`
- **hmacSha256()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- **timingSafeEqual()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- **ops-command-parser.ts** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/ops-command-parser.ts`
- **verifyWebhookSignature()** (4 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **signOAuthState()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- **verifyTwilioSignature()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/twilio-signature.ts`
- **twimlEmptyResponse()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/twiml-response.ts`
- **twimlResponse()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/twiml-response.ts`
- **magic-link.test.ts** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/magic-link.test.ts`
- **buildMagicLinkTwiml()** (3 connections) — `ai-integration-services/backend/supabase/functions/inbound-sms-magic-link/index.ts`
- **getSigningSecret()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- **parseOpsCommand()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/ops-command-parser.ts`
- **reconstructCanonicalUrl()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/twilio-signature.ts`
- **hmacSha1()** (2 connections) — `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- **disambiguateTwiml()** (2 connections) — `ai-integration-services/backend/supabase/functions/inbound-sms-magic-link/index.ts`
- **emptyTwiml()** (2 connections) — `ai-integration-services/backend/supabase/functions/inbound-sms-magic-link/index.ts`
- **escapeXml()** (2 connections) — `ai-integration-services/backend/supabase/functions/sms-inbound/index.ts`
- *... and 11 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- `ai-integration-services/backend/supabase/functions/_shared/magic-link.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- `ai-integration-services/backend/supabase/functions/_shared/ops-command-parser.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/ops-command-parser.ts`
- `ai-integration-services/backend/supabase/functions/_shared/twilio-signature.ts`
- `ai-integration-services/backend/supabase/functions/_shared/twiml-response.ts`
- `ai-integration-services/backend/supabase/functions/inbound-sms-magic-link/index.ts`
- `ai-integration-services/backend/supabase/functions/sms-inbound/index.ts`
- `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`

## Audit Trail

- EXTRACTED: 108 (81%)
- INFERRED: 26 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*