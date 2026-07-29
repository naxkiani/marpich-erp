# ADR-368: Cyber Security — Threat Intelligence & Threat Hunting (P210-H)

## Status

Accepted — P210-H Enterprise Threat Intelligence & Threat Hunting Platform

## Context

ADR-361–367 established SoR `cyber_security` through SOC, SIEM, SOAR, and XDR. P210-H delivers the **strategic cyber intelligence layer**: feed collection, enrichment, fusion, threat entity model, proactive hunting, detection engineering, STIX/TAXII sharing, KG/Twin, AI-assisted intelligence — without inventing a sibling `threat_intel` / `threat_hunting` BC, without reactive-only hunting, and without disconnecting detection engineering from SIEM/XDR/SOAR.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/intel*`. Never unvalidated threat intelligence. Never reactive-only hunting. Never absent knowledge graph integration. Never unexplained AI recommendations. Never disconnected detection engineering. Never non-standard intelligence sharing. Never unsupported threat actor attribution. Operationalise intel to SOC/SIEM/SOAR/XDR via events and Integration Platform — not peer-DB joins.

## Decision

1. SoR remains `cyber_security`
2. Surfaces under `/api/v1/cyber-security/intel*`
3. Law: `ENTERPRISE_CYBER_SECURITY_THREAT_INTELLIGENCE.md`
4. Catalogs: `CYBER_INTEL_*.v1.yaml`
5. Runtime: `cs_platform_intel.py`; aggregates; ACL; foundation
6. Quality gates enforce validation, proactive hunting, KG, explainable AI, connected detection engineering, standards-based sharing, attribution

## Consequences

- Complements P210-D–G; feeds detection engineering into SIEM/XDR; hunts escalate via SOC/SOAR
- Forbidden sibling BCs: `threat_intel`, `threat_hunting`, `cti_platform`

## References

ADR-361–367 · STIX/TAXII · MITRE ATT&CK · MITRE D3FEND · NIST CSF · ISO 27001
