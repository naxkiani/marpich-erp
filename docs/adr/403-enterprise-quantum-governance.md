# ADR-403: Quantum — Enterprise Quantum Governance, Regulation, Ethics & Responsible Computing (P215-K)

## Status

Accepted — SoR `quantum` (P215) continuous trust gate; deepened after P215-A–J delivery

## Context

MEOS requires a governed home for enterprise quantum computing, Quantum AI, and post-classical intelligence. P215-K delivers the **MEOS Quantum Responsible Intelligence Fabric** (policy, regulation, ethics, risk, compliance, audit, accountability, trust, KG/twin) as the governance control plane over all quantum capability surfaces A–J.

**Hard laws:** SoR is `quantum`. Surfaces under `/quantum/governance*`. MEOS Quantum Governance Platform SHALL ensure that all quantum technologies, algorithms, infrastructures and intelligence systems operate within trusted, ethical, compliant and accountable boundaries. PQC cryptography remains `secrets` (P209). Policy evaluation via Policy Engine / P208. Audit via Audit Platform. Approvals/human oversight via Workflow. AI via Enterprise AI. Responsible AI alignment via P214-H / P214-Y ACL (no sibling invention).

## Decision

1. Platform BC `quantum` — capability `CAP-PLT-QC-001`.
2. P215-K surfaces under `/api/v1/quantum/governance*`.
3. Fabric: `meos_quantum_responsible_intelligence_fabric`.
4. Law: `ENTERPRISE_QUANTUM_GOVERNANCE.md` (16-section blueprint).
5. Catalogs: `QUANTUM_GOVERNANCE_*.v1.yaml`.
6. Runtime: `qc_platform_governance.py`; aggregates; ACL; foundation validator.
7. Seven logical governance BCs (BC-01–BC-07) remain inside SoR `quantum`.
8. Forbidden sibling BCs for governance fragments remain forbidden.
9. P215-A–J are delivered capability surfaces under the same SoR; K remains the continuous trust gate.
10. Peer ACL: P209 / P210 / P212, P214-H / P214-Y, P215-A–J, Policy Engine, Audit, Workflow.

## Consequences

- Quantum workloads cannot ship without governance bindings.
- Foundation for P215-L twin / reality modeling.
- No duplication of Policy Engine, Audit, Secrets/PQC, Cyber, or Responsible AI SoRs.

## Alternatives considered

| Option | Rejected because |
|---|---|
| New `contexts/quantum_governance` BC | Sibling BC ban |
| Module-local PDP | Violates Policy Engine law |
| Local audit ledger in quantum | Violates Audit Platform |
| Own PQC / HSM in governance | Violates secrets (P209) |
| Embed Responsible AI / ethics LLM fork | Violates P214-H / P214-Y / AI Platform |

## References

ENTERPRISE_POLICY_ENGINE.md · ENTERPRISE_AUDIT_PLATFORM.md · P209 secrets · P210 cyber · P212 data_governance · P214-H · P214-Y · P215-A–J · ENTERPRISE_QUANTUM_GOVERNANCE.md
