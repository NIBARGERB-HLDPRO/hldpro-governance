# Graph Report - .  (2026-04-09)

## Corpus Check
- Large corpus: 830 files · ~967,693 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 2361 nodes · 2958 edges · 218 communities detected
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 567 edges (avg confidence: 0.52)
- Token cost: 126,200 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `TwentyCRMConnector` - 29 edges
2. `GHLCRMConnector` - 25 edges
3. `LocalCRMConnector` - 23 edges
4. `NullCRMConnector` - 21 edges
5. `AI Integration Services Master Brief` - 20 edges
6. `N8nClient` - 15 edges
7. `TwilioClient` - 15 edges
8. `VapiClient` - 15 edges
9. `VoiceflowClient` - 14 edges
10. `Primary Navigation Tabs` - 13 edges

## Surprising Connections (you probably didn't know these)
- `AI Voice Receptionist (Product 1)` --semantically_similar_to--> `Prompt Template System (Handlebars)`  [INFERRED] [semantically similar]
  AI_INTEGRATION_SERVICES.md → docs/ARCHITECTURE.md
- `MED-001: Sanitize database schema names` --semantically_similar_to--> `Error Handler (_shared/error-handler.ts)`  [INFERRED] [semantically similar]
  docs/security-reports/2026-03-24-staging-assessment.md → scripts/compendium/PERSONA.md
- `Edge Function Registry (199 functions)` --references--> `Error Handling & Security (PentAGI Remediation)`  [INFERRED]
  REPO_EDGE_FUNCTIONS.md → docs/ARCHITECTURE.md
- `CRM + Automation System (Product 3)` --references--> `CRMConnector Abstraction Interface`  [INFERRED]
  AI_INTEGRATION_SERVICES.md → ARCHITECTURE.md
- `Phase 0: Shared Infrastructure (Routing, Estimating, PWA)` --references--> `Trades Core Vertical Addon`  [INFERRED]
  docs/VERTICAL_ADDONS_PLAN.md → AI_INTEGRATION_SERVICES.md

## Hyperedges (group relationships)
- **Five Core Products AI Integration System** — core_product_voice_receptionist, core_product_chatbot, core_product_crm, core_product_landing_pages, core_product_review_responder [EXTRACTED 1.00]
- **Platform Services Ecosystem** — platform_billing, platform_provisioning, platform_health [EXTRACTED 0.95]
- **Backend Architecture Pattern: CRMConnector + Webhook Hub** — architecture_crmconnector, webhook_receiver_hub, error_handling_security [EXTRACTED 0.90]
- **Security & Compliance Layer (Plaid, Vault, RLS)** — plaid_integration, vault_security, infosec_policy [EXTRACTED 0.95]
- **Vertical Addon Ecosystem with Phases** — vertical_addons_plan, vertical_addons_phase0, vertical_addons_phase1 [EXTRACTED 1.00]
- **Data Intelligence Analytics Pipeline** — cross_client_benchmarking, churn_risk_detection, ab_prompt_testing [EXTRACTED 0.95]
- **Infrastructure Cost Reduction Stack** — n8n_self_hosted, postal_email_server, client_provisioner_orchestration [EXTRACTED 0.95]
- **CRM Abstraction Layer Architecture** — crm_connector_interface, twenty_crm, finance_system_build_plan [EXTRACTED 0.90]
- **Defense-in-Depth Security Layers (CI → Staging → Pentest)** — ci_cd_github_actions_governance_gate, staging_first_migration_deployment, security_implementation_plan_4_phases [EXTRACTED 1.00]
- **Compliance Frameworks (HIPAA + E-SIGN + A2P 10DLC)** — hipaa_vendor_baa_checklist, esign_consent_legal_requirements, a2p_10dlc_twilio_carrier_registration [EXTRACTED 1.00]
- **Platform Infrastructure Layer (Supabase + Docker + Cloudflare)** — supabase_projects_prod_staging, docker_verified_images_20_services, cloudflare_pages_dns_4_projects [EXTRACTED 1.00]
- **Security Hardening Sprint 2 PR Pipeline** — codex_review_2026_04_06, security_hardening_sprint_2, fleet_report_2026_04_06 [EXTRACTED 0.95]
- **E-Sign Storage Modernization Pipeline** — supabase_hipaa_baseline_2026_04_07, esign_storage_hardening_2026_04_07, production_esign_rollout_2026_04_07 [EXTRACTED 1.00]
- **Data Dictionary Synchronization Audit Chain** — data_dictionary_sync_2026_04_07, data_dictionary_body_drift_2026_04_08, data_dictionary_coverage_gap [EXTRACTED 0.90]
- **Client Onboarding Core Flow** — client_onboarding_diagram, portal_provision_orchestrator, stripe_service [EXTRACTED 1.00]
- **AI Voice Ecosystem** — voice_receptionist_diagram, vapi_service, twilio_service, twenty_crm_service [EXTRACTED 0.95]
- **Vertical Addon Suite** — solar_pack_onepager, legal_pack_onepager, real_estate_pack_onepager [INFERRED 0.85]
- **Lead Management and Capture System** — feature_voice_receptionist, feature_chatbot, lead_capture_flow [EXTRACTED 1.00]
- **Reputation Management and Engagement** — feature_reviews, review_detection, review_response_auto [EXTRACTED 1.00]
- **Business Intelligence and Performance Tracking** — feature_reports, feature_rankings, ads_campaign_insights [INFERRED 0.75]
- **Third-Party Data Integration Ecosystem** — integration_jobber, integration_housecall_pro, integration_servicetitan [EXTRACTED 1.00]
- **HLD Pro Core Product Features** — business_owner_voice_receptionist_usecase, business_owner_crm_usecase, business_owner_brain_feature, business_owner_finance_feature [EXTRACTED 1.00]
- **Dashboard & Intelligence (Briefing, Reports, Assistant)** — business_owner_briefing_feature, business_owner_reports_feature, business_owner_assistant_feature [EXTRACTED 1.00]
- **Lead Re-engagement & Email Campaign Workflow** — business_owner_reactivation_usecase, business_owner_email_usecase, business_owner_crm_usecase [INFERRED 0.80]
- **Planning, Versioning & Governance Docs** — plans_readme, gc_addon_versioning_roadmap, gc_pm_board_versioning_guidelines, claude_md_conflict_resolution [EXTRACTED 1.00]
- **Industry Vertical Implementation (HVAC Focus)** — business_owner_hvac_one_pager, business_owner_voice_receptionist_usecase, business_owner_crm_usecase [EXTRACTED 1.00]
- **Security Assessment → Error Findings → Remediation Queue** — staging_assessment_report, error_disclosure_findings, med_001_schema_sanitization [EXTRACTED 1.00]
- **Demo Receptionist System Implementation** — demo_receptionist_system, alex_ai_receptionist, dallas_climate_solutions [EXTRACTED 1.00]
- **AIS Integration Ecosystem** — vapi_integration, voiceflow_integration, stripe_integration [EXTRACTED 1.00]

## Communities

