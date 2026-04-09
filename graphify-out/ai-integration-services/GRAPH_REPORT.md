# Graph Report - /Users/bennibarger/Developer/HLDPRO/ai-integration-services  (2026-04-09)

## Corpus Check
- Large corpus: 965 files · ~1,428,846 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1883 nodes · 2533 edges · 111 communities detected
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 519 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TwentyCRMConnector` - 29 edges
2. `GHLCRMConnector` - 25 edges
3. `LocalCRMConnector` - 23 edges
4. `NullCRMConnector` - 21 edges
5. `N8nClient` - 15 edges
6. `TwilioClient` - 15 edges
7. `VapiClient` - 15 edges
8. `VoiceflowClient` - 14 edges
9. `GoogleCalendarConnector` - 11 edges
10. `ServiceTitanConnector` - 11 edges

## Surprising Connections (you probably didn't know these)
- `handleBulkApprove()` --calls--> `loadBrainData()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/ai-integration-services/apps/portal/src/pages/dashboard/DashboardBrain.tsx → /Users/bennibarger/Developer/HLDPRO/ai-integration-services/apps/marketing/src/portal/pages/dashboard/DashboardBrain.tsx
- `handleBulkDelete()` --calls--> `loadBrainData()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/ai-integration-services/apps/portal/src/pages/dashboard/DashboardBrain.tsx → /Users/bennibarger/Developer/HLDPRO/ai-integration-services/apps/marketing/src/portal/pages/dashboard/DashboardBrain.tsx
- `sendReminderSMS()` --calls--> `TWILIO_ACCOUNT_SID()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/permit-monitor/index.ts
- `sendReminderSMS()` --calls--> `TWILIO_AUTH_TOKEN()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/permit-monitor/index.ts
- `sendReminderSMS()` --calls--> `TWILIO_FROM_NUMBER()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → /Users/bennibarger/Developer/HLDPRO/ai-integration-services/backend/supabase/functions/permit-monitor/index.ts

## Communities

### Community 0 - "Webhook receiver Supabase"
Cohesion: 0.01
Nodes (166): agentCritic(), agentIntake(), agentPackager(), agentPresenter(), agentResearcher(), alertOperator(), amortize(), applyEventFilters() (+158 more)

### Community 1 - "Wizard Handle"
Cohesion: 0.01
Nodes (32): getConversationHistory(), handleKeyDown(), handleSend(), handleCancel(), loadData(), handleResync(), handleSave(), extractCallFromAuditEntry() (+24 more)

### Community 2 - "Real enrollment founder Sign"
Cohesion: 0.02
Nodes (26): browserSignIn(), cleanupClientByEmail(), cleanupTestClient(), findAuthUsersByEmail(), findClientByEmail(), findClientsByEmail(), getAuthTokens(), isLocalUrl() (+18 more)

### Community 3 - "Support Feature roadmap Analytics"
Cohesion: 0.02
Nodes (2): handleSave(), saveTargets()

### Community 4 - "Api Admin Use"
Cohesion: 0.02
Nodes (0): 

### Community 5 - "Leads Reseller"
Cohesion: 0.03
Nodes (6): extractLeadFromAuditEntry(), handleExport(), inferSource(), leadsToCSV(), formatDate(), formatTime()

### Community 6 - "Api Plans Sections"
Cohesion: 0.04
Nodes (8): trackCheckoutStarted(), trackCtaClick(), trackEvent(), trackPlanSelected(), handleSubmit(), validate(), planSavings(), planTotal()

### Community 7 - "Compendium Extract Assemble"
Cohesion: 0.08
Nodes (29): assembleOverview(), extractSection(), readFile(), assemblePatterns(), readFileIfExists(), truncateFailFastLog(), consolidateClaudePack(), readModular() (+21 more)

### Community 8 - "Api Prompts"
Cohesion: 0.06
Nodes (7): handleSubmit(), next(), validateStep(), extractVariables(), validateVariables(), useCreatePromptVersion(), useRollbackPromptVersion()

### Community 9 - "Connectors Crm Twenty"
Cohesion: 0.11
Nodes (1): TwentyCRMConnector

### Community 10 - "Connectors Crm Null"
Cohesion: 0.09
Nodes (2): NullCRMConnector, NullServiceConnector

### Community 11 - "Connectors Crm Ghl"
Cohesion: 0.14
Nodes (1): GHLCRMConnector

### Community 12 - "Connectors Crm Local"
Cohesion: 0.11
Nodes (1): LocalCRMConnector

### Community 13 - "Assistant chat Tour"
Cohesion: 0.09
Nodes (0): 

