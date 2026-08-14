# ADR 658 — MEOS Enterprise Process Composer, Low-Code/No-Code Process Engineering & Visual Automation Platform (MEPCVA)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p301 · mepcva · process-composer · low-code · no-code · visual-engineering · productization
- **Related:** [ADR 659](659-meos-enterprise-process-testing-simulation-quality-assurance-digital-process-validation-platform.md) · [ADR 657](657-meos-enterprise-process-automation-marketplace-reusable-process-intelligence-platform.md) · [ADR 656](656-meos-enterprise-process-mining-process-intelligence-continuous-optimization-platform.md) · [Law P301](../architecture/ENTERPRISE_MEOS_PROCESS_COMPOSER_LOW_CODE_NO_CODE_PROCESS_ENGINEERING_VISUAL_AUTOMATION_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Visual Process Engineering / Low-Code/No-Code Composition Experience** — without replacing Process Marketplace (P300), Process Intelligence (P299), Agentic Process Automation (P298), Workflow Execution (P260), Agent Orchestration (P266), Decision Execution (P261), Application Lifecycle (P259), Governance (P270), or Application Runtime (P257), and without promoting designs directly to production.

## Decision

1. Establish SoR **`process_composer_operating`** as MEPCVA fabric under API **`/api/v1/process-composer-operating*`**, schema **`process_composer_operating_*`**.
2. Capability **`CAP-PLT-MEPCVA-001`**; fabric id **`meos_enterprise_process_composer_low_code_no_code_process_engineering_visual_automation_platform_framework`**.
3. **Boundary law (hard):**
   - **P300** = Marketplace / Reusable Assets · **P299** = Process Intelligence · **P298** = Agentic Process Automation
   - **P260** = Workflow Execution · **P266** = Agent Orchestration · **P261** = Decision Execution · **P257** = Runtime
   - **P259** = Lifecycle · **P270** = Governance
   - **P301** = Visual Process Engineering / Design-Time Composition
   - **P302** = Process Testing / QA / Digital Process Validation (delivered; distinct)
   - **P303** = Process Release / Deployment / Environment Lifecycle (delivered)
   - **P304** = Process Observability / Continuous Operational Intelligence (delivered)
   - **P305** = Incident Management / Service Reliability / Resilience Engineering (next)
4. Federate-by-contract: P300, P299, P298, P257–P266, P270, P294, P297, P214-Z, Policy, Workflow — never dual-write execution tables; never embed local LLM; never local metrics/approval engines.
5. Process designs, versions and release candidates are **versioned, explainable, reproducible, auditable**. Production path requires **Validate → Simulate → Review → Govern → Package (P300) → Lifecycle (P259)**.
6. P301 is **DESIGN-TIME** — may Design · Compose · Configure · Validate · Simulate · Recommend · Package — and must **NOT** Execute Workflow · Execute Agent · Execute Decision · Execute Transaction · Modify Production State Directly.
7. AI-generated processes remain **Draft** until validated and governed; AI suggestions require explainability.
8. Prefer reuse via P300 / duplication detection before creating new assets.
9. Simulation via P265; intelligence via P299; simulation ≠ execute.
10. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–9 MEPCVA roadmap (P301-A…I); **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- P300 remains marketplace; P260/P266/P261/P257 remain execution; P259 remains lifecycle; MEPCVA owns visual design-time engineering experience.
- Direct production deploy from composer or merging P300–P303 / P260/P266 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Visual Composer inside P300 Marketplace | Violates marketplace distribution vs design-time engineering split |
| Execute workflows from canvas domain | Violates P260 ownership |
| Promote AI drafts directly to production | Violates Human Governance · Draft-until-governed law |
| Own simulation/intelligence engines | Violates P265/P299 ownership |
| Second governance approval engine in composer | Violates P270 / Workflow ownership |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P300 · P299 · P260 · P266 · P259 · P270 · P265 · Workflow · Policy · Audit)
- [x] Design-time only · AI drafts · simulation ≠ execute · no local LLM
- [x] P300 · P260 · P266 · P259 · P270 boundaries preserved explicitly
- [x] No direct production deploy · no execution of workflow/agent/decision/transaction
- [x] P302 MEPQDV · P303 MEPRED · P304 MEPOCI delivered · P305 stub announced
