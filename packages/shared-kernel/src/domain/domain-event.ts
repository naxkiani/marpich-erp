import { UniqueEntityId } from "./unique-entity-id";
import { TenantId } from "./tenant-id";

export interface DomainEventMetadata {
  readonly correlationId: string;
  readonly causationId?: string | undefined;
  readonly tenantId: TenantId;
  readonly userId?: string | undefined;
  readonly occurredAt: Date;
}

export abstract class DomainEvent {
  readonly eventId: UniqueEntityId;
  readonly aggregateId: UniqueEntityId;
  readonly metadata: DomainEventMetadata;
  abstract readonly eventName: string;
  abstract readonly eventVersion: number;

  protected constructor(
    aggregateId: UniqueEntityId,
    metadata: DomainEventMetadata,
    eventId?: UniqueEntityId,
  ) {
    this.eventId = eventId ?? UniqueEntityId.create();
    this.aggregateId = aggregateId;
    this.metadata = metadata;
  }

  toPayload(): Record<string, unknown> {
    return {
      eventId: this.eventId.toString(),
      eventName: this.eventName,
      eventVersion: this.eventVersion,
      aggregateId: this.aggregateId.toString(),
      metadata: {
        correlationId: this.metadata.correlationId,
        causationId: this.metadata.causationId,
        tenantId: this.metadata.tenantId.toString(),
        userId: this.metadata.userId,
        occurredAt: this.metadata.occurredAt.toISOString(),
      },
    };
  }
}
