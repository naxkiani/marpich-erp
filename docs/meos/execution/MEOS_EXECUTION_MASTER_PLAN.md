# MEOS Execution Master Plan

**Status:** ACTIVE · Productization + Execution phase  
**Governance:** Enterprise Architecture Governance Standard **11.0**  
**Checkpoint:** P310 complete (architecture) → execution begins here  
**Overall readiness:** `NOT_READY` (see [MEOS_PRODUCTION_READINESS.md](MEOS_PRODUCTION_READINESS.md))

## Principle

Optimize for **real functionality + integration + reliability**, not number of blueprints, modules, or screens.  
Reuse existing Core platforms (Identity, AuthZ, Search, Notifications, Workflow, Audit, AI, Documents). **Never duplicate engines.**

## Wave model (dependency order)

| Wave | Focus | Gate before next |
|------|--------|------------------|
| **01** Platform Core | Identity, Tenant, AuthZ, Shell (nav/search/notify/AI), Audit, Search, Workflow UI, Event honesty, Postgres path | User login → navigate → search → notify → AI → workflow tasks → audit |
| **02** Business Core | CRM/Sales/Procurement/Finance/HR/Inventory (activate existing or implement, not blueprints) | Functional CRUD + events + audit |
| **03** Intelligence | Analytics, Data Mesh (P263), Knowledge Graph (P264), Information Intelligence (P310), AI depth | Permission-aware intelligence |
| **04** Governance & Security | Policy, Compliance, Privacy (P269), Cyber (P268), Zero Trust | Deny-by-default + immutable audit |
| **05** Autonomy | P266/P267 agents, self-healing (human-gated) | Policy + approval for high risk |

## P0–P5 priority

- **P0** Security / data integrity / one-shell honesty  
- **P1** Shared MEOS infrastructure (design system, CI, persistence)  
- **P2** Core business apps  
- **P3** Intelligence apps  
- **P4** Advanced AI / autonomy  
- **P5** Specialized / optional  

Never implement P5 while P0/P1 is broken.

## Phase map (01–40 → execution)

| Master phases | Execution action |
|---------------|------------------|
| 01 Architecture completion | This pack + continuous registry updates |
| 02–06 Design system / UX / shell / factory / FE | Wave 01 shell + tokens; Application Registry runtime |
| 07–09 Backend / DB / events | Postgres for Wave 01 cores; ROUTER honesty; outbox reuse |
| 10–14 Identity / workflow / AI / search / notifications | Activate existing APIs + Task Center UI |
| 15–23 Analytics → twins → autonomy | Later waves |
| 24–27 Application activation + UI quality | Registry-driven; no fake ACTIVE |
| 28–40 Test → prod → launch certification | Wave 01 CI first; full gates later |

## Current first slice (this execution)

1. Audit pack (this directory) — **exists; refresh continuously**  
2. Auth-wired ONE SEARCH / ONE NOTIFICATION / ONE AI — **done**  
3. Registry-driven ONE NAV + Command Palette — **done**  
4. Workflow Task Center UI — **done**  
5. ROUTER_SPECS honesty + Postgres Wave 01 runbook — **done**  
6. Design tokens + Wave 01 CI smoke — **done**  
7. **Phase A complete:** Healthcare loop + money-path 038–045 + activate→nav tests  
8. **Wave 03 activated:** intelligence smoke (search/analytics/AI)  
9. **Wave 04 activated:** privacy/DR runbooks + policy desk + perf baseline  
10. **Wave 05 gated:** AutonomyGate deny-by-default + flag/policy/workflow requirements  
11. **P1 identity/authz SQL + Postgres adapters** — merged (`main`)  
12. **Executive home Live Pulse + shared KpiStrip desks** — PR #16 (`feature/dashboard-home-complete`)  
13. **P0 DR scripts** — `meos-postgres-backup.sh` + `meos-postgres-restore-drill.sh`  
14. **P0 session cookie** — JWT in cookie + middleware exp/shape validation  

## Next dependency-ordered work

1. Land / merge dashboard PR #16 onto `main`  
2. Ops: schedule backups + `MEOS_BACKUP_S3_URI` + record restore drills  
3. Edge: HS256 verify session cookie when `JWT_SECRET` available to Next  
4. Registry YAML sync (nav IDs without app entries)  
5. Deepen Wave 02 Functional loops (education/banking beyond demo) — only after 1–3

## Definition of Functional

User → Login → Open app → Real data → Create/Update → Search/Filter → Workflow → Authorize → Events → Audit → Analytics → Notification → AI (if applicable) → Logout.

Fake seed-only demos do **not** count as Functional.

## Registry updates

After every verified task, update [MEOS_APPLICATION_REGISTRY.md](MEOS_APPLICATION_REGISTRY.md) / `.v1.yaml` and [MEOS_PRODUCTION_READINESS.md](MEOS_PRODUCTION_READINESS.md).