### Community 14 - "Training Train qwen3 lora"
Cohesion: 0.14
Nodes (18): export_gguf(), load_dataset(), main(), parse_args(), HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:, Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format, # TODO: Implement when RunPod environment is ready, Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl (+10 more)

### Community 15 - "Support Support queue Api"
Cohesion: 0.11
Nodes (0): 

### Community 16 - "Integrations Bookings"
Cohesion: 0.16
Nodes (10): callEdgeFunction(), getStageIndex(), handleApprove(), handleCancel(), handleExecute(), handleNewBooking(), PipelineProgressBar(), fetchSyncLogs() (+2 more)

### Community 17 - "N8n client Supabase"
Cohesion: 0.21
Nodes (1): N8nClient

### Community 18 - "Twilio client Supabase"
Cohesion: 0.22
Nodes (1): TwilioClient

### Community 19 - "Vapi client Supabase"
Cohesion: 0.3
Nodes (1): VapiClient

### Community 20 - "Voiceflow client Supabase"
Cohesion: 0.21
Nodes (1): VoiceflowClient

### Community 21 - "Roof overlay Measure"
Cohesion: 0.18
Nodes (4): buildLegend(), parsePitch(), pitchColor(), RoofOverlay()

### Community 22 - "Brain Handle"
Cohesion: 0.23
Nodes (9): handleBulkApprove(), handleBulkDelete(), handleFileUpload(), handleManualSubmit(), handlePdfUpload(), handlePricingApproval(), handlePricingEdit(), handleWebScrape() (+1 more)

### Community 23 - "Setup readiness Supabase"
Cohesion: 0.15
Nodes (0): 

### Community 24 - "Roof math Supabase"
Cohesion: 0.21
Nodes (7): getPitchCategory(), getPitchCategoryFromRatio(), pitchRatioToRise(), processGoogleSegments(), sqFeetToSquares(), sqMetersToSqFeet(), sqMetersToSquares()

### Community 25 - "Finance Handle"
Cohesion: 0.33
Nodes (9): apiCall(), handleApproveMatch(), handleConnectAccount(), handleCreateInvoice(), handleRejectMatch(), handleSendInvoice(), handleSyncTransactions(), handleTriggerMatching() (+1 more)

### Community 26 - "Connectors Google calendar Supabase"
Cohesion: 0.2
Nodes (1): GoogleCalendarConnector

### Community 27 - "Connectors Servicetitan Supabase"
Cohesion: 0.2
Nodes (1): ServiceTitanConnector

### Community 28 - "Connectors Jobber Supabase"
Cohesion: 0.18
Nodes (1): JobberConnector

### Community 29 - "Purchase Supabase"
Cohesion: 0.42
Nodes (10): buildOwnerName(), ensureClientProducts(), ensureCrmConfig(), ensureProvisioningSteps(), ensureReferralTracking(), finalizePortalPurchase(), nonEmpty(), shouldReplaceBusinessName() (+2 more)

### Community 30 - "Calcom client Supabase"
Cohesion: 0.29
Nodes (1): CalcomClient

### Community 31 - "Setup compliance gates"
Cohesion: 0.42
Nodes (9): buildBaseRow(), derivePlaidDesiredTiming(), derivePlaidGate(), deriveSharedSmsA2PGate(), findA2PAssociationForNumber(), loadComplianceSignals(), nowIso(), setGateState() (+1 more)

### Community 32 - "Esign Supabase"
Cohesion: 0.2
Nodes (2): computeSha256(), hashPdfFromUrl()

### Community 33 - "Connectors Ad Meta"
Cohesion: 0.29
Nodes (1): MetaAdConnector

### Community 34 - "Connectors Ad Nextdoor"
Cohesion: 0.27
Nodes (1): NextdoorAdConnector

### Community 35 - "Connectors Housecall Supabase"
Cohesion: 0.22
Nodes (1): HousecallProConnector

### Community 36 - "Gc Gcsub Line"
Cohesion: 0.25
Nodes (5): apiFetch(), getToken(), handleSend(), handleSubmit(), handleUpload()

### Community 37 - "Setup connection tasks"
Cohesion: 0.33
Nodes (8): buildInitialSetupConnectionTaskRows(), deriveIncompleteWizardResumePath(), deriveSetupResumePath(), deriveStatusFromSignals(), isStep1Incomplete(), loadIntegrationSignals(), syncSetupConnectionTasksForClient(), withDefaultTaskState()

### Community 38 - "Connectors Ad Google"
Cohesion: 0.29
Nodes (1): GoogleAdsConnector

