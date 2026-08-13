# MEOS UI/UX Gap Report

**Date:** 2026-08-11 · **Surface:** `frontend/apps/admin_portal`

## Verdict

AppShell skeleton exists. It is **not** yet ONE NAV + ONE SEARCH + ONE AI + ONE NOTIFICATION with beautiful consistent UX.

## ONE surface scorecard

| Law | Status | Gap |
|-----|--------|-----|
| ONE IDENTITY | Partial | Real JWT login; per-page seed/login remains |
| ONE NAVIGATION | Fail → P0 fix | Flat hardcoded links; mobile sidebar hidden |
| ONE SEARCH | Fail → P0 fix | Unauthenticated GlobalSearch; no navigation |
| ONE AI | Partial | Shell AI calls API; page-local assistants remain |
| ONE NOTIFICATION | Fail → P0 fix | Bell unauthenticated; separate desk |
| ONE WORKFLOW | Fail → P0 fix | No desk until P0 |
| ONE AUDIT | Partial | Audit desk exists; shell not unified |
| Beautiful/consistent | Partial | Tokens OK; giant page components; emoji icon buttons |

## P0 UI work (this execution)

1. Auth-wire GlobalSearch + NotificationCenter
2. Registry-driven nav + command palette
3. Workflow desk
4. Mobile nav drawer
5. Route protection for `/` and `/modules`

## Non-goals (now)

- Do not invent industry_portal / POS / mobile_shell apps yet
- Do not extract all modules into packages before shell works
- Do not add more decorative screens
