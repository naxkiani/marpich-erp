"use client";

import { clsx } from "clsx";
import { useMemo, useState } from "react";

export type Column<T> = {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
};

export function DataTable<T extends Record<string, unknown>>({
  columns,
  rows,
  selectable,
  onSelectionChange,
}: {
  columns: Column<T>[];
  rows: T[];
  selectable?: boolean;
  onSelectionChange?: (ids: string[]) => void;
}) {
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const sorted = useMemo(() => {
    if (!sortKey) return rows;
    return [...rows].sort((a, b) => {
      const av = String(a[sortKey] ?? "");
      const bv = String(b[sortKey] ?? "");
      return sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
    });
  }, [rows, sortKey, sortDir]);

  const toggleSort = (key: string) => {
    if (sortKey === key) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const toggleRow = (id: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      onSelectionChange?.([...next]);
      return next;
    });
  };

  return (
    <div className="mp-table-wrap">
      <table className="mp-table">
        <thead>
          <tr>
            {selectable ? <th scope="col" className="mp-table-check" /> : null}
            {columns.map((col) => (
              <th key={col.key} scope="col">
                {col.sortable ? (
                  <button type="button" className="mp-table-sort" onClick={() => toggleSort(col.key)}>
                    {col.header}
                    {sortKey === col.key ? (sortDir === "asc" ? " ↑" : " ↓") : null}
                  </button>
                ) : (
                  col.header
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, i) => {
            const id = String(row.id ?? i);
            return (
              <tr key={id} className={clsx(selected.has(id) && "mp-table-row-selected")}>
                {selectable ? (
                  <td>
                    <input
                      type="checkbox"
                      checked={selected.has(id)}
                      onChange={() => toggleRow(id)}
                      aria-label={`Select row ${id}`}
                    />
                  </td>
                ) : null}
                {columns.map((col) => (
                  <td key={col.key}>
                    {col.render ? col.render(row) : String(row[col.key] ?? "")}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export type FormFieldConfig = {
  name: string;
  label: string;
  type?: "text" | "email" | "number" | "select";
  required?: boolean;
  options?: { value: string; label: string }[];
  help?: string;
};

export function SmartForm({
  fields,
  initialValues,
  onSubmit,
  autosave,
  onAutosave,
}: {
  fields: FormFieldConfig[];
  initialValues: Record<string, string>;
  onSubmit: (values: Record<string, string>) => void;
  autosave?: boolean;
  onAutosave?: (values: Record<string, string>) => void;
}) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const next: Record<string, string> = {};
    for (const f of fields) {
      if (f.required && !values[f.name]?.trim()) next[f.name] = `${f.label} is required`;
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const update = (name: string, value: string) => {
    setValues((v) => {
      const next = { ...v, [name]: value };
      if (autosave && onAutosave) onAutosave(next);
      return next;
    });
  };

  return (
    <form
      className="mp-form"
      onSubmit={(e) => {
        e.preventDefault();
        if (validate()) onSubmit(values);
      }}
    >
      {fields.map((field) => (
        <div key={field.name} className="mp-field">
          <label htmlFor={field.name}>
            {field.label}
            {field.required ? " *" : null}
          </label>
          {field.type === "select" ? (
            <select
              id={field.name}
              className="mp-select"
              value={values[field.name] ?? ""}
              onChange={(e) => update(field.name, e.target.value)}
            >
              {field.options?.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          ) : (
            <input
              id={field.name}
              className="mp-input"
              type={field.type ?? "text"}
              value={values[field.name] ?? ""}
              onChange={(e) => update(field.name, e.target.value)}
              aria-invalid={!!errors[field.name]}
              aria-describedby={field.help ? `${field.name}-help` : undefined}
            />
          )}
          {field.help ? (
            <span id={`${field.name}-help`} className="mp-field-help">
              {field.help}
            </span>
          ) : null}
          {errors[field.name] ? (
            <span className="mp-field-error" role="alert">
              {errors[field.name]}
            </span>
          ) : null}
        </div>
      ))}
      <button type="submit" className="mp-btn mp-btn-primary">
        Save
      </button>
    </form>
  );
}

export function AdvancedFilterBar({
  filters,
  onChange,
}: {
  filters: { id: string; label: string; type: "text" | "date" }[];
  onChange: (values: Record<string, string>) => void;
}) {
  const [values, setValues] = useState<Record<string, string>>({});

  const update = (id: string, value: string) => {
    setValues((prev) => {
      const next = { ...prev, [id]: value };
      onChange(next);
      return next;
    });
  };

  return (
    <div className="mp-filter-bar" role="search">
      {filters.map((f) => (
        <label key={f.id} className="mp-filter-item">
          <span>{f.label}</span>
          <input
            className="mp-input"
            type={f.type === "date" ? "date" : "text"}
            value={values[f.id] ?? ""}
            onChange={(e) => update(f.id, e.target.value)}
          />
        </label>
      ))}
    </div>
  );
}

export function ExportButton({
  label = "Export",
  rows,
  filename = "export.csv",
}: {
  label?: string;
  rows: Record<string, unknown>[];
  filename?: string;
}) {
  const exportCsv = () => {
    if (rows.length === 0) return;
    const keys = Object.keys(rows[0]!);
    const csv = [keys.join(","), ...rows.map((r) => keys.map((k) => JSON.stringify(r[k] ?? "")).join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <button type="button" className="mp-btn" onClick={exportCsv}>
      {label}
    </button>
  );
}

export function ImportDialog({
  label = "Import",
  onImport,
}: {
  label?: string;
  onImport: (rows: Record<string, string>[]) => void;
}) {
  const [open, setOpen] = useState(false);

  const onFile = async (file: File) => {
    const text = await file.text();
    const lines = text.trim().split("\n");
    const headers = lines[0]?.split(",") ?? [];
    const rows = lines.slice(1).map((line) => {
      const cols = line.split(",");
      return Object.fromEntries(headers.map((h, i) => [h.trim(), cols[i]?.trim() ?? ""]));
    });
    onImport(rows);
    setOpen(false);
  };

  return (
    <>
      <button type="button" className="mp-btn" onClick={() => setOpen(true)}>
        {label}
      </button>
      {open ? (
        <div className="mp-overlay" onClick={() => setOpen(false)}>
          <div className="mp-panel mp-animate-in" onClick={(e) => e.stopPropagation()}>
            <header>Import CSV</header>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) void onFile(f);
              }}
            />
          </div>
        </div>
      ) : null}
    </>
  );
}

export function PrintButton({ label = "Print" }: { label?: string }) {
  return (
    <button type="button" className="mp-btn" onClick={() => window.print()}>
      {label}
    </button>
  );
}
