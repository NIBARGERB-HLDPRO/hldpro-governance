# Graph Report - /Users/bennibarger/Developer/HLDPRO/ai-integration-services  (2026-04-09)

## Corpus Check
- Large corpus: 965 files · ~1,428,753 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

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

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (166): agentCritic(), agentIntake(), agentPackager(), agentPresenter(), agentResearcher(), alertOperator(), amortize(), applyEventFilters() (+158 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (32): getConversationHistory(), handleKeyDown(), handleSend(), handleCancel(), loadData(), handleResync(), handleSave(), extractCallFromAuditEntry() (+24 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (26): browserSignIn(), cleanupClientByEmail(), cleanupTestClient(), findAuthUsersByEmail(), findClientByEmail(), findClientsByEmail(), getAuthTokens(), isLocalUrl() (+18 more)

### Community 3 - "Community 3"
Cohesion: 0.02
Nodes (2): handleSave(), saveTargets()

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (6): extractLeadFromAuditEntry(), handleExport(), inferSource(), leadsToCSV(), formatDate(), formatTime()

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (8): trackCheckoutStarted(), trackCtaClick(), trackEvent(), trackPlanSelected(), handleSubmit(), validate(), planSavings(), planTotal()

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (29): assembleOverview(), extractSection(), readFile(), assemblePatterns(), readFileIfExists(), truncateFailFastLog(), consolidateClaudePack(), readModular() (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (7): handleSubmit(), next(), validateStep(), extractVariables(), validateVariables(), useCreatePromptVersion(), useRollbackPromptVersion()

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (1): TwentyCRMConnector

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (2): NullCRMConnector, NullServiceConnector

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (1): GHLCRMConnector

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (1): LocalCRMConnector

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (18): export_gguf(), load_dataset(), main(), parse_args(), HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:, Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format, # TODO: Implement when RunPod environment is ready, Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl (+10 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 0.16
Nodes (10): callEdgeFunction(), getStageIndex(), handleApprove(), handleCancel(), handleExecute(), handleNewBooking(), PipelineProgressBar(), fetchSyncLogs() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.21
Nodes (1): N8nClient

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (1): TwilioClient

### Community 19 - "Community 19"
Cohesion: 0.3
Nodes (1): VapiClient

### Community 20 - "Community 20"
Cohesion: 0.21
Nodes (1): VoiceflowClient

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (4): buildLegend(), parsePitch(), pitchColor(), RoofOverlay()

### Community 22 - "Community 22"
Cohesion: 0.23
Nodes (9): handleBulkApprove(), handleBulkDelete(), handleFileUpload(), handleManualSubmit(), handlePdfUpload(), handlePricingApproval(), handlePricingEdit(), handleWebScrape() (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.15
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 0.21
Nodes (7): getPitchCategory(), getPitchCategoryFromRatio(), pitchRatioToRise(), processGoogleSegments(), sqFeetToSquares(), sqMetersToSqFeet(), sqMetersToSquares()

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (9): apiCall(), handleApproveMatch(), handleConnectAccount(), handleCreateInvoice(), handleRejectMatch(), handleSendInvoice(), handleSyncTransactions(), handleTriggerMatching() (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.2
Nodes (1): GoogleCalendarConnector

### Community 27 - "Community 27"
Cohesion: 0.2
Nodes (1): ServiceTitanConnector

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (1): JobberConnector

### Community 29 - "Community 29"
Cohesion: 0.42
Nodes (10): buildOwnerName(), ensureClientProducts(), ensureCrmConfig(), ensureProvisioningSteps(), ensureReferralTracking(), finalizePortalPurchase(), nonEmpty(), shouldReplaceBusinessName() (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (1): CalcomClient

### Community 31 - "Community 31"
Cohesion: 0.42
Nodes (9): buildBaseRow(), derivePlaidDesiredTiming(), derivePlaidGate(), deriveSharedSmsA2PGate(), findA2PAssociationForNumber(), loadComplianceSignals(), nowIso(), setGateState() (+1 more)

### Community 32 - "Community 32"
Cohesion: 0.2
Nodes (2): computeSha256(), hashPdfFromUrl()

### Community 33 - "Community 33"
Cohesion: 0.29
Nodes (1): MetaAdConnector

### Community 34 - "Community 34"
Cohesion: 0.27
Nodes (1): NextdoorAdConnector

### Community 35 - "Community 35"
Cohesion: 0.22
Nodes (1): HousecallProConnector

### Community 36 - "Community 36"
Cohesion: 0.25
Nodes (5): apiFetch(), getToken(), handleSend(), handleSubmit(), handleUpload()

### Community 37 - "Community 37"
Cohesion: 0.33
Nodes (8): buildInitialSetupConnectionTaskRows(), deriveIncompleteWizardResumePath(), deriveSetupResumePath(), deriveStatusFromSignals(), isStep1Incomplete(), loadIntegrationSignals(), syncSetupConnectionTasksForClient(), withDefaultTaskState()

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (1): GoogleAdsConnector

### Community 39 - "Community 39"
Cohesion: 0.27
Nodes (5): findAdminUserByEmail(), isLocalUrl(), resolveAppUrl(), signInAndInject(), signInWithPassword()

### Community 40 - "Community 40"
Cohesion: 0.31
Nodes (5): callProvision(), runActivation(), seedActivateSteps(), supaRest(), waitForTerminal()

### Community 41 - "Community 41"
Cohesion: 0.25
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (2): calculateIRR(), calculateSavings()

### Community 43 - "Community 43"
Cohesion: 0.43
Nodes (6): createLinkToken(), exchangePublicToken(), getAccounts(), getBalance(), getBaseUrl(), plaidFetch()

### Community 44 - "Community 44"
Cohesion: 0.43
Nodes (7): assessConfidence(), emptyResults(), extractLinearMeasurements(), getTagDoubles(), getTagValue(), parseDSM(), parseTiffTags()

### Community 45 - "Community 45"
Cohesion: 0.38
Nodes (3): getVapiKey(), vapiGet(), vapiPatch()

### Community 46 - "Community 46"
Cohesion: 0.57
Nodes (6): analyticsInsert(), analyticsSelect(), analyticsUpdate(), analyticsUpsert(), buildHeaders(), buildUrl()

### Community 47 - "Community 47"
Cohesion: 0.43
Nodes (5): drainQueue(), enqueue(), isAuthEndpoint(), isSupabaseMutation(), openDB()

### Community 48 - "Community 48"
Cohesion: 0.6
Nodes (5): decodeBase64Url(), encodeBase64Url(), getSigningSecret(), signOAuthState(), verifyOAuthState()

### Community 49 - "Community 49"
Cohesion: 0.53
Nodes (4): honoErrorHandler(), safeErrorResponse(), safeHeaders(), sanitizeError()

### Community 50 - "Community 50"
Cohesion: 0.4
Nodes (2): centsToUsd(), formatEstimateForPdf()

### Community 51 - "Community 51"
Cohesion: 0.53
Nodes (4): buildMatchingPrompt(), callClaudeForMatching(), matchTransactions(), parseAndValidateMatches()

### Community 52 - "Community 52"
Cohesion: 0.6
Nodes (5): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage()

### Community 53 - "Community 53"
Cohesion: 0.6
Nodes (5): callClaudeAndWrap(), callLocal(), findActiveExperiment(), logRoutingDecision(), routeLLM()

### Community 54 - "Community 54"
Cohesion: 0.53
Nodes (4): buildStatutoryFields(), dateSigned(), prefilled(), sig()

### Community 55 - "Community 55"
Cohesion: 0.6
Nodes (5): generateAuditLogs(), generateInvoices(), generateProvisioningSteps(), generateTransactions(), seed()

### Community 56 - "Community 56"
Cohesion: 0.6
Nodes (5): deleteMatchingSources(), getPackFiles(), loadConfig(), main(), uploadBatch()

### Community 57 - "Community 57"
Cohesion: 0.53
Nodes (4): loadConfig(), main(), prompt(), setupProfile()

### Community 58 - "Community 58"
Cohesion: 0.6
Nodes (5): deleteExistingFiles(), getPackFiles(), loadConfig(), main(), uploadFiles()

### Community 59 - "Community 59"
Cohesion: 0.47
Nodes (3): exportCSV(), exportJSON(), triggerBrowserDownload()

### Community 60 - "Community 60"
Cohesion: 0.6
Nodes (3): estimateDriveMinutes(), haversineKm(), scoreWorker()

### Community 61 - "Community 61"
Cohesion: 0.7
Nodes (4): getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors()

### Community 62 - "Community 62"
Cohesion: 0.5
Nodes (4): annotate_screenshot(), build_docx(), Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re, Add red boxes and labels to a screenshot.

### Community 63 - "Community 63"
Cohesion: 0.6
Nodes (3): isLocalUrl(), resolveAppUrl(), resolvePortalBaseUrl()

### Community 64 - "Community 64"
Cohesion: 0.5
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 0.83
Nodes (3): callClaude(), getModelTier(), logToCorpus()

### Community 66 - "Community 66"
Cohesion: 0.5
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (2): getApiKey(), sendEmail()

### Community 68 - "Community 68"
Cohesion: 0.5
Nodes (0): 

### Community 69 - "Community 69"
Cohesion: 0.5
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 0.5
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (2): getSupabaseClient(), resolveAuthContext()

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (2): getAdConnector(), getAllAdConnectors()

### Community 73 - "Community 73"
Cohesion: 0.5
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 0.83
Nodes (3): main(), stripeGet(), stripeRequest()

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (2): containsPII(), stripPII()

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (2): generateEmbedding(), hashEmbedding()

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (2): finalizeDocumentCore(), getExistingFinalizeState()

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (2): calculateTakeoff(), round2()

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (2): validateInputComplexity(), walk()

### Community 82 - "Community 82"
Cohesion: 0.67
Nodes (0): 

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (0): 

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (0): 

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (0): 

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (0): 

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (0): 

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (0): 

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (0): 

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **13 isolated node(s):** `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:`, `Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format`, `Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 84`** (2 nodes): `forwarding-instructions.ts`, `buildForwardingInstructionsHtml()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (2 nodes): `gate-checks.ts`, `runGateChecks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (2 nodes): `purchase-access-email.ts`, `sendPortalAccessEmail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (2 nodes): `setup-plan.ts`, `createDefaultSetupPlan()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (2 nodes): `vapi-brain-tool.ts`, `getBrainToolDefinition()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (2 nodes): `advance.ts`, `advanceSigningWorkflow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (2 nodes): `area-code-consent.ts`, `getConsentType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (2 nodes): `notify.ts`, `notifyPartyCore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (2 nodes): `memory-injector.ts`, `fetchContext()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (2 nodes): `audit.ts`, `emitAuditLog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (2 nodes): `capture-tester-guide-screenshots.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (2 nodes): `seed-report-data.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (2 nodes): `seed-demo-accounts.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (2 nodes): `preflight-probe.spec.ts`, `runPreflight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (2 nodes): `WizardStep5.tsx`, `WizardStep5()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (2 nodes): `DemoCallBanner.tsx`, `DemoCallBanner()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (1 nodes): `config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (1 nodes): `finance-types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `interface.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (1 nodes): `pentagi-flow.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (1 nodes): `marketing-portal.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (1 nodes): `plaid-screenshots.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (1 nodes): `CorpusLayout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Community 5` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._