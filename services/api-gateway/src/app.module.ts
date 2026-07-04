import {
  Module,
  NestModule,
  MiddlewareConsumer,
  RequestMethod,
} from "@nestjs/common";
import { GatewayController } from "./gateway.controller";
import { TenantResolutionMiddleware } from "./middleware/tenant-resolution.middleware";

@Module({
  controllers: [GatewayController],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer
      .apply(TenantResolutionMiddleware)
      .exclude(
        { path: "health", method: RequestMethod.GET },
        { path: "platform", method: RequestMethod.GET },
        { path: "industry-packs", method: RequestMethod.ALL },
        { path: "industry-packs/*path", method: RequestMethod.ALL },
        { path: "modules", method: RequestMethod.ALL },
        { path: "auth/login", method: RequestMethod.POST },
        { path: "auth/register", method: RequestMethod.POST },
        { path: "auth/refresh", method: RequestMethod.POST },
      )
      .forRoutes("*");
  }
}
