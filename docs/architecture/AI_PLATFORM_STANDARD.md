# Marpich AI Platform Standard

**Status:** Canonical — AI is a **platform service**, not an optional add-on  
**Audience:** Product, engineering, AI agents, module authors  
**Companions:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) · [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) · [CORE_PLATFORM.md](CORE_PLATFORM.md) · [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md) · [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md)

**Rule: AI is not an extra feature. Every module must expose the full AI surface below via the Core AI Service.**

---

## Platform Law

| Principle | Meaning |
|-----------|---------|
| **AI is a platform service** | One AI Service (`/api/v1/ai`) — models, prompts, inference, jobs, insights |
| **Modules expose, never embed** | No module-local LLM clients, vector DBs, or model weights |
| **Every module is AI-ready** | Activation registers hooks; UI uses `AIAssistantPanel` + module endpoints |
| **Tenant-scoped** | All inference, prompts, and insights carry `tenant_id` |

```
┌─────────────────────────────────────────────────────────────┐
│                    AI SERVICE (Core Platform)                │
│  /infer · /jobs · /insights · /documents/extract · …        │
└────────────────────────────┬────────────────────────────────┘
                             │ hooks + events
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   healthcare.*        education.*          banking.*
   aiHooks in manifest  same 14 surfaces     same 14 surfaces
```

---

## Required AI Surfaces — Every Module Must Expose

No module ships without declaring and wiring **all** capabilities (N/A only with ADR + product approval).

| # | Surface | Purpose | Platform API / pattern |
|---|---------|---------|------------------------|
| 1 | **AI Insights** | Actionable findings from domain data | `GET /api/v1/ai/insights?module={moduleId}` |
| 2 | **Predictions** | Forward-looking outcomes | `POST /api/v1/ai/infer` + `ai.prediction.completed` event |
| 3 | **Recommendations** | Next-best-action suggestions | Prompt hook `{moduleId}.recommendations` |
| 4 | **Summaries** | Condense records, threads, documents | Prompt hook `{moduleId}.summarize` |
| 5 | **Search** | Semantic / hybrid search over module entities | [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md) + AI rerank |
| 6 | **Assistant** | Conversational help for module workflows | `AIAssistantPanel` + `{moduleId}.assistant` prompt |
| 7 | **Automation** | AI-triggered workflows and tasks | Workflow hooks + `ai.automation.triggered` |
| 8 | **Document Intelligence** | OCR, classification, extraction | AI Service → [ENTERPRISE_DOCUMENT_EXCHANGE.md](ENTERPRISE_DOCUMENT_EXCHANGE.md) |
| 9 | **Voice Commands** | Speech → intent → action | Platform voice gateway → module intent map |
| 10 | **Chat Interface** | Persistent module-scoped chat threads | `/api/v1/ai/chat/sessions` (module context) |
| 11 | **Report Explanation** | Natural language report narrative | Report Engine + `{moduleId}.report.explain` |
| 12 | **Anomaly Detection** | Outlier / fraud / compliance signals | Subscribe domain events → `ai.anomaly.detected` |
| 13 | **Forecasting** | Time-series and demand projections | `POST /api/v1/ai/jobs` (forecast job type) |
| 14 | **Optimization Suggestions** | Efficiency and cost improvements | Insight type `optimization` on `/insights` |
| 15 | **Health Analysis** | Platform telemetry RCA + anomaly | `POST /api/v1/ai/health/analyze` — [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md) |

---

## Module Manifest — AI Block (required)

`context.yaml` / `IModuleManifest` must include:

```yaml
ai:
  enabled: true
  surfaces:
    insights: true
    predictions: true
    recommendations: true
    summaries: true
    search: true
    assistant: true
    automation: true
    document_intelligence: true
    voice_commands: true
    chat: true
    report_explanation: true
    anomaly_detection: true
    forecasting: true
    optimization: true
  prompt_templates:
    - id: "{moduleId}.assistant"
      purpose: "Conversational assistant for module workflows"
    - id: "{moduleId}.summarize"
      purpose: "Summarize primary aggregate"
    - id: "{moduleId}.recommendations"
      purpose: "Next-best-action recommendations"
    - id: "{moduleId}.report.explain"
      purpose: "Explain generated reports"
  event_subscriptions:
    - domain events that feed anomaly detection and predictions
  event_publications:
    - ai.insight.generated (module-scoped payload)
    - ai.prediction.completed
    - ai.anomaly.detected
  permissions:
    - "{moduleId}.ai.read"
    - "{moduleId}.ai.infer"
    - "{moduleId}.ai.admin"
```

TypeScript manifest fields: `aiSurfaces`, `aiPromptTemplates`, `aiPermissions` — see [MODULE_SYSTEM.md](MODULE_SYSTEM.md).

---

## Backend Integration (every module)

```
backend/contexts/{module}/
├── application/
│   └── ai_service.py          # ACL — calls platform AI API only
├── presentation/
│   └── ai_router.py           # /api/v1/{module}/ai/* proxies to platform + module context
└── context.yaml               # ai: block (all surfaces true)
```

| Rule | Detail |
|------|--------|
| **No direct model calls** | Use `shared/infrastructure/ai/` client (when implemented) or HTTP to `/api/v1/ai` |
| **Context injection** | Pass `tenant_id`, `module_id`, aggregate IDs in every inference request |
| **Audit** | All AI calls emit auditable events |
| **Permissions** | Guard with `{moduleId}.ai.infer` |

---

## Frontend Integration (every module UI)

| Surface | Component / hook |
|---------|------------------|
| Assistant, Chat | `AIAssistantPanel` + module chat route |
| Insights, Recommendations | `AIInsightsPanel` in `PageLayout` actions |
| Search | `GlobalSearch` + module semantic index |
| Report explanation | `ReportExplainButton` on report views |
| Voice | Platform voice button in AppShell |

Reuse `@marpich/shared` — never build module-local chat UI from scratch.

---

## Module AI Checklist (copy per module)

```markdown
## AI Platform (all required)

- [ ] AI Insights
- [ ] Predictions
- [ ] Recommendations
- [ ] Summaries
- [ ] Search (semantic / hybrid)
- [ ] Assistant
- [ ] Automation
- [ ] Document Intelligence
- [ ] Voice Commands
- [ ] Chat Interface
- [ ] Report Explanation
- [ ] Anomaly Detection
- [ ] Forecasting
- [ ] Optimization Suggestions
- [ ] context.yaml `ai:` block complete
- [ ] Permissions `{moduleId}.ai.*` registered
- [ ] No embedded LLM / vector store in module
```

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-ai-platform.mdc` |
| AI Service spec | [CORE_PLATFORM.md](CORE_PLATFORM.md) § AI Service |
| Module structure | [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) |

**Review rejection:** Modules treating AI as optional, or missing manifest surfaces, are incomplete.
