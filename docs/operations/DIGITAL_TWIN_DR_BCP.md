# Digital Twin — Disaster Recovery & Business Continuity

**ADR-209 · Prompt 199-D1**

## RPO / RTO (topology-driven)

| Topology | RPO | RTO |
|----------|-----|-----|
| single_region | 5m | 30m |
| multi_region | 1m | 5m |
| edge | site-local cache; sync when online | per edge profile |

Configurable via Policy / topology catalog — never hardcoded in domain.

## Recovery modes

1. **Warm standby** (default): async replica DB + Event Mesh mirror  
2. **Hot standby** (banking/gov): active-active twins with conflict Policy  
3. **Rebuild**: snapshot + event replay from mesh offset · full SoR sync if corrupted  

## Continuity

- Edge sites continue with cached projections (read-only recommendations)  
- Authoritative mutations stay in source BCs  
- Break-glass: disable twin Intelligence flags; keep Identity Auth alive  

## Backup

- Postgres PITR for `identity_twin`  
- Snapshot objects (if offloaded) via platform object storage lifecycle  
- Test restore quarterly (chaos calendar)