### Community 39 - "Live full Url"
Cohesion: 0.27
Nodes (5): findAdminUserByEmail(), isLocalUrl(), resolveAppUrl(), signInAndInject(), signInWithPassword()

### Community 40 - "Load provisioning Client"
Cohesion: 0.31
Nodes (5): callProvision(), runActivation(), seedActivateSteps(), supaRest(), waitForTerminal()

### Community 41 - "Vault Supabase"
Cohesion: 0.25
Nodes (0): 

### Community 42 - "Solar savings Supabase"
Cohesion: 0.29
Nodes (2): calculateIRR(), calculateSavings()

### Community 43 - "Plaid client Supabase"
Cohesion: 0.43
Nodes (6): createLinkToken(), exchangePublicToken(), getAccounts(), getBalance(), getBaseUrl(), plaidFetch()

### Community 44 - "Geotiff processor Supabase"
Cohesion: 0.43
Nodes (7): assessConfidence(), emptyResults(), extractLinearMeasurements(), getTagDoubles(), getTagValue(), parseDSM(), parseTiffTags()

### Community 45 - "Vapi Supabase"
Cohesion: 0.38
Nodes (3): getVapiKey(), vapiGet(), vapiPatch()

### Community 46 - "Analytics db Supabase"
Cohesion: 0.57
Nodes (6): analyticsInsert(), analyticsSelect(), analyticsUpdate(), analyticsUpsert(), buildHeaders(), buildUrl()

### Community 47 - "Pwa Public Drain"
Cohesion: 0.43
Nodes (5): drainQueue(), enqueue(), isAuthEndpoint(), isSupabaseMutation(), openDB()

### Community 48 - "Oauth state Supabase"
Cohesion: 0.6
Nodes (5): decodeBase64Url(), encodeBase64Url(), getSigningSecret(), signOAuthState(), verifyOAuthState()

### Community 49 - "Error handler Supabase"
Cohesion: 0.53
Nodes (4): honoErrorHandler(), safeErrorResponse(), safeHeaders(), sanitizeError()

### Community 50 - "Estimate engine Supabase"
Cohesion: 0.4
Nodes (2): centsToUsd(), formatEstimateForPdf()

### Community 51 - "Ai matcher Supabase"
Cohesion: 0.53
Nodes (4): buildMatchingPrompt(), callClaudeForMatching(), matchTransactions(), parseAndValidateMatches()

### Community 52 - "Cogs Supabase"
Cohesion: 0.6
Nodes (5): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage()

### Community 53 - "Llm Supabase"
Cohesion: 0.6
Nodes (5): callClaudeAndWrap(), callLocal(), findActiveExperiment(), logRoutingDecision(), routeLLM()

### Community 54 - "Seed esign templates"
Cohesion: 0.53
Nodes (4): buildStatutoryFields(), dateSigned(), prefilled(), sig()

### Community 55 - "Seed Generate"
Cohesion: 0.6
Nodes (5): generateAuditLogs(), generateInvoices(), generateProvisioningSteps(), generateTransactions(), seed()

### Community 56 - "Compendium Upload notebooklm"
Cohesion: 0.6
Nodes (5): deleteMatchingSources(), getPackFiles(), loadConfig(), main(), uploadBatch()

### Community 57 - "Compendium Setup browser"
Cohesion: 0.53
Nodes (4): loadConfig(), main(), prompt(), setupProfile()

### Community 58 - "Compendium Upload claude"
Cohesion: 0.6
Nodes (5): deleteExistingFiles(), getPackFiles(), loadConfig(), main(), uploadFiles()

### Community 59 - "Cogs export Csv"
Cohesion: 0.47
Nodes (3): exportCSV(), exportJSON(), triggerBrowserDownload()

### Community 60 - "Routing engine Supabase"
Cohesion: 0.6
Nodes (3): estimateDriveMinutes(), haversineKm(), scoreWorker()

### Community 61 - "Cors Supabase"
Cohesion: 0.7
Nodes (4): getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors()

### Community 62 - "Tester guide docx"
Cohesion: 0.5
Nodes (4): annotate_screenshot(), build_docx(), Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re, Add red boxes and labels to a screenshot.

### Community 63 - "Playwright Url"
Cohesion: 0.6
Nodes (3): isLocalUrl(), resolveAppUrl(), resolvePortalBaseUrl()

### Community 64 - "Contact Industries"
Cohesion: 0.5
Nodes (0): 

### Community 65 - "Corpus Supabase"
Cohesion: 0.83
Nodes (3): callClaude(), getModelTier(), logToCorpus()

