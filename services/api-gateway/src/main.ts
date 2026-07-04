import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  app.enableCors();
  app.setGlobalPrefix("api/v1");
  const port = process.env.API_GATEWAY_PORT ?? 4000;
  await app.listen(port);
  console.log(`[api-gateway] listening on :${port}`);
}

bootstrap().catch((err: unknown) => {
  console.error("[api-gateway] fatal:", err);
  process.exit(1);
});
