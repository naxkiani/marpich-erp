"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useLocale } from "@marpich/shared";

const LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/modules", label: "Modules" },
];

export function ShellNav() {
  const pathname = usePathname();
  const { t } = useLocale();

  return (
    <nav aria-label="Main">
      {LINKS.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          aria-current={pathname === link.href ? "page" : undefined}
        >
          {link.label}
        </Link>
      ))}
      <span className="mp-nav-muted">{t("app.name")}</span>
    </nav>
  );
}
