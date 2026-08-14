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
}: {
  items: Array<{ label: string; value: string | number }>;
}) {
  return (
    <div className="mp-desk-chrome-metrics" aria-label="Metrics">
      {items.map((item) => (
        <div key={item.label} className="mp-desk-chrome-metric">
          <span>{item.label}</span>
          <strong>{item.value}</strong>
        </div>
      ))}
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
