"use client";

import { LoginGate, useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated } = useAuth();
  const returnTo = searchParams.get("returnTo") ?? "/";

  if (isAuthenticated) {
    router.replace(returnTo.startsWith("/") ? returnTo : "/");
  }

  return (
    <PageLayout
      title="Sign in"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Sign in" },
      ]}
    >
      <p className="mp-auth-page-desc">
        Centralized identity for all Marpich admin dashboards. One session is shared across enterprise, tax, and FX modules.
      </p>
      <LoginGate
        title="Sign in to Marpich"
        onConnected={() => router.replace(returnTo.startsWith("/") ? returnTo : "/")}
      />
    </PageLayout>
  );
}
