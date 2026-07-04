import { Module } from "@nestjs/common";
import { IdentityModule } from "./presentation/identity.module";

@Module({
  imports: [IdentityModule],
})
export class AppModule {}
