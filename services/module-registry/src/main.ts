import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix("api/v1");
  const port = process.env.MODULE_REGISTRY_PORT ?? 4003;
  await app.listen(port);
  console.log(`[module-registry] listening on :${port}`);
}

bootstrap().catch((err: unknown) => {
  console.error("[module-registry] fatal:", err);
  process.exit(1);
});