### Community 0 - "Edge Function Handlers"
Cohesion: 0.01
Nodes (166): agentCritic(), agentIntake(), agentPackager(), agentPresenter(), agentResearcher(), alertOperator(), amortize(), applyEventFilters() (+158 more)

### Community 1 - "Portal UI Components"
Cohesion: 0.01
Nodes (32): getConversationHistory(), handleKeyDown(), handleSend(), handleCancel(), loadData(), handleResync(), handleSave(), extractCallFromAuditEntry() (+24 more)

### Community 2 - "Operator Dashboard Shell"
Cohesion: 0.02
Nodes (9): fetchSyncLogs(), handleManage(), handleResync(), extractLeadFromAuditEntry(), handleExport(), inferSource(), leadsToCSV(), formatDate() (+1 more)

### Community 3 - "A2P and Corpus Analytics"
Cohesion: 0.02
Nodes (2): handleSave(), saveTargets()

### Community 4 - "E2E Test Specs"
Cohesion: 0.02
Nodes (26): browserSignIn(), cleanupClientByEmail(), cleanupTestClient(), findAuthUsersByEmail(), findClientByEmail(), findClientsByEmail(), getAuthTokens(), isLocalUrl() (+18 more)

### Community 5 - "Admin Panel Hooks"
Cohesion: 0.02
Nodes (7): handleSubmit(), next(), validateStep(), extractVariables(), validateVariables(), useCreatePromptVersion(), useRollbackPromptVersion()

### Community 6 - "Product Brief Concepts"
Cohesion: 0.03
Nodes (65): Ad Intelligence Platform, Business Brain RAG System, COGS Tracking System (3-layer), Corpus Infrastructure (v1.5), Personal AI Chief of Staff, Email Assistant v2, E-Signature Platform, Finance System with Plaid (+57 more)

### Community 7 - "Marketing Site Billing"
Cohesion: 0.04
Nodes (6): trackCheckoutStarted(), trackCtaClick(), trackEvent(), trackPlanSelected(), handleSubmit(), validate()

### Community 8 - "Codex Ingestion Pipeline"
Cohesion: 0.08
Nodes (29): assembleOverview(), extractSection(), readFile(), assemblePatterns(), readFileIfExists(), truncateFailFastLog(), consolidateClaudePack(), readModular() (+21 more)

### Community 9 - "Twenty CRM Connector"
Cohesion: 0.11
Nodes (1): TwentyCRMConnector

### Community 10 - "Null CRM Connector"
Cohesion: 0.09
Nodes (2): NullCRMConnector, NullServiceConnector

### Community 11 - "Architecture Diagrams"
Cohesion: 0.12
Nodes (28): Auto Repair Shop AI Assistant, Cal.com (Scheduling), Claude Haiku Model, Claude Sonnet Model, Client Onboarding Pipeline, E-Signature Platform, Email System, Google Business Profile (+20 more)

### Community 12 - "Marketing Landing Page"
Cohesion: 0.08
Nodes (2): planSavings(), planTotal()

### Community 13 - "Dashboard Home Wireframe"
Cohesion: 0.08
Nodes (27): Ad Creatives Feature, AI Assistant Tab, AI Voice Receptionist Feature, Appointments Booked Metric, Billing Tab, Business Brain Tab, Calls Answered Metric, Calls Tab (+19 more)

### Community 14 - "GHL CRM Connector"
Cohesion: 0.14
Nodes (1): GHLCRMConnector

### Community 15 - "Local CRM Connector"
Cohesion: 0.11
Nodes (1): LocalCRMConnector

### Community 16 - "Feature Narratives"
Cohesion: 0.13
Nodes (21): Automated Follow-up Sequences, Bilingual AI System, Reactivation Campaigns, AI Chatbot Widget, CRM and Lead Management, Keyword Rank Tracking, Monthly AI Performance Reports, AI Review Responder (+13 more)

### Community 17 - "Qwen3 LoRA Training"
Cohesion: 0.14
Nodes (18): export_gguf(), load_dataset(), main(), parse_args(), HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:, Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format, # TODO: Implement when RunPod environment is ready, Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl (+10 more)

### Community 18 - "Demo Receptionist KB"
Cohesion: 0.11
Nodes (18): Alex — AI Voice Receptionist, Bright Smile Dental (DFW Demo Persona), Comfort Pro HVAC (DFW Demo Persona), Dallas Climate Solutions (HVAC Company), Dallas Climate Solutions Phone (972-555-0188), Dallas Climate Solutions Service Area (25-mile DFW radius), Demo Receptionist Knowledge Base, HLD Pro AI Receptionist Demo (+10 more)

### Community 19 - "n8n Workflow Client"
Cohesion: 0.21
Nodes (1): N8nClient

### Community 20 - "Twilio SMS Client"
Cohesion: 0.22
Nodes (1): TwilioClient

### Community 21 - "VAPI Voice Client"
Cohesion: 0.3
Nodes (1): VapiClient

### Community 22 - "Referral Admin System"
Cohesion: 0.12
Nodes (0): 

### Community 23 - "Voiceflow Chat Client"
Cohesion: 0.21
Nodes (1): VoiceflowClient

### Community 24 - "Governance Context Sync"
Cohesion: 0.26
Nodes (12): buildFilePath(), buildMarkdown(), createBranch(), encodeBase64Utf8(), ensureBranch(), ensurePullRequest(), getBranchSha(), getExistingFileSha() (+4 more)

### Community 25 - "Brain Dashboard UI"
Cohesion: 0.23
Nodes (9): handleBulkApprove(), handleBulkDelete(), handleFileUpload(), handleManualSubmit(), handlePdfUpload(), handlePricingApproval(), handlePricingEdit(), handleWebScrape() (+1 more)

### Community 26 - "Setup Readiness Derive"
Cohesion: 0.15
Nodes (0): 

### Community 27 - "Roof Math Calculations"
Cohesion: 0.21
Nodes (7): getPitchCategory(), getPitchCategoryFromRatio(), pitchRatioToRise(), processGoogleSegments(), sqFeetToSquares(), sqMetersToSqFeet(), sqMetersToSquares()

### Community 28 - "Finance Dashboard UI"
Cohesion: 0.33
Nodes (9): apiCall(), handleApproveMatch(), handleConnectAccount(), handleCreateInvoice(), handleRejectMatch(), handleSendInvoice(), handleSyncTransactions(), handleTriggerMatching() (+1 more)

### Community 29 - "Google Calendar Connector"
Cohesion: 0.2
Nodes (1): GoogleCalendarConnector

### Community 30 - "ServiceTitan Connector"
Cohesion: 0.2
Nodes (1): ServiceTitanConnector

### Community 31 - "Jobber Connector"
Cohesion: 0.18
Nodes (1): JobberConnector

### Community 32 - "Compliance and Legal"
Cohesion: 0.18
Nodes (12): A2P 10DLC Carrier Registration (Twilio + TCR workflow), Certificate of Completion (bundled audit evidence), Compliance Implementation (HIPAA, E-SIGN, A2P, SOC 2), E-SIGN Compliance (4 legal requirements: intent, consent, association, retention), Native E-Signature Platform (Phase 0-S), healthcare_data Schema (separate PHI storage with stricter RLS), HIPAA Vendor BAA Checklist (Supabase, Anthropic, VAPI, Twilio), PHI Access Log (immutable, 6-year retention minimum) (+4 more)

