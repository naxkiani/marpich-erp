# Marpich Plugin SDK

Official SDK for building third-party Marpich plugins.

**Canonical docs:** [ENTERPRISE_PLUGIN_PLATFORM.md](../../docs/architecture/ENTERPRISE_PLUGIN_PLATFORM.md)  
**Manifest schema:** [PLUGIN_MANIFEST.v1.json](../../docs/architecture/plugins/PLUGIN_MANIFEST.v1.json)  
**Marketplace:** [MARKETPLACE_ARCHITECTURE.md](../../docs/architecture/plugins/MARKETPLACE_ARCHITECTURE.md)

---

## Plugin types

| Type | Extension point |
|------|-----------------|
| `module` | `platform.module.register` |
| `widget` | `ui.dashboard.widget` |
| `report` | `analytics.report.template` |
| `dashboard` | `analytics.dashboard.layout` |
| `theme` | `ui.theme.override` |
| `ai_skill` | `ai.skill.register` |
| `integration` | `integration.connector.register` |
| `workflow_extension` | `workflow.hook.register` |

---

## Quick start

```bash
# Scaffold a new plugin
npx @marpich/plugin-sdk init com.acme.sales-widget --type widget

# Validate manifest
npx @marpich/plugin-sdk validate

# Pack for submission
npx @marpich/plugin-sdk pack

# Sign (requires publisher key)
npx @marpich/plugin-sdk sign --key ~/.marpich/publisher.pem

# Submit to marketplace
npx @marpich/plugin-sdk publish --api https://api.marpich.dev
```

---

## Manifest example

```json
{
  "pluginId": "com.acme.sales-widget",
  "pluginVersion": "1.0.0",
  "pluginType": "widget",
  "displayName": "Acme Sales KPI",
  "publisher": { "id": "com.acme", "name": "Acme Corp" },
  "permissions": ["analytics.read", "sales.orders.read"],
  "extensionPoints": ["ui.dashboard.widget"],
  "sandbox": {
    "network": "deny",
    "filesystem": "read_only",
    "maxMemoryMb": 64
  },
  "signature": {
    "algorithm": "ed25519",
    "publicKeyFingerprint": "sha256:...",
    "packageChecksum": "sha256:..."
  }
}
```

---

## SDK packages

| Package | Language | Path |
|---------|----------|------|
| `@marpich/plugin-sdk` | TypeScript | `packages/plugin-sdk/` |
| `marpich-plugin-sdk` | Python | `packages/plugin-sdk/python/` |

---

## Requirements

Plugins **must** be:

- **Sandboxed** — runtime enforces profile from manifest
- **Versioned** — semver only; append-only history
- **Signed** — ed25519 or rsa-pss-sha256
- **Permission controlled** — declare + grant at install
- **Upgradeable** — compatible semver upgrade path

---

## Runtime integration

Host applications invoke plugins via `IPluginRuntime`:

```typescript
const widgets = await runtime.listExtensions({
  tenantId: 'acme',
  extensionPoint: 'ui.dashboard.widget',
});

const result = await runtime.invoke({
  tenantId: 'acme',
  pluginId: 'com.acme.sales-widget',
  extensionPoint: 'ui.dashboard.widget',
  payload: { dashboardId: 'executive' },
});
```

---

## CLI commands

| Command | Description |
|---------|-------------|
| `init` | Scaffold plugin project |
| `validate` | Validate manifest against schema |
| `pack` | Create distributable package |
| `sign` | Sign package with publisher key |
| `publish` | Submit to marketplace API |
| `test` | Run sandbox invocation tests |

---

## Forbidden

- Direct imports of platform internals
- Unsigned packages in production
- Exceeding declared sandbox limits
- Requesting undeclared permissions at runtime
