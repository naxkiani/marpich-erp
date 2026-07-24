# Modules desk & Platform Dashboard — architecture notes

**Owning platform:** Core Platform (`core_platform`) — industry packs & tenants  
**UI surfaces:** `/modules` (P32), `/` Dashboard (P33)

## Modules desk (P32)

`ModulesDeskPage` — UI-only care depth on the pack catalog:

- StepProgress: browse → filter → select → launch
- Left rail + `useAutosave` (`marpich.modules.desk.draft`)
- Print + Export · i18n en/fa/ar

## Platform Dashboard (P33)

`DashboardPage` — same platform APIs, UI care depth:

- StepProgress: sign in → catalog → provision → operate
- Workflow panel on the existing rail
- `useAutosave` (`marpich.dashboard.platform.draft`) — never stores password
- i18n en/fa/ar

## API reuse

`GET /api/v1/platform/industry-packs` · tenants via `platformClient` (provision / activate / suspend).

No new aggregates — Core Platform remains SoR for packs and tenants.
