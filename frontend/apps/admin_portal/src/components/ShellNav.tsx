"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@marpich/auth-provider";
import { groupedApplicationNav, useLocale, useTenantModules } from "@marpich/shared";
import { useMemo } from "react";

export function ShellNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, session, user, logout, hasPermission } = useAuth();
  const { enabledModules, snapshot } = useTenantModules();

  const groups = useMemo(() => {
    if (!isAuthenticated) {
      return groupedApplicationNav()
        .map((g) => ({
          ...g,
          items: g.items.filter((i) => i.group === "home" || i.id === "security"),
        }))
        .filter((g) => g.items.length > 0);
    }
    const moduleGate = snapshot ? enabledModules : undefined;
    return groupedApplicationNav(hasPermission, moduleGate);
  }, [enabledModules, hasPermission, isAuthenticated, snapshot]);

  async function onLogout() {
    await logout();
    router.push("/login");
  }

  return (
    <div className="mp-shell-nav">
      <nav aria-label="Main" className="mp-shell-nav-scroll">
        {groups.map((group) => (
          <div key={group.group} className="mp-nav-group">
            <div className="mp-nav-group-label">{t(group.labelKey)}</div>
            <ul className="mp-nav-list">
              {group.items.map((link) => {
                const current =
                  pathname === link.href ||
                  (link.href !== "/" && pathname.startsWith(`${link.href}/`));
                const label =
                  link.href === "/account/security"
                    ? t("nav.mySecurity")
                    : link.labelKey
                      ? t(link.labelKey)
                      : link.label;
                return (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="mp-nav-link"
                      aria-current={current ? "page" : undefined}
                    >
                      {label}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      <div className="mp-shell-nav-footer">
        <div className="mp-shell-auth">
          {isLoading ? (
            <span className="mp-nav-muted">{t("accountSecurity.loading")}</span>
          ) : isAuthenticated && session ? (
            <>
              <span className="mp-nav-user" title={user?.email ?? undefined}>
                {user?.email ?? t("accountSecurity.signedIn")}
              </span>
              <span className="mp-nav-muted">{session.tenantId}</span>
              <Link href="/account/change-password" className="mp-nav-link mp-nav-link--footer">
                {t("nav.changePassword")}
              </Link>
              <button type="button" className="mp-btn mp-btn-ghost mp-nav-logout" onClick={() => void onLogout()}>
                {t("accountSecurity.logout")}
              </button>
            </>
          ) : (
            <Link href="/login" className="mp-btn mp-btn-primary">
              {t("accountSecurity.step.signIn")}
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
