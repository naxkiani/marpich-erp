"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type SearchHit = { id: string; title: string; subtitle?: string; href?: string };

export function GlobalSearch() {
  const { t } = useLocale();
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [loading, setLoading] = useState(false);

  const search = useCallback(async (q: string) => {
    if (!q.trim()) {
      setHits([]);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(
        `${API_URL}/api/v1/search/query?q=${encodeURIComponent(q)}&limit=8`,
      );
      if (!res.ok) throw new Error("search failed");
      const data = (await res.json()) as { results?: SearchHit[] };
      setHits(data.results ?? []);
    } catch {
      setHits([{ id: "local", title: q, subtitle: "Local navigation (API offline)" }]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => search(query), 300);
    return () => window.clearTimeout(timer);
  }, [query, search]);

  return (
    <div className="mp-global-search">
      <label className="sr-only" htmlFor="global-search">
        {t("shell.search")}
      </label>
      <input
        id="global-search"
        className="mp-input mp-search-input"
        placeholder={t("shell.search")}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-expanded={hits.length > 0}
        aria-controls="global-search-results"
      />
      {query && (
        <ul id="global-search-results" className="mp-search-results mp-animate-in" role="listbox">
          {loading ? <li className="mp-search-muted">…</li> : null}
          {hits.map((hit) => (
            <li key={hit.id} role="option">
              <button type="button" className="mp-search-hit" onClick={() => setQuery("")}>
                <strong>{hit.title}</strong>
                {hit.subtitle ? <span>{hit.subtitle}</span> : null}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
