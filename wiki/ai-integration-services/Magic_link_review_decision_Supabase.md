# Magic link review decision Supabase

> 29 nodes · cohesion 0.16

## Key Concepts

- **index.ts** (19 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **index.ts** (19 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/magic-link-review-decision/index.ts`
- **tryReadEnvSecret()** (13 connections) — `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- **intake-validator.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **intake-validator.ts** (11 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/_shared/intake-validator.ts`
- **responseJson()** (7 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **isObject()** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **validateAgainstSchema()** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **createTrialCoupon()** (6 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **sendDenySms()** (6 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **schemaMatches()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **sendReviewSms()** (5 connections) — `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- **isExpired()** (4 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **resolveTwilioFrom()** (4 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **reviewPhone()** (4 connections) — `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- **schemaMatchesType()** (4 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **mergeOperatorOverride()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **normalizePhone()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **payloadFromIntake()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **slugifyBusinessName()** (3 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- **addDetail()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **joinPath()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **schemaAnyOfMatches()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **validatePayload()** (3 connections) — `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- **buildLamPayload()** (2 connections) — `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- *... and 4 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/intake-validator.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/intake-validator.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- `ai-integration-services/backend/supabase/functions/magic-link-intake-submit/index.ts`
- `ai-integration-services/backend/supabase/functions/magic-link-review-decision/index.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/_shared/intake-validator.test.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/_shared/intake-validator.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/magic-link-review-decision/index.ts`

## Audit Trail

- EXTRACTED: 138 (84%)
- INFERRED: 27 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*