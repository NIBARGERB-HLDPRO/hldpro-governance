# Graph Report - seek-and-ponder  (2026-04-21)

## Corpus Check
- Large corpus: 249 files · ~290,370 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 533 nodes · 765 edges · 85 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 70 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Urim query Supabase|Urim query Supabase]]
- [[_COMMUNITY_Persona Persona respond expansion Source|Persona Persona respond expansion Source]]
- [[_COMMUNITY_Batch ingest dhc Ppp|Batch ingest dhc Ppp]]
- [[_COMMUNITY_Persona source parser|Persona source parser]]
- [[_COMMUNITY_Web Collections Highlights|Web Collections Highlights]]
- [[_COMMUNITY_Persona respond Supabase|Persona respond Supabase]]
- [[_COMMUNITY_Corpus Supabase|Corpus Supabase]]
- [[_COMMUNITY_Embed corpus Urim|Embed corpus Urim]]
- [[_COMMUNITY_Web Auth|Web Auth]]
- [[_COMMUNITY_Persona embed chunks|Persona embed chunks]]
- [[_COMMUNITY_Historical source materializer|Historical source materializer]]
- [[_COMMUNITY_Persona pack Detect|Persona pack Detect]]
- [[_COMMUNITY_Mlx embed Qwen|Mlx embed Qwen]]
- [[_COMMUNITY_Mobile Tabs Use|Mobile Tabs Use]]
- [[_COMMUNITY_Embeddings Supabase|Embeddings Supabase]]
- [[_COMMUNITY_Persona Persona respond Expect|Persona Persona respond Expect]]
- [[_COMMUNITY_Core Json|Core Json]]
- [[_COMMUNITY_Historical persona seed|Historical persona seed]]
- [[_COMMUNITY_Web Use font scale|Web Use font scale]]
- [[_COMMUNITY_Batch ingest jod|Batch ingest jod]]
- [[_COMMUNITY_Ingest jst lof|Ingest jst lof]]
- [[_COMMUNITY_Email Supabase|Email Supabase]]
- [[_COMMUNITY_Persona Persona source expansion retrieval|Persona Persona source expansion retrieval]]
- [[_COMMUNITY_Batch ingest seer|Batch ingest seer]]
- [[_COMMUNITY_Persona Persona embed chunks|Persona Persona embed chunks]]
- [[_COMMUNITY_Ingest corpus Insert|Ingest corpus Insert]]
- [[_COMMUNITY_Cited text Web|Cited text Web]]
- [[_COMMUNITY_Offline banner Mobile|Offline banner Mobile]]
- [[_COMMUNITY_Qwen bridge Mjs|Qwen bridge Mjs]]
- [[_COMMUNITY_Mobile Tabs Search|Mobile Tabs Search]]
- [[_COMMUNITY_Web Local browser flows|Web Local browser flows]]
- [[_COMMUNITY_Mobile Reader Chapter|Mobile Reader Chapter]]
- [[_COMMUNITY_Mobile Tabs Profile|Mobile Tabs Profile]]
- [[_COMMUNITY_Urim Urim query Count|Urim Urim query Count]]
- [[_COMMUNITY_Research Historical public domain registry|Research Historical public domain registry]]
- [[_COMMUNITY_Deploy Issue 93 google sso|Deploy Issue 93 google sso]]
- [[_COMMUNITY_Persona Historical persona retrieval|Persona Historical persona retrieval]]
- [[_COMMUNITY_Persona Historical source materializer|Persona Historical source materializer]]
- [[_COMMUNITY_Feedback Web|Feedback Web]]
- [[_COMMUNITY_Pricing Web|Pricing Web]]
- [[_COMMUNITY_Signup Web|Signup Web]]
- [[_COMMUNITY_Mobile Login Handle|Mobile Login Handle]]
- [[_COMMUNITY_Mobile Signup Handle|Mobile Signup Handle]]
- [[_COMMUNITY_Mobile Collections Handle|Mobile Collections Handle]]
- [[_COMMUNITY_Mobile Db Book|Mobile Db Book]]
- [[_COMMUNITY_Mobile Db Highlight|Mobile Db Highlight]]
- [[_COMMUNITY_Mobile Db Collection|Mobile Db Collection]]
- [[_COMMUNITY_Mobile Db Collection|Mobile Db Collection]]
- [[_COMMUNITY_Mobile Db Note|Mobile Db Note]]
- [[_COMMUNITY_Mobile Db Verse|Mobile Db Verse]]
- [[_COMMUNITY_Vitest|Vitest]]
- [[_COMMUNITY_Urim Local cli driver|Urim Local cli driver]]
- [[_COMMUNITY_Urim Urim query adversarial|Urim Urim query adversarial]]
- [[_COMMUNITY_Corpus Corpus search|Corpus Corpus search]]
- [[_COMMUNITY_Web Pwa shell|Web Pwa shell]]
- [[_COMMUNITY_Deploy Issue 92 staged core|Deploy Issue 92 staged core]]
- [[_COMMUNITY_Deploy Qwen bridge|Deploy Qwen bridge]]
- [[_COMMUNITY_Deploy Deploy|Deploy Deploy]]
- [[_COMMUNITY_Persona Persona source registry|Persona Persona source registry]]
- [[_COMMUNITY_Persona Historical persona seed|Persona Historical persona seed]]
- [[_COMMUNITY_Persona Persona respond adversarial|Persona Persona respond adversarial]]
- [[_COMMUNITY_Persona Persona live promotion|Persona Persona live promotion]]
- [[_COMMUNITY_Persona Persona source schema|Persona Persona source schema]]
- [[_COMMUNITY_Persona Persona pack|Persona Persona pack]]
- [[_COMMUNITY_Persona Persona web entry|Persona Persona web entry]]
- [[_COMMUNITY_Persona Persona respond|Persona Persona respond]]
- [[_COMMUNITY_Persona Persona source parser|Persona Persona source parser]]
- [[_COMMUNITY_Persona Persona seed restoration corpus|Persona Persona seed restoration corpus]]
- [[_COMMUNITY_Persona Persona source approval|Persona Persona source approval]]
- [[_COMMUNITY_Persona Persona source ingest|Persona Persona source ingest]]
- [[_COMMUNITY_Web Vite|Web Vite]]
- [[_COMMUNITY_Web Eslint|Web Eslint]]
- [[_COMMUNITY_Home Web|Home Web]]
- [[_COMMUNITY_Web Supabase|Web Supabase]]
- [[_COMMUNITY_Web Public|Web Public]]
- [[_COMMUNITY_Mobile|Mobile]]
- [[_COMMUNITY_Corpus sync progress|Corpus sync progress]]
- [[_COMMUNITY_Mobile Supabase|Mobile Supabase]]
- [[_COMMUNITY_Mobile|Mobile]]
- [[_COMMUNITY_Mobile Reader Book|Mobile Reader Book]]
- [[_COMMUNITY_Mobile Tabs|Mobile Tabs]]
- [[_COMMUNITY_Mobile Tabs|Mobile Tabs]]
- [[_COMMUNITY_Mobile Tabs Reader|Mobile Tabs Reader]]
- [[_COMMUNITY_Mobile Db Schema|Mobile Db Schema]]
- [[_COMMUNITY_Mobile Db|Mobile Db]]

