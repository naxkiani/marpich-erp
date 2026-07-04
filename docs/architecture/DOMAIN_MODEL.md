# Domain Model

## Ubiquitous Language

| Term | Definition |
|------|-----------|
| **Tenant** | An organization using the platform (hospital, bank, school) |
| **Industry Pack** | A configuration bundle activating modules for a vertical |
| **Module** | A composable capability with manifest, permissions, and events |
| **Bounded Context** | A domain boundary with its own model and ubiquitous language |
| **Aggregate** | Consistency boundary; all invariants enforced within |
| **Integration Event** | Cross-context message via event bus |
| **Provisioning** | Saga that creates tenant, schema, modules, and admin user |

## Core Aggregates

### Platform Context

```
Tenant (root)
├── Subscription
└── ModuleActivation[]

User (root) [Identity]
├── Role[]
└── Session[]

Module (root) [Registry]
├── ModuleVersion[]
└── TenantActivation[]
```

### Finance Context (shared across industries)

```
ChartOfAccounts (root)
├── Account[]
└── FiscalPeriod[]

JournalEntry (root)
├── JournalLine[]
└── PostingReference

Invoice (root)
├── InvoiceLine[]
└── PaymentApplication[]
```

### Healthcare Context

```
Patient (root)
├── Demographics
├── InsurancePolicy[]
└── ConsentRecord[]

Encounter (root)
├── ClinicalNote[]
├── Diagnosis[]
└── Procedure[]

Prescription (root)
└── PrescriptionLine[]
```

## Cross-Context References

Aggregates reference other contexts by **ID only**, never by object reference:

```typescript
// ✅ Correct
interface InvoiceLine {
  patientId: UniqueEntityId;  // reference to Healthcare context
}

// ❌ Forbidden
interface InvoiceLine {
  patient: Patient;  // direct cross-context coupling
}
```

## Event Catalog (Platform)

| Event | Producer | Consumers |
|-------|----------|-----------|
| `tenant.provisioned` | Tenant Service | Identity, Module Registry, AI |
| `module.activated` | Module Registry | All domain services |
| `user.created` | Identity | Audit, Notifications |
| `industry-pack.activated` | Tenant Service | AI, Reporting |

## Industry Pack → Module Mapping

See `packages/shared-kernel/src/contracts/industry-packs.ts` for the complete mapping of 25 industry verticals to composable modules.