### Community 33 - "Business Owner Features"
Cohesion: 0.21
Nodes (12): AI Assistant Feature (Account-Aware), Business Brain: RAG Pricing Intelligence, Morning Briefing & Dashboard Home, CRM + Automation: 2 AM Lead Capture, Email Campaigns & AI Inbox Triage, Finance Dashboard: Bank, Invoices, AI Reconciliation, HVAC One-Pager: Stop Losing Jobs to Voicemail, Reactivation Engine: Warm Lead Re-engagement (+4 more)

### Community 34 - "Portal Purchase Flow"
Cohesion: 0.42
Nodes (10): buildOwnerName(), ensureClientProducts(), ensureCrmConfig(), ensureProvisioningSteps(), ensureReferralTracking(), finalizePortalPurchase(), nonEmpty(), shouldReplaceBusinessName() (+2 more)

### Community 35 - "Cal.com Booking Client"
Cohesion: 0.29
Nodes (1): CalcomClient

### Community 36 - "Compliance Gates Sync"
Cohesion: 0.42
Nodes (9): buildBaseRow(), derivePlaidDesiredTiming(), derivePlaidGate(), deriveSharedSmsA2PGate(), findA2PAssociationForNumber(), loadComplianceSignals(), nowIso(), setGateState() (+1 more)

### Community 37 - "E-Signature Core"
Cohesion: 0.2
Nodes (2): computeSha256(), hashPdfFromUrl()

### Community 38 - "Meta Ads Connector"
Cohesion: 0.29
Nodes (1): MetaAdConnector

### Community 39 - "Nextdoor Ads Connector"
Cohesion: 0.27
Nodes (1): NextdoorAdConnector

### Community 40 - "HouseCall Pro Connector"
Cohesion: 0.22
Nodes (1): HousecallProConnector

### Community 41 - "GC Sub Portal UI"
Cohesion: 0.25
Nodes (5): apiFetch(), getToken(), handleSend(), handleSubmit(), handleUpload()

### Community 42 - "Error State Screens"
Cohesion: 0.18
Nodes (11): MFA Gate Redirect Error State, Plaid Consent/Finance 404 Error Screen, Plan Selection 404 Error State, 404 Not Found HTTP Response, 404 NOT_FOUND HTTP Status, Deployment Not Found Error, Error Code: DEPLOYMENT_NOT_FOUND, Error ID: cle1::pzxlt-1775510040134-079548777486 (+3 more)

### Community 43 - "Setup Connection Tasks"
Cohesion: 0.33
Nodes (8): buildInitialSetupConnectionTaskRows(), deriveIncompleteWizardResumePath(), deriveSetupResumePath(), deriveStatusFromSignals(), isStep1Incomplete(), loadIntegrationSignals(), syncSetupConnectionTasksForClient(), withDefaultTaskState()

### Community 44 - "Google Ads Connector"
Cohesion: 0.29
Nodes (1): GoogleAdsConnector

### Community 45 - "Live E2E Full Spec"
Cohesion: 0.27
Nodes (5): findAdminUserByEmail(), isLocalUrl(), resolveAppUrl(), signInAndInject(), signInWithPassword()

### Community 46 - "Load Test Provisioning"
Cohesion: 0.31
Nodes (5): callProvision(), runActivation(), seedActivateSteps(), supaRest(), waitForTerminal()

### Community 47 - "Roof Overlay Renderer"
Cohesion: 0.31
Nodes (4): buildLegend(), parsePitch(), pitchColor(), RoofOverlay()

### Community 48 - "Upgrade Feature Set"
Cohesion: 0.22
Nodes (9): AI Review Response Automation (Claude-generated responses), Google Review Request Automation (2hr delayed SMS), Missed Call Text Back (auto SMS within 15s), AI Monthly Performance Report (Claude-generated narratives), Competitive Rank Tracker (Google Maps weekly rankings), Reactivation Campaigns (quarterly stale contact outreach), Upgrade Implementation (8 Features Across Tiers), AI Voicemail Transcription + Auto-Followup (+1 more)

### Community 49 - "Product Plan Tiers"
Cohesion: 0.31
Nodes (9): AI Chatbot Widget Product, CRM & Automation System Product, Elite Plan ($997/mo), HLD Pro Platform Overview, Pro Plan ($597/mo), Reactivation Campaigns Product, AI Review Responder Product, Starter Plan ($297/mo) (+1 more)

### Community 50 - "Vault Secrets Manager"
Cohesion: 0.25
Nodes (0): 

### Community 51 - "Solar Savings Calculator"
Cohesion: 0.29
Nodes (2): calculateIRR(), calculateSavings()

### Community 52 - "Plaid Banking Client"
Cohesion: 0.43
Nodes (6): createLinkToken(), exchangePublicToken(), getAccounts(), getBalance(), getBaseUrl(), plaidFetch()

### Community 53 - "GeoTIFF DSM Processor"
Cohesion: 0.43
Nodes (7): assessConfidence(), emptyResults(), extractLinearMeasurements(), getTagDoubles(), getTagValue(), parseDSM(), parseTiffTags()

### Community 54 - "Booking Pipeline UI"
Cohesion: 0.43
Nodes (7): callEdgeFunction(), getStageIndex(), handleApprove(), handleCancel(), handleExecute(), handleNewBooking(), PipelineProgressBar()

### Community 55 - "Platform Progress Tracker"
Cohesion: 0.25
Nodes (8): Ad Intelligence Platform Phase 1 (Meta, Google, Nextdoor OAuth), Email Assistant (Gmail/Outlook OAuth with zero body storage), Feature Registry (AIS Platform Capabilities), Health & Alerts (8-service API monitoring with SMS/email), MiroFish Simulation Engine (Claude tool_use persona simulation), Platform Progress Summary (2026-03-26 Session), V1 Alpha Launch Prep (feature gating and beta badges), VAPI SMS Integration (outbound SMS during calls + inbound AI replies)

### Community 56 - "Security Audit Findings"
Cohesion: 0.25
Nodes (8): Brain Query Using Claude as Fake Embedding Model, Codex-Style Code Review 2026-04-06, Codex Reviewer — HLD Pro Second-Opinion Agent, 6 Functions Missing verify_jwt in config.toml, Security Code Review Findings, Security Hardening Sprint 2, Stripe Webhook Timing Attack Vulnerability, Wildcard CORS in 22 Edge Functions

### Community 57 - "VAPI Helper Utilities"
Cohesion: 0.38
Nodes (3): getVapiKey(), vapiGet(), vapiPatch()

### Community 58 - "Analytics DB Layer"
Cohesion: 0.57
Nodes (6): analyticsInsert(), analyticsSelect(), analyticsUpdate(), analyticsUpsert(), buildHeaders(), buildUrl()

### Community 59 - "Service Worker Queue"
Cohesion: 0.43
Nodes (5): drainQueue(), enqueue(), isAuthEndpoint(), isSupabaseMutation(), openDB()