## God Nodes (most connected - your core abstractions)
1. `buildChunks()` - 12 edges
2. `ingestPersonaSource()` - 12 edges
3. `getSupabaseServiceClient()` - 12 edges
4. `embedPersonaChunks()` - 10 edges
5. `parseSections()` - 9 edges
6. `seedRestorationPersonaCorpus()` - 9 edges
7. `useAuth()` - 9 edges
8. `parsePersonaSource()` - 8 edges
9. `materializeHistoricalSources()` - 8 edges
10. `approvePersonaSources()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Reader()` --calls--> `useAuth()`  [INFERRED]
  seek-and-ponder/apps/web/src/pages/Reader.tsx → seek-and-ponder/apps/mobile/src/lib/auth.tsx
- `prepareRestorationPersonas()` --calls--> `embedPersonaChunks()`  [INFERRED]
  seek-and-ponder/tests/persona/persona-respond-restoration.e2e.test.ts → seek-and-ponder/scripts/persona-embed-chunks.ts
- `prepareExpandedPersonas()` --calls--> `embedPersonaChunks()`  [INFERRED]
  seek-and-ponder/tests/persona/persona-respond-expansion.e2e.test.ts → seek-and-ponder/scripts/persona-embed-chunks.ts
- `main()` --calls--> `ingestPersonaSource()`  [INFERRED]
  seek-and-ponder/scripts/batch-ingest-jod.ts → seek-and-ponder/scripts/persona-source-ingest.ts
