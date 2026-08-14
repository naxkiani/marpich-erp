# ADR-374: Cyber Security — Deployment, DevSecOps, Kubernetes & Observability (P210-N)

## Status

Accepted — P210-N Enterprise Deployment, DevSecOps, Kubernetes, Scalability & Observability Platform

## Context

ADR-361–373 established SoR `cyber_security` through AI governance. P210-N delivers the **cloud-native operating backbone**: automated deployment, DevSecOps validation, Kubernetes security, IaC/GitOps, service mesh, scalability/HA/DR, and security observability — without inventing sibling `deploy_platform` / `devsecops` / `k8s_platform` BCs, without replacing Enterprise Observability Platform telemetry plumbing, and without local secrets stores (P209).

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/deploy*`. Never non-automated deployment. Never incomplete Kubernetes security. Never non-reproducible infrastructure. Never missing observability. Never manual-only scaling. Never undefined disaster recovery. Never unintegrated security controls. Never DevSecOps pipelines without validation. Deployment approvals via Workflow; secrets/signing via P209; metrics/logs/traces via Enterprise Observability (OTel); SIEM/SOAR/XDR consume security observability events.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/deploy*`
3. Law: `ENTERPRISE_CYBER_SECURITY_DEPLOY.md`
4. Catalogs: `CYBER_DEPLOY_*.v1.yaml`
5. Runtime: `cs_platform_deploy.py`; aggregates; ACL; foundation
6. Quality gates enforce automation, K8s security, IaC reproducibility, observability, auto-scaling, DR, integrated controls, pipeline validation

## Consequences

- Operational backbone for all P210-D–M fabric domains
- Forbidden sibling BCs: `deploy_platform`, `devsecops`, `k8s_platform`, `cyber_observability`
- Distinct from enterprise observability (telemetry plumbing) and CI runners owned by platform engineering outside domain logic

## References

ADR-361–373 · ENTERPRISE_OBSERVABILITY_PLATFORM.md · SECURITY_STANDARD.md · PERFORMANCE_STANDARD.md · CIS Kubernetes Benchmark · NIST SP 800-190 · SLSA · Sigstore
