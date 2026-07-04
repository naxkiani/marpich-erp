# Module architecture

## Ubiquitous language

| Term | Definition |
|------|------------|
| Example | Primary aggregate in this scaffold |

## Aggregates

- **ExampleAggregate** — owns `name`, scoped by `tenant_id`

## Events published

- `module_id.example.created` (v1)

## Events consumed

- `identity.user.created` — optional ACL handler in `infrastructure/messaging/`

## Related ADRs

- ADR-031 Module architecture consistency
- ADR-017 Module structure standard
