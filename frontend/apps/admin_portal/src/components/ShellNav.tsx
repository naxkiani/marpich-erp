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
  { href: "/enterprise/document-studio", label: "Document Studio" },
  { href: "/enterprise/messenger", label: "Messenger" },
  { href: "/enterprise/federation", label: "Federation" },
  { href: "/enterprise/connector-framework", label: "Connectors" },
  { href: "/enterprise/ai-security", label: "AI Security" },
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
      <div className="mp-shell-auth">
        {isLoading ? (
          <span className="mp-nav-muted">Checking session…</span>
        ) : isAuthenticated && session ? (
          <>
            <span className="mp-nav-muted">
              {user?.email ?? "Signed in"} · {session.tenantId}
            </span>
            <Link href="/account/change-password">Change password</Link>
            <button type="button" className="mp-btn" onClick={() => void onLogout()}>
              Sign out
            </button>
          </>
        ) : (
          <Link href="/login">Sign in</Link>
        )}
      </div>
    </nav>
  );
}
