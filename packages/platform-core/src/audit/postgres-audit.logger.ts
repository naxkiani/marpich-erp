import { Pool } from "pg";
import { v4 as uuidv4 } from "uuid";
import type { AuditEntry, IAuditLogger } from "./index";

export class PostgresAuditLogger implements IAuditLogger {
  constructor(private readonly pool: Pool) {}

  async log(entry: AuditEntry): Promise<void> {
    await this.pool.query(
      `INSERT INTO platform.audit_log
        (id, tenant_id, correlation_id, actor_id, action, resource_type, resource_id, payload, ip_address)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
      [
        uuidv4(),
        entry.tenantId,
        entry.correlationId,
        entry.actorId ?? null,
        entry.action,
        entry.resourceType,
        entry.resourceId ?? null,
        entry.payload ? JSON.stringify(entry.payload) : null,
        entry.ipAddress ?? null,
      ],
    );
  }
}

export class ConsoleAuditLogger implements IAuditLogger {
  async log(entry: AuditEntry): Promise<void> {
    console.log(
      JSON.stringify({ type: "audit", ...entry, occurredAt: new Date().toISOString() }),
    );
  }
}
