import type { Metadata } from "next";
import "@marpich/shared/theme/tokens.css";
import "@marpich/shared/components.css";
import "@marpich/core/shell/shell.css";
import "./globals.css";
import { AuthProvider } from "@marpich/auth-provider";
import { MarpichProviders, AppShell } from "@marpich/core";
import { ShellNav } from "@/components/ShellNav";

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
            <AppShell nav={<ShellNav />}>{children}</AppShell>
          </AuthProvider>
        </MarpichProviders>
      </body>
    </html>
  );
}
