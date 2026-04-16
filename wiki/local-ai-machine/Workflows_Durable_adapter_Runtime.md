# Workflows Durable adapter Runtime

> 69 nodes · cohesion 0.05

## Key Concepts

- **contracts.ts** (11 connections) — `local-ai-machine/src/types/contracts.ts`
- **durable_adapter.ts** (11 connections) — `local-ai-machine/src/workflows/interfaces/durable_adapter.ts`
- **native_orchestrator.ts** (9 connections) — `local-ai-machine/src/orchestrator/native_orchestrator.ts`
- **runtime_envelope.ts** (8 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **runtime_reconciliation.ts** (8 connections) — `local-ai-machine/src/workflows/runtime_reconciliation.ts`
- **TemporalExecutionAdapter** (7 connections) — `local-ai-machine/src/workflows/durable_adapter.ts`
- **runtime_resolver_activity.ts** (7 connections) — `local-ai-machine/src/workflows/runtime_resolver_activity.ts`
- **runtime_workflow_runner.ts** (7 connections) — `local-ai-machine/src/workflows/runtime_workflow_runner.ts`
- **activities.ts** (6 connections) — `local-ai-machine/src/workflows/activities.ts`
- **resolver_gate.ts** (6 connections) — `local-ai-machine/src/workflows/resolver_gate.ts`
- **amps_router.ts** (5 connections) — `local-ai-machine/src/orchestrator/amps_router.ts`
- **.invokeVerificationActivity()** (5 connections) — `local-ai-machine/src/workflows/durable_adapter.ts`
- **orchestrateWithClient()** (5 connections) — `local-ai-machine/src/orchestrator/native_orchestrator.ts`
- **pdp.ts** (5 connections) — `local-ai-machine/src/auth/pdp.ts`
- **PolicyDecisionPoint** (5 connections) — `local-ai-machine/src/auth/pdp.ts`
- **buildDelegatedExecutionEnvelope()** (5 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **requiredString()** (5 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **workflowId()** (5 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **buildFromActivity()** (4 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **buildFromVerification()** (4 connections) — `local-ai-machine/src/workflows/runtime_envelope.ts`
- **buildSyscallReconciliationEvents()** (4 connections) — `local-ai-machine/src/workflows/runtime_reconciliation.ts`
- **worker.ts** (4 connections) — `local-ai-machine/src/workflows/worker.ts`
- **buildSignalPayload()** (3 connections) — `local-ai-machine/src/workflows/durable_adapter.ts`
- **requiredString()** (3 connections) — `local-ai-machine/src/workflows/durable_adapter.ts`
- **leanNativeOrchestrator()** (3 connections) — `local-ai-machine/src/orchestrator/native_orchestrator.ts`
- *... and 44 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/src/auth/pdp.ts`
- `local-ai-machine/src/orchestrator/amps_router.ts`
- `local-ai-machine/src/orchestrator/native_orchestrator.ts`
- `local-ai-machine/src/orchestrator/runtime_resolver.ts`
- `local-ai-machine/src/types/contracts.ts`
- `local-ai-machine/src/workflows/activities.ts`
- `local-ai-machine/src/workflows/durable_adapter.ts`
- `local-ai-machine/src/workflows/interfaces/durable_adapter.ts`
- `local-ai-machine/src/workflows/ragWorkflow.ts`
- `local-ai-machine/src/workflows/resolver_gate.ts`
- `local-ai-machine/src/workflows/runtime_envelope.ts`
- `local-ai-machine/src/workflows/runtime_reconciliation.ts`
- `local-ai-machine/src/workflows/runtime_resolver_activity.ts`
- `local-ai-machine/src/workflows/runtime_workflow_runner.ts`
- `local-ai-machine/src/workflows/worker.ts`

## Audit Trail

- EXTRACTED: 156 (69%)
- INFERRED: 70 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*