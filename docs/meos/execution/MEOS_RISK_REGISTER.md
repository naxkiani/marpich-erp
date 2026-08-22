# MEOS Enterprise Risk Register

**Date:** 2026-08-18T05:56:36Z · **P328 overlay:** 2026-08-18T13:00:00Z  
**Owners:** **NOT_AVAILABLE** (not invented). Unowned critical: **R-01**.  
**Likelihood/impact:** qualitative, from launch evidence only — not production telemetry.  
**Numeric score / appetite:** **NOT_SCORED** / **NOT_DECLARED**.  
**Machine overlay:** [MEOS_RISK_REGISTRY.v1.yaml](./MEOS_RISK_REGISTRY.v1.yaml) · [MEOS_RISK_REGISTRY.md](./MEOS_RISK_REGISTRY.md)

| ID | Category | Risk | Impact | Likelihood | Severity | Current control | Evidence | Mitigation | Residual |
|----|----------|------|--------|------------|----------|-----------------|----------|------------|----------|
| R-01 | AVAILABILITY | No production cluster | Cannot go live | Certain (now) | Critical | Demo/workstation only | P313 G26, P314 | Provision real production | High until cluster exists |
| R-02 | OPERATIONAL | No production rollback exercise | Cannot recover a live release | Certain | High | Restore drill on demo DB | P313 G27 | Exercise after first prod deploy | High |
| R-03 | SECURITY | No production alerting | Failures undiagnosable in prod | High if launched anyway | High | `/health` `/ready` in code | P313 G23 | Alerting on real cluster | High |
| R-04 | AI | Stub assist mistaken for production AI | Misleading trust | Medium | High | Assist permissioned 401/200 | P313 G18 | Do not activate AI until governed model | High |
| R-05 | PRIVACY | DSAR/erasure not runtime-certified | Privacy rights unproven | Medium if PII in prod | High | Policy evaluate smoke | P313 G19 | Runtime privacy path before prod PII | High |
| R-06 | SECURITY | Dirty SHA / no immutable prod release | Unattributable deploy | Certain | High | git `e941141-dirty` | P313 G25 | Tag + CI on immutable SHA | Medium |
| R-07 | COMPLIANCE | No mapped production jurisdiction | Cannot claim compliance | Certain | High | None | P317 | Map obligations after deploy region known | High |

No additional risks invented from empty production logs.  
**P328:** states remain **ASSESSED**. Production monitoring **none**. Do not add taxonomy fillers (FINANCIAL, REPUTATIONAL, …) without evidence.
