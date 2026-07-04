# Marpich Frontend (Next.js / React / TypeScript)

Modular UI aligned with backend bounded contexts.

> **Every page must satisfy:** [UI Page Standard](../docs/architecture/UI_PAGE_STANDARD.md) — 23 required items (shell + content). **Never skip any.**

## Layout

```
frontend/
├── core/                 # App shell, auth provider, theme, i18n/RTL
│   └── shell/            # CommandPalette, GlobalSearch, NotificationCenter, …
├── shared/               # Design system, hooks, utils
│   └── components/       # DataTable, SmartForm, EmptyState, Skeleton, …
├── modules/              # Feature modules (mirror backend)
│   ├── platform/
│   ├── finance/
│   └── …
└── apps/                 # Deployable Next.js applications
    ├── admin_portal/
    ├── industry_portal/
    ├── pos/
    └── mobile_shell/
```

## Module contract

Every module under `modules/{namespace}/{capability}/`:

| Layer | Responsibility |
|-------|----------------|
| `domain/` | Types, view models, client-side domain rules |
| `application/` | State, use cases, API clients |
| `infrastructure/` | Fetch adapters, local storage, WebSocket |
| `presentation/` | Components, pages, hooks |
| `tests/` | Unit + component tests |
| `docs/` | UX, permissions, AI/search/export hooks |

See also: [Module Structure Standard](../docs/architecture/MODULE_STRUCTURE_STANDARD.md).

## App Shell (every page — do not reimplement in modules)

| Widget | Component |
|--------|-----------|
| Command Palette | `CommandPalette` — `Cmd/Ctrl+K` |
| Global Search | `GlobalSearch` → `/api/v1/search/query` |
| Notification Center | `NotificationCenter` → `/api/v1/notifications` |
| Help | `HelpButton` |
| AI Assistant | `AIAssistantPanel` |
| Breadcrumb | `Breadcrumb` |
| Keyboard Shortcuts | `KeyboardShortcutsDialog` — `?` |
| Dark Mode | `ThemeProvider` + `ThemeToggle` |
| RTL / LTR | `LocaleProvider` + `DirectionProvider` |
| Responsive | Collapsible nav + breakpoints |

## Page content (every route)

Skeleton loading · Progress · Undo · Autosave · Empty states · Micro animations · Beautiful tables · Smart forms · Advanced filters · Export · Import · Print · Accessibility (WCAG 2.1 AA)

Use shared components from `shared/components/` — see UI Page Standard for full checklist.

## Run

```bash
cd frontend
pnpm install
pnpm dev
# Admin portal → http://localhost:3001
```

Environment:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
