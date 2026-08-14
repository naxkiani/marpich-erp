# Enterprise Cyber Security — Threat Intelligence & Hunting (P210-H)

**SoR:** `cyber_security` · **ADR:** 368 · **API:** `/api/v1/cyber-security/intel*`

## Mission

Collect, enrich, analyse, correlate, share and act upon cyber threat intelligence — predict attacks, enable proactive hunting, support AI-assisted investigations, continuously improve defence.

## Vision

Autonomous Threat Intelligence Fabric: every threat understood, every campaign correlated, every indicator enriched, every hunt evidence-driven, every detection continuously improved, every lesson strengthens resilience.

## Architecture layers

External Intelligence → Collection → Normalization → Enrichment → Threat Intelligence Fusion → Knowledge Graph → Threat Analytics → Threat Hunting → Detection Engineering → SOC / SIEM / SOAR → Executive Intelligence

## Hard laws (quality gates)

- Never threat intelligence cannot be validated
- Never threat hunting is reactive only
- Never knowledge graph integration is absent
- Never AI cannot explain recommendations
- Never detection engineering is disconnected
- Never intelligence sharing lacks standards
- Never threat actor attribution is unsupported

## Boundaries

| Concern | Owner |
|---|---|
| CTI / hunting / detection engineering packs | `cyber_security` (this surface) |
| Alert triage | P210-D SOC |
| Telemetry analytics | P210-E SIEM |
| Response playbooks | P210-F SOAR |
| Endpoint/network signals | P210-G XDR |
| IR lifecycle | `security_incident` |
| Feed connectors | Integration Platform |
| Platform KG fabric (enterprise) | P210-K (planned); local intel graph bindings here |

## Forbidden

- Sibling BC `threat_intel`, `threat_hunting`, `cti_platform`
- Unvalidated / untrusted feeds without source trust scoring
- Reactive-only hunting (no hypothesis / proactive planner)
- AI recommendations without explanation
- Detection packs that never publish to SIEM/XDR
- Proprietary-only sharing without STIX/TAXII (or equivalent standards)
- Attribution without supported actor/campaign model

## Compliance

ISO 27001 · NIST CSF · MITRE ATT&CK · MITRE D3FEND · STIX/TAXII · SOC 2
