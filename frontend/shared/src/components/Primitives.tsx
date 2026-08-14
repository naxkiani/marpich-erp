"use client";

import { clsx } from "clsx";

export type BreadcrumbItem = { label: string; href?: string };

export function Breadcrumb({ items = [] }: { items?: BreadcrumbItem[] }) {
  const crumbs = items ?? [];
  if (crumbs.length === 0) return null;

  return (
    <nav aria-label="Breadcrumb" className="mp-breadcrumb">
      <ol>
        {crumbs.map((item, i) => (
          <li key={`${item.label}-${i}`}>
            {item.href && i < crumbs.length - 1 ? (
              <a href={item.href}>{item.label}</a>
            ) : (
              <span aria-current={i === crumbs.length - 1 ? "page" : undefined}>
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
        <div className="mp-progress-fill mp-progress-fill--gold" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export type StepProgressItem = string | { id?: string; label: string };

function resolveStep(step: StepProgressItem, index: number): { key: string; label: string } {
  if (typeof step === "string") {
    return { key: `step-${index}-${step}`, label: step };
  }
  const label = typeof step?.label === "string" ? step.label : String(step ?? "");
  const id = typeof step?.id === "string" && step.id ? step.id : `idx-${index}`;
  return { key: `step-${id}`, label };
}

export function StepProgress({
  steps,
  current,
}: {
  steps: StepProgressItem[];
  current: number;
}) {
  return (
    <ol className="mp-step-progress">
      {steps.map((step, i) => {
        const resolved = resolveStep(step, i);
        return (
          <li key={resolved.key} className={clsx(i <= current && "mp-step-active")}>
            <span className="mp-step-index">{i + 1}</span>
            <span>{resolved.label}</span>
          </li>
        );
      })}
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
