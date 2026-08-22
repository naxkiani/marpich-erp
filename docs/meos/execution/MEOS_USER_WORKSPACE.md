# MEOS User Workspace

**Date:** 2026-08-18T06:46:00Z  
**Shell SoR:** `frontend/core/src/shell/AppShell.tsx` via `AuthenticatedAppShell`.  
**Companion:** [MEOS_P320_ENTERPRISE_EXPERIENCE.md](./MEOS_P320_ENTERPRISE_EXPERIENCE.md)

## One platform, one shell

Every authenticated page uses AppShell: skip link, nav toggle, brand, **GlobalSearch**, command palette (⌘K), **NotificationCenter**, help, **AIAssistantPanel**, locale, theme, sidebar, `#main-content`.

Commands are AuthZ- and module-gated (`filterApplicationNav`). Inactive modules stay out of nav after snapshot load.

## Workspace by role (actual)

| Role code | Name | Workspace today |
|-----------|------|-----------------|
| `admin` | Administrator | Full nav the tenant has enabled |
| `staff` | Education Staff | Education permissions — not a separate shell |
| `student` | Student | Read academics permissions |
| `clinic_staff` / `hospital_staff` / `pharmacy_staff` / `laboratory_staff` | Healthcare staff | Healthcare desks if modules enabled |

There is **no** workspace switcher product (executive vs operator). Differentiation is **permissions ∩ enabled_modules**.

## Task → context → action

Task Center: `/enterprise/workflows` (`WorkflowDeskPage`) loads `/api/v1/workflow/tasks` + definitions. Complete via Task Center. Home pulse links open tasks to the same desk.

## Notification lifecycle

`EVENT → inbox API → NotificationCenter → mark read (PATCH) → optional Open desk`. Channels beyond in-app: Notification Platform exists; production delivery **NOT_AVAILABLE**. Priority taxonomy in UI: **INCOMPLETE** (unread badge only).

## Search

`GET /api/v1/search/query` plus local application nav hits. Unauthenticated: nav-only + sign-in message. Fail-soft if API down. Fake hits: **not generated** (empty/error if none).

## Copilot

Must display disclaimer. Must not invent live KPIs or incidents. Confirmation for high-impact actions: AutonomyGate (P319), not this panel.
