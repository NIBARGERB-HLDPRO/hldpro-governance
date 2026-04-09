# Graph Report - ai-integration-services  (2026-04-09)

## Corpus Check
- Large corpus: 974 files · ~1,435,928 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1902 nodes · 2562 edges · 119 communities detected
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 531 edges (avg confidence: 0.5)
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
  ai-integration-services/apps/portal/src/pages/dashboard/DashboardBrain.tsx → ai-integration-services/apps/marketing/src/portal/pages/dashboard/DashboardBrain.tsx
- `handleBulkDelete()` --calls--> `loadBrainData()`  [INFERRED]
  ai-integration-services/apps/portal/src/pages/dashboard/DashboardBrain.tsx → ai-integration-services/apps/marketing/src/portal/pages/dashboard/DashboardBrain.tsx
- `sendReminderSMS()` --calls--> `TWILIO_ACCOUNT_SID()`  [INFERRED]
  ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → ai-integration-services/backend/supabase/functions/permit-monitor/index.ts
- `sendReminderSMS()` --calls--> `TWILIO_AUTH_TOKEN()`  [INFERRED]
  ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → ai-integration-services/backend/supabase/functions/permit-monitor/index.ts
- `sendReminderSMS()` --calls--> `TWILIO_FROM_NUMBER()`  [INFERRED]
  ai-integration-services/backend/supabase/functions/hvac-maintenance-alert/index.ts → ai-integration-services/backend/supabase/functions/permit-monitor/index.ts

## Communities

### Community 0 - "Webhook receiver Supabase"
Cohesion: 0.01
Nodes (166): agentCritic(), agentIntake(), agentPackager(), agentPresenter(), agentResearcher(), alertOperator(), amortize(), applyEventFilters() (+158 more)

### Community 1 - "Wizard Handle"
Cohesion: 0.01
Nodes (26): handleCancel(), loadData(), handleResync(), handleSave(), extractCallFromAuditEntry(), inferOutcome(), loadCampaigns(), triggerCampaign() (+18 more)

### Community 2 - "Support Feature roadmap Analytics"
Cohesion: 0.02
Nodes (2): handleSave(), saveTargets()

### Community 3 - "Api Admin Clients"
Cohesion: 0.02
Nodes (7): handleSubmit(), next(), validateStep(), extractVariables(), validateVariables(), useCreatePromptVersion(), useRollbackPromptVersion()

### Community 4 - "Link crawler Sign"
Cohesion: 0.03
Nodes (22): browserSignIn(), cleanupClientByEmail(), cleanupTestClient(), findAuthUsersByEmail(), findClientByEmail(), findClientsByEmail(), getAuthTokens(), isLocalUrl() (+14 more)

### Community 5 - "Api Plans Reseller"
Cohesion: 0.04
Nodes (6): trackCheckoutStarted(), trackCtaClick(), trackEvent(), trackPlanSelected(), handleSubmit(), validate()

### Community 6 - "Support Support queue Assistant"
Cohesion: 0.05
Nodes (0): 

### Community 7 - "Compendium Extract Assemble"
Cohesion: 0.08
Nodes (29): assembleOverview(), extractSection(), readFile(), assemblePatterns(), readFileIfExists(), truncateFailFastLog(), consolidateClaudePack(), readModular() (+21 more)

### Community 8 - "Connectors Crm Twenty"
Cohesion: 0.11
Nodes (1): TwentyCRMConnector

### Community 9 - "Connectors Crm Null"
Cohesion: 0.09
Nodes (2): NullCRMConnector, NullServiceConnector

### Community 10 - "Sections Value stack Flow"
Cohesion: 0.08
Nodes (2): planSavings(), planTotal()

### Community 11 - "Connectors Crm Ghl"
Cohesion: 0.14
Nodes (1): GHLCRMConnector

### Community 12 - "Connectors Crm Local"
Cohesion: 0.11
Nodes (1): LocalCRMConnector

### Community 13 - "Job queue Pwa"
Cohesion: 0.1
Nodes (2): formatDate(), formatTime()

### Community 14 - "Training Train qwen3 lora"
Cohesion: 0.14
Nodes (18): export_gguf(), load_dataset(), main(), parse_args(), HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:, Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format, # TODO: Implement when RunPod environment is ready, Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl (+10 more)

