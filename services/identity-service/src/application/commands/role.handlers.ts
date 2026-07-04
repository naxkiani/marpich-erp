import { Injectable, Inject } from "@nestjs/common";
import { Result, UniqueEntityId, TenantId } from "@marpich/shared-kernel";
import {
  AUDIT_LOGGER,
  type IAuditLogger,
  CACHE_SERVICE,
  type ICacheService,
  OUTBOX_PUBLISHER,
  type IOutboxPublisher,
} from "@marpich/platform-core";
import {
  ROLE_REPOSITORY,
  type IRoleRepository,
  PERMISSION_REPOSITORY,
  type IPermissionRepository,
  USER_REPOSITORY,
  type IUserRepository,
} from "../../domain/ports/identity.ports";
import { Role } from "../../domain/role.aggregate";
import { RoleAssignedEvent } from "../../domain/events/identity.events";

@Injectable()
export class CreateRoleHandler {
  constructor(
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(PERMISSION_REPOSITORY) private readonly permissions: IPermissionRepository,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
  ) {}

  async execute(params: {
    tenantId: string;
    code: string;
    name: string;
    description?: string | undefined;
    permissionCodes?: string[] | undefined;
    correlationId: string;
    actorId?: string | undefined;
  }): Promise<Result<{ roleId: string }>> {
    const existing = await this.roles.findByCode(params.tenantId, params.code);
    if (existing) return Result.fail("identity.errors.role_exists");

    const permissionIds: string[] = [];
    for (const code of params.permissionCodes ?? []) {
      const id = await this.permissions.findIdByCode(code);
      if (id) permissionIds.push(id);
    }

    const role = Role.create({
      tenantId: params.tenantId,
      code: params.code,
      name: params.name,
      description: params.description,
      permissionIds,
    });

    await this.roles.save(role);

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: params.actorId,
      action: "identity.role.created",
      resourceType: "role",
      resourceId: role.id.toString(),
      payload: { code: role.code },
    });

    await this.cache.del(`identity:roles:${params.tenantId}`);

    return Result.ok({ roleId: role.id.toString() });
  }
}

@Injectable()
export class AssignRoleHandler {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(OUTBOX_PUBLISHER) private readonly events: IOutboxPublisher,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
  ) {}

  async execute(params: {
    tenantId: string;
    userId: string;
    roleId: string;
    correlationId: string;
    actorId?: string | undefined;
  }): Promise<Result<void>> {
    const user = await this.users.findById(params.tenantId, UniqueEntityId.create(params.userId));
    if (!user) return Result.fail("identity.errors.user_not_found");

    const role = await this.roles.findById(params.tenantId, UniqueEntityId.create(params.roleId));
    if (!role) return Result.fail("identity.errors.role_not_found");

    user.assignRole(params.roleId);
    await this.users.save(user);

    const event = new RoleAssignedEvent(
      user.id,
      params.tenantId,
      {
        correlationId: params.correlationId,
        tenantId: TenantId.create(params.tenantId),
        occurredAt: new Date(),
        ...(params.actorId !== undefined ? { userId: params.actorId } : {}),
      },
      { userId: params.userId, roleId: params.roleId },
    );
    await this.events.publish(event);

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: params.actorId,
      action: "identity.role.assigned",
      resourceType: "user",
      resourceId: params.userId,
      payload: { roleId: params.roleId, roleCode: role.code },
    });

    await this.cache.del(`identity:authz:${params.tenantId}:*`);
    await this.cache.del(`identity:user:${params.tenantId}:${params.userId}`);

    return Result.ok(undefined);
  }
}
