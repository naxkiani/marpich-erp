import { DomainEvent, UniqueEntityId, TenantId } from "@marpich/shared-kernel";

export interface TenantProvisionedPayload {
  name: string;
  industryPack: string;
  enabledModules: string[];
}

export class TenantProvisionedEvent extends DomainEvent {
  readonly eventName = "tenant.provisioned";
  readonly eventVersion = 1;
  readonly payload: TenantProvisionedPayload;

  constructor(
    aggregateId: UniqueEntityId,
    tenantId: TenantId,
    metadata: {
      correlationId: string;
      tenantId: TenantId;
      occurredAt: Date;
      userId?: string;
    },
    payload: TenantProvisionedPayload,
  ) {
    super(aggregateId, metadata);
    this.payload = payload;
  }

  override toPayload(): Record<string, unknown> {
    return {
      ...super.toPayload(),
      payload: this.payload,
    };
  }
}
