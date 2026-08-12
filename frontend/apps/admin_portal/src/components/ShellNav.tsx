"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@marpich/auth-provider";
import { groupedApplicationNav, useLocale } from "@marpich/shared";

export function ShellNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, session, user, logout } = useAuth();
  const groups = groupedApplicationNav();

  async function onLogout() {
    await logout();
    router.push("/login");
  }

  return (
    <nav aria-label="Main">
      {groups.map((group) => (
        <div key={group.group} className="mp-nav-group">
          <div className="mp-nav-group-label">{group.label}</div>
          {group.items.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href ? "page" : undefined}
            >
              {link.href === "/account/security" ? t("nav.mySecurity") : link.label}
            </Link>
          ))}
        </div>
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
