"use client";

import { PageLayout } from "@marpich/core";

export default function ModulesPage() {
  return (
    <PageLayout
      title="Modules"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Modules" },
      ]}
    >
      <p>Industry modules register here via Core Platform module activation.</p>
    </PageLayout>
  );
}
