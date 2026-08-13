"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast,
  DeskAlert,
  DeskChrome,
  useLocale} from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { fetchStockLevels, upsertStock, type StockLevel } from "@/lib/inventoryClient";

export function InventoryDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [stock, setStock] = useState<StockLevel[]>([]);
  const [sku, setSku] = useState("SALES-STD");
  const [quantity, setQuantity] = useState("100");

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const page = await fetchStockLevels(session);
      setStock(page.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load Inventory");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onUpsert() {
    if (!session) return;
    try {
      await upsertStock(session, { sku, quantity });
      push({ message: "Stock saved" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Save failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="Inventory" subtitle="Stock levels">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Inventory" subtitle="Stock levels">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage stock levels."
          action={
            <Link className="mp-btn mp-btn-accent" href="/login">
              Sign in
            </Link>
          }
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Inventory" subtitle="Stock · Reservations (CAP-ENT-042)">
      <DeskChrome>
      <ProgressBar value={progress} />
      {error ? <DeskAlert>{error}</DeskAlert> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Placed sales orders reserve SKU <code>SALES-STD</code>.{" "}
        <Link href="/sales">Open Sales</Link>
      </p>

      <section className="mp-stack" style={{ marginBlock: "1rem" }}>
        <h2>Seed / set stock</h2>
        <div className="mp-form-row">
          <input className="mp-input" value={sku} onChange={(e) => setSku(e.target.value)} placeholder="SKU" />
          <input
            className="mp-input"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            placeholder="On hand"
          />
          <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onUpsert()}>
            Save stock
          </button>
        </div>
      </section>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : stock.length === 0 ? (
        <EmptyState title="No stock" description="Seed a SKU before converting sales orders." />
      ) : (
        <DataTable
          columns={[
            { key: "sku", header: "SKU" },
            { key: "quantity_on_hand", header: "On hand" },
            { key: "quantity_reserved", header: "Reserved" },
            { key: "quantity_available", header: "Available" },
          ]}
          rows={stock}
        />
      )}
          </DeskChrome>
    </PageLayout>
  );
}
