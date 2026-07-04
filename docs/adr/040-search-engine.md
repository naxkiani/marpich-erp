# ADR-040: Enterprise Search Engine — Security-First Discovery

## Status

Accepted

## Context

Marpich requires unified discovery across 40+ modules without cross-database queries (ADR-012, SERVICE_BOUNDARIES). The existing `search` context provides event-driven indexing, basic full-text, suggest, and query audit — but lacks canonical design for global/module/semantic/AI/OCR/document/image search, saved searches, ranking, permission-filtered results, analytics, and history.

Product leadership mandated: **every search respects security permissions.**

## Decision

Adopt **`docs/architecture/ENTERPRISE_SEARCH_ENGINE.md`** as canonical search law.

### Search modes

Global, Module, Full Text, Semantic, AI Search, Document, OCR, Image Metadata.

### Security-first pipeline

JWT + tenant → execute query on tenant partition → **per-hit permission filter** (fail closed) → rank → log history/analytics.

### Indexing

Integration events only — never module DB reads. OCR and embeddings via AI Service. OpenSearch for production full-text.

### Features

Filters, saved searches, suggestions, ranking, tenant isolation, search analytics, search history.

### Module rule

Register index events + `read_permission` facet; query via Search API only.

## Consequences

- Permission filter layer required before returning hits
- AI Service provides embeddings and AI search parse/rerank — Search orchestrates
- Saved searches and history APIs added
- OpenSearch migration path documented

## Alternatives considered

- Per-module Elasticsearch — rejected (duplication, no global search)
- Search without ACL post-filter — rejected (security law)
- Direct module DB full-text — rejected (SERVICE_BOUNDARIES)
