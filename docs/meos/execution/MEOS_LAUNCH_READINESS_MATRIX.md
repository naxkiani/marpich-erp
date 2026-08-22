# MEOS Launch Readiness Matrix (P352)

Command: `python3 scripts/meos-launch-readiness.py`  
G26 command (unchanged): `python3 scripts/meos-ext-g26-readiness.py`

| Capability | Product | Production (G26) |
|------------|---------|------------------|
| PRODUCT_BUILD | TRUE | n/a |
| LOCAL | TRUE (compose.dev + Postgres `:5433` accepting) | LOCAL ≠ PRODUCTION |
| DEMO | TRUE (compose meosprod package) | COMPOSE_IS_PRODUCTION = FALSE |
| DOCKER / DOCKER_BUILD | TRUE after local build PASS | not G26 |
| DATABASE | READY on `:5433` | G26-02 BLOCKED |
| MIGRATION | TRUE (check + restore replay) | no prod migrate |
| BACKUP | CONFIGURED + local PASS | not PRODUCTION_BACKUP |
| RESTORE | local RESTORE_TEST PASS | PRODUCTION NOT_VERIFIED |
| OBSERVABILITY | CONFIGURED | G23 FAIL |
| SECURITY | CONFIGURED (probes, non-root, settings gates) | not prod verified |
| RELEASE | BLOCKED (dirty SHA) | G26-05 FAIL |
| VPS | READY_FOR_CREDENTIALS | — |
| HOSTINGER_VPS | PARTIAL / READY_FOR_CREDENTIALS (VPS package; not run on Hostinger) | shared = INCOMPATIBLE |
| AWS/Azure/GCP/K8s | READY_FOR_CREDENTIALS | G26-01 BLOCKED |

G26_READY remains FALSE. P0=1. P313 not started. ACTIVE=0. Traffic NOT_ENABLED.
