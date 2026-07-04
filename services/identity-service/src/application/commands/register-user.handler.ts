import { Injectable, Inject } from "@nestjs/common";
import { Result } from "@marpich/shared-kernel";
import {
  AUDIT_LOGGER,
  type IAuditLogger,
  OUTBOX_PUBLISHER,
  type IOutboxPublisher,
  CACHE_SERVICE,
  type ICacheService,
} from "@marpich/platform-core";
import { User } from "../../domain/user.aggregate";
import {
  USER_REPOSITORY,
  type IUserRepository,
  PASSWORD_HASHER,
  type IPasswordHasher,
  ROLE_REPOSITORY,
  type IRoleRepository,
} from "../../domain/ports/identity.ports";
import { Role } from "../../domain/role.aggregate";

@Injectable()
export class RegisterUserHandler {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(PASSWORD_HASHER) private readonly hasher: IPasswordHasher,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(OUTBOX_PUBLISHER) private readonly events: IOutboxPublisher,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
  ) {}

  async execute(params: {
    tenantId: string;
    email: string;
    password: string;
    displayName: string;
    locale?: string | undefined;
    roleCode?: string | undefined;
    correlationId: string;
    actorId?: string | undefined;
    ipAddress?: string | undefined;
  }): Promise<Result<{ userId: string; email: string }>> {
    const exists = await this.users.existsByEmail(params.tenantId, params.email);
    if (exists) {
      return Result.fail("identity.errors.email_exists");
    }

    const passwordHash = await this.hasher.hash(params.password);
    const roleIds: string[] = [];

    if (params.roleCode) {
      const role = await this.roles.findByCode(params.tenantId, params.roleCode);
      if (role) roleIds.push(role.id.toString());
    } else {
      await this.ensureDefaultAdminRole(params.tenantId);
      const adminRole = await this.roles.findByCode(params.tenantId, "admin");
      if (adminRole) roleIds.push(adminRole.id.toString());
    }

    const user = User.register({
      tenantId: params.tenantId,
      email: params.email,
      passwordHash,
      displayName: params.displayName,
      locale: params.locale,
      roleIds,
      correlationId: params.correlationId,
      actorId: params.actorId,
    });

    for (const roleId of roleIds) {
      user.assignRole(roleId);
    }

    await this.users.save(user);

    for (const event of user.domainEvents) {
      await this.events.publish(event);
    }
    user.clearDomainEvents();

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: params.actorId,
      action: "identity.user.registered",
      resourceType: "user",
      resourceId: user.id.toString(),
      payload: { email: user.email },
      ipAddress: params.ipAddress,
    });

    await this.cache.del(`identity:users:${params.tenantId}:*`);

    return Result.ok({ userId: user.id.toString(), email: user.email });
  }

  private async ensureDefaultAdminRole(tenantId: string): Promise<void> {
    const existing = await this.roles.findByCode(tenantId, "admin");
    if (existing) return;

    const admin = Role.create({
      tenantId,
      code: "admin",
      name: "Administrator",
      description: "Full platform access within tenant",
      isSystem: true,
      permissionIds: [
        "00000000-0000-4000-8000-000000000001",
        "00000000-0000-4000-8000-000000000002",
        "00000000-0000-4000-8000-000000000003",
        "00000000-0000-4000-8000-000000000004",
        "00000000-0000-4000-8000-000000000005",
        "00000000-0000-4000-8000-000000000006",
        "00000000-0000-4000-8000-000000000007",
        "00000000-0000-4000-8000-000000000008",
        "00000000-0000-4000-8000-000000000009",
        "00000000-0000-4000-8000-000000000010",
      ],
    });
    await this.roles.save(admin);
  }
}
