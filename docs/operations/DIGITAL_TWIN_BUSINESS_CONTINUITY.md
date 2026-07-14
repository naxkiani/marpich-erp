# Digital Twin — Business Continuity Guide

**Prompt:** V03-C02-P199-D2.2 · **ADR-210**  
**Engine SoR:** Business Continuity Platform (ADR-159)  
**Profile:** `docs/architecture/identity/TWIN_BCP_PROFILE.v1.yaml`

## Law

Twin BC plans are **registered** with the platform BC engine. Twin docs define critical functions and degrade modes — they do not replace industry BC for banking/healthcare/etc.

## Critical twin functions

| Function | Degrade mode |
|----------|--------------|
| Twin API | Fail closed on AuthZ-critical facet reads if stale beyond Policy |
| Sync workers | Pause noncritical consumers; keep security facet consumers |
| Intelligence | Feature-flag off (`twin.intelligence.enabled`) |
| Graph | Reduce max hops; Directory hydrate only |

## Emergency operations workflow

1. Declare incident (Sev1/2) via IR runbook.  
2. BC plan activation in ADR-159 (twin function id).  
3. Disable intelligence / enable read-only twin as Policy allows.  
4. Notify tenants via Notification Platform.  
5. Prefer Identity/Federation continuity over twin for login path.  
6. Post-event: recover projections (DR guide) + PIR.

## Industry continuity

Identity · Financial · Banking · University · Healthcare · Government continuity remain with owning BC packs. Twin is a **projection dependency**, not the SoR continuity owner.