### Community 66 - "Preference injector Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 67 - "Email Supabase"
Cohesion: 0.67
Nodes (2): getApiKey(), sendEmail()

### Community 68 - "Crypto Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 69 - "Provisioning plan Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 70 - "Rate limiter Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 71 - "Auth Supabase"
Cohesion: 0.67
Nodes (2): getSupabaseClient(), resolveAuthContext()

### Community 72 - "Connectors Factory Supabase"
Cohesion: 0.67
Nodes (2): getAdConnector(), getAllAdConnectors()

### Community 73 - "Analyze bugs Categorize"
Cohesion: 0.5
Nodes (0): 

### Community 74 - "Setup stripe addon products"
Cohesion: 0.83
Nodes (3): main(), stripeGet(), stripeRequest()

### Community 75 - "Pii Supabase"
Cohesion: 1.0
Nodes (2): containsPII(), stripPII()

### Community 76 - "Vapi owner Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 77 - "Embeddings Supabase"
Cohesion: 1.0
Nodes (2): generateEmbedding(), hashEmbedding()

### Community 78 - "Voice Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 79 - "Finalize Supabase"
Cohesion: 1.0
Nodes (2): finalizeDocumentCore(), getExistingFinalizeState()

### Community 80 - "Roof takeoff Supabase"
Cohesion: 1.0
Nodes (2): calculateTakeoff(), round2()

### Community 81 - "Input validator Supabase"
Cohesion: 1.0
Nodes (2): validateInputComplexity(), walk()

### Community 82 - "Seed finance demo"
Cohesion: 0.67
Nodes (0): 

### Community 83 - "Affiliate program Reseller"
Cohesion: 0.67
Nodes (0): 

### Community 84 - "Forwarding instructions Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Gate checks Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 86 - "Purchase access email"
Cohesion: 1.0
Nodes (0): 

### Community 87 - "Setup plan Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 88 - "Vapi brain tool"
Cohesion: 1.0
Nodes (0): 

### Community 89 - "Advance Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 90 - "Area consent Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 91 - "Notify Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 92 - "Memory injector Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Audit Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 94 - "Capture tester guide screenshots"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Seed report"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Seed demo accounts"
Cohesion: 1.0
Nodes (0): 

### Community 97 - "Preflight Run"
Cohesion: 1.0
Nodes (0): 

### Community 98 - "Wizard Wizard step5"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Demo call banner"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Finance types Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Connectors Interface Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Pentagi Pentagi flow"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Plaid screenshots"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Tailwind"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Postcss"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Corpus Corpus"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **13 isolated node(s):** `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:`, `Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format`, `Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Forwarding instructions Supabase`** (2 nodes): `forwarding-instructions.ts`, `buildForwardingInstructionsHtml()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gate checks Supabase`** (2 nodes): `gate-checks.ts`, `runGateChecks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Purchase access email`** (2 nodes): `purchase-access-email.ts`, `sendPortalAccessEmail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Setup plan Supabase`** (2 nodes): `setup-plan.ts`, `createDefaultSetupPlan()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vapi brain tool`** (2 nodes): `vapi-brain-tool.ts`, `getBrainToolDefinition()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Advance Supabase`** (2 nodes): `advance.ts`, `advanceSigningWorkflow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Area consent Supabase`** (2 nodes): `area-code-consent.ts`, `getConsentType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Notify Supabase`** (2 nodes): `notify.ts`, `notifyPartyCore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memory injector Supabase`** (2 nodes): `memory-injector.ts`, `fetchContext()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Audit Supabase`** (2 nodes): `audit.ts`, `emitAuditLog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Capture tester guide screenshots`** (2 nodes): `capture-tester-guide-screenshots.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seed report`** (2 nodes): `seed-report-data.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seed demo accounts`** (2 nodes): `seed-demo-accounts.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Preflight Run`** (2 nodes): `preflight-probe.spec.ts`, `runPreflight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wizard Wizard step5`** (2 nodes): `WizardStep5.tsx`, `WizardStep5()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo call banner`** (2 nodes): `DemoCallBanner.tsx`, `DemoCallBanner()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Supabase`** (1 nodes): `config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Finance types Supabase`** (1 nodes): `finance-types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Connectors Interface Supabase`** (1 nodes): `interface.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pentagi Pentagi flow`** (1 nodes): `pentagi-flow.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (1 nodes): `marketing-portal.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Plaid screenshots`** (1 nodes): `plaid-screenshots.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tailwind`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Postcss`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Corpus Corpus`** (1 nodes): `CorpusLayout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Webhook receiver Supabase` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Wizard Handle` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Real enrollment founder Sign` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Support Feature roadmap Analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Api Admin Use` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Leads Reseller` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._