- `buildPersonaIngestPayload()` --calls--> `parsePersonaSource()`  [INFERRED]
  seek-and-ponder/scripts/persona-source-ingest.ts → seek-and-ponder/scripts/persona-source-parser.ts

## Communities

### Community 0 - "Urim query Supabase"
Cohesion: 0.06
Nodes (27): emitAuditLog(), getSupabaseClient(), getSupabaseServiceClient(), resolveAuthContext(), getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors() (+19 more)

### Community 1 - "Persona Persona respond expansion Source"
Cohesion: 0.06
Nodes (33): fetchPersonas(), promotePersonasLive(), publicHeaders(), resolvePersonaIds(), validateOptions(), adminHeaders(), hashEmbedding(), invokePersona() (+25 more)

### Community 2 - "Batch ingest dhc Ppp"
Cohesion: 0.09
Nodes (27): fetchText(), ingestVolume(), main(), parseArgs(), parseChapters(), stripPgWrapper(), toIngestInput(), fetchText() (+19 more)

### Community 3 - "Persona source parser"
Cohesion: 0.15
Nodes (29): buildChunks(), buildCitationLabel(), defaultHeading(), extractAtomicClaims(), extractAttributionFlags(), extractDoNotOverstate(), extractEntities(), extractFrontMatter() (+21 more)

### Community 4 - "Web Collections Highlights"
Cohesion: 0.09
Nodes (17): addVerseToCollection(), createCollection(), deleteCollection(), getCollections(), handleCreate(), handleDelete(), handleRemoveVerse(), handleSaveNote() (+9 more)

### Community 5 - "Persona respond Supabase"
Cohesion: 0.13
Nodes (19): buildContextEvidence(), buildSystemPrompt(), buildVoiceSection(), deferralResponse(), detectScriptureRefs(), detectTopics(), lexicalOverlap(), mentionsOtherPersona() (+11 more)

### Community 6 - "Corpus Supabase"
Cohesion: 0.18
Nodes (19): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage(), buildLocalCliCommand(), buildLocalCliPrompt(), callClaude() (+11 more)

### Community 7 - "Embed corpus Urim"
Cohesion: 0.18
Nodes (15): fetchVerses(), getEmbeddings(), getMlxEmbeddings(), getOpenAiEmbeddings(), getQwenEmbeddings(), main(), normalizeAndPadEmbedding(), runLocalEmbeddingHelper() (+7 more)

### Community 8 - "Web Auth"
Cohesion: 0.11
Nodes (9): App(), PublicRoute(), AuthProvider(), useAuth(), KnowledgeBase(), KnowledgeBase(), Login(), Onboarding() (+1 more)

### Community 9 - "Persona embed chunks"
Cohesion: 0.24
Nodes (13): brainHeaders(), embeddingModelFor(), embedPersonaChunks(), fetchEligiblePersonaChunks(), fetchEmbeddingQueue(), fetchEmbeddings(), fetchOpenAiEmbeddings(), getMlxEmbeddings() (+5 more)

### Community 10 - "Historical source materializer"
Cohesion: 0.26
Nodes (13): cleanupSourceText(), federalistAuthorForBlock(), fetchText(), firstFederalistTitle(), getTrancheConfig(), historicalPersonaUuid(), materializeHistoricalSources(), relativePath() (+5 more)

