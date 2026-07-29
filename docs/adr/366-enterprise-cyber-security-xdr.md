# ADR-366: Cyber Security — Enterprise XDR / EDR / NDR Platform (P210-G)

## Status

Accepted — P210-G Enterprise Extended / Endpoint / Network Detection & Response

## Context

ADR-361–365 established SoR `cyber_security` through SOC and SOAR. P210-G delivers the **unified detection & active defence layer**: EDR endpoint protection, NDR network visibility, XDR cross-domain correlation, detection engineering, AI threat analytics, threat hunting, and safeguarded automated response — without inventing sibling `xdr` / `edr` / `ndr` BCs, without siloed correlation, and without bypassing SOAR (P210-F), Workflow (approvals), or `security_incident` (IR lifecycle).

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/xdr*`. Never incomplete endpoint telemetry. Never insufficient network visibility. Never siloed XDR correlation. Never absent AI analytics. Never non-evolvable detection rules. Never unsafeguarded automated response. Never unverifiable agent integrity. Destructive response gated by AuthZ + Workflow; orchestration via SOAR playbooks. Telemetry plumbing via Observability / Integration — not peer-DB joins.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/xdr*`
3. Law: `ENTERPRISE_CYBER_SECURITY_XDR.md`
4. Catalogs: `CYBER_XDR_*.v1.yaml`
5. Runtime: `cs_platform_xdr.py`; aggregates; ACL; foundation
6. Quality gates enforce telemetry completeness, network visibility, unified correlation, AI analytics, evolvable rules, response safeguards, agent integrity

## Consequences

- Complements P210-D SOC, P210-F SOAR, and planned P210-E SIEM
- Emits detection signals for SOC/SIEM; triggers SOAR for multi-system response
- Forbidden sibling BCs: `xdr`, `edr`, `ndr`

## References

ADR-361–365 · ENTERPRISE_WORKFLOW_ENGINE.md · INTEGRATION_PLATFORM.md · MITRE ATT&CK · MITRE D3FEND · NIST CSF
