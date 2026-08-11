# ADR 644 — MEOS Enterprise Cloud, Platform Engineering & Infrastructure Automation Intelligence Platform (MECPEI)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p287 · mecpei · cloud · platform-engineering · iac · gitops · kubernetes · kubernetes · kubernetes · productization
- **Related:** [ADR 643](643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md) · [ADR 642](642-meos-enterprise-service-management-sla-operations-intelligent-service-delivery-platform.md) · [ADR 632](632-meos-enterprise-asset-intelligence-autonomous-asset-management-platform.md) · [ADR 628](628-meos-enterprise-financial-intelligence-autonomous-finance-platform.md) · [ADR 645](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md) · [Law P287](../architecture/ENTERPRISE_MEOS_CLOUD_PLATFORM_ENGINEERING_INFRASTRUCTURE_AUTOMATION_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **Cloud / Platform Engineering / Infrastructure Automation / Internal Developer Platform** productization layer — without replacing Technology Operations/Observability (P286), Service Management (P285), Secrets, Feature Flags, or Financial Control (P271), and without ungated production provision/deploy.

## Decision

1. Establish SoR **`platform_engineering_operating`** as MECPEI fabric under API **`/api/v1/platform-engineering-operating*`**, schema **`platform_engineering_operating_*`**.
2. Capability **`CAP-PLT-MECPEI-001`**; fabric id **`meos_enterprise_cloud_platform_engineering_infrastructure_automation_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P286** = observes and operationalizes technology
   - **P287** = provisions, configures, deploys, automates, optimizes, governs
   - **P287 does not replace P286**
4. Federate-by-contract: P286, P285, P271, P275, Secrets, Feature Flags, Observability, Integration, Workflow — never fork Technology Operations APIs; never local secrets/flags/metrics; never local approval engines; never local GL.
5. Infrastructure definitions, environments, configurations and deployments are **versioned, declarative, reproducible, auditable**. Material provision/deploy require **Policy + Risk + Approval + Observability + Rollback + Verification + Audit** (or published Autonomy Threshold).
6. **No AI Agent may execute uncontrolled production changes outside Policy + Delegation Authority.** Autonomous actions require Authorization + Policy + Budget + Architecture + Security + Risk Threshold + Delegation.
7. Inference → **P214-Z** only; no module-local LLM.
8. Twin deploy/capacity scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MECPEI roadmap (P287-A…D) and **P288** DevSecOps / Secure Software Supply Chain series (delivered as normative law + ADR 645).
- P286 remains ops/observability SoR; MECPEI owns platform engineering, IaC, IDP and gated automation overlays.
- Ungated infrastructure mutation or merging P286+P287 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed IaC/deploy inside P286 Technology Ops | Violates observe vs provision/deploy split |
| Store cloud secrets in platform tables | Violates Secrets Platform law |
| Local feature flags for progressive delivery | Violates Feature Flag System law |
| Dual-write cloud cost into GL | Violates Financial Kernel / P271 |
| Ungated agent provision/deploy | Violates human platform governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P286 · P285 · P271 · Secrets · Feature Flags · Workflow · Policy · Audit)
- [x] Versioned IaC/environments · Policy-as-Code · rollback law
- [x] P286 boundary preserved explicitly
- [x] No ungated production provision/deploy · no local secrets
- [x] P288 delivered — [ADR 645 / MEDSSAD](645-meos-enterprise-devsecops-secure-software-supply-chain-application-delivery-intelligence-platform.md)
- [x] P289 delivered — [ADR 646 / MEAAGSI](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md)
