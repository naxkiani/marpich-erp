import { Injectable, Inject } from "@nestjs/common";
import { v4 as uuidv4 } from "uuid";
import { Result } from "@marpich/shared-kernel";
import {
  AUDIT_LOGGER,
  type IAuditLogger,
  OUTBOX_PUBLISHER,
  type IOutboxPublisher,
  CACHE_SERVICE,
  type ICacheService,
  PermissionEvaluator,
} from "@marpich/platform-core";
import {
  USER_REPOSITORY,
  type IUserRepository,
  PASSWORD_HASHER,
  type IPasswordHasher,
  TOKEN_SERVICE,
  type ITokenService,
  PERMISSION_REPOSITORY,
  type IPermissionRepository,
  ROLE_REPOSITORY,
  type IRoleRepository,
  SESSION_REPOSITORY,
  type ISessionRepository,
  MFA_SERVICE,
  type IMfaService,
  NOTIFICATION_SERVICE,
  type INotificationService,
  ABAC_POLICY_REPOSITORY,
  type IAbacPolicyRepository,
} from "../../domain/ports/identity.ports";

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  mfaRequired: boolean;
  mfaToken?: string | undefined;
}

@Injectable()
export class LoginUserHandler {
  private readonly permissionEvaluator = new PermissionEvaluator();

  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    @Inject(PASSWORD_HASHER) private readonly hasher: IPasswordHasher,
    @Inject(TOKEN_SERVICE) private readonly tokens: ITokenService,
    @Inject(PERMISSION_REPOSITORY) private readonly permissions: IPermissionRepository,
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(SESSION_REPOSITORY) private readonly sessions: ISessionRepository,
    @Inject(MFA_SERVICE) private readonly mfa: IMfaService,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(OUTBOX_PUBLISHER) private readonly events: IOutboxPublisher,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
    @Inject(NOTIFICATION_SERVICE) private readonly notifications: INotificationService,
    @Inject(ABAC_POLICY_REPOSITORY) private readonly abacPolicies: IAbacPolicyRepository,
  ) {}

  async execute(params: {
    tenantId: string;
    email: string;
    password: string;
    mfaCode?: string | undefined;
    mfaToken?: string | undefined;
    correlationId: string;
    ipAddress?: string | undefined;
    userAgent?: string | undefined;
  }): Promise<Result<AuthTokens>> {
    const user = await this.users.findByEmail(params.tenantId, params.email);
    if (!user) {
      return Result.fail("identity.errors.invalid_credentials");
    }

    if (user.isLocked()) {
      return Result.fail("identity.errors.account_locked");
    }

    const valid = await this.hasher.verify(params.password, user.passwordHash);
    if (!valid) {
      user.recordFailedLogin();
      await this.users.save(user);
      await this.audit.log({
        tenantId: params.tenantId,
        correlationId: params.correlationId,
        action: "identity.login.failed",
        resourceType: "user",
        resourceId: user.id.toString(),
        ipAddress: params.ipAddress,
      });
      return Result.fail("identity.errors.invalid_credentials");
    }

    if (user.mfaEnabled) {
      if (!params.mfaCode && !params.mfaToken) {
        const mfaToken = await this.issueMfaChallenge(user.id.toString(), params.tenantId);
        return Result.ok({
          accessToken: "",
          refreshToken: "",
          expiresIn: 0,
          mfaRequired: true,
          mfaToken,
        });
      }

      if (params.mfaToken) {
        const pending = await this.cache.get<{ userId: string; tenantId: string }>(
          `identity:mfa:${params.mfaToken}`,
        );
        if (!pending || pending.userId !== user.id.toString()) {
          return Result.fail("identity.errors.invalid_mfa_token");
        }
      }

      if (params.mfaCode) {
        const secret = user.mfaSecret;
        if (!secret) return Result.fail("identity.errors.mfa_not_configured");

        const validTotp = this.mfa.verifyToken(secret, params.mfaCode);
        const validBackup = !validTotp && user.consumeBackupCode(params.mfaCode);
        if (!validTotp && !validBackup) {
          return Result.fail("identity.errors.invalid_mfa_code");
        }
        if (validBackup) await this.users.save(user);
      }
    }

    const { roleCodes, permissionCodes } = await this.resolveAuthorization(
      params.tenantId,
      [...user.roleIds],
    );

    const policies = await this.abacPolicies.findByTenant(params.tenantId);
    const abacOk = this.permissionEvaluator.evaluateAbac(
      {
        tenantId: params.tenantId,
        userId: user.id.toString(),
        permissions: permissionCodes,
        roles: roleCodes,
        attributes: user.toSnapshot().attributes as Record<string, unknown>,
        resource: "auth",
        action: "login",
      },
      policies,
    );
    if (!abacOk) {
      return Result.fail("identity.errors.access_denied");
    }

    user.recordSuccessfulLogin(params.correlationId, params.ipAddress);
    await this.users.save(user);

    for (const event of user.domainEvents) {
      await this.events.publish(event);
    }
    user.clearDomainEvents();

    const payload = {
      sub: user.id.toString(),
      tenantId: params.tenantId,
      email: user.email,
      roles: roleCodes,
      permissions: permissionCodes,
      locale: user.toSnapshot().locale as string,
      attributes: user.toSnapshot().attributes as Record<string, unknown>,
    };

    const accessToken = this.tokens.signAccess(payload);
    const refreshToken = this.tokens.signRefresh(payload);
    const refreshHash = this.tokens.hashRefreshToken(refreshToken);

    await this.sessions.create({
      id: uuidv4(),
      tenantId: params.tenantId,
      userId: user.id.toString(),
      refreshTokenHash: refreshHash,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      ...(params.ipAddress !== undefined ? { ipAddress: params.ipAddress } : {}),
      ...(params.userAgent !== undefined ? { userAgent: params.userAgent } : {}),
    });

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: user.id.toString(),
      action: "identity.login.success",
      resourceType: "user",
      resourceId: user.id.toString(),
      ipAddress: params.ipAddress,
    });

    await this.notifications.sendLoginAlert(params.tenantId, user.email, params.ipAddress);

    return Result.ok({
      accessToken,
      refreshToken,
      expiresIn: Number(process.env.JWT_ACCESS_TTL ?? 900),
      mfaRequired: false,
    });
  }

  private async issueMfaChallenge(userId: string, tenantId: string): Promise<string> {
    const token = uuidv4();
    await this.cache.set(`identity:mfa:${token}`, { userId, tenantId }, 300);
    return token;
  }

  private async resolveAuthorization(
    tenantId: string,
    roleIds: string[],
  ): Promise<{ roleCodes: string[]; permissionCodes: string[] }> {
    const roles = await this.roles.list(tenantId);
    const roleCodes = roles
      .filter((r) => roleIds.includes(r.id.toString()))
      .map((r) => r.code);

    const permissionCodes = await this.permissions.findCodesByRoleIds(tenantId, roleIds);
    if (roleCodes.includes("admin")) {
      permissionCodes.push("*");
    }

    const cacheKey = `identity:authz:${tenantId}:${roleIds.sort().join(",")}`;
    const cached = await this.cache.get<{ roleCodes: string[]; permissionCodes: string[] }>(cacheKey);
    if (cached) return cached;

    const result = { roleCodes, permissionCodes: [...new Set(permissionCodes)] };
    await this.cache.set(cacheKey, result, 600);
    return result;
  }
}
