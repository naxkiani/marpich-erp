interface GuardResult {
  succeeded: boolean;
  message?: string;
}

export class Guard {
  static againstNullOrUndefined(value: unknown, fieldName: string): GuardResult {
    if (value === null || value === undefined) {
      return { succeeded: false, message: `${fieldName} is required` };
    }
    return { succeeded: true };
  }

  static againstEmptyString(value: string, fieldName: string): GuardResult {
    if (!value || value.trim().length === 0) {
      return { succeeded: false, message: `${fieldName} cannot be empty` };
    }
    return { succeeded: true };
  }

  static combine(results: GuardResult[]): GuardResult {
    const failed = results.find((r) => !r.succeeded);
    return failed ?? { succeeded: true };
  }
}
