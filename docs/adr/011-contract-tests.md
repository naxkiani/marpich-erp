# ADR-011: Contract Tests

## Status

Accepted

## Context

Marpich exposes **contract-first REST APIs** and **versioned integration events**. Without automated contract tests, frontend clients, industry modules, and external integrators can break silently when payloads drift.

## Decision

Introduce a **contract test suite** under `tests/contracts/` with three layers:

### 1. Integration event contracts

- Base envelope schema: `docs/architecture/events/_envelope.v1.json`
- Per-event schemas: `{event_name}.v{version}.json`
- Validator: `shared/contracts/event_validator.py` (JSON Schema draft-07)
- Auto-discovery of all `IntegrationEvent` subclasses via `shared/contracts/event_samples.py`

### 2. OpenAPI surface contracts

- Assert required paths exist in `/api/openapi.json`
- Assert platform tags are registered
- Assert public list endpoints return `{ "data": ... }` envelope

### 3. Runtime contract tests

- Capture events during real API flows (e.g. tenant provision)
- Validate captured envelopes against registered schemas

## Rules

- New integration event → add JSON schema in `docs/architecture/events/` before merge
- Breaking REST or event change → bump version + ADR
- CI runs `pytest tests/contracts` with memory backend (no Postgres required)

## Consequences

- `jsonschema` added to dev dependencies
- Schema drift fails CI before consumers break
- Event catalog grows incrementally; unregistered events still must pass base envelope tests