### Community 60 - "Infrastructure Inventory"
Cohesion: 0.29
Nodes (7): Cloudflare Pages & DNS (hldpro.com, dashboard, reseller, pwa), Docker Verified Images (n8n, Twenty, Bigcapital, etc.), Edge Functions (166+ functions across all domains), Service Registry (Verified Names and Endpoints), Stripe Live Products (Starter/Professional/Elite pricing), Supabase Projects (Production + Staging), VAPI Assistants & Phone Numbers (Bilingual squad)

### Community 61 - "Login Pricing Screen"
Cohesion: 0.38
Nodes (7): AI-Powered Business System, 7 Day Free Trial Banner, Get Started Call-to-Action Buttons, Plaid Login Failed Screen, Elite Pricing Tier ($997), Professional Pricing Tier, Starter Pricing Tier ($297)

### Community 62 - "OAuth State Signing"
Cohesion: 0.6
Nodes (5): decodeBase64Url(), encodeBase64Url(), getSigningSecret(), signOAuthState(), verifyOAuthState()

### Community 63 - "Error Handler Middleware"
Cohesion: 0.53
Nodes (4): honoErrorHandler(), safeErrorResponse(), safeHeaders(), sanitizeError()

### Community 64 - "Estimate Engine Logic"
Cohesion: 0.4
Nodes (2): centsToUsd(), formatEstimateForPdf()

### Community 65 - "AI Transaction Matcher"
Cohesion: 0.53
Nodes (4): buildMatchingPrompt(), callClaudeForMatching(), matchTransactions(), parseAndValidateMatches()

### Community 66 - "COGS Event Tracker"
Cohesion: 0.6
Nodes (5): currentBillingPeriod(), emitCacheHit(), emitCOGS(), getModelTier(), trackClaudeUsage()

### Community 67 - "LLM Router AB Testing"
Cohesion: 0.6
Nodes (5): callClaudeAndWrap(), callLocal(), findActiveExperiment(), logRoutingDecision(), routeLLM()

### Community 68 - "E-Sign Template Seeder"
Cohesion: 0.53
Nodes (4): buildStatutoryFields(), dateSigned(), prefilled(), sig()

### Community 69 - "Staging Data Seeder"
Cohesion: 0.6
Nodes (5): generateAuditLogs(), generateInvoices(), generateProvisioningSteps(), generateTransactions(), seed()

### Community 70 - "NotebookLM Uploader"
Cohesion: 0.6
Nodes (5): deleteMatchingSources(), getPackFiles(), loadConfig(), main(), uploadBatch()

### Community 71 - "Browser Setup Script"
Cohesion: 0.53
Nodes (4): loadConfig(), main(), prompt(), setupProfile()

### Community 72 - "Claude Project Uploader"
Cohesion: 0.6
Nodes (5): deleteExistingFiles(), getPackFiles(), loadConfig(), main(), uploadFiles()

### Community 73 - "COGS Export Generator"
Cohesion: 0.47
Nodes (3): exportCSV(), exportJSON(), triggerBrowserDownload()

### Community 74 - "Security Access Control"
Cohesion: 0.4
Nodes (6): Zero Trust Access Control Architecture, Audit Log Architecture (INSERT-only, no modification), OAuth Token Refresh with Mutex Locking, Role-Based Access Control via Row Level Security, Supabase Vault for Credential Storage and Edge Function Access, Webhook Signature Verification (VAPI, Twilio, Cal.com, Voiceflow)

### Community 75 - "CI/CD Deploy Pipeline"
Cohesion: 0.33
Nodes (6): CI/CD Pipeline (GitHub Actions with governance checks), Cloudflare Pages Frontend Deployment (hldpro.com, dashboard, reseller, pwa), Staging-First Deployment Pipeline, Edge Function Deployment with Staging Verification, Secrets Synchronization with Stripe Live Key Hardening, Staging-First Deployment Pattern (test before production)

### Community 76 - "E-Sign Storage Hardening"
Cohesion: 0.33
Nodes (6): E-Sign Bucket Privacy Flip (Public to Private), E-Sign Public Bucket (Storage Infrastructure), E-Sign Storage Hardening Impact Assessment, BAA Agreements Table (Healthcare Data), Production E-Sign Rollout Verification 2026-04-07, Supabase HIPAA Baseline Assessment

### Community 77 - "Overlord Audit Findings"
Cohesion: 0.33
Nodes (6): check-errors.sh uses set -euo pipefail (Bug), Gitleaks Scan Non-Blocking (|| true), Governance Drift Findings, npm audit Non-Blocking (continue-on-error), Overlord Deep Audit 2026-04-06, Overlord Governance Score 21/22

### Community 78 - "Integration Connectors"
Cohesion: 0.33
Nodes (6): Business Brain Pricing Intelligence, Housecall Pro Integration, Jobber Integration, QuickBooks Integration, ServiceTitan Integration, ServiceConnector Integrations Feature

### Community 79 - "Dashboard Calls Page"
Cohesion: 0.33
Nodes (6): Dashboard Calls Page, AI Receptionist Feature, Calls Section, Dashboard Navigation Tabs, Empty State Message, Search and Filter Controls

### Community 80 - "Onboarding Wizard Steps"
Cohesion: 0.33
Nodes (6): Call-to-Action Button, Dark Theme Design System, HelpPro Partners Page UI, Top Navigation Bar, Subheading: Without Adding Headcount, Value Proposition: $82k/Year Revenue Addition

### Community 81 - "Trial Lifecycle Billing"
Cohesion: 0.33
Nodes (6): Data Usage Section, Footer with Links, Information Collection Section, Page Header with Branding, Policy Section List, Privacy Policy Page

### Community 82 - "Notification Dispatcher"
Cohesion: 0.4
Nodes (6): Call-to-Action Buttons - Primary Actions, Visual Design - Dark Theme, Blue Accent Colors, Feature Cards - Real-Time Data, Institutional Access, Integration, Footer Navigation - Legal, Support, Product Links, Hero Section - Financial Data Partnership, Value Propositions - Security, Compliance, API Access

### Community 83 - "Prompt Template Engine"
Cohesion: 0.4
Nodes (6): Action Controls (Pipeline, Add Contact, Export), AI Assistant Feature, Dashboard Leads View, Empty State Message, Leads & Contacts Section, Navigation Tabs

### Community 84 - "Worker Routing Engine"
Cohesion: 0.6
Nodes (3): estimateDriveMinutes(), haversineKm(), scoreWorker()

### Community 85 - "CORS Security Headers"
Cohesion: 0.7
Nodes (4): getAllowedOrigins(), getCorsHeaders(), getSecurityHeaders(), handleCors()

### Community 86 - "Tester Guide Builder"
Cohesion: 0.5
Nodes (4): annotate_screenshot(), build_docx(), Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re, Add red boxes and labels to a screenshot.

### Community 87 - "Playwright Test Config"
Cohesion: 0.6
Nodes (3): isLocalUrl(), resolveAppUrl(), resolvePortalBaseUrl()

### Community 88 - "GC Owner Portal UI"
Cohesion: 0.4
Nodes (0): 

