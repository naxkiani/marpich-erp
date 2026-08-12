import { apiGet, apiPut, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type StockLevel = {
  id: string;
  sku: string;
  quantity_on_hand: string;
  quantity_reserved: string;
  quantity_available: string;
  updated_at?: string;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadInventorySession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchStockLevels(session: ApiSession): Promise<Page<StockLevel>> {
  return apiGet<Page<StockLevel>>("/api/v1/inventory/stock?limit=50", session);
}

export async function upsertStock(
  session: ApiSession,
  payload: { sku: string; quantity: string },
): Promise<StockLevel> {
  return apiPut<StockLevel>("/api/v1/inventory/stock", session, {
    sku: payload.sku,
    quantity: payload.quantity,
  });
}
