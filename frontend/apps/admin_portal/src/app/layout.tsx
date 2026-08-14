import type { Metadata } from "next";
import "@marpich/shared/theme/tokens.css";
import "@marpich/shared/components.css";
import "@marpich/core/shell/shell.css";
import "./globals.css";
import { AuthProvider } from "@marpich/auth-provider";
import { MarpichProviders } from "@marpich/core";
import { AuthenticatedAppShell } from "@/components/AuthenticatedAppShell";

export const metadata: Metadata = {
  title: "Marpich Admin Portal",
  description: "Enterprise modular platform — admin portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <MarpichProviders>
          <AuthProvider>
            <AuthenticatedAppShell>{children}</AuthenticatedAppShell>
          </AuthProvider>
        </MarpichProviders>
      </body>
    </html>
  );
}
