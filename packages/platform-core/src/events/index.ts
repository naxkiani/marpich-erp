import { Pool } from "pg";
import { v4 as uuidv4 } from "uuid";
import type { DomainEvent } from "@marpich/shared-kernel";

export interface IOutboxPublisher {
  publish(event: DomainEvent): Promise<void>;
}

export const OUTBOX_PUBLISHER = Symbol("OUTBOX_PUBLISHER");

export class PostgresOutboxPublisher implements IOutboxPublisher {
  constructor(private readonly pool: Pool) {}

  async publish(event: DomainEvent): Promise<void> {
    const payload = event.toPayload();
    await this.pool.query(
      `INSERT INTO platform.outbox (id, tenant_id, event_name, event_version, payload)
       VALUES ($1, $2, $3, $4, $5)`,
      [
        uuidv4(),
        event.metadata.tenantId.toString(),
        event.eventName,
        event.eventVersion,
        JSON.stringify(payload),
      ],
    );
  }
}

export class ConsoleOutboxPublisher implements IOutboxPublisher {
  async publish(event: DomainEvent): Promise<void> {
    console.log(
      JSON.stringify({
        type: "domain_event",
        ...event.toPayload(),
      }),
    );
  }
}
