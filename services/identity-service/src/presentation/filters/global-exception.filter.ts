import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from "@nestjs/common";
import type { Response } from "express";
import { translateError, isRtlLocale } from "../../infrastructure/i18n/messages";

@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<{ headers: Record<string, string> }>();
    const locale = request.headers["accept-language"]?.split(",")[0] ?? "en-US";

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let errorKey = "identity.errors.internal";
    let message = "Internal server error";

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const body = exception.getResponse();
      if (typeof body === "object" && body !== null) {
        const obj = body as Record<string, unknown>;
        if (typeof obj.error === "string") {
          errorKey = obj.error;
          message = translateError(errorKey, locale);
        } else if (typeof obj.message === "string") {
          message = obj.message;
        }
      } else if (typeof body === "string") {
        message = translateError(body, locale) || body;
        errorKey = body;
      }
    }

    response.status(status).json({
      error: errorKey,
      message,
      statusCode: status,
      locale,
      direction: isRtlLocale(locale) ? "rtl" : "ltr",
      timestamp: new Date().toISOString(),
    });
  }
}
