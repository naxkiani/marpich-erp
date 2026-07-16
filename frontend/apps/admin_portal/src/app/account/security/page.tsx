"use client";

import { PageLayout } from "@marpich/core";
import { EmptyState, useToast } from "@marpich/shared";
import { useAuth } from "@marpich/auth-provider";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

/**
 * End-user self-service security portal.
 * Dark/light + RTL/LTR inherit from AppShell / locale provider.
 */
export default function AccountSecurityPage() {
  const router = useRouter();
  const { push } = useToast();
  const { isAuthenticated, isLoading, user, session } = useAuth();
  const [privacyOn, setPrivacyOn] = useState(true);
  const [marketingConsent, setMarketingConsent] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login?returnTo=/account/security");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !isAuthenticated) return null;

  return (
    <PageLayout
      title="Security & privacy"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Account" },
        { label: "Security" },
      ]}
    >
      <div className="mx-auto max-w-3xl space-y-8" dir="auto">
        <section aria-label="Profile">
          <h2 className="text-lg font-semibold">Profile</h2>
          <p className="mp-nav-muted">{user?.email ?? "Signed in"} · tenant {session?.tenantId}</p>
        </section>

        <section className="grid gap-3 sm:grid-cols-2" aria-label="Security modules">
          <Link className="rounded border p-4 hover:bg-black/5 dark:hover:bg-white/5" href="/account/mfa">
            <h3 className="font-medium">Passwordless / MFA</h3>
            <p className="text-sm opacity-80">Enroll factors and step-up methods</p>
          </Link>
          <Link className="rounded border p-4 hover:bg-black/5 dark:hover:bg-white/5" href="/account/passkeys">
            <h3 className="font-medium">Passkey registration</h3>
            <p className="text-sm opacity-80">WebAuthn credentials for passwordless login</p>
          </Link>
          <Link className="rounded border p-4 hover:bg-black/5 dark:hover:bg-white/5" href="/account/change-password">
            <h3 className="font-medium">Recovery options</h3>
            <p className="text-sm opacity-80">Password reset and recovery channels</p>
          </Link>
          <div className="rounded border p-4">
            <h3 className="font-medium">Trusted devices</h3>
            <p className="text-sm opacity-80">Managed via MFA trusted-device APIs</p>
            <EmptyState title="No local devices listed" description="Devices sync from MFA platform." />
          </div>
        </section>

        <section aria-label="Sessions">
          <h2 className="text-lg font-semibold">Active sessions</h2>
          <p className="text-sm opacity-80">Current session: {session?.tenantId ?? "—"}</p>
          <button
            type="button"
            className="mp-btn mt-2"
            onClick={() => push({ title: "Session sync", description: "Use global logout via federation SLO" })}
          >
            Refresh session status
          </button>
        </section>

        <section aria-label="Privacy controls">
          <h2 className="text-lg font-semibold">Privacy & consent</h2>
          <label className="mt-2 flex items-center gap-2">
            <input
              type="checkbox"
              checked={privacyOn}
              onChange={(e) => setPrivacyOn(e.target.checked)}
            />
            Minimize analytics identifiers
          </label>
          <label className="mt-2 flex items-center gap-2">
            <input
              type="checkbox"
              checked={marketingConsent}
              onChange={(e) => setMarketingConsent(e.target.checked)}
            />
            Allow security notification emails
          </label>
        </section>

        <section aria-label="Linked accounts">
          <h2 className="text-lg font-semibold">Linked accounts</h2>
          <EmptyState
            title="No linked federated accounts"
            description="Link enterprise IdP accounts from SSO settings when available."
          />
        </section>
      </div>
    </PageLayout>
  );
}
