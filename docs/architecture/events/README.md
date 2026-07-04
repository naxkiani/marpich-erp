# Integration Event Contracts

Versioned JSON Schema definitions for cross-context integration events.

## Layout

| File pattern | Purpose |
|---|---|
| `_envelope.v1.json` | Base envelope — tenant, organization, user, security_context, correlation, timestamp |
| `{event_name}.v{version}.json` | Event-specific payload contract |

See [ENTERPRISE_EVENT_BUS.md](../ENTERPRISE_EVENT_BUS.md) for publisher/subscriber architecture.

Example: `platform.tenant.provisioned.v1.json`

## Validation

- Runtime/tests: `shared/contracts/event_validator.py`
- Contract tests: `tests/contracts/test_integration_event_contracts.py`

## Rules

1. Every new `IntegrationEvent` must pass the base envelope contract test
2. Register a specific schema before exposing the event to external consumers
3. Breaking payload changes require a new `event_version` and schema file
