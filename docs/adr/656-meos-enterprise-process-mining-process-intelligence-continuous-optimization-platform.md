# ADR 656 — MEOS Enterprise Process Mining, Process Intelligence & Continuous Optimization Platform (MEPICO)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p299 · mepico · process-mining · process-intelligence · continuous-optimization · productization
- **Related:** [ADR 657](657-meos-enterprise-process-automation-marketplace-reusable-process-intelligence-platform.md) · [ADR 655](655-meos-enterprise-agentic-process-automation-autonomous-enterprise-execution-platform.md) · [ADR 654](654-meos-enterprise-ai-interaction-agentic-workspace-human-ai-collaboration-platform.md) · [Law P299](../architecture/ENTERPRISE_MEOS_PROCESS_MINING_PROCESS_INTELLIGENCE_CONTINUOUS_OPTIMIZATION_PLATFORM.md) · [AI_PLATFORM_STANDARD.md](../architecture/AI_PLATFORM_STANDARD.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Process Mining / Process Intelligence / Continuous Optimization** productization layer — without replacing Agentic Process Adaptation (P298), Workflow Execution (P260), Agent Orchestration (P266), Application Runtime (P257), Digital Twin (P265), Knowledge Graph (P264), Enterprise Analytics (P262), or Governance (P270), and without directly mutating production workflows or deploying ungated optimizations.

## Decision

1. Establish SoR **`process_intelligence_operating`** as MEPICO fabric under API **`/api/v1/process-intelligence-operating*`**, schema **`process_intelligence_operating_*`**.
2. Capability **`CAP-PLT-MEPICO-001`**; fabric id **`meos_enterprise_process_mining_process_intelligence_continuous_optimization_platform_framework`**.
3. **Boundary law (hard):**
   - **P260** = Workflow Definition / Execution / State
   - **P266** = Agent Orchestration
   - **P298** = Agentic Process Automation / Adaptation
   - **P299** = Process Mining / Intelligence / Continuous Optimization
   - **P300** = Reusable Process Ecosystem & Marketplace (delivered; distinct)
   - **P301** = Visual Process Engineering / Low-Code Composition (delivered; distinct)
4. Federate-by-contract: P298, P260, P257, P261–P266, P270, P294, P297, P214-Z, Policy, Workflow — never dual-write workflow/adaptation/runtime tables; never embed local LLM; never local metrics/approval engines.
5. Process models, optimization proposals and recommendations are **versioned, explainable, reproducible, auditable**. Material changes require **Governance (P270) → Adaptation (P298) → Workflow (P260) → Runtime (P257)**.
6. P299 may Observe · Analyze · Predict · Simulate · Recommend — and must **NOT** Execute Transactions · Modify Production Workflow · Change Authorization · Change Policy · Deploy Autonomous Changes Without Governance.
7. Simulation via P265; simulation ≠ execute. Alerts via P294 Communication Intent only.
8. Canonical Process Event Model + immutable event log with CorrelationId · CausationId · Tenant Isolation · Replay Support.
9. **No AI Agent may deploy process optimizations outside Policy + Governance + P298 Adaptation + Audit.**
10. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–9 MEPICO roadmap (P299-A…I); **P300** MEPAMP · **P301** MEPCVA · **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- P298 remains adaptation; P260 remains workflow; P270 remains governance; MEPICO owns mining, intelligence, prediction, simulation coordination and optimization recommendations.
- Direct workflow mutation or merging P260/P266/P298/P299/P300/P301/P302/P303 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Process Mining inside P298 Adaptation | Violates intelligence vs adaptation split |
| Embed Process Intelligence inside P260 Workflow | Violates workflow engine vs intelligence layer split |
| Own Twin/KG engines for simulation/semantics | Violates P265/P264 ownership |
| Direct DeployApprovedOptimization to workflow tables | Violates P298/P260/P270 boundary law |
| Local metrics store for process KPIs | Violates Observability / Analytics platform law |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P298 · P260 · P270 · P265 · P262 · P294 · Workflow · Policy · Audit)
- [x] Observe/analyze/recommend only · simulation ≠ execute · no local LLM
- [x] P298 · P260 · P266 · P270 boundaries preserved explicitly
- [x] No direct transaction/workflow/policy/authZ mutation
- [x] P300 MEPAMP · P301 MEPCVA · P302 MEPQDV delivered · P303 stub announced