### Community 11 - "Persona pack Detect"
Cohesion: 0.29
Nodes (11): brainHeaders(), buildPersonaContextPack(), detectScriptureRefs(), detectTopics(), fetchCandidates(), lexicalOverlap(), normalizeText(), overlapScore() (+3 more)

### Community 12 - "Mlx embed Qwen"
Cohesion: 0.23
Nodes (9): handleCreate(), load(), extract_embeddings(), fail(), main(), to_list(), fail(), main() (+1 more)

### Community 13 - "Mobile Tabs Use"
Cohesion: 0.17
Nodes (5): selectPersona(), AssistantBubble(), handleSend(), recordActivity(), useTypewriter()

### Community 14 - "Embeddings Supabase"
Cohesion: 0.36
Nodes (10): allowEmbeddingFallback(), generateEmbedding(), generateLocalHelperEmbedding(), generateMlxEmbedding(), generateOpenAiEmbedding(), generateQwenEmbedding(), generateRemoteQwenEmbedding(), hashEmbedding() (+2 more)

### Community 15 - "Persona Persona respond Expect"
Cohesion: 0.36
Nodes (7): adminHeaders(), embed(), hashEmbedding(), invokePersona(), jsonFetch(), seedPersonaRows(), seedScholarUser()

### Community 16 - "Core Json"
Cohesion: 0.33
Nodes (5): invokeFunction(), login(), readJson(), redactedError(), requestJson()

### Community 17 - "Historical persona seed"
Cohesion: 0.43
Nodes (6): approveSource(), brainHeaders(), publicHeaders(), seedHistoricalPersonaCorpus(), uniquePersonas(), upsertPersonas()

### Community 18 - "Web Use font scale"
Cohesion: 0.29
Nodes (5): onStorage(), handleFontSize(), fontSizeToZoom(), loadFontSize(), saveFontSize()

### Community 19 - "Batch ingest jod"
Cohesion: 0.52
Nodes (6): fetchText(), gutenbergUrl(), main(), parseArgs(), parseDiscourses(), toIngestInput()

### Community 20 - "Ingest jst lof"
Cohesion: 0.62
Nodes (6): ingestJST(), ingestLOF(), insertVerses(), main(), parseJSTMarkdown(), upsertBook()

### Community 21 - "Email Supabase"
Cohesion: 0.57
Nodes (5): BUTTON(), streakReminderEmail(), upgradePromptEmail(), welcomeEmail(), WRAPPER()

### Community 22 - "Persona Persona source expansion retrieval"
Cohesion: 0.7
Nodes (4): brainHeaders(), hashEmbedding(), jsonFetch(), patchPersonaEmbedding()

### Community 23 - "Batch ingest seer"
Cohesion: 0.7
Nodes (4): fetchText(), main(), parseArticles(), toIngestInput()

### Community 24 - "Persona Persona embed chunks"
Cohesion: 0.5
Nodes (0): 

### Community 25 - "Ingest corpus Insert"
Cohesion: 0.83
Nodes (3): ingest(), insertVersesBatch(), upsertBook()

### Community 26 - "Cited text Web"
Cohesion: 0.5
Nodes (0): 

### Community 27 - "Offline banner Mobile"
Cohesion: 0.5
Nodes (2): OfflineBanner(), useNetworkStatus()

### Community 28 - "Qwen bridge Mjs"
Cohesion: 0.67
Nodes (0): 

### Community 29 - "Mobile Tabs Search"
Cohesion: 0.67
Nodes (1): handleSearch()

### Community 30 - "Web Local browser flows"
Cohesion: 0.67
Nodes (0): 

### Community 31 - "Mobile Reader Chapter"
Cohesion: 0.67
Nodes (0): 

### Community 32 - "Mobile Tabs Profile"
Cohesion: 0.67
Nodes (0): 

