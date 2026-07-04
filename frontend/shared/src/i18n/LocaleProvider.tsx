"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

export type Locale = "en-US" | "fa-IR" | "ar-SA";

const RTL_LOCALES: Locale[] = ["fa-IR", "ar-SA"];

const MESSAGES: Record<Locale, Record<string, string>> = {
  "en-US": {
    "app.name": "Marpich",
    "shell.search": "Search",
    "shell.notifications": "Notifications",
    "shell.help": "Help",
    "shell.ai": "AI Assistant",
    "shell.shortcuts": "Keyboard shortcuts",
    "shell.commandPalette": "Command palette",
    "demo.title": "Platform Dashboard",
    "demo.empty": "No records yet",
    "demo.add": "Add record",
    "common.export": "Export",
    "common.import": "Import",
    "common.print": "Print",
    "common.undo": "Undo",
    "common.save": "Save",
    "common.filter": "Filter",
  },
  "fa-IR": {
    "app.name": "مارپیچ",
    "shell.search": "جستجو",
    "shell.notifications": "اعلان‌ها",
    "shell.help": "راهنما",
    "shell.ai": "دستیار هوش مصنوعی",
    "shell.shortcuts": "میانبرهای صفحه‌کلید",
    "shell.commandPalette": "پالت فرمان",
    "demo.title": "داشبورد پلتفرم",
    "demo.empty": "رکوردی وجود ندارد",
    "demo.add": "افزودن رکورد",
    "common.export": "خروجی",
    "common.import": "ورودی",
    "common.print": "چاپ",
    "common.undo": "بازگردانی",
    "common.save": "ذخیره",
    "common.filter": "فیلتر",
  },
  "ar-SA": {
    "app.name": "مارpich",
    "shell.search": "بحث",
    "shell.notifications": "الإشعارات",
    "shell.help": "مساعدة",
    "shell.ai": "المساعد الذكي",
    "shell.shortcuts": "اختصارات لوحة المفاتيح",
    "shell.commandPalette": "لوحة الأوامر",
    "demo.title": "لوحة المنصة",
    "demo.empty": "لا توجد سجلات",
    "demo.add": "إضافة سجل",
    "common.export": "تصدير",
    "common.import": "استيراد",
    "common.print": "طباعة",
    "common.undo": "تراجع",
    "common.save": "حفظ",
    "common.filter": "تصفية",
  },
};

type LocaleContextValue = {
  locale: Locale;
  dir: "ltr" | "rtl";
  setLocale: (locale: Locale) => void;
  t: (key: string) => string;
};

const LocaleContext = createContext<LocaleContextValue | null>(null);

export function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en-US");

  useEffect(() => {
    const stored = localStorage.getItem("marpich-locale") as Locale | null;
    if (stored && MESSAGES[stored]) setLocaleState(stored);
  }, []);

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
    localStorage.setItem("marpich-locale", next);
  }, []);

  const dir: "ltr" | "rtl" = RTL_LOCALES.includes(locale) ? "rtl" : "ltr";

  const t = useCallback(
    (key: string) => MESSAGES[locale][key] ?? MESSAGES["en-US"][key] ?? key,
    [locale],
  );

  const value = useMemo(
    () => ({ locale, dir, setLocale, t }),
    [locale, dir, setLocale, t],
  );

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
  return ctx;
}

export function DirectionProvider({ children }: { children: ReactNode }) {
  const { dir, locale } = useLocale();
  return (
    <div dir={dir} lang={locale} style={{ minHeight: "100%" }}>
      {children}
    </div>
  );
}

export function LocaleSwitcher() {
  const { locale, setLocale } = useLocale();
  return (
    <select
      className="mp-select"
      value={locale}
      onChange={(e) => setLocale(e.target.value as Locale)}
      aria-label="Language"
    >
      <option value="en-US">English</option>
      <option value="fa-IR">فارسی</option>
      <option value="ar-SA">العربية</option>
    </select>
  );
}
