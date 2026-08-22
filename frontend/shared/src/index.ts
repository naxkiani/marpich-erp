export { ThemeProvider, ThemeToggle, useTheme, type Theme } from "./theme/ThemeProvider";
export {
  LocaleProvider,
  DirectionProvider,
  LocaleSwitcher,
  useLocale,
  type Locale,
} from "./i18n/LocaleProvider";

export {
  API_URL,
  BFF_API_PREFIX,
  getPlatformAuthHeaders,
  loadPlatformSession,
  platformApiUrl,
  PLATFORM_SESSION_KEY,
  type PlatformSession,
} from "./platform/session";
export {
  APPLICATION_NAV,
  MODULE_LAUNCH_CATALOG,
  NAV_GROUP_LABEL_KEYS,
  NAV_GROUP_LABELS,
  NAV_GROUP_ORDER,
  PACK_LAUNCH_CATALOG,
  activatableModulesForPack,
  canAccessApp,
  filterApplicationNav,
  groupedApplicationNav,
  isModuleEnabledForApp,
  isPackComingSoon,
  launchEntryForModule,
  launchHrefForModule,
  launchHrefForPack,
  packLaunchEntry,
  searchApplicationNav,
  type AppNavItem,
  type ModuleLaunchEntry,
  type ModuleLaunchStatus,
  type NavGroupId,
  type PackLaunchEntry,
  type PermissionPredicate,
} from "./platform/applicationRegistry";
export {
  TenantModulesProvider,
  useTenantModules,
  type TenantModulesSnapshot,
} from "./platform/TenantModulesProvider";
export {
  matchesAnyPermission,
  matchesPermission,
} from "./platform/permissions";
export {
  PRODUCT_ENTITLEMENT_PATH,
  clientEntitlementIsNotAuthoritative,
  type EntitlementStatus,
} from "./platform/productEntitlement";
export {
  DeskAlert,
  DeskChrome,
  DeskFormRow,
  DeskMetrics,
  DeskPanel,
  DeskStack,
  DeskToolbar,
  KpiStrip,
  mapDeskStatsToKpiItems,
  type KpiStripItem,
} from "./components/DeskChrome";

export { CommandPalette, type CommandItem } from "./components/CommandPalette";
export { GlobalSearch } from "./components/GlobalSearch";
export {
  NotificationCenter,
  HelpButton,
  AIAssistantPanel,
} from "./components/ShellWidgets";
export {
  KeyboardShortcutsDialog,
  useGlobalKeyboardShortcuts,
  useAutosave,
} from "./components/KeyboardShortcutsDialog";
export { ToastProvider, UndoToast, useToast } from "./components/UndoToast";
export {
  Breadcrumb,
  Skeleton,
  SkeletonTable,
  ProgressBar,
  StepProgress,
  EmptyState,
  type BreadcrumbItem,
} from "./components/Primitives";
export {
  DataTable,
  SmartForm,
  AdvancedFilterBar,
  ExportButton,
  ImportDialog,
  PrintButton,
  type Column,
  type FormFieldConfig,
} from "./components/DataUi";
