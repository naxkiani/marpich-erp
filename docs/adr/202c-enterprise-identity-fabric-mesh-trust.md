# ADR-202c: Enterprise Identity Fabric Mesh & Trust Intelligence (P198-C1)

## Status
Accepted

## Context
P198-A delivered federation domain and trust pairwise relationships.
P198-B delivered the protocol gateway (OAuth/OIDC/SAML/SCIM).
Enterprises still need a continuous zero-trust fabric: mesh topology across
IdPs and industry systems, a traversable trust graph, risk-based federation,
and executive security visibility — without forking Adaptive Auth, Identity Risk,
or Directory Identity Graph platforms.

## Decision
1. Extend `identity_federation` with Fabric Security services (no new BC).
2. Identity Fabric Mesh — topology, discovery, routing, sync, monitoring over
   providers/partners/tenants (config/plugin driven).
3. Trust Graph — local projection with nodes/edges/queries/propagation;
   production syncs to Directory Identity Graph via integration events.
4. Zero Trust Federation — every request validates identity/device/app/location/
   behavior/session/network/org/risk/trust/policy; Adaptive Auth ACL for PDP.
5. Risk-based federation — local composite scoring + Identity Risk
   `score_federation` ACL (`FEDERATION_RISK_SCORING`).
6. Session/token federation engines for cross-app SSO, SLO, token exchange.
7. Immutable `FederationAuditStore` + trust metrics + security dashboard.
8. Policies: `federation.zero_trust.*`, `federation.mesh.*`, `federation.risk.*`,
   `federation.trust.graph.*`, `federation.session.cross_app.*`.

## Consequences
- API surface under `/api/v1/federation/fabric/*`
- Cross-context calls only via ACL adapters (containers), never domain imports
- Mesh/trust graph remain policy-driven; no hardcoded IdPs or trust rules

## Compliance
Enterprise Architecture Governance Standard 8.4 — Zero Trust, Identity Fabric Native.
