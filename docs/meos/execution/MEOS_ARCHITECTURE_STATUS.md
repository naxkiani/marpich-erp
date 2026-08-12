# MEOS Architecture Status

**Date:** 2026-08-12 · **Verdict:** Architecture-rich, execution-incomplete · Drift present

## Inventory

| Asset | Count / note |
|-------|----------------|
| `backend/contexts/` packages | ~79 |
| Empty scaffolds | 18 (crm, sales, tax, HR, …) |
| `registry.py` ALL_CONTEXTS | ~67 (≠ filesystem) |
| ROUTER_SPECS entries | 200+ |
| Missing packages in ROUTER_SPECS | **26** (silent skip at startup) |
| Default persistence | `memory` (`settings.persistence_backend`) |
| Postgres adapters present | Many Wave 01/healthcare contexts |

## Missing ROUTER packages (must not advertise as live)

`adaptive_authentication`, `ai_cfo_assistant`, `ai_governance`, `ai_security`, `data_protection`, `enterprise_api_gateway`, `enterprise_automation_platform`, `enterprise_decision_support`, `enterprise_event_bus`, `enterprise_executive_dashboard`, `enterprise_forecasting`, `enterprise_integration_security`, `enterprise_message_orchestration`, `enterprise_reliability_platform`, `enterprise_saga_orchestration`, `enterprise_webhook_platform`, `financial_ai_analytics`, `financial_anomaly_detection`, `financial_data_science`, `financial_kpi`, `fraud_detection`, `grc`, `mfa`, `natural_language_analytics`, `reporting`, `security`

**Action (Wave 01):** `filter_available_specs()` in `startup_registry.py` omits modules where `importlib.util.find_spec` is None before registration; omitted lists returned from `configure_application`.

## Boundary laws (still binding)

- No cross-context domain imports  
- Documents = blob SoR (`document_id`)  
- Workflow = P260 / `workflow` context only  
- AI inference via AI platform / P214-Z ACL — no module-local LLM  
- Audit via audit context + events — no local audit tables in business modules  

## Technical debt

1. Registry vs filesystem drift  
2. Silent `ModuleNotFoundError` skips hide broken routes  
3. Memory default blocks multi-instance / durable demos  
4. Frontend monolith under `admin_portal` (no `frontend/modules/`)  
5. Blueprint series P297–P310 docs without matching SoR scaffolds (by design until activation)

## Production architecture baseline

Monolith FastAPI + Next.js admin portal is acceptable for Wave 01. Microservices extraction is **not** a P0 requirement. Event fabric + outbox patterns already exist—activate consumers rather than rewrite.
