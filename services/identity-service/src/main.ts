import { NestFactory } from "@nestjs/core";
import { ValidationPipe } from "@nestjs/common";
import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger";
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

  const swaggerConfig = new DocumentBuilder()
    .setTitle("Marpich Identity Service")
    .setDescription(
      "Enterprise identity — JWT, RBAC, ABAC, MFA, audit, events, multi-tenant",
    )
    .setVersion("0.1.0")
    .addBearerAuth()
    .addApiKey({ type: "apiKey", name: "X-Tenant-ID", in: "header" }, "tenant")
    .addTag("Auth")
    .addTag("Users")
    .addTag("Roles")
    .addTag("Monitoring")
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup("api/docs", app, document);

  const port = process.env.IDENTITY_SERVICE_PORT ?? 4001;
  await app.listen(port);
  console.log(`[identity-service] listening on :${port}`);
  console.log(`[identity-service] swagger: http://localhost:${port}/api/docs`);
}

bootstrap().catch((err: unknown) => {
  console.error("[identity-service] fatal:", err);
  process.exit(1);
});
