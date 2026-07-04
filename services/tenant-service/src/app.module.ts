import { Module } from "@nestjs/common";
import { TenantModule } from "./presentation/tenant.module";

@Module({
  imports: [TenantModule],
})
export class AppModule {}
