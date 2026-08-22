# MEOS P320 — Enterprise Experience, Workspace & Adoption

**Date:** 2026-08-18T06:46:00Z  
**Decision:** Production UX **not certified**. Experience maturity: **`FUNCTIONAL`** (partial shell + desks). **Not** CONSISTENT (unverified a11y/E2E), USABLE (no journey proof), PRODUCTIVE, ADOPTED, or EXCELLENT.  
**P321:** **opened as integration fabric gate** — no production-active integrations. See [MEOS_P321_INTEGRATION_FABRIC.md](./MEOS_P321_INTEGRATION_FABRIC.md).  
**P334:** **ADOPTED remains false**. Overlay [MEOS_ADOPTION_STANDARD.md](./MEOS_ADOPTION_STANDARD.md). Demo loops are not DAU.

P320 consolidates the existing AppShell, Task Center, search, notifications, and copilot. It is **not** a new frontend, design system, portal, workflow engine, or AI platform.

## 1. Actual P319 status (precondition)

| Signal | Actual |
|--------|--------|
| P319 | **`BLOCK_AUTOMATION`**; 0 ACTIVE automations |
| P318 | Intelligence **FOUNDATION**; Decision Fabric not declared |
| P317 | **`TRUST_CRITICAL`** |
| P316 | SRE **NOT STARTED** |
| `PRODUCTION_STATE` | **false** (`PRODUCTION_ACTIVE`) |
| `APPLICATION_STATE` | Registry `NOT_READY`; **no app ACTIVE** |
| `INTELLIGENCE_STATE` | FOUNDATION |
| `AUTOMATION_STATE` | BLOCK_AUTOMATION |
| `UIUX_STATE` | AppShell **IMPLEMENTED**; P313 **G20 FAIL** / **G21 FAIL** |
| `SEARCH_STATE` | Shell + `/api/v1/search/query`; production **NOT_AVAILABLE** |
| `TASK_STATE` | `WorkflowDeskPage` + `/api/v1/workflow/tasks` |
| `NOTIFICATION_STATE` | Inbox API + NotificationCenter |
| `AI_STATE` | Copilot → stub assist (G18) |

Do **not** treat a route or menu item as production-ready.

## 2. Experience inventory

| Surface | Location | Map |
|---------|----------|-----|
| Global shell | `frontend/core/src/shell/AppShell.tsx` | **IMPLEMENTED** / **CONNECTED** to layout |
| Navigation | `ShellNav` + `filterApplicationNav` (AuthZ ∩ modules) | **FUNCTIONAL** (code); production **VERIFIED** = no |
| Dashboards | Home pulse, banking/observability desks | Home = catalog counts; **INCOMPLETE** as exec SSOT |
| Applications | Registry TESTED desks vs `coming_soon` | Mixed; empty verticals **INCOMPLETE** |
| Search | `GlobalSearch.tsx` | **CONNECTED**; E2E production **NOT_AVAILABLE** |
| Task Center | `/enterprise/workflows` | **FUNCTIONAL** vs API; production **NOT_AVAILABLE** |
| Notifications | Shell panel + desk | **FUNCTIONAL** vs inbox API |
| AI copilot | `AIAssistantPanel` | **IMPLEMENTED**; replies are **not FACT** |
| Forms/tables | `@marpich/shared` DataTable / filters | **IMPLEMENTED** on Functional desks |
| Workflow UX | Workflow desk | **CONNECTED** to backend tasks |
| Settings/admin | partial | **INCOMPLETE** |
| Duplicate | Default AppShell commands vs AuthZ-filtered commands | Auth path uses filtered commands — OK |

## 3–4. Roles (repository only)

From `Role` aggregate: `admin`, `staff` (education), `student`, `clinic_staff`, `hospital_staff`, `pharmacy_staff`, `laboratory_staff`.  
**Not invented:** EXECUTIVE / ANALYST / AUDITOR / CUSTOMER as first-class workspace personas (no dedicated workspace switcher).  
Nav is **permission + enabled_modules**, not a named executive/operator workspace product.

## 5. Personalization

Widgets/favorites/saved-search persistence: **NOT_IMPLEMENTED** as a user-workspace store. Must not bypass AuthZ if added later.

## 6–10. Shell, search, tasks, notifications, actions

See [MEOS_USER_WORKSPACE.md](./MEOS_USER_WORKSPACE.md). Contextual KPI drill-down to banking from catalog counts was removed in P318.

## 11–12. Executive / operator

Executive: home pulse with **DATA_QUALITY_WARNING** — not production health tiles.  
Operator: Task Center + notifications + search — **no** separate operator shell. Minimize-exec-info: **NOT_IMPLEMENTED** as a distinct layout.

## 13. Application experience vs registry

Reconciled with [MEOS_APPLICATION_REGISTRY.md](./MEOS_APPLICATION_REGISTRY.md): **no ACTIVE**. TESTED apps have desks + APIs (demo/workstation). `coming_soon` must stay hidden/gated.

## 14–16. Forms, tables, workflow

Shared components exist. Production UX of every form: **IMPLEMENTED_UNVERIFIED**. Workflow current/next/owner from API fields when present.

## 17–18. AI copilot / action safety

Copilot calls `/api/v1/ai/assist`. P320 UI shows **disclaimer** (not FACT; DATA_NOT_AVAILABLE). High-impact AI actions remain gated (P319 AutonomyGate). No silent execute.

## 19. Knowledge

No second knowledge UI. Graph is catalog/ACL only (P318).

## 20–22. Responsive / RTL / a11y

Responsive nav toggle exists. `DirectionProvider` + fa-IR/ar-SA. P320 localized skip-link, menu, search errors, copilot strings.  
**G20** Playwright: **FAIL** / not run. **G21** a11y measurement: **FAIL** / **NOT_AVAILABLE**. Do not claim WCAG compliance.

## 23–25. Visual system / quality / empty states

Tokens in `frontend/shared/src/theme/tokens.css`. Shared EmptyState/Skeleton on desks. Remaining hardcoded English may still exist on some desks. Arabic `app.name` typo (`مارpich`) **fixed** to ماربيتش.

## 26–28. Onboarding / productivity / adoption

First-run product tour: **NOT_IMPLEMENTED**. Click-depth / DAU: **NOT_AVAILABLE**. Do not invent adoption.

## 29–31. Feedback / performance / privacy UX

No second feedback platform. Bundle/RUM: **NOT_AVAILABLE**. Permission errors exist on pulse/search (fail-soft).

## 32. Activation

No registry promotions this phase.

## 33–34. E2E / production UX

No Playwright in repo. Contract tests (auth on home-pulse) ≠ browser journeys. **Do not certify** from screenshots. LOGIN→…→AUDIT production path: **NOT_AVAILABLE** / G20 **FAIL**.

## 35. Documentation

Created: this file, [MEOS_USER_WORKSPACE.md](./MEOS_USER_WORKSPACE.md), [MEOS_UX_QUALITY_REPORT.md](./MEOS_UX_QUALITY_REPORT.md), [MEOS_ADOPTION_STATUS.md](./MEOS_ADOPTION_STATUS.md).  
Updated: [MEOS_UIUX_STATUS.md](./MEOS_UIUX_STATUS.md) (not duplicated).

## 36. Maturity

```
FUNCTIONAL → CONSISTENT → USABLE → PRODUCTIVE → ADOPTED → EXCELLENT
     ▲
  current (partial)
```

**ADOPTED is not claimed.**