### Community 89 - "Provisioning Runbook"
Cohesion: 0.4
Nodes (5): Client Provisioner Orchestration Function, Cost Reduction Plan, n8n Self-Hosted Automation Engine, Postal Self-Hosted Email Server, Provisioning Pipeline Runbook

### Community 90 - "Data Intelligence Plan"
Cohesion: 0.4
Nodes (5): A/B Prompt Testing Infrastructure, Analytics Data Dictionary, Churn Risk Detection Scoring Model, Cross-Client Benchmarking Engine, Data Intelligence Engine Implementation Plan

### Community 91 - "Roof Measurement Engine"
Cohesion: 0.4
Nodes (5): GeoTIFF Processing (DSM edge detection for ridge/valley/eave/hip), NRCA Waste Factor Lookup (pitch + complexity → waste %), buildingInsights API (roof area, pitch, azimuth from satellite), Roof Measurement Engine (Google Solar API + GeoTIFF), Xactimate-Compatible Scope Output (RFG category codes)

### Community 92 - "Customer Signup Workflow"
Cohesion: 0.4
Nodes (5): A2P Customer Signup Workflow (SMS Onboarding), GC Addon Pack Versioning Roadmap, GC PM Board Versioning & Release Guidelines, HLD Pro Full Customer Provisioning Automation Plan, Plan Ingestion Pipeline & Backlog Status

### Community 93 - "Brain Upload UI"
Cohesion: 0.6
Nodes (5): Business Brain Dashboard UI, AI Assistant Feature, Business Brain Feature, Dashboard Navigation Menu, Data Upload Capability

### Community 94 - "Corpus LLM Logger"
Cohesion: 0.83
Nodes (3): callClaude(), getModelTier(), logToCorpus()

### Community 95 - "Preference Injector"
Cohesion: 0.5
Nodes (0): 

### Community 96 - "Email Sender Utility"
Cohesion: 0.67
Nodes (2): getApiKey(), sendEmail()

### Community 97 - "Crypto HMAC Utilities"
Cohesion: 0.5
Nodes (0): 

### Community 98 - "Provisioning Step Plan"
Cohesion: 0.5
Nodes (0): 

### Community 99 - "Rate Limiter Guard"
Cohesion: 0.5
Nodes (0): 

### Community 100 - "Auth Client Factory"
Cohesion: 0.67
Nodes (2): getSupabaseClient(), resolveAuthContext()

### Community 101 - "Ad Connector Factory"
Cohesion: 0.67
Nodes (2): getAdConnector(), getAllAdConnectors()

### Community 102 - "Bug Analyzer Script"
Cohesion: 0.5
Nodes (0): 

### Community 103 - "Stripe Addon Setup"
Cohesion: 0.83
Nodes (3): main(), stripeGet(), stripeRequest()

### Community 104 - "Demo Voice Config"
Cohesion: 0.5
Nodes (4): Demo Voice Receptionist Implementation Plan, Demo Voice Receptionist Sales Asset, ElevenLabs Flash v2.5 TTS Provider, VAPI Squad Bilingual Configuration

### Community 105 - "Portal Provision Triggers"
Cohesion: 0.67
Nodes (4): portal-provision Edge Function (step-based dispatch engine), Client Onboarding Portal (5-Phase Sprint Plan), Deferred Provisioning Queue (pgmq for blocked steps), Track A Immediate Provisioning (payment_complete trigger)

### Community 106 - "Release Roadmap Versions"
Cohesion: 0.5
Nodes (4): Release Roadmap (v1.4 through v2.0), v1.4 Current Sprint (bug fixes and in-progress items), v1.5 CoS Foundation (corpus infrastructure + preference model), v1.6 CoS Proactive + Reactive (monitoring and conversation)

### Community 107 - "Analytics Runbook"
Cohesion: 0.5
Nodes (4): Data Intelligence Engine (Analytics Runbook), Churn Risk Scorer (5-component risk model with weighting), CRM Analytics Job (call statistics and performance metrics), Transcript Analyzer (Claude Haiku token costing and cost tracking)

### Community 108 - "MFA Enrollment Error"
Cohesion: 0.67
Nodes (4): 404 Not Found Error, Deployment Not Found Error, Error Message Information Box, MFA Enrollment Error Screen

### Community 109 - "Finance Plaid Error"
Cohesion: 0.5
Nodes (4): 404 NOT_FOUND Error Page, Finance Dashboard Plaid Link - Deployment Error, DEPLOYMENT_NOT_FOUND Error Code, Deployment Not Found - Error Message

### Community 110 - "TOS Signup Error"
Cohesion: 0.5
Nodes (4): ToS Acceptance Signup - Error Screen, 404 Not Found Error, DEPLOYMENT_NOT_FOUND Error Code, Error Help Message with Documentation Link

### Community 111 - "PWA App Icons"
Cohesion: 0.5
Nodes (4): PWA App Logo Icon (192px), PWA App Icon (512x512), Letter H Branding Symbol, Progressive Web App

### Community 112 - "PII Detector"
Cohesion: 1.0
Nodes (2): containsPII(), stripPII()

### Community 113 - "VAPI Owner Tools"
Cohesion: 0.67
Nodes (0): 

### Community 114 - "Embedding Generator"
Cohesion: 1.0
Nodes (2): generateEmbedding(), hashEmbedding()

### Community 115 - "Voice Config Merger"
Cohesion: 0.67
Nodes (0): 

### Community 116 - "Document Finalizer"
Cohesion: 1.0
Nodes (2): finalizeDocumentCore(), getExistingFinalizeState()

### Community 117 - "Roof Takeoff Calc"
Cohesion: 1.0
Nodes (2): calculateTakeoff(), round2()

### Community 118 - "Input Validator"
Cohesion: 1.0
Nodes (2): validateInputComplexity(), walk()

### Community 119 - "Finance Demo Seeder"
Cohesion: 0.67
Nodes (0): 

### Community 120 - "Affiliate Program UI"
Cohesion: 0.67
Nodes (0): 

### Community 121 - "Solar Vertical Addon"
Cohesion: 0.67
Nodes (3): Google Solar API Integration, Solar Proposal Generation Engine, Solar Panel Sales Vertical Addon Plan

### Community 122 - "Auth RLS Bug Reports"
Cohesion: 0.67
Nodes (3): Alexander Bug Report (2026-04-03), auth.users in RLS Policies Error Pattern, RLS Policy Gaps Error Pattern

### Community 123 - "AI Dashboard Assistant"
Cohesion: 0.67
Nodes (3): Backoffice AI Assistant Dashboard Widget, Backoffice AI Assistant Implementation Plan, Voice Capture with Web Speech API

### Community 124 - "Plaid MFA Auth"
Cohesion: 0.67
Nodes (3): Plaid MFA Security Requirement, Plaid Security Questionnaire Responses, WebAuthn Passkey Implementation for MFA

### Community 125 - "Pricing Intelligence"
Cohesion: 0.67
Nodes (3): Magic Link Invitations (72hr expiry, SMS + email deep-link), Pricing Intelligence Portal (Market-Rate Templates), Pricing Intelligence (quarterly refresh with >10% drift detection)

