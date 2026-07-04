import { Injectable, Inject } from "@nestjs/common";
import { Result } from "@marpich/shared-kernel";
import {
  AUDIT_LOGGER,
  type IAuditLogger,
  CACHE_SERVICE,
  type ICacheService,
} from "@marpich/platform-core";
import {
  SESSION_REPOSITORY,
  type ISessionRepository,
  TOKEN_SERVICE,
  type ITokenService,
} from "../../domain/ports/identity.ports";

@Injectable()
export class LogoutUserHandler {
  constructor(
    @Inject(SESSION_REPOSITORY) private readonly sessions: ISessionRepository,
    @Inject(TOKEN_SERVICE) private readonly tokens: ITokenService,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
  ) {}

  async execute(params: {
    tenantId: string;
    userId: string;
    refreshToken?: string | undefined;
    correlationId: string;
    revokeAll?: boolean | undefined;
    ipAddress?: string | undefined;
  }): Promise<Result<{ revoked: boolean }>> {
    if (params.revokeAll) {
      await this.sessions.revokeAllForUser(params.tenantId, params.userId);
    } else if (params.refreshToken) {
      const hash = this.tokens.hashRefreshToken(params.refreshToken);
      const session = await this.sessions.findByRefreshTokenHash(hash);
      if (session && session.tenantId === params.tenantId) {
        await this.sessions.revoke(session.id);
      }
    } else {
      await this.sessions.revokeAllForUser(params.tenantId, params.userId);
    }

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: params.userId,
      action: "identity.logout",
      resourceType: "session",
      resourceId: params.userId,
      ipAddress: params.ipAddress,
    });

    await this.cache.delPattern(`identity:authz:${params.tenantId}:*`);

    return Result.ok({ revoked: true });
  }
}
