# Marpich UI Page Standard

**Status:** Canonical — every page must satisfy all items  
**Audience:** Frontend engineering, AI agents, designers  
**Companions:** [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) · [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md)

**Rule: Never skip any item. Shell provides globals; pages provide data patterns.**

---

## Architecture — Shell vs Page

```
┌─────────────────────────────────────────────────────────────────┐
│  App Shell (frontend/core/shell/) — wraps EVERY page            │
│  Command Palette · Global Search · Notifications · Help · AI    │
│  Breadcrumb · Shortcuts · Dark Mode · RTL/LTR · Responsive nav    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Page (frontend/modules/.../presentation/pages/)                 │
│  Skeleton · Progress · Undo · Autosave · Empty · Tables · Forms  │
│  Filters · Export · Import · Print · Micro animations · A11y      │
└─────────────────────────────────────────────────────────────────┘
```

| Scope | Provided by | Pages must NOT reimplement |
|-------|-------------|----------------------------|
| **Shell** | `AppShell` layout in `frontend/core/shell/` | Command palette, global search, notification drawer |
| **Page** | Module `presentation/` components | Domain tables, forms, filters — using shared design system |
| **Shared** | `frontend/shared/components/` | Reusable Table, Form, FilterBar, EmptyState, Skeleton |

---

## Required on Every Page (complete checklist)

### A — App Shell (global — mount once in layout)

| # | Requirement | Implementation |
|---|-------------|----------------|
| 1 | **Command Palette** | `Cmd+K` / `Ctrl+K` — actions, navigation, recent items (`CommandPalette`) |
| 2 | **Global Search** | Platform search API `/api/v1/search/query` — header search with suggest |
| 3 | **Notification Center** | Bell icon + inbox panel — `/api/v1/notifications` |
| 4 | **Help Button** | Context-sensitive help link / docs drawer per route |
| 5 | **AI Assistant** | Side panel or modal — module AI hooks from manifest |
| 6 | **Breadcrumb** | Route-derived trail; module namespace + resource |
| 7 | **Keyboard Shortcuts** | `?` opens shortcut sheet; standard bindings documented |
| 8 | **Dark Mode** | Theme toggle + `prefers-color-scheme`; CSS variables in `shared/theme/` |
| 9 | **RTL / LTR** | `dir` from locale; logical CSS; `fa-IR`, `ar-SA`, `en-US` minimum |
| 10 | **Responsive Design** | Mobile → tablet → desktop breakpoints; collapsible nav |

### B — Page content (every route/view)

| # | Requirement | Implementation |
|---|-------------|----------------|
| 11 | **Skeleton Loading** | `SkeletonTable`, `SkeletonForm` while data fetching |
| 12 | **Progress Indicators** | Linear/circular for long ops; step progress for wizards |
| 13 | **Undo** | Toast with undo for destructive/reversible actions |
| 14 | **Autosave** | Debounced save on forms; draft indicator |
| 15 | **Empty States** | Illustration + primary action when no data |
| 16 | **Micro Animations** | Subtle transitions (150–250ms); respect `prefers-reduced-motion` |
| 17 | **Beautiful Tables** | Shared `DataTable` — sort, select, column resize, sticky header |
| 18 | **Smart Forms** | Validation, field-level errors, dependent fields, inline help |
| 19 | **Advanced Filters** | FilterBar — date range, multi-select, saved filter presets |
| 20 | **Export** | CSV/Excel/PDF via platform report or client export |
| 21 | **Import** | Upload + validation preview + error report |
| 22 | **Print** | Print stylesheet / print-friendly view |
| 23 | **Accessibility** | WCAG 2.1 AA — focus order, ARIA, contrast, screen reader labels |

---

## Shared Component Library (reuse — never duplicate)

Build once in `frontend/shared/components/`:

| Component | Export name |
|-----------|-------------|
| Command palette | `CommandPalette` |
| Global search | `GlobalSearch` |
| Notifications | `NotificationCenter` |
| Help | `HelpButton` |
| AI panel | `AIAssistantPanel` |
| Breadcrumb | `Breadcrumb` |
| Shortcut overlay | `KeyboardShortcutsDialog` |
| Theme | `ThemeProvider`, `ThemeToggle` |
| Locale | `LocaleProvider`, `DirectionProvider` |
| Data table | `DataTable` |
| Form | `SmartForm`, `FormField` |
| Filters | `AdvancedFilterBar` |
| Empty state | `EmptyState` |
| Skeleton | `Skeleton`, `SkeletonTable` |
| Progress | `ProgressBar`, `StepProgress` |
| Export/Import | `ExportButton`, `ImportDialog` |
| Print | `PrintButton` |
| Undo toast | `UndoToast` |

Pages import from `@marpich/shared` — **never** copy inline implementations.

---

## Page Template (required structure)

```tsx
// frontend/modules/{ns}/{capability}/presentation/pages/ExamplePage.tsx

export function ExamplePage() {
  return (
    <PageLayout
      title={t("example.title")}
      breadcrumb={breadcrumb}
      actions={<PageActions export import print />}
    >
      <AdvancedFilterBar … />
      {isLoading ? <SkeletonTable /> : (
        data.length === 0 ? <EmptyState … /> : <DataTable … />
      )}
      <SmartForm autosave … />
    </PageLayout>
  );
}
```

`PageLayout` lives in `frontend/core/shell/` and assumes shell globals are already mounted.

---

## Keyboard Shortcuts (minimum standard)

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Command palette |
| `Cmd/Ctrl + /` | Focus global search |
| `?` | Show shortcuts |
| `Cmd/Ctrl + S` | Save (when form focused) |
| `Cmd/Ctrl + Z` | Undo last action (when available) |
| `Esc` | Close modal / panel |

---

## Accessibility Requirements

- Focus trap in modals; restore focus on close
- All interactive elements keyboard reachable
- Color contrast ≥ 4.5:1 (text), 3:1 (UI components)
- `aria-live` for async updates (save, export complete)
- Skip link to main content
- `prefers-reduced-motion`: disable non-essential animations

---

## PR Checklist (copy per page)

```markdown
## UI Page Standard (all required)

### Shell (via AppShell)
- [ ] Command Palette
- [ ] Global Search
- [ ] Notification Center
- [ ] Help Button
- [ ] AI Assistant
- [ ] Breadcrumb
- [ ] Keyboard Shortcuts
- [ ] Dark Mode
- [ ] RTL/LTR
- [ ] Responsive Design

### Page content
- [ ] Skeleton Loading
- [ ] Progress Indicators
- [ ] Undo
- [ ] Autosave
- [ ] Empty States
- [ ] Micro Animations
- [ ] Beautiful Tables
- [ ] Smart Forms
- [ ] Advanced Filters
- [ ] Export
- [ ] Import
- [ ] Print
- [ ] Accessibility
```

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-ui-page-standard.mdc` |
| App shell | `frontend/core/shell/` (implement globals here) |
| Design system | `frontend/shared/components/` |
| Frontend README | `frontend/README.md` |

**Review rejection:** New pages that bypass `AppShell` or reimplement shell widgets are incomplete.