### Community 126 - "GitHub Project Workflow"
Cohesion: 0.67
Nodes (3): GitHub Issues + Projects Board (daily/weekly workflow), Project Management Quick Reference (GitHub Issues/Projects), WIP Limits (max 3 In Progress items enforced)

### Community 127 - "Data Dictionary Drift"
Cohesion: 0.67
Nodes (3): Data Dictionary Body Drift Report 2026-04-08, Data Dictionary Coverage Gap, Data Dictionary Sync Report 2026-04-07

### Community 128 - "PentAGI Automation"
Cohesion: 0.67
Nodes (3): PentAGI Automation Runbook, PentAGI Droplet (104.248.60.107), PentAGI GraphQL API

### Community 129 - "Forwarding Instructions"
Cohesion: 1.0
Nodes (0): 

### Community 130 - "Gate Check Runner"
Cohesion: 1.0
Nodes (0): 

### Community 131 - "Purchase Access Email"
Cohesion: 1.0
Nodes (0): 

### Community 132 - "Setup Plan Creator"
Cohesion: 1.0
Nodes (0): 

### Community 133 - "VAPI Brain Tool"
Cohesion: 1.0
Nodes (0): 

### Community 134 - "Signing Workflow Advance"
Cohesion: 1.0
Nodes (0): 

### Community 135 - "Area Code Consent"
Cohesion: 1.0
Nodes (0): 

### Community 136 - "Party Notification Core"
Cohesion: 1.0
Nodes (0): 

### Community 137 - "Memory Context Injector"
Cohesion: 1.0
Nodes (0): 

### Community 138 - "Audit Log Emitter"
Cohesion: 1.0
Nodes (0): 

### Community 139 - "Screenshot Capture Script"
Cohesion: 1.0
Nodes (0): 

### Community 140 - "Report Data Seeder"
Cohesion: 1.0
Nodes (0): 

### Community 141 - "Demo Account Seeder"
Cohesion: 1.0
Nodes (0): 

### Community 142 - "Preflight Probe Spec"
Cohesion: 1.0
Nodes (0): 

### Community 143 - "Wizard Step Five"
Cohesion: 1.0
Nodes (0): 

### Community 144 - "Demo Call Banner"
Cohesion: 1.0
Nodes (0): 

### Community 145 - "Admin Portal Plan"
Cohesion: 1.0
Nodes (2): Admin Back Office & Client Portal Plan, Deprecated Portal Warning

### Community 146 - "Marketing Site Plan"
Cohesion: 1.0
Nodes (2): Marketing Website Plan (hldpro.com), Partners Subdomain & Reseller Marketing Plan

### Community 147 - "Support Ticket System"
Cohesion: 1.0
Nodes (2): Customer Support and Ticket Portal Plan, Support Ticket Portal System

### Community 148 - "Competitive Value Pricing"
Cohesion: 1.0
Nodes (2): Competitive Value Proposition (feature/price comparison vs tools), Value Stack Implementation (Competitive Differentiation)

### Community 149 - "Demo Assistant Config"
Cohesion: 1.0
Nodes (2): Demo Assistant Alex (8-industry expansion with pricing), Industry-Aware Demo Assistant (8-Industry Expansion)

### Community 150 - "Cross-Trade Marketplace"
Cohesion: 1.0
Nodes (2): Cross-Trade Marketplace — Architecture Diagram, Cross-Trade Marketplace System

### Community 151 - "Analytics Reporting System"
Cohesion: 1.0
Nodes (2): Analytics and Reporting System — Architecture Diagram, Analytics and Reporting System

### Community 152 - "AI Assistant System"
Cohesion: 1.0
Nodes (2): AI Chat Assistant — Product Data-Flow Diagram, AI Chat Assistant System

### Community 153 - "Support Referral System"
Cohesion: 1.0
Nodes (2): Support + Referral System — Architecture Diagram, Support + Referral System

### Community 154 - "Business Brain System"
Cohesion: 1.0
Nodes (2): Business Brain — System Architecture Diagram, Business Brain System (RAG + Pricing)

### Community 155 - "Finance System Hub"
Cohesion: 1.0
Nodes (2): Finance System — Integration Topology Diagram, Finance System (finance-api Hub)

### Community 156 - "Ad Intelligence System"
Cohesion: 1.0
Nodes (2): Ad Creatives & Campaign Management — System Architecture Diagram, Ad Intelligence and Creatives System

### Community 157 - "Service Connector System"
Cohesion: 1.0
Nodes (2): ServiceConnector System (Field Service Integration), ServiceConnector — System Architecture Diagram

### Community 158 - "CRM Automation System"
Cohesion: 1.0
Nodes (2): CRM + Automation Data-Flow Diagram, CRM + Automation System

### Community 159 - "E2E Test Results"
Cohesion: 1.0
Nodes (2): E2E Test Results (2026-03-26), E2E Test Results (2026-04-07)

### Community 160 - "Ad Campaign Insights"
Cohesion: 1.0
Nodes (2): AI Ad Campaign Intelligence, Google and Facebook Ads Use Case

### Community 161 - "HIPAA Security Audit"
Cohesion: 1.0
Nodes (2): Supabase HIPAA Exposure Audit Runbook, Supabase Security + HIPAA Readiness Plan v3.1

### Community 162 - "Webhook Receiver Security"
Cohesion: 1.0
Nodes (2): webhook-receiver Edge Function, WEBHOOK SIGNATURE BYPASS Test

### Community 163 - "Checkout Session Security"
Cohesion: 1.0
Nodes (2): CHECKOUT INJECTION Test, checkout-session Edge Function

### Community 164 - "Config"
Cohesion: 1.0
Nodes (0): 

### Community 165 - "Finance Types"
Cohesion: 1.0
Nodes (0): 

### Community 166 - "Interface"
Cohesion: 1.0
Nodes (0): 

### Community 167 - "Pentagi Flow Spec"
Cohesion: 1.0
Nodes (0): 

### Community 168 - "Vite Env D"
Cohesion: 1.0
Nodes (0): 

### Community 169 - "Marketing Portal Spec"
Cohesion: 1.0
Nodes (0): 

### Community 170 - "Plaid Screenshots Spec"
Cohesion: 1.0
Nodes (0): 

### Community 171 - "Tailwind Config"
Cohesion: 1.0
Nodes (0): 

### Community 172 - "Vite Config"
Cohesion: 1.0
Nodes (0): 

### Community 173 - "Postcss Config"
Cohesion: 1.0
Nodes (0): 

### Community 174 - "Corpuslayout"
Cohesion: 1.0
Nodes (0): 

### Community 175 - "Vertical Hvac"
Cohesion: 1.0
Nodes (1): HVAC Vertical Addon

### Community 176 - "Vertical Roofing"
Cohesion: 1.0
Nodes (1): Roofing Vertical Addon

### Community 177 - "Vertical Solar"
Cohesion: 1.0
Nodes (1): Solar Vertical Addon

### Community 178 - "Vertical Legal"
Cohesion: 1.0
Nodes (1): Legal Vertical Addon

### Community 179 - "Platform Billing"
Cohesion: 1.0
Nodes (1): Billing Service