### Community 33 - "Urim Urim query Count"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Research Historical public domain registry"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Deploy Issue 93 google sso"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Persona Historical persona retrieval"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Persona Historical source materializer"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Feedback Web"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Pricing Web"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Signup Web"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Mobile Login Handle"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Mobile Signup Handle"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Mobile Collections Handle"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Mobile Db Book"
Cohesion: 1.0
Nodes (1): Book

### Community 45 - "Mobile Db Highlight"
Cohesion: 1.0
Nodes (1): Highlight

### Community 46 - "Mobile Db Collection"
Cohesion: 1.0
Nodes (1): CollectionVerse

### Community 47 - "Mobile Db Collection"
Cohesion: 1.0
Nodes (1): Collection

### Community 48 - "Mobile Db Note"
Cohesion: 1.0
Nodes (1): Note

### Community 49 - "Mobile Db Verse"
Cohesion: 1.0
Nodes (1): Verse

### Community 50 - "Vitest"
Cohesion: 1.0
Nodes (0): 

### Community 51 - "Urim Local cli driver"
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Urim Urim query adversarial"
Cohesion: 1.0
Nodes (0): 

### Community 53 - "Corpus Corpus search"
Cohesion: 1.0
Nodes (0): 

### Community 54 - "Web Pwa shell"
Cohesion: 1.0
Nodes (0): 

### Community 55 - "Deploy Issue 92 staged core"
Cohesion: 1.0
Nodes (0): 

### Community 56 - "Deploy Qwen bridge"
Cohesion: 1.0
Nodes (0): 

### Community 57 - "Deploy Deploy"
Cohesion: 1.0
Nodes (0): 

### Community 58 - "Persona Persona source registry"
Cohesion: 1.0
Nodes (0): 

### Community 59 - "Persona Historical persona seed"
Cohesion: 1.0
Nodes (0): 

### Community 60 - "Persona Persona respond adversarial"
Cohesion: 1.0
Nodes (0): 

### Community 61 - "Persona Persona live promotion"
Cohesion: 1.0
Nodes (0): 

### Community 62 - "Persona Persona source schema"
Cohesion: 1.0
Nodes (0): 

### Community 63 - "Persona Persona pack"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Persona Persona web entry"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Persona Persona respond"
Cohesion: 1.0
Nodes (0): 

### Community 66 - "Persona Persona source parser"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Persona Persona seed restoration corpus"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Persona Persona source approval"
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Persona Persona source ingest"
Cohesion: 1.0
Nodes (0): 

### Community 70 - "Web Vite"
Cohesion: 1.0
Nodes (0): 

### Community 71 - "Web Eslint"
Cohesion: 1.0
Nodes (0): 

### Community 72 - "Home Web"
Cohesion: 1.0
Nodes (0): 

### Community 73 - "Web Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 74 - "Web Public"
Cohesion: 1.0
Nodes (0): 

### Community 75 - "Mobile"
Cohesion: 1.0
Nodes (0): 

### Community 76 - "Corpus sync progress"
Cohesion: 1.0
Nodes (0): 

### Community 77 - "Mobile Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 78 - "Mobile"
Cohesion: 1.0
Nodes (0): 

### Community 79 - "Mobile Reader Book"
Cohesion: 1.0
Nodes (0): 

### Community 80 - "Mobile Tabs"
Cohesion: 1.0
Nodes (0): 

### Community 81 - "Mobile Tabs"
Cohesion: 1.0
Nodes (0): 

### Community 82 - "Mobile Tabs Reader"
Cohesion: 1.0
Nodes (0): 

### Community 83 - "Mobile Db Schema"
Cohesion: 1.0
Nodes (0): 

