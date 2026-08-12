"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";
import { API_URL, getPlatformAuthHeaders } from "../platform/session";
import { searchApplicationNav } from "../platform/applicationRegistry";

type SearchHit = { id: string; title: string; subtitle?: string; href?: string };

export function GlobalSearch() {
  const { t } = useLocale();
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (q: string) => {
    if (!q.trim()) {
      setHits([]);
      setError(null);
      return;
    }
    setLoading(true);
    setError(null);
    const navHits: SearchHit[] = searchApplicationNav(q).map((app) => ({
      id: `nav:${app.id}`,
      title: app.label,
      subtitle: "Application",
      href: app.href,
    }));
    const headers = getPlatformAuthHeaders();
    if (!headers) {
      setHits(navHits);
      setError("Sign in to search platform records.");
      setLoading(false);
      return;
    }
    try {
      const res = await fetch(
        `${API_URL}/api/v1/search/query?q=${encodeURIComponent(q)}&limit=8`,
        { headers },
      );
      if (!res.ok) {
        setHits(navHits);
        setError(`Search unavailable (${res.status}). Showing applications.`);
        return;
      }
      const json = (await res.json()) as {
        data?: { items?: Array<{ id?: string; title?: string; entity_type?: string; entity_id?: string }> };
        results?: SearchHit[];
      };
      const items = json.data?.items ?? [];
      const apiHits: SearchHit[] = items.map((item, idx) => ({
        id: String(item.id ?? item.entity_id ?? `hit-${idx}`),
        title: item.title ?? item.entity_id ?? "Result",
        subtitle: item.entity_type,
        href: undefined,
      }));
      const merged = [...navHits, ...apiHits].slice(0, 12);
      setHits(merged.length ? merged : navHits);
    } catch {
      setHits(navHits);
      setError("Search API offline. Showing applications.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void search(query), 300);
    return () => window.clearTimeout(timer);
  }, [query, search]);

  function openHit(hit: SearchHit) {
    setQuery("");
    setHits([]);
    if (hit.href) {
      window.location.href = hit.href;
    }
  }

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
      {query ? (
        <ul id="global-search-results" className="mp-search-results mp-animate-in" role="listbox">
          {loading ? <li className="mp-search-muted">…</li> : null}
          {error ? <li className="mp-search-muted">{error}</li> : null}
          {hits.map((hit) => (
            <li key={hit.id} role="option">
              <button type="button" className="mp-search-hit" onClick={() => openHit(hit)}>
                <strong>{hit.title}</strong>
                {hit.subtitle ? <span>{hit.subtitle}</span> : null}
              </button>
            </li>
          ))}
          {!loading && hits.length === 0 ? (
            <li className="mp-search-muted">No matches</li>
          ) : null}
        </ul>
      ) : null}
    </div>
  );
}