### Community 15 - "N8n client Supabase"
Cohesion: 0.21
Nodes (1): N8nClient

### Community 16 - "Twilio client Supabase"
Cohesion: 0.22
Nodes (1): TwilioClient

### Community 17 - "Vapi client Supabase"
Cohesion: 0.3
Nodes (1): VapiClient

### Community 18 - "Api Referrals"
Cohesion: 0.12
Nodes (0): 

### Community 19 - "Voiceflow client Supabase"
Cohesion: 0.21
Nodes (1): VoiceflowClient

### Community 20 - "Operator governance Supabase"
Cohesion: 0.26
Nodes (12): buildFilePath(), buildMarkdown(), createBranch(), encodeBase64Utf8(), ensureBranch(), ensurePullRequest(), getBranchSha(), getExistingFileSha() (+4 more)

### Community 21 - "Brain Handle"
Cohesion: 0.23
Nodes (9): handleBulkApprove(), handleBulkDelete(), handleFileUpload(), handleManualSubmit(), handlePdfUpload(), handlePricingApproval(), handlePricingEdit(), handleWebScrape() (+1 more)

### Community 22 - "Setup readiness Supabase"
Cohesion: 0.15
Nodes (0): 

### Community 23 - "Roof math Supabase"
Cohesion: 0.21
Nodes (7): getPitchCategory(), getPitchCategoryFromRatio(), pitchRatioToRise(), processGoogleSegments(), sqFeetToSquares(), sqMetersToSqFeet(), sqMetersToSquares()

### Community 24 - "Finance Handle"
Cohesion: 0.33
Nodes (9): apiCall(), handleApproveMatch(), handleConnectAccount(), handleCreateInvoice(), handleRejectMatch(), handleSendInvoice(), handleSyncTransactions(), handleTriggerMatching() (+1 more)

### Community 25 - "Connectors Google calendar Supabase"
Cohesion: 0.2
Nodes (1): GoogleCalendarConnector

### Community 26 - "Connectors Servicetitan Supabase"
Cohesion: 0.2
Nodes (1): ServiceTitanConnector

### Community 27 - "Connectors Jobber Supabase"
Cohesion: 0.18
Nodes (1): JobberConnector

### Community 28 - "Purchase Supabase"
Cohesion: 0.42
Nodes (10): buildOwnerName(), ensureClientProducts(), ensureCrmConfig(), ensureProvisioningSteps(), ensureReferralTracking(), finalizePortalPurchase(), nonEmpty(), shouldReplaceBusinessName() (+2 more)

### Community 29 - "Calcom client Supabase"
Cohesion: 0.29
Nodes (1): CalcomClient

### Community 30 - "Setup compliance gates"
Cohesion: 0.42
Nodes (9): buildBaseRow(), derivePlaidDesiredTiming(), derivePlaidGate(), deriveSharedSmsA2PGate(), findA2PAssociationForNumber(), loadComplianceSignals(), nowIso(), setGateState() (+1 more)

### Community 31 - "Esign Supabase"
Cohesion: 0.2
Nodes (2): computeSha256(), hashPdfFromUrl()

### Community 32 - "Connectors Ad Meta"
Cohesion: 0.29
Nodes (1): MetaAdConnector

### Community 33 - "Connectors Ad Nextdoor"
Cohesion: 0.27
Nodes (1): NextdoorAdConnector

### Community 34 - "Connectors Housecall Supabase"
Cohesion: 0.22
Nodes (1): HousecallProConnector

### Community 35 - "Gc Gcsub Line"
Cohesion: 0.25
Nodes (5): apiFetch(), getToken(), handleSend(), handleSubmit(), handleUpload()

### Community 36 - "Setup connection tasks"
Cohesion: 0.33
Nodes (8): buildInitialSetupConnectionTaskRows(), deriveIncompleteWizardResumePath(), deriveSetupResumePath(), deriveStatusFromSignals(), isStep1Incomplete(), loadIntegrationSignals(), syncSetupConnectionTasksForClient(), withDefaultTaskState()

### Community 37 - "Connectors Ad Google"
Cohesion: 0.29
Nodes (1): GoogleAdsConnector

### Community 38 - "Live full Url"
Cohesion: 0.27
Nodes (5): findAdminUserByEmail(), isLocalUrl(), resolveAppUrl(), signInAndInject(), signInWithPassword()

