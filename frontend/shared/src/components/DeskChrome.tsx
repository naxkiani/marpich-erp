"use client";

import type { ReactNode } from "react";
import "./deskChrome.css";

export function DeskChrome({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={`mp-desk-chrome${className ? ` ${className}` : ""}`}>{children}</div>;
}

export function DeskAlert({ children }: { children: ReactNode }) {
  return (
    <p className="mp-desk-chrome-alert" role="alert">
      {children}
    </p>
  );
}

export function DeskPanel({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="mp-desk-chrome-panel">
      <header className="mp-desk-chrome-head">
        <h2>{title}</h2>
      </header>
      <div className="mp-desk-chrome-body">{children}</div>
    </section>
  );
}

export function DeskMetrics({
  items,
  loading = false,
}: {
  items: Array<{
    label: string;
    value: string | number;
    href?: string;
    tone?: "default" | "ok" | "warn" | "danger";
    hint?: string;
  }>;
  loading?: boolean;
}) {
  return (
    <div className="mp-desk-chrome-metrics" aria-label="Metrics" aria-busy={loading || undefined}>
      {items.map((item) => {
        const tone = item.tone && item.tone !== "default" ? ` mp-desk-chrome-metric--${item.tone}` : "";
        const inner = (
          <>
            <span>{item.label}</span>
            <strong>{loading ? "…" : item.value}</strong>
            {item.hint ? <em className="mp-desk-chrome-metric-hint">{item.hint}</em> : null}
          </>
        );
        if (item.href) {
          return (
            <a
              key={item.label}
              href={item.href}
              className={`mp-desk-chrome-metric mp-desk-chrome-metric--link${tone}`}
            >
              {inner}
            </a>
          );
        }
        return (
          <div key={item.label} className={`mp-desk-chrome-metric${tone}`}>
            {inner}
          </div>
        );
      })}
    </div>
  );
}

/** Compact KPI strip for home / executive surfaces (shared, RTL-safe). */
export function KpiStrip({
  items,
  loading = false,
  label,
}: {
  items: Array<{
    id: string;
    label: string;
    value: string | number;
    href?: string;
    tone?: "default" | "ok" | "warn" | "danger";
  }>;
  loading?: boolean;
  label?: string;
}) {
  return (
    <div
      className="mp-kpi-strip"
      role="group"
      aria-label={label ?? "KPI"}
      aria-busy={loading || undefined}
    >
      {items.map((item) => {
        const tone = item.tone && item.tone !== "default" ? ` mp-kpi-card--${item.tone}` : "";
        const body = (
          <>
            <span className="mp-kpi-card-label">{item.label}</span>
            <strong className="mp-kpi-card-value">{loading ? "…" : item.value}</strong>
          </>
        );
        if (item.href) {
          return (
            <a key={item.id} href={item.href} className={`mp-kpi-card mp-kpi-card--link${tone}`}>
              {body}
            </a>
          );
        }
        return (
          <div key={item.id} className={`mp-kpi-card${tone}`}>
            {body}
          </div>
        );
      })}
    </div>
  );
}

export function DeskToolbar({ children }: { children: ReactNode }) {
  return <div className="mp-desk-chrome-toolbar">{children}</div>;
}

export function DeskFormRow({ children }: { children: ReactNode }) {
  return <div className="mp-desk-chrome-form-row">{children}</div>;
}

export function DeskStack({ children }: { children: ReactNode }) {
  return <div className="mp-desk-chrome-stack">{children}</div>;
}
