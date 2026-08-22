/** Home pulse helpers — fail-soft sync contract for the executive home. */
import assert from "node:assert/strict";
import test from "node:test";

import {
  homePulseHasDataQualityWarning,
  homePulseHasPartialErrors,
  type HomePulseResult,
} from "./homePulseClient";

function emptyPulse(errors: HomePulseResult["errors"] = {}): HomePulseResult {
  return {
    loadedAt: new Date().toISOString(),
    analytics: null,
    unreadNotifications: 0,
    recentNotifications: [],
    openTasks: 0,
    recentTasks: [],
    auditStats: null,
    recentAudit: [],
    errors,
  };
}

test("homePulseHasPartialErrors is false when clean", () => {
  assert.equal(homePulseHasPartialErrors(emptyPulse()), false);
  assert.equal(homePulseHasPartialErrors(null), false);
});

test("homePulseHasPartialErrors is true when any source failed", () => {
  assert.equal(
    homePulseHasPartialErrors(emptyPulse({ analytics: "forbidden" })),
    true,
  );
});

test("homePulseHasDataQualityWarning is true only for catalog-count warning", () => {
  assert.equal(homePulseHasDataQualityWarning(null), false);
  assert.equal(homePulseHasDataQualityWarning(emptyPulse()), false);
  const warned = emptyPulse();
  warned.analytics = {
    metrics_count: 0,
    dashboards_count: 0,
    alerts_count: 0,
    data_quality: { status: "DATA_QUALITY_WARNING" },
  };
  assert.equal(homePulseHasDataQualityWarning(warned), true);
});
