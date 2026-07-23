"use client";

import { AccountLoginPage } from "@/components/AccountLoginPage";
import { Suspense } from "react";

export default function LoginRoutePage() {
  return (
    <Suspense fallback={null}>
      <AccountLoginPage />
    </Suspense>
  );
}