### Community 84 - "Mobile Db"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **6 isolated node(s):** `Book`, `Highlight`, `CollectionVerse`, `Collection`, `Note` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Urim Urim query Count`** (2 nodes): `urim-query.contract.test.ts`, `countMatches()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Research Historical public domain registry`** (2 nodes): `loadRegistry()`, `historical-public-domain-registry.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Issue 93 google sso`** (2 nodes): `issue-93-google-sso-contract.test.ts`, `placeholderLine()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Historical persona retrieval`** (2 nodes): `parseVector()`, `historical-persona-retrieval.e2e.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Historical source materializer`** (2 nodes): `countFederalistEssays()`, `historical-source-materializer.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Feedback Web`** (2 nodes): `handleSubmit()`, `Feedback.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pricing Web`** (2 nodes): `Pricing.tsx`, `handleCheckout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Signup Web`** (2 nodes): `Signup.tsx`, `handleSubmit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Login Handle`** (2 nodes): `login.tsx`, `handleLogin()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Signup Handle`** (2 nodes): `signup.tsx`, `handleSignup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Collections Handle`** (2 nodes): `[id].tsx`, `handleRemove()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Book`** (2 nodes): `Book`, `Book.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Highlight`** (2 nodes): `Highlight`, `Highlight.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Collection`** (2 nodes): `CollectionVerse`, `CollectionVerse.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Collection`** (2 nodes): `Collection`, `Collection.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Note`** (2 nodes): `Note.ts`, `Note`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Verse`** (2 nodes): `Verse.ts`, `Verse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vitest`** (1 nodes): `vitest.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Urim Local cli driver`** (1 nodes): `local-cli-driver.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Urim Urim query adversarial`** (1 nodes): `urim-query.adversarial.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Corpus Corpus search`** (1 nodes): `corpus-search.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Pwa shell`** (1 nodes): `pwa-shell.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Issue 92 staged core`** (1 nodes): `issue-92-staged-core-smoke.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Qwen bridge`** (1 nodes): `qwen-bridge-smoke.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Deploy Deploy`** (1 nodes): `deploy-script.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona source registry`** (1 nodes): `persona-source-registry.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Historical persona seed`** (1 nodes): `historical-persona-seed.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona respond adversarial`** (1 nodes): `persona-respond-adversarial.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona live promotion`** (1 nodes): `persona-live-promotion.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona source schema`** (1 nodes): `persona-source-schema.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona pack`** (1 nodes): `persona-context-pack.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona web entry`** (1 nodes): `persona-web-entry.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona respond`** (1 nodes): `persona-respond.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona source parser`** (1 nodes): `persona-source-parser.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona seed restoration corpus`** (1 nodes): `persona-seed-restoration-corpus.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona source approval`** (1 nodes): `persona-source-approval.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persona Persona source ingest`** (1 nodes): `persona-source-ingest.contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Vite`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Eslint`** (1 nodes): `eslint.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Home Web`** (1 nodes): `Home.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Supabase`** (1 nodes): `supabase.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Public`** (1 nodes): `sw.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Corpus sync progress`** (1 nodes): `CorpusSyncProgress.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Supabase`** (1 nodes): `supabase.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile`** (1 nodes): `_layout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Reader Book`** (1 nodes): `[bookId].tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Tabs`** (1 nodes): `_layout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Tabs`** (1 nodes): `index.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Tabs Reader`** (1 nodes): `reader.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db Schema`** (1 nodes): `schema.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Db`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ingestPersonaSource()` connect `Batch ingest dhc Ppp` to `Historical persona seed`, `Batch ingest jod`, `Persona Persona respond expansion Source`, `Batch ingest seer`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `seedRestorationPersonaCorpus()` connect `Persona Persona respond expansion Source` to `Batch ingest dhc Ppp`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `buildPersonaIngestPayload()` connect `Batch ingest dhc Ppp` to `Persona source parser`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `ingestPersonaSource()` (e.g. with `main()` and `main()`) actually correct?**
  _`ingestPersonaSource()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `getSupabaseServiceClient()` (e.g. with `findActiveExperiment()` and `logRoutingDecision()`) actually correct?**
  _`getSupabaseServiceClient()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `embedPersonaChunks()` (e.g. with `prepareRestorationPersonas()` and `prepareExpandedPersonas()`) actually correct?**
  _`embedPersonaChunks()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Book`, `Highlight`, `CollectionVerse` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._