### Community 180 - "Platform Provisioning"
Cohesion: 1.0
Nodes (1): Provisioning Service (21-step orchestrator)

### Community 181 - "Platform Health"
Cohesion: 1.0
Nodes (1): Health Check Service

### Community 182 - "Data Dictionary"
Cohesion: 1.0
Nodes (1): Data Dictionary - Schema Reference

### Community 183 - "Business Brain Plan"
Cohesion: 1.0
Nodes (1): Business Brain - RAG Pricing Intelligence Plan

### Community 184 - "Architecture Doc"
Cohesion: 1.0
Nodes (1): Architecture Document

### Community 185 - "Tester Guide"
Cohesion: 1.0
Nodes (1): HLD Pro v1.0 Alpha Tester Guide

### Community 186 - "Error Patterns"
Cohesion: 1.0
Nodes (1): Error Patterns Index

### Community 187 - "Bilingual Tts Plan"
Cohesion: 1.0
Nodes (1): Bilingual AI Voice TTS Decision Plan

### Community 188 - "Integration Sandbox Guide"
Cohesion: 1.0
Nodes (1): Integration Sandbox and Testing Guide

### Community 189 - "Vercel Deployment Runbook"
Cohesion: 1.0
Nodes (1): Vercel Deployment Runbook

### Community 190 - "Beta Launch Plan"
Cohesion: 1.0
Nodes (1): Beta Launch Plan for hldpro.com

### Community 191 - "Session Summary 2026 03 25"
Cohesion: 1.0
Nodes (1): Session Summary 2026-03-25

### Community 192 - "Pentagi Setup"
Cohesion: 1.0
Nodes (1): PentAGI Operations Guide

### Community 193 - "Wrong Codebase Edits Pattern"
Cohesion: 1.0
Nodes (1): Wrong Codebase Edits Error Pattern

### Community 194 - "A2P 10Dlc Campaign Registra..."
Cohesion: 1.0
Nodes (1): A2P 10DLC Campaign Registration (Twilio SMS)

### Community 195 - "Security Implementation Pla..."
Cohesion: 1.0
Nodes (1): Security Implementation Plan (GitHub + Staging + Audit Skill + PentAGI)

### Community 196 - "Rollback Procedures Emergen..."
Cohesion: 1.0
Nodes (1): Rollback Procedures (Emergency Recovery)

### Community 197 - "Cross Repo Deps Shared Supa..."
Cohesion: 1.0
Nodes (1): Cross-Repo Dependencies (Shared Infrastructure)

### Community 198 - "Benchmark Compute Industry ..."
Cohesion: 1.0
Nodes (1): Benchmark Compute (industry competitor comparison)

### Community 199 - "Fail Fast Log Document"
Cohesion: 1.0
Nodes (0): 

### Community 200 - "Fleet Report 2026 04 06"
Cohesion: 1.0
Nodes (1): Fleet Health Report 2026-04-06

### Community 201 - "Design References Readme"
Cohesion: 1.0
Nodes (1): HLD Pro Design References

### Community 202 - "Kb 05 Support"
Cohesion: 1.0
Nodes (1): HLD Pro Support and Ticket System

### Community 203 - "Kb 09 Rankings"
Cohesion: 1.0
Nodes (1): HLD Pro Rankings and SEO Tracking

### Community 204 - "Kb 13 Bilingual"
Cohesion: 1.0
Nodes (1): HLD Pro Bilingual AI Setup

### Community 205 - "Kb 11 Campaigns"
Cohesion: 1.0
Nodes (1): HLD Pro Campaigns and Reactivation

### Community 206 - "Kb 03 Crm"
Cohesion: 1.0
Nodes (1): HLD Pro CRM and Automation System

### Community 207 - "Kb 07 Business Brain"
Cohesion: 1.0
Nodes (1): HLD Pro Business Brain Pricing Intelligence

### Community 208 - "Kb 06 Chatbot"
Cohesion: 1.0
Nodes (1): HLD Pro AI Chatbot Widget

### Community 209 - "Kb 10 Website"
Cohesion: 1.0
Nodes (1): HLD Pro Website Editor

### Community 210 - "Kb 12 Reports"
Cohesion: 1.0
Nodes (1): HLD Pro Monthly AI Performance Reports

### Community 211 - "Kb 08 Reviews"
Cohesion: 1.0
Nodes (1): HLD Pro Reviews and Reputation Management

### Community 212 - "Kb 02 Voice"
Cohesion: 1.0
Nodes (1): HLD Pro AI Voice Receptionist

### Community 213 - "Support Ticket System"
Cohesion: 1.0
Nodes (1): Support Ticket System

### Community 214 - "Narrative Esign"
Cohesion: 1.0
Nodes (1): E-Signatures Use Case

### Community 215 - "Esign Flow"
Cohesion: 1.0
Nodes (1): E-Signature Signing Flow

### Community 216 - "Hld Pro V1 Alpha Beta Launc..."
Cohesion: 1.0
Nodes (1): HLD Pro V1 Alpha/Beta Launch Plan

### Community 217 - "Claude Md Conflict Resolution"
Cohesion: 1.0
Nodes (1): CLAUDE.md Conflict Resolution Runbook

