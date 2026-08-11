# ADR 657 — MEOS Enterprise Process Automation Marketplace & Reusable Process Intelligence Platform (MEPAMP)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p300 · mepamp · marketplace · process-assets · reusable · certification · productization
- **Related:** [ADR 658](658-meos-enterprise-process-composer-low-code-no-code-process-engineering-visual-automation-platform.md) · [ADR 656](656-meos-enterprise-process-mining-process-intelligence-continuous-optimization-platform.md) · [ADR 655](655-meos-enterprise-agentic-process-automation-autonomous-enterprise-execution-platform.md) · [Law P300](../architecture/ENTERPRISE_MEOS_PROCESS_AUTOMATION_MARKETPLACE_REUSABLE_PROCESS_INTELLIGENCE_PLATFORM.md) · [ENTERPRISE_PLUGIN_PLATFORM.md](../architecture/ENTERPRISE_PLUGIN_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Process Automation Marketplace / Reusable Process Asset Ecosystem** productization layer — without replacing Application Lifecycle (P259), Workflow Execution (P260), Agent Orchestration (P266), Decision Execution (P261), Agentic Process Automation (P298), Process Intelligence (P299), Plugin Platform, or Application Runtime (P257), and without ungated install/activation of process assets.

## Decision

1. Establish SoR **`process_marketplace_operating`** as MEPAMP fabric under API **`/api/v1/process-marketplace-operating*`**, schema **`process_marketplace_operating_*`**.
2. Capability **`CAP-PLT-MEPAMP-001`**; fabric id **`meos_enterprise_process_automation_marketplace_reusable_process_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P259** = Application Lifecycle / Activation
   - **P260** = Workflow Execution · **P266** = Agent Orchestration · **P261** = Decision Execution · **P257** = Runtime
   - **P298** = Agentic Process Automation · **P299** = Process Intelligence
   - **P300** = Reusable Process Ecosystem & Marketplace
   - **P301** = Visual Process Engineering / Low-Code Composition (delivered; distinct)
   - **P302** = Process Testing / QA / Digital Process Validation (delivered; distinct)
4. Federate-by-contract: P259–P266, P270, P294, P297–P299, Plugin Platform, P214-Z, Policy, Workflow — never dual-write workflow/agent/runtime/plugin tables; never embed local LLM; never local metrics/approval engines.
5. Assets, packages, installations and certifications are **versioned, explainable, reproducible, auditable**. Material activation requires **Compatibility + Security + Policy + Certification + Governance Approval + P259 Lifecycle**.
6. P300 may Discover · Validate · Package · Install · Coordinate Activation · Govern Marketplace Lifecycle — and must **NOT** Execute Workflow · Execute Agent · Execute Transaction · Execute Business Decision.
7. Plugin Platform remains sole signed third-party extension runtime; MEPAMP federates process-asset catalogs and may reference `plugin_id` — never unsigned packages in production.
8. Ratings must not override governance certification; license metering only (billing via Financial Kernel / Q2C ACL).
9. Simulation via P265 before install when Policy requires; simulation ≠ execute.
10. Inference → **P214-Z** only; no module-local LLM.

## Consequences

- Unlocks Phase 1–9 MEPAMP roadmap (P300-A…I); **P301** MEPCVA · **P302** MEPQDV · **P303** MEPRED · **P304** MEPOCI · **P305** MEIRRE · **P306** MEESOP · **P307** MEKNOL · **P308** MEDCIM · **P309** MERILG · **P310** MEIGSI delivered; **P311** DLP / Information Protection / Adaptive Data Security Control series unblocked.
- P259 remains lifecycle; P260/P266/P261/P257 remain execution; P298/P299 remain adaptation/intelligence; MEPAMP owns marketplace registry, certification, trust and installation coordination.
- Ungated install/activate or merging P259–P303 / Plugin Platform SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed Process Marketplace inside Plugin Platform only | Violates first-party process-asset ecosystem vs third-party plugin split |
| Embed install/activate as second Lifecycle Engine | Violates P259 ownership |
| Execute workflows/agents from marketplace domain | Violates P260/P266 ownership |
| Ratings override certification | Violates Human Governance · Trust-Based Deployment |
| Ungated partner publishing without verification | Violates Security · Certification · Contract gates |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P259 · P260 · P266 · P298 · P299 · Plugin Platform · P270 · Workflow · Policy · Audit)
- [x] Discover/validate/install/coordinate only · simulation ≠ execute · no local LLM
- [x] P259 · P260 · P266 · P298 · P299 · Plugin Platform boundaries preserved explicitly
- [x] No ungated install/activate · no unsigned production packages
- [x] P301 MEPCVA · P302 MEPQDV delivered · P303 stub announced
