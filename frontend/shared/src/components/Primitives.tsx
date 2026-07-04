"use client";

import { clsx } from "clsx";

export type BreadcrumbItem = { label: string; href?: string };

export function Breadcrumb({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav aria-label="Breadcrumb" className="mp-breadcrumb">
      <ol>
        {items.map((item, i) => (
          <li key={`${item.label}-${i}`}>
            {item.href && i < items.length - 1 ? (
              <a href={item.href}>{item.label}</a>
            ) : (
              <span aria-current={i === items.length - 1 ? "page" : undefined}>
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={clsx("mp-skeleton", className)} aria-hidden />;
}

export function SkeletonTable({ rows = 5, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="mp-skeleton-table" role="status" aria-label="Loading">
      {Array.from({ length: rows }).map((_, r) => (
        <div key={r} className="mp-skeleton-row">
          {Array.from({ length: cols }).map((__, c) => (
            <Skeleton key={c} className="mp-skeleton-cell" />
          ))}
        </div>
      ))}
    </div>
  );
}

export function ProgressBar({ value, label }: { value: number; label?: string }) {
  const pct = Math.min(100, Math.max(0, value));
  return (
    <div className="mp-progress" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
      {label ? <span className="mp-progress-label">{label}</span> : null}
      <div className="mp-progress-track">
        <div className="mp-progress-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export function StepProgress({ steps, current }: { steps: string[]; current: number }) {
  return (
    <ol className="mp-step-progress">
      {steps.map((step, i) => (
        <li key={step} className={clsx(i <= current && "mp-step-active")}>
          <span className="mp-step-index">{i + 1}</span>
          <span>{step}</span>
        </li>
      ))}
    </ol>
  );
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="mp-empty mp-animate-in">
      <div className="mp-empty-icon" aria-hidden>
        ◌
      </div>
      <h3>{title}</h3>
      {description ? <p>{description}</p> : null}
      {action}
    </div>
  );
}
