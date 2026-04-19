# Graph Report - seek-and-ponder  (2026-04-18)

## Corpus Check
- Large corpus: 2941 files · ~2,227,663 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 180 nodes · 235 edges · 27 communities detected
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `routeLLM()` - 5 edges
2. `ingestJST()` - 5 edges
3. `WRAPPER()` - 4 edges
4. `BUTTON()` - 4 edges
5. `getCorsHeaders()` - 4 edges
6. `emitCOGS()` - 4 edges
7. `ingestLOF()` - 4 edges
8. `logToCorpus()` - 3 edges
9. `sanitizeError()` - 3 edges
10. `safeErrorResponse()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Mobile Auth Web"
Cohesion: 0.08
Nodes (2): getSupabaseClient(), resolveAuthContext()

### Community 1 - "Mobile Db Models"
Cohesion: 0.12
Nodes (8): Book, Collection, CollectionVerse, Highlight, handleCreate(), load(), Note, Verse

### Community 2 - "Web Highlights Reader"
Cohesion: 0.14
Nodes (0): 

### Community 3 - "Web Collections"
Cohesion: 0.17
Nodes (0): 

### Community 4 - "Mobile Tabs Sync"
Cohesion: 0.22
Nodes (0): 

### Community 5 - "Email Supabase"
Cohesion: 0.57
Nodes (5): BUTTON(), streakReminderEmail(), upgradePromptEmail(), welcomeEmail(), WRAPPER()

### Community 6 - "Ingest jst lof"
Cohesion: 0.62
Nodes (6): ingestJST(), ingestLOF(), insertVerses(), main(), parseJSTMarkdown(), upsertBook()

### Community 7 - "Error handler Supabase"
Cohesion: 0.53
Nodes (4): honoErrorHandler(), safeErrorResponse(), safeHeaders(), sanitizeError()

### Community 8 - "Vault Supabase"
Cohesion: 0.33
Nodes (0): 

### Community 9 - "Cogs Supabase"
Cohesion: 0.6
Nodes (5): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage()

### Community 10 - "Llm Supabase"
Cohesion: 0.6
Nodes (5): callClaudeAndWrap(), callLocal(), findActiveExperiment(), logRoutingDecision(), routeLLM()

### Community 11 - "Cors Supabase"
Cohesion: 0.7
Nodes (4): getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors()

### Community 12 - "Embed corpus Embeddings"
Cohesion: 0.6
Nodes (3): fetchVersesWithoutEmbeddings(), getEmbeddings(), main()

### Community 13 - "Mobile Tabs Urim"
Cohesion: 0.4
Nodes (0): 

### Community 14 - "Corpus Supabase"
Cohesion: 0.83
Nodes (3): callClaude(), getModelTier(), logToCorpus()

### Community 15 - "Crypto Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 16 - "Rate limiter Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 17 - "Ingest corpus Insert"
Cohesion: 0.83
Nodes (3): ingest(), insertVersesBatch(), upsertBook()

### Community 18 - "Embeddings Supabase"
Cohesion: 1.0
Nodes (2): generateEmbedding(), hashEmbedding()

### Community 19 - "Supabase Eslint"
Cohesion: 0.67
Nodes (0): 

### Community 20 - "Input validator Supabase"
Cohesion: 1.0
Nodes (2): validateInputComplexity(), walk()

### Community 21 - "Notify Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Audit Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Corpus Scriptures json master Make"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Web Vite"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Web"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Mobile Reader Book"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **6 isolated node(s):** `Note`, `Highlight`, `CollectionVerse`, `Book`, `Collection` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Notify Supabase`** (2 nodes): `notify.ts`, `notifyPartyCore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Audit Supabase`** (2 nodes): `audit.ts`, `emitAuditLog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Corpus Scriptures json master Make`** (1 nodes): `make-flat.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Vite`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web`** (1 nodes): `main.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Reader Book`** (1 nodes): `[bookId].tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 4 inferred relationships involving `routeLLM()` (e.g. with `findActiveExperiment()` and `callClaudeAndWrap()`) actually correct?**
  _`routeLLM()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ingestJST()` (e.g. with `parseJSTMarkdown()` and `upsertBook()`) actually correct?**
  _`ingestJST()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `WRAPPER()` (e.g. with `welcomeEmail()` and `streakReminderEmail()`) actually correct?**
  _`WRAPPER()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `BUTTON()` (e.g. with `welcomeEmail()` and `streakReminderEmail()`) actually correct?**
  _`BUTTON()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `getCorsHeaders()` (e.g. with `getSecurityHeaders()` and `getAllowedOrigins()`) actually correct?**
  _`getCorsHeaders()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Note`, `Highlight`, `CollectionVerse` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Mobile Auth Web` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._