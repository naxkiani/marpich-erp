import { Injectable } from "@nestjs/common";
import type { INotificationService } from "../../domain/ports/identity.ports";
import { StructuredLogger } from "@marpich/platform-core";

@Injectable()
export class ConsoleNotificationService implements INotificationService {
  private readonly logger = new StructuredLogger("identity-notifications");

  async sendMfaEnabled(tenantId: string, email: string, locale: string): Promise<void> {
    this.logger.info("MFA enabled notification", { tenantId, email, locale });
  }

  async sendLoginAlert(tenantId: string, email: string, ipAddress?: string): Promise<void> {
    this.logger.info("Login alert notification", { tenantId, email, ipAddress });
  }
}
