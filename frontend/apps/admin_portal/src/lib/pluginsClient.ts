import {
  type ApiSession,
  apiDelete,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadPluginsSession,
  saveSession as savePluginsSession,
} from "./clientAuth";

export type { ApiSession };

export const loginPluginsSession = createClientLogin("Plugin Marketplace Admin");
export { loadPluginsSession, savePluginsSession };

export type PluginListing = {
  plugin_id: string;
  plugin_type: string;
  display_name: string;
  description: string;
  publisher_id: string;
  publisher_name: string;
  current_version: string;
  permissions: string[];
  extension_points: string[];
  sandbox_profile: string;
  trust_level: string;
  status: string;
  version_count: number;
};

export type PluginInstallation = {
  plugin_id: string;
  installed_version: string;
  enabled: boolean;
  granted_permissions: string[];
  sandbox_profile: string;
};

export type MarketplaceDashboard = {
  listings_by_type: Record<string, number>;
  installed_count: number;
  pending_submissions: number;
  sandbox_violations_24h: number;
  top_publishers: Array<{ publisher: string; listings: number; installs: number }>;
  upgrade_backlog: Array<{
    plugin_id: string;
    current_version: string;
    latest_version: string;
  }>;
};

export async function fetchMarketplaceDashboard(session: ApiSession): Promise<MarketplaceDashboard> {
  return apiGet("/api/v1/plugins/marketplace/dashboard", session);
}

export async function fetchMarketplaceListings(session: ApiSession): Promise<PluginListing[]> {
  return apiGet("/api/v1/plugins/marketplace/listings", session);
}

export async function fetchInstalledPlugins(session: ApiSession): Promise<PluginInstallation[]> {
  return apiGet("/api/v1/plugins/installed", session);
}

export async function installPlugin(
  session: ApiSession,
  pluginId: string,
  grantedPermissions: string[],
): Promise<PluginInstallation> {
  return apiPost(`/api/v1/plugins/${encodeURIComponent(pluginId)}/install`, session, {
    granted_permissions: grantedPermissions,
    config: {},
  });
}

export async function uninstallPlugin(session: ApiSession, pluginId: string): Promise<unknown> {
  return apiDelete(`/api/v1/plugins/${encodeURIComponent(pluginId)}/install`, session);
}

export async function invokePlugin(
  session: ApiSession,
  pluginId: string,
  extensionPoint: string,
  payload: Record<string, unknown> = {},
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/plugins/invoke", session, {
    plugin_id: pluginId,
    extension_point: extensionPoint,
    payload,
  });
}

export async function verifyPlugin(
  session: ApiSession,
  pluginId: string,
): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/plugins/${encodeURIComponent(pluginId)}/verify`, session);
}