### Community 39 - "Load provisioning Client"
Cohesion: 0.31
Nodes (5): callProvision(), runActivation(), seedActivateSteps(), supaRest(), waitForTerminal()

### Community 40 - "Real enrollment founder"
Cohesion: 0.27
Nodes (4): envSeed(), fetchStripeCustomer(), loadPurchaseSeed(), splitName()

### Community 41 - "Roof overlay Pitch"
Cohesion: 0.31
Nodes (4): buildLegend(), parsePitch(), pitchColor(), RoofOverlay()

### Community 42 - "Leads Handle"
Cohesion: 0.28
Nodes (4): extractLeadFromAuditEntry(), handleExport(), inferSource(), leadsToCSV()

### Community 43 - "Integrations Handle"
Cohesion: 0.28
Nodes (3): fetchSyncLogs(), handleManage(), handleResync()

### Community 44 - "Vault Supabase"
Cohesion: 0.25
Nodes (0): 

### Community 45 - "Solar savings Supabase"
Cohesion: 0.29
Nodes (2): calculateIRR(), calculateSavings()

### Community 46 - "Plaid client Supabase"
Cohesion: 0.43
Nodes (6): createLinkToken(), exchangePublicToken(), getAccounts(), getBalance(), getBaseUrl(), plaidFetch()

### Community 47 - "Geotiff processor Supabase"
Cohesion: 0.43
Nodes (7): assessConfidence(), emptyResults(), extractLinearMeasurements(), getTagDoubles(), getTagValue(), parseDSM(), parseTiffTags()

### Community 48 - "Estimate builder Line"
Cohesion: 0.32
Nodes (3): callEdge(), handleGenerate(), handleSend()

### Community 49 - "Bookings Handle"
Cohesion: 0.43
Nodes (7): callEdgeFunction(), getStageIndex(), handleApprove(), handleCancel(), handleExecute(), handleNewBooking(), PipelineProgressBar()

### Community 50 - "Vapi Supabase"
Cohesion: 0.38
Nodes (3): getVapiKey(), vapiGet(), vapiPatch()

### Community 51 - "Analytics db Supabase"
Cohesion: 0.57
Nodes (6): analyticsInsert(), analyticsSelect(), analyticsUpdate(), analyticsUpsert(), buildHeaders(), buildUrl()

### Community 52 - "Pwa Public Drain"
Cohesion: 0.43
Nodes (5): drainQueue(), enqueue(), isAuthEndpoint(), isSupabaseMutation(), openDB()

### Community 53 - "Oauth state Supabase"
Cohesion: 0.6
Nodes (5): decodeBase64Url(), encodeBase64Url(), getSigningSecret(), signOAuthState(), verifyOAuthState()

### Community 54 - "Error handler Supabase"
Cohesion: 0.53
Nodes (4): honoErrorHandler(), safeErrorResponse(), safeHeaders(), sanitizeError()

### Community 55 - "Estimate engine Supabase"
Cohesion: 0.4
Nodes (2): centsToUsd(), formatEstimateForPdf()

### Community 56 - "Ai matcher Supabase"
Cohesion: 0.53
Nodes (4): buildMatchingPrompt(), callClaudeForMatching(), matchTransactions(), parseAndValidateMatches()

### Community 57 - "Cogs Supabase"
Cohesion: 0.6
Nodes (5): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage()

### Community 58 - "Llm Supabase"
Cohesion: 0.6
Nodes (5): callClaudeAndWrap(), callLocal(), findActiveExperiment(), logRoutingDecision(), routeLLM()

### Community 59 - "Seed esign templates"
Cohesion: 0.53
Nodes (4): buildStatutoryFields(), dateSigned(), prefilled(), sig()

### Community 60 - "Seed Generate"
Cohesion: 0.6
Nodes (5): generateAuditLogs(), generateInvoices(), generateProvisioningSteps(), generateTransactions(), seed()

### Community 61 - "Compendium Upload notebooklm"
Cohesion: 0.6
Nodes (5): deleteMatchingSources(), getPackFiles(), loadConfig(), main(), uploadBatch()

### Community 62 - "Compendium Setup browser"
Cohesion: 0.53
Nodes (4): loadConfig(), main(), prompt(), setupProfile()

