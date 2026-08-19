# MEOS Production Environment Record (P350)

**Date:** 2026-08-19T12:20:00Z  
**Purpose:** Record what production environment evidence exists **now**. Not a live environment.  
**P350_STATUS:** BLOCKED  
**PRODUCTION_IDENTITY:** LOCAL  
**This record is not a GO-LIVE certificate.**

No passwords, tokens, private keys, kubeconfig contents, or secret values are stored here.

## Identity

| Field | Value |
|-------|--------|
| Provider | NOT_SELECTED / NOT_AVAILABLE |
| Recommended class (P349) | MANAGED_KUBERNETES_PLUS_MANAGED_POSTGRESQL |
| Cluster identity | NOT_AVAILABLE |
| Region / location | NOT_AVAILABLE |
| Kubernetes API | NOT_AVAILABLE |
| Cluster version | NOT_AVAILABLE |
| Authorized identity | NOT_AVAILABLE |
| Namespace `marpich` | NOT_AVAILABLE |
| Helm release | NOT_DEPLOYED |
| Flux HelmRelease applied | NO |
| Deployed commit | NOT_AVAILABLE |
| Image | NOT_AVAILABLE |
| Image digest | NOT_AVAILABLE |
| Production hostname (live) | NOT_DEFINED |
| Helm DESIGNED hostname | `auth.marpich.io` (not DNS evidence) |

## Local observations (NON_PRODUCTION)

| Field | Value | Class |
|-------|--------|--------|
| PGHOST | 127.0.0.1 | LOCAL |
| PGPORT | 5433 | NON_PRODUCTION |
| Compose `:5444` | designed in `docker-compose.meos-prod.yml` | NON_PRODUCTION |
| Local `/health` | not used as G26-08 | NON_PRODUCTION |
| Git describe | 47258dfd-dirty | FORBIDDEN |
| `git status --short` empty | FALSE | FAIL G26-05 |

## Controls (production)

| Control | Status |
|---------|--------|
| Public-CA TLS | NOT_AVAILABLE |
| Secret manager | NOT_CONFIGURED |
| Ingress | NOT_AVAILABLE |
| Network policy (live) | NOT_AVAILABLE |
| Production backup ID | NOT_AVAILABLE |
| Production restore ID | NOT_AVAILABLE |
| Rollback exercised | NO (CONFIGURED only) |
| G23 alerts | FAIL |
| Tenant / app activation | ACTIVE_APPLICATIONS = 0 (unchanged) |
| Production traffic | NOT_ENABLED |

## Reuse path (designed, unused)

CI `identity-federation-enterprise.yml` → GHCR `ghcr.io/marpich/marpich-backend` → Helm `marpich-iam` → optional Flux → Kubernetes.

## Certification freeze

P0 = 1. P313 = NOT_CERTIFIED. P313_REENTRY_READY = FALSE. PRODUCTION_CERTIFIED = FALSE. GO_LIVE_READY = FALSE. GO_LIVE_AUTHORIZATION = NOT_APPROVED.
