# MEOS Release Registry

**Date:** 2026-08-18T11:50:00Z  
**Machine:** [MEOS_RELEASE_REGISTRY.v1.yaml](./MEOS_RELEASE_REGISTRY.v1.yaml)  
**Overall:** `NOT_RELEASE_CANDIDATE` · **`production_release_count: 0`**  
**P334:** inventoried changes have `release_id: NONE` except CHG-G25 tagging REL-P324-GOVERNANCE (LOCAL, **NOT_DEPLOYED**).

Law: never mark **RELEASE_CANDIDATE**, **APPROVED**, **DEPLOYED**, or **PRODUCTION_RELEASE** without evidence. Git describe at this gate: **`e941141-dirty`**.

## Lifecycle states (vocabulary)

`DEVELOPMENT` → `BUILD` → `VALIDATION` → `TESTING` → `SECURITY_REVIEW` → `CERTIFICATION` → `RELEASE_CANDIDATE` → `APPROVED` → `DEPLOYED` → `VERIFIED` → `ROLLED_BACK` → `DEPRECATED` → `RETIRED`

Honesty labels: `NOT_DEPLOYED` · `NOT_CERTIFIED` · `NOT_EXERCISED` · `BLOCKED`.

## Recorded releases (actual)

| RELEASE_ID | VERSION | COMMIT | ENV | TEST | SECURITY | CERT | DEPLOY | ROLLBACK | Production? |
|------------|---------|--------|-----|------|----------|------|--------|----------|-------------|
| `REL-P313-CERT-ATTEMPT` | NOT_TAGGED | `e941141` | LOCAL | PARTIAL | TRUST_CRITICAL | **NOT_CERTIFIED** | **NOT_DEPLOYED** | **NOT_EXERCISED** | **false** |
| `REL-P324-GOVERNANCE` | NOT_TAGGED | `e941141-dirty` | LOCAL | not green on immutable SHA | TRUST_CRITICAL | **NOT_CERTIFIED** | **NOT_DEPLOYED** | **NOT_EXERCISED** | **false** |

No CI build ID, container digest, or production artifact digest is recorded — those were **not found**.

## Environments

| Env | Actual |
|-----|--------|
| LOCAL | docker-compose.dev.yml (Postgres `:5433`) |
| TEST | GitHub Actions jobs (memory + service Postgres) |
| STAGING / CERTIFICATION | **NOT_IMPLEMENTED** |
| PRODUCTION | **BLOCKED** (G26) |

## Capture

`./scripts/meos-release-evidence.sh` writes `docs/meos/execution/.last_release_evidence.json` from git. It **cannot** set `production_release: true`.
