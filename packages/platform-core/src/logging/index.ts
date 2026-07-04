export type LogLevel = "debug" | "info" | "warn" | "error";

export interface LogContext {
  service?: string | undefined;
  correlationId?: string | undefined;
  tenantId?: string | undefined;
  userId?: string | undefined;
  [key: string]: unknown;
}

export interface IPlatformLogger {
  debug(message: string, context?: LogContext): void;
  info(message: string, context?: LogContext): void;
  warn(message: string, context?: LogContext): void;
  error(message: string, context?: LogContext, error?: Error): void;
}

export const PLATFORM_LOGGER = Symbol("PLATFORM_LOGGER");

export class StructuredLogger implements IPlatformLogger {
  constructor(private readonly service: string) {}

  private write(level: LogLevel, message: string, context?: LogContext, err?: Error): void {
    const entry: Record<string, unknown> = {
      level,
      service: this.service,
      message,
      timestamp: new Date().toISOString(),
      ...context,
    };
    if (err) {
      entry.errorName = err.name;
      entry.errorMessage = err.message;
      entry.stack = err.stack;
    }
    const line = JSON.stringify(entry);
    if (level === "error") console.error(line);
    else if (level === "warn") console.warn(line);
    else console.log(line);
  }

  debug(message: string, context?: LogContext): void {
    this.write("debug", message, context);
  }

  info(message: string, context?: LogContext): void {
    this.write("info", message, context);
  }

  warn(message: string, context?: LogContext): void {
    this.write("warn", message, context);
  }

  error(message: string, context?: LogContext, error?: Error): void {
    this.write("error", message, context, error);
  }
}
