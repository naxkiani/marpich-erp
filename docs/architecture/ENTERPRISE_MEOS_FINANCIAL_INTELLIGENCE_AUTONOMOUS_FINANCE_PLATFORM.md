# MEOS Enterprise Financial Intelligence & Autonomous Finance Platform (MEFIAF)

**Status:** Normative (P271) — series foundation · **Productization & Experience Evolution Phase**  
**SoR:** `autonomous_finance_operating` · **ADR:** [628](../adr/628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · **Capability:** `CAP-PLT-MEFIAF-001`  
**Fabric:** `meos_enterprise_financial_intelligence_autonomous_finance_platform_framework` · **Governance Standard:** MEOS 11.0  
> **API:** `/api/v1/autonomous-finance-operating*` · **Builds on:** P270 MEGRSC · P269 MEPCRI · P268 MECZTD · P267 MEAOSH · P266 MEAAOI · P265 MEDTIP · P264 MEKGSI · P263 MEDIMOP · P262 MEIAOI · P261 MEBRDI · P260 MEWEOP · P258 MESCC · P257 MERAF · P259 MDMAL · [P231 EAFIEOP](ENTERPRISE_AUTONOMOUS_FINANCIAL_INTELLIGENCE_ECONOMIC_OPTIMIZATION_PLATFORM.md) · [Enterprise Financial Kernel](ENTERPRISE_FINANCIAL_KERNEL.md) · Accounting · Treasury · Banking peers · Policy Engine · Compliance · Audit · Workflow · P214-Z · **Next:** P271-A · **Peer series:** [P272 MESCIAL](ENTERPRISE_MEOS_SUPPLY_CHAIN_INTELLIGENCE_AUTONOMOUS_LOGISTICS_PLATFORM.md) (Supply Network OS productization — never fork `/api/v1/supply-chain-intelligence*` or dual-write inventory ledgers) · [P276 MEPIASP](ENTERPRISE_MEOS_PROCUREMENT_INTELLIGENCE_AUTONOMOUS_SOURCING_PLATFORM.md) (Source-to-Pay OS — budget/commitment control via this Finance OS; never local GL in procurement) · [P277 MESIARO](ENTERPRISE_MEOS_SALES_INTELLIGENCE_AUTONOMOUS_REVENUE_OPERATIONS_PLATFORM.md) (Sales/RevOps OS — revenue/margin/pricing financial control stays here; never local GL in sales OS) · [P278 MEQTCIP](ENTERPRISE_MEOS_REVENUE_BILLING_QUOTE_TO_CASH_INTELLIGENCE_PLATFORM.md) (Quote-to-Cash OS — operational revenue cycle; P271 remains Financial Control; never dual-write AR/finance ledgers; never local GL in Q2C) · [P279 METRCIP](ENTERPRISE_MEOS_REVENUE_RECOGNITION_TREASURY_CASH_INTELLIGENCE_PLATFORM.md) (Treasury/RevRec/Cash OS — feeds recognition/cash context; **does not replace P271**; never dual-write treasury ledgers; never local GL) · [P280 MEFPAPM](ENTERPRISE_MEOS_FINANCIAL_PLANNING_BUDGETING_AUTONOMOUS_PERFORMANCE_MANAGEMENT_PLATFORM.md) (FP&A / Budgeting / Performance OS — consumes governed actuals; never dual-write budget into GL; never replace Financial Control) · [P281 MEMACPI](ENTERPRISE_MEOS_MANAGEMENT_ACCOUNTING_COST_PROFITABILITY_INTELLIGENCE_PLATFORM.md) (Management Accounting / Cost & Profitability OS — interpretive cost/profitability; never dual-write cost into GL; never replace Financial Control) · [P282 MEPRIAP](ENTERPRISE_MEOS_PRICING_INTELLIGENCE_REVENUE_OPTIMIZATION_AUTONOMOUS_PRICING_PLATFORM.md) (Pricing / Revenue Optimization OS — never ungated price commits; never replace Financial Control) · [P283 MECIAP](ENTERPRISE_MEOS_CONTRACT_INTELLIGENCE_COMMERCIAL_AGREEMENT_AUTONOMOUS_CONTRACT_PLATFORM.md) (Contract / Agreement OS — never ungated binding commits; never replace Financial Control) · [P284 MECCPI](ENTERPRISE_MEOS_COMMERCIAL_COMPLIANCE_OBLIGATION_CONTRACT_PERFORMANCE_INTELLIGENCE_PLATFORM.md) (Commercial Performance Assurance — never ungated penalty/credit) · [P285 MESMIP](ENTERPRISE_MEOS_SERVICE_MANAGEMENT_SLA_OPERATIONS_INTELLIGENT_SERVICE_DELIVERY_PLATFORM.md) (Service Delivery — never ungated production changes) · [P286 MEITOI](ENTERPRISE_MEOS_IT_OPERATIONS_INFRASTRUCTURE_OBSERVABILITY_INTELLIGENCE_PLATFORM.md) (Technology Ops — never ungated infra mutations) · [P287 MECPEI](ENTERPRISE_MEOS_CLOUD_PLATFORM_ENGINEERING_INFRASTRUCTURE_AUTOMATION_INTELLIGENCE_PLATFORM.md) (Cloud / Platform Engineering — cloud cost via this Finance OS / Financial Kernel; never local GL)  
**Hard bindings:** Inference → **P214-Z** · Financial intel/optimization SoR → **P231 `financial_intelligence`** (ACL; never replace `/api/v1/financial-intelligence*`) · GL / journals / COA / postings → **Financial Kernel** (`IFinancialKernel`) — **never duplicate ledger truth** · Accounting docs (AR/AP/invoice) → **accounting** (ACL) · Quote-to-Cash OS → **P278 `quote_to_cash_operating`** (ACL; never replace `/api/v1/quote-to-cash-operating*` — P278 = Q2C execution; P271 = Financial Intelligence / Control) · Treasury / RevRec OS → **P279 `treasury_cash_operating`** (ACL; never replace `/api/v1/treasury-cash-operating*` — P279 ≠ P271; P271 remains Financial Control) · FP&A / Planning OS → **P280 `financial_planning_operating`** (ACL; never replace `/api/v1/financial-planning-operating*` — P280 = Planning/Performance; P271 = Financial Control) · Management Accounting OS → **P281 `management_accounting_operating`** (ACL; never replace `/api/v1/management-accounting-operating*` — P281 = Cost/Profitability; never mutate ledger) · Pricing OS → **P282 `pricing_operating`** (ACL; never replace `/api/v1/pricing-operating*` — never ungated price commits) · Contract OS → **P283 `contract_operating`** (ACL; never replace `/api/v1/contract-operating*` — never ungated binding commits; `document_id` only) · Commercial Performance OS → **P284 `commercial_performance_operating`** (ACL; never replace `/api/v1/commercial-performance-operating*` — never ungated penalty/credit) · Service Management OS → **P285 `service_management_operating`** (ACL; never replace `/api/v1/service-management-operating*` — never ungated production changes) · Technology Operations OS → **P286 `technology_operations_operating`** (ACL; never replace `/api/v1/technology-operations-operating*` — never ungated infra mutations) · Treasury/cash → **treasury** (ACL) · Banking products → **banking** peers (ACL) · Financial strategy/governance → **P270** (ACL) · Compliance/regulatory finance → **P269 / Compliance** (ACL) · Cyber/fraud signals → **P268** (ACL) · Decisions → **P261 / P224** (ACL) · Twin financial simulation → **P227 / P265** (ACL; simulation ≠ post/execute) · KG → **P228 / P264** (ACL) · Finance approvals → **P260 / Workflow** (ACL) · Agents → **P266** (ACL) · Experience Finance Command Center → **P258** (ACL) · Analytics/KPI → **P262** (ACL) · Policy → **Policy Engine** · Audit → **Audit** · AuthN/AuthZ → **Identity** · Market/data vendors → **Integration Platform** · Generic → **Core**.

---

## 1. Header

**MARPICH ENTERPRISE PLATFORM (MEOS)** · Master Blueprint · Enterprise Architecture Governance Standard **11.0** · Prompt **P271** · MEOS Enterprise Financial Intelligence & Autonomous Finance Platform (**MEFIAF**).  
**Platform Domain:** MEOS Enterprise Financial Intelligence Ecosystem · **Capability Category:** Autonomous Finance, Financial Intelligence, Enterprise Accounting, Treasury Intelligence, Financial Planning & AI-Driven Finance Operations · **Strategic Layer:** MEOS Enterprise Value Intelligence Operating Layer.

## 2. Prompt ID

**P271**

## 3. Mission

Deliver the central Financial Intelligence productization layer for managing, analyzing, predicting and intelligently executing enterprise financial activities.

```
Traditional Enterprise Finance → Intelligent Financial Operations
→ Predictive Financial Intelligence → Autonomous Finance Operating Ecosystem
```

**Goal:** Transform Manual Finance Management into an **AI-Native Autonomous Enterprise Finance Operating System**.

Missions: Enterprise Accounting Intelligence · Financial Planning Automation · Budget Intelligence · Treasury Optimization · Revenue Intelligence · Cost Intelligence · Financial Risk Prediction · Cash Flow Optimization · Investment Intelligence · Autonomous Financial Operations (gated).

```
Financial Data → Financial Intelligence → AI Analysis → Prediction
→ Decision Support → Automated Execution (gated) → Continuous Optimization
```

MEFIAF owns **autonomous finance operating fabric** (Finance Command Center contracts, CFO workspace overlays, forecasting/treasury/revenue/cost campaigns, gated automation intents); it does **not** replace P231, Financial Kernel, accounting, treasury, banking or Core — and never posts journals, mutates GL balances, or executes treasury payments without Kernel/peer APIs + Policy + Workflow (+ human authority for material classes).

## 4. Architecture Principles

- Enterprise Architecture Governance Standard **11.0** (binding)
- DDD · CQRS · Event Sourcing · Event-Driven · Hexagonal · Clean · API-First
- Cloud Native · AI Native · Knowledge Graph Native · Digital Twin Native
- Metadata Driven · Configuration Driven · Policy Driven
- Zero Trust · Explainable AI · Responsible AI · Human Governance
- **Continuous Financial Governance**
- Multi-tenant · Fail-closed authorization · Pagination mandatory
- Federate-by-contract only — never peer domain imports / shared tables / local LLM
- **P231 vs Financial Kernel vs MEFIAF:** P231 = financial intel SoR; Kernel = GL/journals/COA foundation; MEFIAF = Finance OS productization — never fork `/api/v1/financial-intelligence*`, never local JournalEntry/GL aggregates
- **Accounting vs Kernel:** accounting owns billing/AR/AP docs; Kernel materializes ledger — MEFIAF orchestrates, never dual-writes either
- Automated posting/payment/investment execute gated by Workflow + Policy; material CFO-class actions require human authority
- Twin financial scenario ≠ production post / pay / settle
- No opaque autonomous finance without explainability + audit trail
- Multi-currency via Shared Kernel `Money` + Kernel FX — never module-local FX engines

## 5. Reference Architecture

```
Financial Experience (P258 Finance Command Center · CFO Workspace · Dashboards · Investment · AI Finance Assistant)
        ↓
┌──────────────────────────────────────────────────────────────┐
│ Autonomous Finance Operating Fabric (SoR autonomous_finance_operating)│
│ Forecast/treasury/revenue/cost campaigns · gated automation intents│
│ schema: autonomous_finance_operating_*                       │
└──────────────────────────────────────────────────────────────┘
        ↓ ACL                         ↓ ACL                    ↓ ACL
 P231 Financial Intel            Financial Kernel         Accounting / Treasury
        ↓
 Autonomous Finance Core · Financial Governance overlays (Policy · Approval · Audit)
        ↓
 Foundation: P266 Agents · P264 KG · P265 Twin · P263 Mesh · P260 Workflow · P270 Governance · P269 Compliance
```

| Layer | Role |
|-------|------|
| Financial Experience | Command Center · CFO · Investment · AI Assistant |
| Financial Intelligence Engine | Analytics · Forecast · Optimization · Risk · Decision overlays |
| Autonomous Finance Core | Accounting automation intents · Budget · Treasury · Revenue · Cost |
| Financial Governance | Policies · Approvals · Audit · Compliance · Regulations |
| Intelligence Foundation | Agents · KG · Twin · Mesh · Workflow · Decision · Governance |

## 6. Core Capabilities

| ID | Capability |
|----|------------|
| MEFIAF-C01 | Enterprise Financial Intelligence Engine (operating overlays) |
| MEFIAF-C02 | Autonomous Accounting Platform (gated intents → Kernel/accounting) |
| MEFIAF-C03 | Financial Planning & Forecasting Intelligence |
| MEFIAF-C04 | Treasury Intelligence Platform |
| MEFIAF-C05 | Revenue Intelligence Platform |
| MEFIAF-C06 | Cost Intelligence Platform |
| MEFIAF-C07 | Financial Risk Intelligence |
| MEFIAF-C08 | Investment Intelligence (recommend only until gated) |
| MEFIAF-C09 | CFO Financial Health Score productization |
| MEFIAF-C10 | MEFIAF Governance Kernel (kill-switch, human gates, transparency) |

### Notes

Financial Intelligence Model: Revenue + Cost + Asset + Liability + Cash Flow → Financial Intelligence (federated signals).  
Accounting lifecycle: Transaction → Classification → Validation → Posting (**Kernel**) → Reporting.  
Planning example: Market Expansion → Revenue Prediction → Cost Simulation → Risk → Investment Recommendation (human approval).  
Treasury flow: Cash Data → Prediction → Optimization → Execution (**treasury** + Workflow).  
Risk domains: Liquidity · Market · Credit · Operational Finance · Investment.

## 7. User Experience Architecture

```
CFO / Executive → Finance Command Center → Financial Intelligence
→ AI Recommendation → Decision → Execution (gated)
```

CFO Intelligence Workspace: Financial Health Score · Revenue Overview · Cash Flow Prediction · Risk Indicators · AI Recommendations.  
AI Finance Assistant: *"What will be our cash position in six months?"* → Analyze → Forecast → Risks → Explain → Recommend.  
Financial Decision Room: Scenario Comparison · Investment Analysis · Budget Decisions · Financial Approval.

## 8. Application Runtime Model

```
Financial Event → Data Processing → AI Analysis → Forecast → Decision
→ Approval → Execution (peer/Kernel) → Learning
```

FinancialIntelligenceInstance: Financial Entity · Transaction Context · Financial State · Prediction · Recommendation · Decision · Audit Trail.

## 9. AI Agents

| Agent | Role | Gate |
|-------|------|------|
| Autonomous Finance Agent | Monitor ops · opportunities · process optimization | Explainability · Audit |
| Financial Forecasting Agent | Revenue · cash flow · scenarios | Non-actuating default |
| Accounting Intelligence Agent | Classify · validate · error detect · posting intents | Kernel ACL · Workflow |
| Treasury Optimization Agent | Liquidity · cash position · risk reduction | Treasury ACL · Workflow |
| Investment Intelligence Agent | Analyze · simulate · allocation recommend | Human authority for material |

**Law:** Agents recommend; post/pay/invest via Financial Kernel / treasury / accounting + Workflow + Policy. Never module-local LLM. Never opaque auto-post. Simulation ≠ execute.

## 10. Domain Driven Design (DDD)

**Core domain:** MEOS Enterprise Financial Intelligence & Autonomous Finance (operating)  
**Strategic type:** Supporting Domain (platform / value intelligence operating layer) — Generic ERP finance remains in Kernel/accounting peers

### Bounded Contexts (logical; single SoR `autonomous_finance_operating`)

| BC | Name | Aggregate root |
|----|------|----------------|
| BC-01 | Accounting Intelligence Operating | `AccountingAutomationCampaignAggregate` |
| BC-02 | Financial Planning Operating | `FinancialPlanOperatingAggregate` |
| BC-03 | Treasury Intelligence Operating | `TreasuryOptimizationCampaignAggregate` |
| BC-04 | Revenue Intelligence Operating | `RevenueIntelligenceCampaignAggregate` |
| BC-05 | Cost Intelligence Operating | `CostIntelligenceCampaignAggregate` |
| BC-06 | Financial Risk / Investment Operating | `FinancialRiskCampaignAggregate` |

### Aggregates

**FinancialAccount (operating projection):** Transactions refs · Balances refs · Rules · History · Reports (peer/Kernel truth)  
**FinancialPlan (operating):** Budget · Forecast · Scenario · Approval · Outcome  
Also: `CashPosition` · `Payment` · `LiquidityPlan` · `RevenueStream` · `PricingModel` · `CustomerValue` · `GrowthOpportunity`

### Value Objects

`FinancialHealthScore` · `ForecastConfidence` · `CashPositionSnapshot` · `VarianceAmount` · `ExplainabilityTraceRef` · `PeerJournalId` · `PeerBudgetId` · `MoneyRef` · `TenantScope`

### Domain Services

`FinancialAnalysisService` · `AccountingAutomationService` (ACL) · `ForecastingService` · `TreasuryOptimizationService` (ACL) · `RevenueOptimizationService` · `AutonomousFinanceGovernanceEngine` · `FinancialExplainabilityService`

**Hard separation:** GL/journals in Financial Kernel; AR/AP docs in accounting; cash ops in treasury; financial intel catalog in P231. MEFIAF stores operating campaigns, forecasts/optimization intents and peer refs only — never local JournalEntry aggregates.

## 11. Event Architecture

### Domain Events

`FinancialTransactionCreated` · `AccountingEntryGenerated` · `BudgetCreated` · `ForecastGenerated` · `CashFlowPredicted` · `FinancialRiskDetected` · `InvestmentRecommended` · `FinancialOptimizationCompleted` · `FinanceGateApplied`

### Event Flow

`Financial Event → Event Processing → AI Financial Analysis → Decision Intelligence → Workflow → Financial Optimization`  
Subscribers: Workflow · Decision · AI Agents · Governance · Analytics · KG · Audit · Kernel ACL consumers

Envelope + outbox + idempotent ACL consumers mandatory.

## 12. CQRS

### Commands

`CreateTransactionCommand` · `GenerateAccountingEntryCommand` · `CreateBudgetCommand` · `RunForecastCommand` · `OptimizeCashFlowCommand` · `ApproveFinancialDecisionCommand` · `ApplyFinanceGateCommand`

(Canonical journal/posting/payment mutations via Financial Kernel / treasury / accounting ACL.)

### Queries

`GetFinancialHealthQuery` · `GetCashFlowPredictionQuery` · `GetRevenueInsightQuery` · `GetBudgetStatusQuery` · `GetFinancialRiskQuery`

Read models under `autonomous_finance_operating_*` only; pagination mandatory; live ledger/cash truth via Kernel/treasury.

## 13. MEOS Integration

| Peer | Mode |
|------|------|
| P231 EAFIEOP | Financial intelligence SoR — **never replace** |
| Financial Kernel | GL / journals / COA — **never duplicate** |
| accounting · treasury · banking | Docs / cash / products — ACL |
| P270 MEGRSC | Financial strategy ↔ enterprise governance |
| P269 · Compliance | Financial regulation assurance |
| P268 | Fraud / financial security signals |
| P261 · P260 · P262 | Decision · approval workflow · analytics |
| P263 · P264 · P265 · P266 · P267 | Mesh · KG · twin · agents · ops |
| P257 · P258 · P259 | Runtime · Finance Command Center · lifecycle |
| Policy · Audit · Identity | Gates · evidence · authority |
| **P272 MESCIAL** | Supply Network OS — **never fork supply-chain-intelligence or dual-write inventory** |
| **P277 MESIARO** | Sales / RevOps OS — **margin/pricing financial control here; never local GL in sales** |
| **P278 MEQTCIP** | Quote-to-Cash OS — **operational revenue cycle; never dual-write AR; P271 remains Financial Control** |
| **P279 METRCIP** | Treasury / RevRec / Cash OS — **feeds P271; never replaces Financial Control; never dual-write treasury** |
| **P280 MEFPAPM** | FP&A / Budgeting / Performance OS — **consumes governed actuals; never dual-write budget into GL** |
| **P281 MEMACPI** | Management Accounting / Cost & Profitability OS — **interpretive cost/profitability; never dual-write cost into GL** |
| **P282 MEPRIAP** | Pricing / Revenue Optimization OS — **never ungated price commits; never replace Financial Control** |
| **P283 MECIAP** | Contract / Agreement OS — **never ungated binding commits; never replace Financial Control** |
| **P284 MECCPI** | Commercial Performance Assurance OS — **never ungated penalty/credit; never replace Financial Control** |
| **P285 MESMIP** | Service Delivery OS — **never ungated production changes; never replace Financial Control** |
| **P286 MEITOI** | Technology Ops / Observability OS — **never ungated infra mutations; never replace Financial Control** |
| **P287 MECPEI** | Cloud / Platform Engineering OS — cloud cost via this Finance OS / Financial Kernel (ACL; never local GL) |
| Core | Generic platform services |

Permissions: `autonomous_finance_operating.intelligence.*` · `autonomous_finance_operating.accounting.*` · `autonomous_finance_operating.planning.*` · `autonomous_finance_operating.treasury.*` · `autonomous_finance_operating.revenue.*` · `autonomous_finance_operating.cost.*` · `autonomous_finance_operating.risk.*` · `autonomous_finance_operating.governance.*` · `autonomous_finance_operating.ai.read` · `autonomous_finance_operating.ai.infer`.

## 14. Implementation Roadmap

| Phase | Focus | Window | Deliverables |
|-------|-------|--------|--------------|
| **P271** | Foundation | — | ADR · capability · fabric · DDD/CQRS · API skeleton · dual tests |
| **Phase 1 / P271-A** | Financial Intelligence Foundation | 3–6 mo | Financial data model overlays · accounting intelligence federation · finance dashboard · reporting |
| **Phase 2 / P271-B** | Intelligent Finance Platform | 6–12 mo | Forecasting AI · treasury intelligence · revenue analytics |
| **Phase 3 / P271-C** | Autonomous Finance Operations | 12–18 mo | AI accounting intents (gated) · automated planning · financial optimization (gated) |
| **Phase 4 / P271-D** | Autonomous Enterprise Finance OS | 18–36 mo | Self-optimizing finance assists · autonomous financial decisions (gated) · continuous value optimization |

Catalogs (planned): `docs/architecture/autonomous_finance_operating/MEFIAF_*_{CAPABILITIES,DDD_CQRS,SECURITY,VALIDATION,ARCHITECTURE}.v1.yaml`

## 15. Quality Gates

- Never MEOS Enterprise Financial Intelligence & Autonomous Finance Platform is missing
- Never Accounting / Forecast / Treasury / Revenue-Cost capabilities are missing
- Never MEFIAF Event Architecture / CQRS Model is missing
- Never MEOS MEFIAF Integration Map is missing
- Never Sibling Autonomous Finance Operating BC (second deployable)
- Never Replace P231 · Financial Kernel · accounting · treasury · Core · AI
- Never Dual-Write GL/Journal Ledgers · Never Fork `/api/v1/financial-intelligence*`
- Never Local JournalEntry Aggregates in MEFIAF · Never Module-Local LLM
- Never Opaque Auto-Post / Auto-Pay · Never Treat Twin Simulation as Production Post

Validate: financial domain architecture · DDD · CQRS · events · accounting accuracy (via Kernel) · forecast reliability · audit traceability · financial control · explainable recommendations · human approval · responsible automation · CFO command center · AI finance assistant · decision workspace.

## 16. Definition of Done

- [ ] ADR **628** accepted; capability `CAP-PLT-MEFIAF-001` registered
- [ ] Law + YAML catalogs under `docs/architecture/autonomous_finance_operating/`
- [ ] Context `backend/contexts/autonomous_finance_operating/` scaffolded
- [ ] Fabric wired + ACL to P231, Financial Kernel, accounting, treasury
- [ ] Outbox events + ACL stubs (P231 · Kernel · Treasury · Workflow · P266 · P214-Z · Audit)
- [ ] Dual tests green; scorecard **ENTERPRISE_GRADE**
- [ ] OpenAPI `/api/v1/autonomous-finance-operating*`
- [ ] Forecast → recommend → gated Kernel/treasury execution path demonstrated
- [ ] **P271-A** unlocked · **P272** supply chain / logistics series unblocked

**MEFIAF is complete when:** MEOS has a Financial Intelligence OS fabric over P231/Kernel; autonomous accounting assists run under gates; forecasting and treasury intelligence operate; revenue/cost optimization assists; finance agents participate under governance; financial events join the Event Mesh; twins/KG support financial reasoning; MEOS progresses toward Autonomous Finance under human/Kernel authority — Governance Standard **11.0**.

**Principle:** MEFIAF productizes autonomous finance intelligence; it never replaces P231 or Financial Kernel, and never posts or pays without Kernel/treasury + Policy + Workflow + Audit accountability.

---

**NEXT EXECUTION:** **P272** — MEOS Enterprise Supply Chain Intelligence & Autonomous Logistics Platform — Procurement Intelligence, Inventory Optimization, Supplier Intelligence, Logistics Automation and Autonomous Supply Network Management (federate P232; never fork peer supply-chain APIs).
