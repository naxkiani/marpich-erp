# MEOS Functional Gap Report

**Date:** 2026-08-11

## What a real user can do today

| Flow | Works? |
|------|--------|
| Authenticate (register/login JWT) | Yes |
| Open dashboard / activate packs | Yes (if API up) |
| Hospital/clinic/pharmacy/lab CRUD desks | Yes (memory default) |
| Document studio / messenger / audit / notifications desks | Demo-level |
| Global search / shell inbox | Degraded → P0 |
| Workflow approvals in UI | No → P0 |
| Tax/sales/CRM/HR | No (scaffold) |

## Functional gaps by platform law

1. **Identity:** MFA package referenced but missing; session cookie is soft guard only
2. **Navigation:** Not activation/permission driven
3. **Search:** API exists; shell not integrated
4. **AI:** Assist exists; grounding/audit incomplete for enterprise use
5. **Notifications:** API exists; shell not integrated
6. **Workflow:** API exists; no UX
7. **Audit:** Desk exists; not all mutations proven durable-audited
8. **Governance:** Policy API exists; no unified governance UX

## Success condition (target)

A user can: open MEOS → authenticate → navigate → open apps → create data → run workflows → search → use AI → see analytics → receive notifications → complete enterprise tasks.

Current distance: **demo slice ≈ 25–35%** of that path; P0 closes shell integration first.
