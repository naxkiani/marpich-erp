import "reflect-metadata";
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { Test } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../dist/app.module";

describe("Identity Service Integration", () => {
  let app: INestApplication;
  const tenantId = "test-hospital";
  let accessToken: string;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    app.setGlobalPrefix("api/v1");
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it("GET /health returns ok", async () => {
    const res = await request(app.getHttpServer()).get("/api/v1/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("ok");
  });

  it("POST /auth/register creates user", async () => {
    const res = await request(app.getHttpServer())
      .post("/api/v1/auth/register")
      .set("X-Tenant-ID", tenantId)
      .send({
        email: "admin@test-hospital.com",
        password: "SecurePass123!",
        displayName: "Admin User",
      });

    expect(res.status).toBe(201);
    expect(res.body.data.email).toBe("admin@test-hospital.com");
  });

  it("POST /auth/login returns JWT", async () => {
    const res = await request(app.getHttpServer())
      .post("/api/v1/auth/login")
      .set("X-Tenant-ID", tenantId)
      .send({
        email: "admin@test-hospital.com",
        password: "SecurePass123!",
      });

    expect(res.status).toBe(200);
    expect(res.body.data.accessToken).toBeTruthy();
    expect(res.body.data.mfaRequired).toBe(false);
    accessToken = res.body.data.accessToken;
  });

  it("GET /users/me returns profile with RBAC", async () => {
    const res = await request(app.getHttpServer())
      .get("/api/v1/users/me")
      .set("X-Tenant-ID", tenantId)
      .set("Authorization", `Bearer ${accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body.data.email).toBe("admin@test-hospital.com");
    expect(res.body.data.permissions).toContain("*");
  });

  it("POST /auth/refresh rotates tokens", async () => {
    const loginRes = await request(app.getHttpServer())
      .post("/api/v1/auth/login")
      .set("X-Tenant-ID", tenantId)
      .send({
        email: "admin@test-hospital.com",
        password: "SecurePass123!",
      });

    const refreshToken = loginRes.body.data.refreshToken;

    const res = await request(app.getHttpServer())
      .post("/api/v1/auth/refresh")
      .set("X-Tenant-ID", tenantId)
      .send({ refreshToken });

    expect(res.status).toBe(200);
    expect(res.body.data.accessToken).toBeTruthy();
    expect(res.body.data.refreshToken).not.toBe(refreshToken);
    accessToken = res.body.data.accessToken;
  });

  it("POST /auth/logout revokes session", async () => {
    const loginRes = await request(app.getHttpServer())
      .post("/api/v1/auth/login")
      .set("X-Tenant-ID", tenantId)
      .send({
        email: "admin@test-hospital.com",
        password: "SecurePass123!",
      });

    const res = await request(app.getHttpServer())
      .post("/api/v1/auth/logout")
      .set("X-Tenant-ID", tenantId)
      .set("Authorization", `Bearer ${loginRes.body.data.accessToken}`)
      .send({ refreshToken: loginRes.body.data.refreshToken });

    expect(res.status).toBe(200);
    expect(res.body.data.revoked).toBe(true);
  });

  it("GET /roles lists roles", async () => {
    const res = await request(app.getHttpServer())
      .get("/api/v1/roles")
      .set("X-Tenant-ID", tenantId)
      .set("Authorization", `Bearer ${accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body.data.length).toBeGreaterThan(0);
  });
});
