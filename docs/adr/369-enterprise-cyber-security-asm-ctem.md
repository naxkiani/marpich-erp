# ADR-369: Cyber Security — ASM & CTEM (P210-I)

## Status

Accepted — P210-I Enterprise Attack Surface Management & Continuous Threat Exposure Management

## Context

ADR-361–368 established SoR `cyber_security` through SOC, SIEM, SOAR, XDR, and Threat Intelligence. P210-I delivers the **enterprise cyber exposure intelligence layer**: continuous asset discovery, internal/external/cloud attack surface mapping, exposure lifecycle, vulnerability intelligence, attack path analysis, AI risk prioritization with business context, remediation orchestration with validation, and continuous CTEM lifecycle — without inventing sibling `asm` / `ctem` / `easm` BCs.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/asm*`. Never incomplete asset discovery. Never non-continuous external attack surface monitoring. Never risk prioritization without business context. Never absent attack path analysis. Never unexplained AI recommendations. Never unvalidated remediation. Never non-continuous CTEM lifecycle. Remediation orchestration via SOAR + Workflow; discovery connectors via Integration Platform; vuln/threat context from P210-H.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/asm*`
3. Law: `ENTERPRISE_CYBER_SECURITY_ASM_CTEM.md`
4. Catalogs: `CYBER_ASM_*.v1.yaml`
5. Runtime: `cs_platform_asm.py`; aggregates; ACL; foundation
6. Quality gates enforce discovery completeness, continuous EASM, business-context risk, attack paths, explainable AI, validated remediation, continuous CTEM

## Consequences

- Complements P210-D–H; feeds exposure signals to SOC/SIEM; remediation via SOAR
- Forbidden sibling BCs: `asm`, `ctem`, `easm`, `caasm`

## References

ADR-361–368 · NIST CSF · NIST SP 800-53 · CIS Controls · ISO 27001 · Gartner CTEM
