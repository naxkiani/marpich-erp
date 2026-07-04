import { Injectable, OnModuleInit } from "@nestjs/common";
import { Inject } from "@nestjs/common";
import { SESSION_REPOSITORY, type ISessionRepository } from "../../domain/ports/identity.ports";
import { StructuredLogger } from "@marpich/platform-core";

/**
 * Background job: purge expired sessions every hour.
 * Production: BullMQ worker on Redis.
 */
@Injectable()
export class SessionCleanupJob implements OnModuleInit {
  private readonly logger = new StructuredLogger("session-cleanup-job");
  private timer?: ReturnType<typeof setInterval>;

  constructor(
    @Inject(SESSION_REPOSITORY) private readonly sessions: ISessionRepository,
  ) {}

  onModuleInit(): void {
    this.timer = setInterval(() => {
      void this.run();
    }, 60 * 60 * 1000);
  }

  async run(): Promise<number> {
    const deleted = await this.sessions.deleteExpired();
    this.logger.info("Expired sessions cleaned", { deleted });
    return deleted;
  }
}
