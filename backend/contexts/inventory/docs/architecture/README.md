# Inventory — stock levels

Tenant-scoped SKU balances. POS decrements via ACL on `pos.sale.completed`
(never cross-schema SQL).

## Persistence (P5.2)

- Memory default; Postgres `inventory.stock_levels` when `PERSISTENCE_BACKEND=postgres`
- Migration: `034_university_inventory_postgres.sql`
- Unique `(tenant_id, sku)` + index on `(tenant_id, …)`
