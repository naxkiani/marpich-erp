import { DomainEvent, UniqueEntityId, TenantId } from "@marpich/shared-kernel";

function eventMeta(
  tenantId: string,
  correlationId: string,
  userId?: string,
): {
  correlationId: string;
  tenantId: TenantId;
  occurredAt: Date;
  userId?: string | undefined;
} {
  return {
    correlationId,
    tenantId: TenantId.create(tenantId),
    occurredAt: new Date(),
    ...(userId !== undefined ? { userId } : {}),
  };
}

export class UserCreatedEvent extends DomainEvent {
  readonly eventName = "identity.user.created";
  readonly eventVersion = 1;

  constructor(
    aggregateId: UniqueEntityId,
    tenantId: string,
    metadata: ReturnType<typeof eventMeta>,
    readonly payload: { email: string; displayName: string },
  ) {
    super(aggregateId, metadata);
  }
}

export class UserLoggedInEvent extends DomainEvent {
  readonly eventName = "identity.user.logged_in";
  readonly eventVersion = 1;

  constructor(
    aggregateId: UniqueEntityId,
    tenantId: string,
    metadata: ReturnType<typeof eventMeta>,
    readonly payload: { ipAddress?: string | undefined },
  ) {
    super(aggregateId, metadata);
  }
}

export class MfaEnabledEvent extends DomainEvent {
  readonly eventName = "identity.mfa.enabled";
  readonly eventVersion = 1;

  constructor(
    aggregateId: UniqueEntityId,
    tenantId: string,
    metadata: ReturnType<typeof eventMeta>,
  ) {
    super(aggregateId, metadata);
  }
}

export class RoleAssignedEvent extends DomainEvent {
  readonly eventName = "identity.role.assigned";
  readonly eventVersion = 1;

  constructor(
    aggregateId: UniqueEntityId,
    tenantId: string,
    metadata: ReturnType<typeof eventMeta>,
    readonly payload: { userId: string; roleId: string },
  ) {
    super(aggregateId, metadata);
  }
}
