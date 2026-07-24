"use client";

import Link from "next/link";
import { PageLayout } from "@marpich/core";
import {
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  Skeleton,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  categoryForPack,
  fetchIndustryPacks,
  jewelForPack,
  launchHrefForPack,
  packInitials,
  type IndustryPack,
  type ModuleCategory,
  type ModuleJewel,
} from "@/lib/platformClient";

const DRAFT_KEY = "marpich.modules.desk.draft";

const CATEGORY_JEWEL_CLASS: Record<ModuleCategory, ModuleJewel> = {
  healthcare: "emerald",
  education: "royal",
  finance: "gold",
  commerce: "orange",
  government: "forest",
  operations: "purple",
  platform: "silver",
};

const CATEGORY_ORDER: ModuleCategory[] = [
  "healthcare",
  "education",
  "finance",
  "commerce",
  "government",
  "operations",
  "platform",
];

type ViewMode = "desk" | "list";

function categoryLabelKey(cat: ModuleCategory): string {
  return `modules.cat.${cat}`;
}

export function ModulesDeskPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(25);
  const [packs, setPacks] = useState<IndustryPack[]>([]);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<ModuleCategory | "all">("all");
  const [view, setView] = useState<ViewMode>("desk");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [draftReady, setDraftReady] = useState(false);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const formDraft = useMemo(
    () => ({ query, category, view, selectedId }),
    [category, query, selectedId, view],
  );

  const persistDraft = useCallback(
    async (values: typeof formDraft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(formDraft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof formDraft>;
        if (typeof parsed.query === "string") setQuery(parsed.query);
        if (
          parsed.category === "all" ||
          (typeof parsed.category === "string" &&
            CATEGORY_ORDER.includes(parsed.category as ModuleCategory))
        ) {
          setCategory(parsed.category as ModuleCategory | "all");
        }
        if (parsed.view === "desk" || parsed.view === "list") setView(parsed.view);
        if (typeof parsed.selectedId === "string" && parsed.selectedId.trim()) {
          setSelectedId(parsed.selectedId);
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const data = await fetchIndustryPacks();
      setPacks(data);
      setSelectedId((prev) => {
        if (prev && data.some((p) => p.pack_id === prev)) return prev;
        return data[0]?.pack_id ?? null;
      });
      setLastAction("catalog");
      setProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : t("dashboard.loadFailed");
      setError(msg);
      setProgress(100);
      push({ message: msg });
    } finally {
      setLoading(false);
    }
  }, [push, t]);

  useEffect(() => {
    void load();
  }, [load]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return packs.filter((p) => {
      const cat = categoryForPack(p.pack_id);
      if (category !== "all" && cat !== category) return false;
      if (!q) return true;
      const hay = [
        p.pack_id,
        p.display_name,
        p.description,
        ...p.required_modules,
        ...p.optional_modules,
      ]
        .join(" ")
        .toLowerCase();
      return hay.includes(q);
    });
  }, [packs, query, category]);

  const grouped = useMemo(() => {
    const map = new Map<ModuleCategory, IndustryPack[]>();
    for (const cat of CATEGORY_ORDER) map.set(cat, []);
    for (const p of filtered) {
      const cat = categoryForPack(p.pack_id);
      map.get(cat)!.push(p);
    }
    return CATEGORY_ORDER.map((cat) => ({
      cat,
      items: map.get(cat) ?? [],
    })).filter((g) => g.items.length > 0);
  }, [filtered]);

  const selected = useMemo(
    () => packs.find((p) => p.pack_id === selectedId) ?? filtered[0] ?? null,
    [packs, selectedId, filtered],
  );

  const lifecycleStep = useMemo(() => {
    if (selected && launchHrefForPack(selected.pack_id)) return 3;
    if (selected) return 2;
    if (query.trim() || category !== "all") return 1;
    if (packs.length > 0) return 0;
    return 0;
  }, [category, packs.length, query, selected]);

  const workflowSteps = useMemo(
    () => [
      { id: "browse", label: t("modules.step.browse") },
      { id: "filter", label: t("modules.step.filter") },
      { id: "select", label: t("modules.step.select") },
      { id: "launch", label: t("modules.step.launch") },
    ],
    [t],
  );

  const exportRows = useMemo(
    () =>
      filtered.map((p) => ({
        pack_id: p.pack_id,
        name: p.display_name,
        category: categoryForPack(p.pack_id),
        required: p.required_modules.join("|"),
        optional: p.optional_modules.join("|"),
      })),
    [filtered],
  );

  const counts = useMemo(() => {
    const byCat = Object.fromEntries(
      CATEGORY_ORDER.map((c) => [c, 0]),
    ) as Record<ModuleCategory, number>;
    for (const p of packs) byCat[categoryForPack(p.pack_id)] += 1;
    return {
      total: packs.length,
      modules: packs.reduce(
        (n, p) => n + p.required_modules.length + p.optional_modules.length,
        0,
      ),
      byCat,
    };
  }, [packs]);

  return (
    <PageLayout
      title={t("modules.title")}
      subtitle={t("modules.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("modules.title") },
      ]}
      actions={
        <>
          <ExportButton label={t("common.export")} rows={exportRows} filename="modules-desk.csv" />
          <PrintButton label={t("common.print")} />
          <button
            type="button"
            className={`mp-btn ${view === "desk" ? "mp-btn-primary" : ""}`}
            aria-pressed={view === "desk"}
            onClick={() => setView("desk")}
          >
            {t("modules.view.desk")}
          </button>
          <button
            type="button"
            className={`mp-btn ${view === "list" ? "mp-btn-primary" : ""}`}
            aria-pressed={view === "list"}
            onClick={() => setView("list")}
          >
            {t("modules.view.list")}
          </button>
          <button type="button" className="mp-btn" disabled={loading} onClick={() => void load()}>
            {t("common.refresh")}
          </button>
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("dashboard.loading") : t("dashboard.ready")}
      />

      {error ? (
        <p className="mp-desk-alert" role="alert">
          {error}
        </p>
      ) : null}

      <div className="mp-desk-shell">
        <aside className="mp-desk-rail" aria-label={t("modules.rail")}>
          <section className="mp-desk-rail-card">
            <header className="mp-desk-rail-head">
              <h2>{t("modules.workflow")}</h2>
            </header>
            <div className="mp-desk-rail-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("modules.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("modules.workflowHint")}</p>
              )}
            </div>
          </section>
          <section className="mp-desk-rail-card">
            <header className="mp-desk-rail-head">
              <h2>{t("modules.rail.status")}</h2>
            </header>
            <div className="mp-desk-rail-body">
              <div className="mp-desk-status-row">
                <span>{t("modules.stat.packs")}</span>
                <strong>{counts.total}</strong>
              </div>
              <div className="mp-desk-status-row">
                <span>{t("modules.stat.visible")}</span>
                <strong>{filtered.length}</strong>
              </div>
              {selected ? (
                <p className="mp-field-help">
                  {t("modules.selected")}: {selected.display_name}
                </p>
              ) : null}
              {lastAction ? (
                <p className="mp-field-help">
                  {t("modules.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>
        </aside>

        <div className="mp-desk-content">
          <div className="mp-desk-toolbar" role="search">
            <label className="mp-desk-search">
              <span className="sr-only">{t("common.filter")}</span>
              <input
                className="mp-input"
                type="search"
                value={query}
                placeholder={t("modules.search")}
                onChange={(e) => setQuery(e.target.value)}
                autoComplete="off"
              />
            </label>
            <div className="mp-desk-cats" role="tablist" aria-label={t("modules.categories")}>
              <button
                type="button"
                role="tab"
                aria-selected={category === "all"}
                className={`mp-desk-chip ${category === "all" ? "mp-desk-chip--on" : ""}`}
                onClick={() => setCategory("all")}
              >
                {t("modules.cat.all")} ({counts.total})
              </button>
              {CATEGORY_ORDER.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  role="tab"
                  aria-selected={category === cat}
                  className={`mp-desk-chip mp-desk-chip--${CATEGORY_JEWEL_CLASS[cat]} ${
                    category === cat ? "mp-desk-chip--on" : ""
                  }`}
                  onClick={() => setCategory(cat)}
                >
                  {t(categoryLabelKey(cat))} ({counts.byCat[cat]})
                </button>
              ))}
            </div>
          </div>

          <div className="mp-desk-metrics" aria-label={t("modules.metrics")}>
            <div>
              <span className="mp-desk-metric-label">{t("modules.stat.packs")}</span>
              <strong>{counts.total}</strong>
            </div>
            <div>
              <span className="mp-desk-metric-label">{t("modules.stat.modules")}</span>
              <strong>{counts.modules}</strong>
            </div>
            <div>
              <span className="mp-desk-metric-label">{t("modules.stat.visible")}</span>
              <strong>{filtered.length}</strong>
            </div>
          </div>

          {loading ? (
            <div className="mp-desk-skeleton" aria-busy="true" aria-label={t("dashboard.loading")}>
              {Array.from({ length: 12 }).map((_, i) => (
                <div key={i} className="mp-desk-skel-tile">
                  <Skeleton />
                </div>
              ))}
            </div>
          ) : filtered.length === 0 ? (
            <EmptyState title={t("demo.empty")} description={t("modules.emptyHint")} />
          ) : (
            <div className={`mp-desk-layout ${selected ? "mp-desk-layout--split" : ""}`}>
              <div className="mp-desk-main">
                {view === "desk"
                  ? grouped.map((group) => (
                      <section
                        key={group.cat}
                        className="mp-desk-section"
                        aria-labelledby={`desk-cat-${group.cat}`}
                      >
                        <header className="mp-desk-section-head">
                          <h2 id={`desk-cat-${group.cat}`}>{t(categoryLabelKey(group.cat))}</h2>
                          <span className="mp-field-help">{group.items.length}</span>
                        </header>
                        <ul className="mp-desk-grid">
                          {group.items.map((pack, index) => {
                            const jewel = jewelForPack(pack.pack_id, index);
                            const active = selected?.pack_id === pack.pack_id;
                            return (
                              <li key={pack.pack_id}>
                                <button
                                  type="button"
                                  className={`mp-desk-tile ${active ? "mp-desk-tile--active" : ""}`}
                                  aria-pressed={active}
                                  onClick={() => {
                                    setSelectedId(pack.pack_id);
                                    setLastAction("select");
                                  }}
                                  onDoubleClick={() => {
                                    const href = launchHrefForPack(pack.pack_id);
                                    if (href) window.location.href = href;
                                  }}
                                >
                                  <span
                                    className={`mp-desk-icon mp-desk-jewel--${jewel}`}
                                    aria-hidden
                                  >
                                    {packInitials(pack.display_name)}
                                  </span>
                                  <span className="mp-desk-tile-body">
                                    <strong>{pack.display_name}</strong>
                                    <span className="mp-desk-tile-id">{pack.pack_id}</span>
                                  </span>
                                </button>
                              </li>
                            );
                          })}
                        </ul>
                      </section>
                    ))
                  : (
                    <ul className="mp-desk-list">
                      {filtered.map((pack, index) => {
                        const jewel = jewelForPack(pack.pack_id, index);
                        const active = selected?.pack_id === pack.pack_id;
                        return (
                          <li key={pack.pack_id}>
                            <button
                              type="button"
                              className={`mp-desk-row ${active ? "mp-desk-row--active" : ""}`}
                              aria-pressed={active}
                              onClick={() => {
                                setSelectedId(pack.pack_id);
                                setLastAction("select");
                              }}
                            >
                              <span
                                className={`mp-desk-icon mp-desk-icon--sm mp-desk-jewel--${jewel}`}
                              >
                                {packInitials(pack.display_name)}
                              </span>
                              <span className="mp-desk-row-main">
                                <strong>{pack.display_name}</strong>
                                <span className="mp-field-help">{pack.description}</span>
                              </span>
                              <span className="mp-desk-row-meta">
                                {pack.required_modules.length}+{pack.optional_modules.length}
                              </span>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  )}
              </div>

              {selected ? (
                <aside className="mp-desk-detail" aria-label={selected.display_name}>
                  <div
                    className={`mp-desk-detail-banner mp-desk-jewel--${jewelForPack(selected.pack_id)}`}
                  >
                    <span className="mp-desk-icon mp-desk-icon--lg" aria-hidden>
                      {packInitials(selected.display_name)}
                    </span>
                    <div>
                      <h2>{selected.display_name}</h2>
                      <p>{selected.pack_id}</p>
                    </div>
                  </div>
                  <p className="mp-desk-detail-desc">{selected.description}</p>
                  <dl className="mp-desk-dl">
                    <div>
                      <dt>{t("modules.field.category")}</dt>
                      <dd>{t(categoryLabelKey(categoryForPack(selected.pack_id)))}</dd>
                    </div>
                    <div>
                      <dt>{t("modules.field.locale")}</dt>
                      <dd>{selected.default_locale}</dd>
                    </div>
                    <div>
                      <dt>{t("modules.field.compliance")}</dt>
                      <dd>
                        {(selected.compliance_frameworks ?? []).join(", ") || "—"}
                      </dd>
                    </div>
                  </dl>

                  <h3>{t("dashboard.requiredModules")}</h3>
                  <ul className="mp-desk-module-tags">
                    {selected.required_modules.map((m) => (
                      <li key={m} className="mp-desk-tag mp-desk-tag--required">
                        {m}
                      </li>
                    ))}
                  </ul>

                  <h3>{t("dashboard.optionalModules")}</h3>
                  {selected.optional_modules.length === 0 ? (
                    <p className="mp-field-help">—</p>
                  ) : (
                    <ul className="mp-desk-module-tags">
                      {selected.optional_modules.map((m) => (
                        <li key={m} className="mp-desk-tag mp-desk-tag--optional">
                          {m}
                        </li>
                      ))}
                    </ul>
                  )}

                  <div className="mp-desk-detail-actions">
                    {launchHrefForPack(selected.pack_id) ? (
                      <Link
                        href={launchHrefForPack(selected.pack_id)!}
                        className="mp-btn mp-btn-primary"
                        onClick={() => setLastAction("launch")}
                      >
                        {t("modules.openApp")}
                      </Link>
                    ) : (
                      <span className="mp-field-help">{t("modules.noAppRoute")}</span>
                    )}
                    <Link href="/" className="mp-btn">
                      {t("demo.title")}
                    </Link>
                  </div>
                </aside>
              ) : null}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .mp-desk-shell {
          display: grid;
          grid-template-columns: minmax(200px, 260px) 1fr;
          gap: 1.15rem;
          margin-top: 0.75rem;
        }
        .mp-desk-rail {
          display: flex;
          flex-direction: column;
          gap: 0.85rem;
        }
        .mp-desk-rail-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: var(--mp-radius, 0.5rem);
          background: var(--mp-bg-elevated, #fff);
        }
        .mp-desk-rail-head {
          padding: 0.7rem 0.9rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .mp-desk-rail-head h2 {
          margin: 0;
          font-size: 0.92rem;
        }
        .mp-desk-rail-body {
          padding: 0.8rem 0.9rem;
          display: flex;
          flex-direction: column;
          gap: 0.55rem;
        }
        .mp-desk-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .mp-desk-content {
          display: flex;
          flex-direction: column;
          gap: 0.85rem;
          min-width: 0;
        }
        .mp-desk-alert {
          color: var(--mp-danger);
          margin: 0.25rem 0 0.75rem;
        }
        .mp-desk-toolbar {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .mp-desk-search {
          display: block;
          max-width: 28rem;
        }
        .mp-desk-cats {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
        }
        .mp-desk-chip {
          border: 1px solid var(--mp-border);
          background: var(--mp-bg-elevated);
          color: var(--mp-fg-muted);
          border-radius: 999px;
          padding: 0.3rem 0.75rem;
          font-size: 0.8rem;
          cursor: pointer;
          transition: background var(--mp-transition), color var(--mp-transition),
            border-color var(--mp-transition);
        }
        .mp-desk-chip--on {
          background: var(--mp-royal);
          border-color: var(--mp-royal);
          color: #fff;
        }
        .mp-desk-chip--emerald.mp-desk-chip--on {
          background: var(--mp-emerald);
          border-color: var(--mp-emerald);
        }
        .mp-desk-chip--gold.mp-desk-chip--on {
          background: var(--mp-gold);
          border-color: var(--mp-gold);
          color: #1a1a1a;
        }
        .mp-desk-chip--orange.mp-desk-chip--on {
          background: var(--mp-orange);
          border-color: var(--mp-orange);
        }
        .mp-desk-chip--forest.mp-desk-chip--on {
          background: var(--mp-forest);
          border-color: var(--mp-forest);
        }
        .mp-desk-chip--purple.mp-desk-chip--on {
          background: var(--mp-purple);
          border-color: var(--mp-purple);
        }
        .mp-desk-chip--silver.mp-desk-chip--on {
          background: var(--mp-silver);
          border-color: var(--mp-silver);
          color: #1a1a1a;
        }
        .mp-desk-metrics {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.75rem;
          padding: 0.85rem 1rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
        }
        .mp-desk-metrics > div {
          padding-inline-start: 0.65rem;
          border-inline-start: 3px solid var(--mp-forest);
        }
        .mp-desk-metrics > div:nth-child(2) {
          border-inline-start-color: var(--mp-royal);
        }
        .mp-desk-metrics > div:nth-child(3) {
          border-inline-start-color: var(--mp-gold);
        }
        .mp-desk-metrics strong {
          display: block;
          font-size: 1.35rem;
          color: var(--mp-forest);
        }
        .mp-desk-metrics > div:nth-child(2) strong {
          color: var(--mp-royal);
        }
        .mp-desk-metrics > div:nth-child(3) strong {
          color: var(--mp-gold);
        }
        .mp-desk-metric-label {
          display: block;
          font-size: 0.78rem;
          color: var(--mp-fg-muted);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .mp-desk-layout {
          display: grid;
          gap: 1.25rem;
          /* Keep desk grid on the visual left in LTR and RTL. */
          direction: ltr;
        }
        .mp-desk-main,
        .mp-desk-detail {
          direction: inherit;
        }
        :global([dir="rtl"]) .mp-desk-main,
        :global([dir="rtl"]) .mp-desk-detail {
          direction: rtl;
        }
        .mp-desk-layout--split {
          grid-template-columns: 1fr minmax(280px, 340px);
          align-items: start;
        }
        .mp-desk-section {
          margin-block-end: 1.5rem;
        }
        .mp-desk-section:last-child {
          margin-block-end: 0;
        }
        .mp-desk-section-head {
          display: flex;
          align-items: baseline;
          justify-content: space-between;
          margin-block-end: 0.75rem;
          padding-block-end: 0.4rem;
          border-block-end: 1px solid var(--mp-border);
        }
        .mp-desk-section-head h2 {
          margin: 0;
          font-size: 0.85rem;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          color: var(--mp-fg-muted);
          font-weight: 600;
        }
        .mp-desk-grid {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(12.5rem, 1fr));
          gap: 0.85rem;
          align-items: stretch;
        }
        .mp-desk-grid > li {
          min-width: 0;
        }
        .mp-desk-tile {
          box-sizing: border-box;
          width: 100%;
          aspect-ratio: 8 / 5; /* 1.6 : 1 rectangle */
          height: auto;
          min-height: 0;
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: flex-start;
          gap: 0.7rem;
          padding: 0.7rem 0.8rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          cursor: pointer;
          text-align: start;
          color: inherit;
          overflow: hidden;
          transition:
            border-color var(--mp-transition),
            transform var(--mp-transition),
            box-shadow var(--mp-transition);
        }
        .mp-desk-tile:hover {
          border-color: var(--mp-gold);
          transform: translateY(-1px);
        }
        .mp-desk-tile--active {
          border-color: var(--mp-gold);
          box-shadow: 0 0 0 1px var(--mp-gold), var(--mp-shadow);
        }
        .mp-desk-icon {
          display: grid;
          place-items: center;
          width: 2.6rem;
          height: 2.6rem;
          border-radius: 0.5rem;
          font-size: 0.8rem;
          font-weight: 700;
          letter-spacing: 0.04em;
          color: #fff;
          flex-shrink: 0;
        }
        .mp-desk-icon--sm {
          width: 2.35rem;
          height: 2.35rem;
          font-size: 0.75rem;
          border-radius: 0.45rem;
          flex-shrink: 0;
        }
        .mp-desk-icon--lg {
          width: 3.5rem;
          height: 3.5rem;
          font-size: 1.05rem;
        }
        .mp-desk-jewel--royal {
          background: linear-gradient(145deg, var(--mp-royal-bright), var(--mp-royal));
        }
        .mp-desk-jewel--emerald {
          background: linear-gradient(145deg, var(--mp-emerald-bright), var(--mp-emerald));
        }
        .mp-desk-jewel--forest {
          background: linear-gradient(145deg, #2f5a48, var(--mp-forest));
        }
        .mp-desk-jewel--gold {
          background: linear-gradient(145deg, var(--mp-gold-soft), var(--mp-gold));
          color: #1a1a1a;
        }
        .mp-desk-jewel--orange {
          background: linear-gradient(145deg, #e06a3a, var(--mp-orange));
        }
        .mp-desk-jewel--purple {
          background: linear-gradient(145deg, var(--mp-purple-soft), var(--mp-purple));
        }
        .mp-desk-jewel--silver {
          background: linear-gradient(145deg, #cfd3da, var(--mp-silver));
          color: #1a1a1a;
        }
        .mp-desk-tile-body {
          display: flex;
          flex-direction: column;
          gap: 0.12rem;
          min-width: 0;
          flex: 1;
          text-align: start;
        }
        .mp-desk-tile-body strong {
          font-size: 0.86rem;
          font-weight: 600;
          line-height: 1.25;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
        .mp-desk-tile-id {
          font-size: 0.68rem;
          color: var(--mp-fg-muted);
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .mp-desk-list {
          list-style: none;
          margin: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          gap: 0.4rem;
        }
        .mp-desk-row {
          width: 100%;
          display: grid;
          grid-template-columns: auto 1fr auto;
          gap: 0.75rem;
          align-items: center;
          padding: 0.7rem 0.85rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          cursor: pointer;
          text-align: start;
          color: inherit;
        }
        .mp-desk-row--active {
          border-color: var(--mp-gold);
          background: color-mix(in srgb, var(--mp-royal) 4%, white);
        }
        .mp-desk-row-main {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
          min-width: 0;
        }
        .mp-desk-row-meta {
          font-size: 0.8rem;
          color: var(--mp-fg-muted);
          font-variant-numeric: tabular-nums;
        }
        .mp-desk-detail {
          position: sticky;
          top: 4.5rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          padding: 0 0 1rem;
          overflow: hidden;
        }
        .mp-desk-detail-banner {
          display: flex;
          align-items: center;
          gap: 0.85rem;
          padding: 1rem;
          color: #fff;
        }
        .mp-desk-detail-banner.mp-desk-jewel--gold,
        .mp-desk-detail-banner.mp-desk-jewel--silver {
          color: #1a1a1a;
        }
        .mp-desk-detail-banner h2 {
          margin: 0;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .mp-desk-detail-banner p {
          margin: 0.15rem 0 0;
          opacity: 0.85;
          font-size: 0.8rem;
        }
        .mp-desk-detail-desc,
        .mp-desk-detail h3,
        .mp-desk-dl,
        .mp-desk-module-tags,
        .mp-desk-detail-actions,
        .mp-desk-detail .mp-field-help {
          padding-inline: 1rem;
        }
        .mp-desk-detail-desc {
          margin: 0.85rem 0;
          color: var(--mp-fg-muted);
          font-size: 0.9rem;
          line-height: 1.45;
        }
        .mp-desk-detail h3 {
          margin: 1rem 0 0.45rem;
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--mp-fg-muted);
        }
        .mp-desk-dl {
          display: grid;
          gap: 0.45rem;
          margin: 0;
        }
        .mp-desk-dl div {
          display: grid;
          grid-template-columns: 7rem 1fr;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .mp-desk-dl dt {
          color: var(--mp-fg-muted);
        }
        .mp-desk-dl dd {
          margin: 0;
        }
        .mp-desk-module-tags {
          list-style: none;
          margin: 0;
          padding-block: 0;
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .mp-desk-tag {
          font-size: 0.72rem;
          padding: 0.2rem 0.45rem;
          border-radius: var(--mp-radius-sm);
          border: 1px solid var(--mp-border);
          background: var(--mp-bg-subtle);
          color: var(--mp-fg);
        }
        .mp-desk-tag--required {
          border-color: color-mix(in srgb, var(--mp-emerald) 35%, var(--mp-border));
          background: var(--mp-success-bg);
        }
        .mp-desk-tag--optional {
          border-color: color-mix(in srgb, var(--mp-purple) 30%, var(--mp-border));
          background: var(--mp-info-bg);
        }
        .mp-desk-detail-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-top: 1.15rem;
        }
        .mp-desk-skeleton {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(12.5rem, 1fr));
          gap: 0.85rem;
        }
        .mp-desk-skel-tile {
          aspect-ratio: 8 / 5;
          border-radius: var(--mp-radius);
          overflow: hidden;
        }
        .mp-desk-skel-tile :global(.mp-skeleton) {
          width: 100%;
          height: 100%;
        }
        @media (max-width: 960px) {
          .mp-desk-shell {
            grid-template-columns: 1fr;
          }
          .mp-desk-layout--split {
            grid-template-columns: 1fr;
          }
          .mp-desk-detail {
            position: static;
          }
          .mp-desk-metrics {
            grid-template-columns: 1fr;
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .mp-desk-tile {
            transition: none;
          }
        }
      `}</style>
    </PageLayout>
  );
}
