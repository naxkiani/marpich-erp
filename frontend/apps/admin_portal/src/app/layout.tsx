import type { Metadata } from "next";
import "@marpich/shared/theme/tokens.css";
import "@marpich/shared/components.css";
import "@marpich/core/shell/shell.css";
import "./globals.css";
import { MarpichProviders, AppShell } from "@marpich/core";
import { ShellNav } from "@/components/ShellNav";

export const metadata: Metadata = {
  title: "Marpich Admin Portal",
  description: "Enterprise modular platform — admin portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <MarpichProviders>
          <AppShell nav={<ShellNav />}>{children}</AppShell>
        </MarpichProviders>
      </body>
    </html>
  );
}