### Community 63 - "Compendium Upload claude"
Cohesion: 0.6
Nodes (5): deleteExistingFiles(), getPackFiles(), loadConfig(), main(), uploadFiles()

### Community 64 - "Cogs export Csv"
Cohesion: 0.47
Nodes (3): exportCSV(), exportJSON(), triggerBrowserDownload()

### Community 65 - "Voice presets Supabase"
Cohesion: 0.5
Nodes (2): getVoiceV3NativeConfig(), getVoiceV3WithFallbackPlan()

### Community 66 - "Routing engine Supabase"
Cohesion: 0.6
Nodes (3): estimateDriveMinutes(), haversineKm(), scoreWorker()

### Community 67 - "Cors Supabase"
Cohesion: 0.7
Nodes (4): getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors()

### Community 68 - "Tester guide docx"
Cohesion: 0.5
Nodes (4): annotate_screenshot(), build_docx(), Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re, Add red boxes and labels to a screenshot.

### Community 69 - "Playwright Url"
Cohesion: 0.6
Nodes (3): isLocalUrl(), resolveAppUrl(), resolvePortalBaseUrl()

### Community 70 - "Chief of staff Handle"
Cohesion: 0.6
Nodes (3): getConversationHistory(), handleKeyDown(), handleSend()

### Community 71 - "Gc Gcowner Fetch"
Cohesion: 0.4
Nodes (0): 

### Community 72 - "Contact Industries"
Cohesion: 0.5
Nodes (0): 

### Community 73 - "Corpus Supabase"
Cohesion: 0.83
Nodes (3): callClaude(), getModelTier(), logToCorpus()

### Community 74 - "Preference injector Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 75 - "Email Supabase"
Cohesion: 0.67
Nodes (2): getApiKey(), sendEmail()

### Community 76 - "Crypto Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 77 - "Provisioning plan Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 78 - "Rate limiter Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 79 - "Auth Supabase"
Cohesion: 0.67
Nodes (2): getSupabaseClient(), resolveAuthContext()

### Community 80 - "Connectors Factory Supabase"
Cohesion: 0.67
Nodes (2): getAdConnector(), getAllAdConnectors()

### Community 81 - "Analyze bugs Categorize"
Cohesion: 0.5
Nodes (0): 

### Community 82 - "Setup stripe addon products"
Cohesion: 0.83
Nodes (3): main(), stripeGet(), stripeRequest()

### Community 83 - "Pii Supabase"
Cohesion: 1.0
Nodes (2): containsPII(), stripPII()

### Community 84 - "Vapi owner Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 85 - "Embeddings Supabase"
Cohesion: 1.0
Nodes (2): generateEmbedding(), hashEmbedding()

### Community 86 - "Voice Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 87 - "Finalize Supabase"
Cohesion: 1.0
Nodes (2): finalizeDocumentCore(), getExistingFinalizeState()

### Community 88 - "Roof takeoff Supabase"
Cohesion: 1.0
Nodes (2): calculateTakeoff(), round2()

### Community 89 - "Input validator Supabase"
Cohesion: 1.0
Nodes (2): validateInputComplexity(), walk()

### Community 90 - "Seed finance demo"
Cohesion: 0.67
Nodes (0): 

### Community 91 - "Affiliate program Reseller"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Forwarding instructions Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Gate checks Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 94 - "Purchase access email"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Setup plan Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Vapi brain tool"
Cohesion: 1.0
Nodes (0): 

### Community 97 - "Advance Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 98 - "Area consent Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Notify Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Memory injector Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Audit Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Capture tester guide screenshots"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Seed report"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Seed demo accounts"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Preflight Run"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Wizard Wizard step5"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Demo call banner"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Finance types Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Connectors Interface Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Pentagi Pentagi flow"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (0): 

### Community 114 - "Plaid screenshots"
Cohesion: 1.0
Nodes (0): 

### Community 115 - "Tailwind"
Cohesion: 1.0
Nodes (0): 

### Community 116 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 117 - "Postcss"
Cohesion: 1.0
Nodes (0): 

### Community 118 - "Corpus Corpus"
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
- **Thin community `Community 113`** (1 nodes): `marketing-portal.spec.ts`
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
- **Should `Support Feature roadmap Analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Api Admin Clients` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Link crawler Sign` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `Api Plans Reseller` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._