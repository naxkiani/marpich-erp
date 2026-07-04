import { Controller, Get } from "@nestjs/common";
import { ApiTags, ApiOperation } from "@nestjs/swagger";
import { Public } from "../decorators/permissions.decorator";

@ApiTags("Monitoring")
@Controller()
export class HealthController {
  @Public()
  @Get("health")
  @ApiOperation({ summary: "Service health and monitoring probe" })
  health() {
    return {
      status: "ok",
      service: "identity-service",
      version: process.env.PLATFORM_VERSION ?? "0.1.0",
      checks: {
        database: process.env.DATABASE_URL ? "configured" : "in-memory",
        redis: process.env.REDIS_URL ? "configured" : "in-memory",
        kafka: process.env.KAFKA_BROKERS ? "configured" : "console",
      },
      features: {
        jwt: true,
        rbac: true,
        abac: true,
        mfa: true,
        audit: true,
        events: true,
        caching: true,
        backgroundJobs: true,
        notifications: true,
        swagger: true,
        localization: true,
        rtl: true,
      },
    };
  }
}
