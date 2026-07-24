# ADR-359: Secrets — Enterprise Deployment, DevSecOps, K8s & Observability (P209-N)

## Status

Accepted — P209-N Enterprise Deployment, DevSecOps, Kubernetes, Scalability & Observability Platform

## Context

ADR-345–358 delivered cryptographic trust capabilities, ops fabric, and governance. P209-N defines the **production operations foundation**: cloud-native deployment, Kubernetes, GitOps/DevSecOps, scalability, HA/DR, observability, and AIOps — still under SoR `secrets`, never a sibling `deploy_platform` / `secrets_sre_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/deploy*`. Never manual deployment. Never incomplete Kubernetes security. Never missing observability. Never CI/CD without security validation. Never undefined scaling strategy. Never unavailable disaster recovery. Never unmanaged infrastructure changes.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/deploy*`
3. Law: `ENTERPRISE_SECRETS_DEPLOY.md`
4. Catalogs: `SECRETS_DEPLOY_*.v1.yaml`
5. Runtime: `secrets_platform_deploy.py`; aggregates; ACL; foundation
6. Observability via Observability Platform; signing via P209-J; workload identity via P209-H; AuthZ / Audit / Workflow reused
7. Logical ops microservices are deployable units under `secrets`, not sibling BCs

## Consequences

- Distinct from `/ops*` (CQRS software fabric) vs `/deploy*` (K8s/DevSecOps/SRE runtime)
- Distinct from `/gov*` (governance/compliance) vs `/deploy*` (production operations)
- Does not invent a second Observability or CI/CD SoR — integrates via ACL + events

## References

ADR-345–358 · PERFORMANCE_STANDARD · ENTERPRISE_OBSERVABILITY_PLATFORM · API_GATEWAY · P209-H / P209-J
