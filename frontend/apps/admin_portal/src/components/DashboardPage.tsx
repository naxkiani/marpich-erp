"use client";

import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  ImportDialog,
  PrintButton,
  ProgressBar,
  SkeletonTable,
  SmartForm,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useMemo, useState } from "react";

type Row = { id: string; name: string; status: string; updated: string };

const INITIAL_ROWS: Row[] = [
  { id: "1", name: "Core Platform", status: "Active", updated: "2026-07-02" },
  { id: "2", name: "Hospital Module", status: "Active", updated: "2026-07-01" },
  { id: "3", name: "Search Service", status: "Active", updated: "2026-06-28" },
];

export function DashboardPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const [loading, setLoading] = useState(false);
  const [rows, setRows] = useState<Row[]>(INITIAL_ROWS);
  const [filtered, setFiltered] = useState<Row[]>(INITIAL_ROWS);
  const [progress, setProgress] = useState(100);
  const [showEmpty, setShowEmpty] = useState(false);

  const formInitial = useMemo(() => ({ name: "", status: "Active" }), []);

  const onAutosave = useCallback((values: Record<string, string>) => {
    console.info("[autosave]", values);
  }, []);

  const { saving } = useAutosave(formInitial, onAutosave, 1200);

  const columns = useMemo(
    () => [
      { key: "name", header: "Module", sortable: true },
      { key: "status", header: "Status", sortable: true },
      { key: "updated", header: "Updated", sortable: true },
    ],
    [],
  );

  const refresh = () => {
    setLoading(true);
    setProgress(20);
    window.setTimeout(() => setProgress(60), 400);
    window.setTimeout(() => {
      setLoading(false);
      setProgress(100);
    }, 900);
  };

  const removeLast = () => {
    setRows((prev) => {
      const next = prev.slice(0, -1);
      setFiltered(next);
      if (next.length === 0) setShowEmpty(true);
      push({
        message: "Record removed",
        onUndo: () => {
          setRows(prev);
          setFiltered(prev);
          setShowEmpty(false);
        },
      });
      return next;
    });
  };

  return (
    <PageLayout
      title={t("demo.title")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("demo.title") },
      ]}
      actions={
        <>
          <ExportButton label={t("common.export")} rows={filtered} />
          <ImportDialog
            label={t("common.import")}
            onImport={(imported) => {
              const mapped: Row[] = imported.map((r, i) => ({
                id: String(Date.now() + i),
                name: r.name ?? "Imported",
                status: r.status ?? "Draft",
                updated: new Date().toISOString().slice(0, 10),
              }));
              setRows((prev) => [...mapped, ...prev]);
              setFiltered((prev) => [...mapped, ...prev]);
              setShowEmpty(false);
            }}
          />
          <PrintButton label={t("common.print")} />
          <button type="button" className="mp-btn" onClick={refresh}>
            Refresh
          </button>
          <button type="button" className="mp-btn mp-btn-primary" onClick={removeLast}>
            Demo undo
          </button>
        </>
      }
    >
      <ProgressBar value={progress} label={loading ? "Loading modules…" : "Ready"} />

      <AdvancedFilterBar
        filters={[
          { id: "q", label: t("common.filter"), type: "text" },
          { id: "from", label: "From", type: "date" },
        ]}
        onChange={(values) => {
          const q = (values.q ?? "").toLowerCase();
          setFiltered(
            rows.filter((r) => !q || r.name.toLowerCase().includes(q)),
          );
        }}
      />

      <div className="mp-demo-grid">
        <section aria-labelledby="modules-heading">
          <h2 id="modules-heading">Modules</h2>
          {loading ? (
            <SkeletonTable rows={4} cols={3} />
          ) : showEmpty || filtered.length === 0 ? (
            <EmptyState
              title={t("demo.empty")}
              description="Activate industry packs from Core Platform."
              action={
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  onClick={() => {
                    setRows(INITIAL_ROWS);
                    setFiltered(INITIAL_ROWS);
                    setShowEmpty(false);
                  }}
                >
                  {t("demo.add")}
                </button>
              }
            />
          ) : (
            <DataTable columns={columns} rows={filtered} selectable />
          )}
        </section>

        <section aria-labelledby="settings-heading">
          <h2 id="settings-heading">
            Settings {saving ? "(saving…)" : ""}
          </h2>
          <SmartForm
            autosave
            onAutosave={onAutosave}
            initialValues={formInitial}
            fields={[
              {
                name: "name",
                label: "Display name",
                required: true,
                help: "Shown in admin portal navigation",
              },
              {
                name: "status",
                label: "Status",
                type: "select",
                options: [
                  { value: "Active", label: "Active" },
                  { value: "Draft", label: "Draft" },
                ],
              },
            ]}
            onSubmit={(values) => push({ message: `Saved ${values.name}` })}
          />
        </section>
      </div>

      <style jsx>{`
        .mp-demo-grid {
          display: grid;
          grid-template-columns: 1.4fr 1fr;
          gap: 1.25rem;
        }
        h2 {
          margin: 0 0 0.75rem;
          font-size: 1.1rem;
        }
        @media (max-width: 960px) {
          .mp-demo-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
