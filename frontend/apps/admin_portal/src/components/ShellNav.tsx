"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@marpich/auth-provider";
import { useLocale } from "@marpich/shared";

const LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/modules", label: "Modules" },
  { href: "/banking/analytics", label: "Banking Analytics" },
  { href: "/education/university", label: "University" },
  { href: "/healthcare/clinic", label: "Clinic" },
  { href: "/healthcare/hospital", label: "Hospital" },
  { href: "/healthcare/pharmacy", label: "Pharmacy" },
  { href: "/healthcare/laboratory", label: "Laboratory" },
  { href: "/enterprise/document-studio", label: "Document Studio" },
  { href: "/enterprise/messenger", label: "Messenger" },
  { href: "/enterprise/notifications", label: "Notifications" },
  { href: "/enterprise/audit", label: "Audit" },
  { href: "/enterprise/federation", label: "Federation" },
  { href: "/enterprise/connector-framework", label: "Connectors" },
  { href: "/enterprise/plugins", label: "Plugins" },
  { href: "/enterprise/observability", label: "Observability" },
  { href: "/enterprise/scheduler", label: "Scheduler" },
  { href: "/enterprise/integration-studio", label: "Integration Studio" },
  { href: "/account/security", label: "My Security" },
];

export function ShellNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, session, user, logout } = useAuth();

  async function onLogout() {
    await logout();
    router.push("/login");
  }

  function linkLabel(href: string, label: string): string {
    if (href === "/account/security") return t("nav.mySecurity");
    return label;
  }

  return (
    <nav aria-label="Main">
      {LINKS.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          aria-current={pathname === link.href ? "page" : undefined}
        >
          {linkLabel(link.href, link.label)}
        </Link>
      ))}
      <span className="mp-nav-muted">{t("app.name")}</span>
      <div className="mp-shell-auth">
        {isLoading ? (
          <span className="mp-nav-muted">{t("accountSecurity.loading")}</span>
        ) : isAuthenticated && session ? (
          <>
            <span className="mp-nav-muted">
              {user?.email ?? t("accountSecurity.signedIn")} · {session.tenantId}
            </span>
            <Link href="/account/change-password">{t("nav.changePassword")}</Link>
            <button type="button" className="mp-btn" onClick={() => void onLogout()}>
              {t("accountSecurity.logout")}
            </button>
          </>
        ) : (
          <Link href="/login">{t("accountSecurity.step.signIn")}</Link>
        )}
      </div>
    </nav>
  );
}
