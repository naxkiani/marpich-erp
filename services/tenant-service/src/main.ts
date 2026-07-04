import { NestFactory } from "@nestjs/core";
import { ValidationPipe } from "@nestjs/common";
import { AppModule } from "./app.module";

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  app.setGlobalPrefix("api/v1");
  const port = process.env.TENANT_SERVICE_PORT ?? 4002;
  await app.listen(port);
  console.log(`[tenant-service] listening on :${port}`);
}

bootstrap().catch((err: unknown) => {
  console.error("[tenant-service] fatal:", err);
  process.exit(1);
});
