const MESSAGES: Record<string, Record<string, string>> = {
  "identity.errors.email_exists": {
    "en-US": "Email already registered",
    "fa-IR": "ایمیل قبلاً ثبت شده است",
    "ar-SA": "البريد الإلكتروني مسجل مسبقاً",
  },
  "identity.errors.invalid_credentials": {
    "en-US": "Invalid email or password",
    "fa-IR": "ایمیل یا رمز عبور نامعتبر است",
    "ar-SA": "بريد إلكتروني أو كلمة مرور غير صحيحة",
  },
  "identity.errors.account_locked": {
    "en-US": "Account is temporarily locked",
    "fa-IR": "حساب موقتاً قفل شده است",
    "ar-SA": "الحساب مقفل مؤقتاً",
  },
  "identity.errors.access_denied": {
    "en-US": "Access denied",
    "fa-IR": "دسترسی رد شد",
    "ar-SA": "تم رفض الوصول",
  },
  "identity.errors.invalid_mfa_code": {
    "en-US": "Invalid MFA code",
    "fa-IR": "کد احراز هویت نامعتبر است",
    "ar-SA": "رمز المصادقة غير صالح",
  },
  "identity.errors.user_not_found": {
    "en-US": "User not found",
    "fa-IR": "کاربر یافت نشد",
    "ar-SA": "المستخدم غير موجود",
  },
  "identity.errors.role_exists": {
    "en-US": "Role already exists",
    "fa-IR": "نقش از قبل وجود دارد",
    "ar-SA": "الدور موجود مسبقاً",
  },
  "identity.errors.role_not_found": {
    "en-US": "Role not found",
    "fa-IR": "نقش یافت نشد",
    "ar-SA": "الدور غير موجود",
  },
  "identity.errors.forbidden": {
    "en-US": "Insufficient permissions",
    "fa-IR": "مجوز کافی نیست",
    "ar-SA": "صلاحيات غير كافية",
  },
};

export function translateError(key: string, locale = "en-US"): string {
  const entry = MESSAGES[key];
  if (!entry) return key;
  return entry[locale] ?? entry["en-US"] ?? key;
}

export function isRtlLocale(locale: string): boolean {
  return locale.startsWith("ar") || locale.startsWith("fa") || locale.startsWith("he");
}