## Knowledge Gaps
- **294 isolated node(s):** `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:`, `Step 1: Load JSONL dataset from local path or R2/S3.      Expected JSONL format`, `Step 2: Load base model with 4-bit quantization + configure LoRA.      Uses Unsl` (+289 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Forwarding Instructions`** (2 nodes): `forwarding-instructions.ts`, `buildForwardingInstructionsHtml()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gate Check Runner`** (2 nodes): `gate-checks.ts`, `runGateChecks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Purchase Access Email`** (2 nodes): `purchase-access-email.ts`, `sendPortalAccessEmail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Setup Plan Creator`** (2 nodes): `setup-plan.ts`, `createDefaultSetupPlan()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `VAPI Brain Tool`** (2 nodes): `vapi-brain-tool.ts`, `getBrainToolDefinition()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Signing Workflow Advance`** (2 nodes): `advance.ts`, `advanceSigningWorkflow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Area Code Consent`** (2 nodes): `area-code-consent.ts`, `getConsentType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Party Notification Core`** (2 nodes): `notify.ts`, `notifyPartyCore()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Memory Context Injector`** (2 nodes): `memory-injector.ts`, `fetchContext()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Audit Log Emitter`** (2 nodes): `audit.ts`, `emitAuditLog()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Screenshot Capture Script`** (2 nodes): `capture-tester-guide-screenshots.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Report Data Seeder`** (2 nodes): `seed-report-data.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo Account Seeder`** (2 nodes): `seed-demo-accounts.ts`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Preflight Probe Spec`** (2 nodes): `preflight-probe.spec.ts`, `runPreflight()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wizard Step Five`** (2 nodes): `WizardStep5.tsx`, `WizardStep5()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo Call Banner`** (2 nodes): `DemoCallBanner.tsx`, `DemoCallBanner()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Admin Portal Plan`** (2 nodes): `Admin Back Office & Client Portal Plan`, `Deprecated Portal Warning`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Marketing Site Plan`** (2 nodes): `Marketing Website Plan (hldpro.com)`, `Partners Subdomain & Reseller Marketing Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Support Ticket System`** (2 nodes): `Customer Support and Ticket Portal Plan`, `Support Ticket Portal System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Competitive Value Pricing`** (2 nodes): `Competitive Value Proposition (feature/price comparison vs tools)`, `Value Stack Implementation (Competitive Differentiation)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo Assistant Config`** (2 nodes): `Demo Assistant Alex (8-industry expansion with pricing)`, `Industry-Aware Demo Assistant (8-Industry Expansion)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cross-Trade Marketplace`** (2 nodes): `Cross-Trade Marketplace — Architecture Diagram`, `Cross-Trade Marketplace System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Analytics Reporting System`** (2 nodes): `Analytics and Reporting System — Architecture Diagram`, `Analytics and Reporting System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AI Assistant System`** (2 nodes): `AI Chat Assistant — Product Data-Flow Diagram`, `AI Chat Assistant System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Support Referral System`** (2 nodes): `Support + Referral System — Architecture Diagram`, `Support + Referral System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Business Brain System`** (2 nodes): `Business Brain — System Architecture Diagram`, `Business Brain System (RAG + Pricing)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Finance System Hub`** (2 nodes): `Finance System — Integration Topology Diagram`, `Finance System (finance-api Hub)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ad Intelligence System`** (2 nodes): `Ad Creatives & Campaign Management — System Architecture Diagram`, `Ad Intelligence and Creatives System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Service Connector System`** (2 nodes): `ServiceConnector System (Field Service Integration)`, `ServiceConnector — System Architecture Diagram`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `CRM Automation System`** (2 nodes): `CRM + Automation Data-Flow Diagram`, `CRM + Automation System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `E2E Test Results`** (2 nodes): `E2E Test Results (2026-03-26)`, `E2E Test Results (2026-04-07)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ad Campaign Insights`** (2 nodes): `AI Ad Campaign Intelligence`, `Google and Facebook Ads Use Case`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `HIPAA Security Audit`** (2 nodes): `Supabase HIPAA Exposure Audit Runbook`, `Supabase Security + HIPAA Readiness Plan v3.1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Webhook Receiver Security`** (2 nodes): `webhook-receiver Edge Function`, `WEBHOOK SIGNATURE BYPASS Test`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Checkout Session Security`** (2 nodes): `CHECKOUT INJECTION Test`, `checkout-session Edge Function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Config`** (1 nodes): `config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Finance Types`** (1 nodes): `finance-types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Interface`** (1 nodes): `interface.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pentagi Flow Spec`** (1 nodes): `pentagi-flow.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite Env D`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Marketing Portal Spec`** (1 nodes): `marketing-portal.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Plaid Screenshots Spec`** (1 nodes): `plaid-screenshots.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tailwind Config`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite Config`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Postcss Config`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Corpuslayout`** (1 nodes): `CorpusLayout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vertical Hvac`** (1 nodes): `HVAC Vertical Addon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vertical Roofing`** (1 nodes): `Roofing Vertical Addon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vertical Solar`** (1 nodes): `Solar Vertical Addon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vertical Legal`** (1 nodes): `Legal Vertical Addon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Platform Billing`** (1 nodes): `Billing Service`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Platform Provisioning`** (1 nodes): `Provisioning Service (21-step orchestrator)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Platform Health`** (1 nodes): `Health Check Service`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Data Dictionary`** (1 nodes): `Data Dictionary - Schema Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Business Brain Plan`** (1 nodes): `Business Brain - RAG Pricing Intelligence Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Architecture Doc`** (1 nodes): `Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tester Guide`** (1 nodes): `HLD Pro v1.0 Alpha Tester Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Error Patterns`** (1 nodes): `Error Patterns Index`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bilingual Tts Plan`** (1 nodes): `Bilingual AI Voice TTS Decision Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Integration Sandbox Guide`** (1 nodes): `Integration Sandbox and Testing Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vercel Deployment Runbook`** (1 nodes): `Vercel Deployment Runbook`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Beta Launch Plan`** (1 nodes): `Beta Launch Plan for hldpro.com`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Session Summary 2026 03 25`** (1 nodes): `Session Summary 2026-03-25`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pentagi Setup`** (1 nodes): `PentAGI Operations Guide`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wrong Codebase Edits Pattern`** (1 nodes): `Wrong Codebase Edits Error Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `A2P 10Dlc Campaign Registra...`** (1 nodes): `A2P 10DLC Campaign Registration (Twilio SMS)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Security Implementation Pla...`** (1 nodes): `Security Implementation Plan (GitHub + Staging + Audit Skill + PentAGI)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Rollback Procedures Emergen...`** (1 nodes): `Rollback Procedures (Emergency Recovery)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cross Repo Deps Shared Supa...`** (1 nodes): `Cross-Repo Dependencies (Shared Infrastructure)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Benchmark Compute Industry ...`** (1 nodes): `Benchmark Compute (industry competitor comparison)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fail Fast Log Document`** (1 nodes): `FAIL_FAST_LOG.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Fleet Report 2026 04 06`** (1 nodes): `Fleet Health Report 2026-04-06`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Design References Readme`** (1 nodes): `HLD Pro Design References`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 05 Support`** (1 nodes): `HLD Pro Support and Ticket System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 09 Rankings`** (1 nodes): `HLD Pro Rankings and SEO Tracking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 13 Bilingual`** (1 nodes): `HLD Pro Bilingual AI Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 11 Campaigns`** (1 nodes): `HLD Pro Campaigns and Reactivation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 03 Crm`** (1 nodes): `HLD Pro CRM and Automation System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 07 Business Brain`** (1 nodes): `HLD Pro Business Brain Pricing Intelligence`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 06 Chatbot`** (1 nodes): `HLD Pro AI Chatbot Widget`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 10 Website`** (1 nodes): `HLD Pro Website Editor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 12 Reports`** (1 nodes): `HLD Pro Monthly AI Performance Reports`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 08 Reviews`** (1 nodes): `HLD Pro Reviews and Reputation Management`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kb 02 Voice`** (1 nodes): `HLD Pro AI Voice Receptionist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Support Ticket System`** (1 nodes): `Support Ticket System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Narrative Esign`** (1 nodes): `E-Signatures Use Case`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Esign Flow`** (1 nodes): `E-Signature Signing Flow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hld Pro V1 Alpha Beta Launc...`** (1 nodes): `HLD Pro V1 Alpha/Beta Launch Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Claude Md Conflict Resolution`** (1 nodes): `CLAUDE.md Conflict Resolution Runbook`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Build HLD Pro V1 Alpha Tester Guide as .docx with annotated screenshots. Adds re`, `Add red boxes and labels to a screenshot.`, `HLD Pro — Qwen3-8B QLoRA Fine-Tuning Script Runs on RunPod A100 80GB GPU  Usage:` to the rest of the system?**
  _294 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Edge Function Handlers` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Portal UI Components` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Operator Dashboard Shell` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `A2P and Corpus Analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `E2E Test Specs` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `Admin Panel Hooks` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._