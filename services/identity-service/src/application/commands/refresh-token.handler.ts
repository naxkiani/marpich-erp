import { Injectable, Inject } from "@nestjs/common";
import { v4 as uuidv4 } from "uuid";
import { Result } from "@marpich/shared-kernel";
import {
  AUDIT_LOGGER,
  type IAuditLogger,
  CACHE_SERVICE,
  type ICacheService,
} from "@marpich/platform-core";
import {
  USER_REPOSITORY,
  type IUserRepository,
  TOKEN_SERVICE,
  type ITokenService,
  PERMISSION_REPOSITORY,
  type IPermissionRepository,
  ROLE_REPOSITORY,
  type IRoleRepository,
  SESSION_REPOSITORY,
  type ISessionRepository,
} from "../../domain/ports/identity.ports";
import { UniqueEntityId } from "@marpich/shared-kernel";
import type { AuthTokens } from "./login-user.handler";

@Injectable()
export class RefreshTokenHandler {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    @Inject(TOKEN_SERVICE) private readonly tokens: ITokenService,
    @Inject(PERMISSION_REPOSITORY) private readonly permissions: IPermissionRepository,
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(SESSION_REPOSITORY) private readonly sessions: ISessionRepository,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
  ) {}

  async execute(params: {
    tenantId: string;
    refreshToken: string;
    correlationId: string;
    ipAddress?: string | undefined;
    userAgent?: string | undefined;
  }): Promise<Result<AuthTokens>> {
    let payload;
    try {
      payload = this.tokens.verifyRefresh(params.refreshToken);
    } catch {
      return Result.fail("identity.errors.invalid_refresh_token");
    }

    if (payload.tenantId !== params.tenantId) {
      return Result.fail("identity.errors.invalid_refresh_token");
    }

    const hash = this.tokens.hashRefreshToken(params.refreshToken);
    const session = await this.sessions.findByRefreshTokenHash(hash);
    if (!session || session.expiresAt < new Date()) {
      return Result.fail("identity.errors.session_expired");
    }

    const user = await this.users.findById(
      params.tenantId,
      UniqueEntityId.create(payload.sub),
    );
    if (!user || user.status !== "active") {
      return Result.fail("identity.errors.user_inactive");
    }

    const { roleCodes, permissionCodes } = await this.resolveAuthorization(
      params.tenantId,
      [...user.roleIds],
    );

    const tokenPayload = {
      sub: user.id.toString(),
      tenantId: params.tenantId,
      email: user.email,
      roles: roleCodes,
      permissions: permissionCodes,
      locale: user.toSnapshot().locale as string,
      attributes: user.toSnapshot().attributes as Record<string, unknown>,
    };

    const accessToken = this.tokens.signAccess(tokenPayload);
    const newRefreshToken = this.tokens.signRefresh(tokenPayload);

    await this.sessions.revoke(session.id);
    await this.sessions.create({
      id: uuidv4(),
      tenantId: params.tenantId,
      userId: user.id.toString(),
      refreshTokenHash: this.tokens.hashRefreshToken(newRefreshToken),
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      ...(params.ipAddress !== undefined ? { ipAddress: params.ipAddress } : {}),
      ...(params.userAgent !== undefined ? { userAgent: params.userAgent } : {}),
    });

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: user.id.toString(),
      action: "identity.token.refreshed",
      resourceType: "session",
      resourceId: session.id,
      ipAddress: params.ipAddress,
    });

    return Result.ok({
      accessToken,
      refreshToken: newRefreshToken,
      expiresIn: Number(process.env.JWT_ACCESS_TTL ?? 900),
      mfaRequired: false,
    });
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
