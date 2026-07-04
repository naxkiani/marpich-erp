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
import * as QRCode from "qrcode";
import {
  USER_REPOSITORY,
  type IUserRepository,
  MFA_SERVICE,
  type IMfaService,
  NOTIFICATION_SERVICE,
  type INotificationService,
} from "../../domain/ports/identity.ports";
import { UniqueEntityId } from "@marpich/shared-kernel";

@Injectable()
export class SetupMfaHandler {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    @Inject(MFA_SERVICE) private readonly mfa: IMfaService,
    @Inject(AUDIT_LOGGER) private readonly audit: IAuditLogger,
    @Inject(OUTBOX_PUBLISHER) private readonly events: IOutboxPublisher,
    @Inject(CACHE_SERVICE) private readonly cache: ICacheService,
    @Inject(NOTIFICATION_SERVICE) private readonly notifications: INotificationService,
  ) {}

  async execute(params: {
    tenantId: string;
    userId: string;
    correlationId: string;
    verifyCode: string;
    pendingSecret: string;
    ipAddress?: string | undefined;
  }): Promise<Result<{ backupCodes: string[] }>> {
    const user = await this.users.findById(params.tenantId, UniqueEntityId.create(params.userId));
    if (!user) return Result.fail("identity.errors.user_not_found");

    if (!this.mfa.verifyToken(params.pendingSecret, params.verifyCode)) {
      return Result.fail("identity.errors.invalid_mfa_code");
    }

    const backupCodes = this.mfa.generateBackupCodes(8);
    user.enableMfa(params.pendingSecret, backupCodes, params.correlationId);
    await this.users.save(user);

    for (const event of user.domainEvents) {
      await this.events.publish(event);
    }
    user.clearDomainEvents();

    await this.audit.log({
      tenantId: params.tenantId,
      correlationId: params.correlationId,
      actorId: params.userId,
      action: "identity.mfa.enabled",
      resourceType: "user",
      resourceId: params.userId,
      ipAddress: params.ipAddress,
    });

    await this.notifications.sendMfaEnabled(params.tenantId, user.email, user.toSnapshot().locale as string);
    await this.cache.del(`identity:user:${params.tenantId}:${params.userId}`);

    return Result.ok({ backupCodes });
  }

  async initiate(params: {
    tenantId: string;
    userId: string;
    email: string;
  }): Promise<{ secret: string; qrCodeDataUrl: string; otpauthUri: string }> {
    const secret = this.mfa.generateSecret();
    const issuer = process.env.PLATFORM_NAME ?? "Marpich ERP";
    const otpauthUri = this.mfa.generateUri(params.email, secret, issuer);
    const qrCodeDataUrl = await QRCode.toDataURL(otpauthUri);

    await this.cache.set(
      `identity:mfa-setup:${params.tenantId}:${params.userId}`,
      { secret },
      600,
    );

    return { secret, qrCodeDataUrl, otpauthUri };
  }

  async getPendingSecret(tenantId: string, userId: string): Promise<string | null> {
    const pending = await this.cache.get<{ secret: string }>(`identity:mfa-setup:${tenantId}:${userId}`);
    return pending?.secret ?? null;
  }
}
