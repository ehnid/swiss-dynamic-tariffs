"""Tests for the bundled tariff dashboard frontend."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from custom_components.swiss_dynamic_tariffs.const import (
    DASHBOARD_CARD_TYPE,
    PANEL_COMPONENT_NAME,
    VERSION,
)

ROOT = Path(__file__).parents[1]
FRONTEND_PATH = (
    ROOT
    / "custom_components"
    / "swiss_dynamic_tariffs"
    / "frontend"
    / "swiss-dynamic-tariffs.js"
)


def test_frontend_and_panel_versions_match_manifest():
    """Keep cache-busting URLs and versioned panel elements synchronized."""

    source = FRONTEND_PATH.read_text(encoding="utf-8")

    assert f'const FRONTEND_VERSION = "{VERSION}";' in source
    assert PANEL_COMPONENT_NAME == (
        f"swiss-dynamic-tariffs-panel-{VERSION.replace('.', '-')}"
    )
    assert (
        f'const DASHBOARD_PANEL_TAG = "{DASHBOARD_CARD_TYPE.removeprefix("custom:")}";'
        in source
    )
    assert ".grid-line.zero-line" in source


def test_legacy_history_is_reconstructed_on_quarter_hour_grid(tmp_path):
    """Retain today's prices recorded before period attributes were introduced."""

    node = os.environ.get("NODE_BINARY") or shutil.which("node")
    if not node:
        pytest.skip("Node.js is not installed")

    source = FRONTEND_PATH.read_text(encoding="utf-8")
    runner = tmp_path / "frontend-history-test.cjs"
    runner.write_text(
        """
global.HTMLElement = class {
  attachShadow() {
    this.shadowRoot = {};
    return this.shadowRoot;
  }
};
global.ResizeObserver = class {
  observe() {}
  disconnect() {}
};
global.customElements = {
  elements: new Map(),
  constructors: new Set(),
  get(name) { return this.elements.get(name); },
  define(name, value) {
    if (this.constructors.has(value)) {
      throw new Error("Constructor already registered");
    }
    this.elements.set(name, value);
    this.constructors.add(value);
  },
};
global.window = {};
"""
        + source
        + """
(async () => {
Date.now = () => Date.parse("2026-01-15T12:07:00Z");
const entityId = "sensor.test_current_price";
const response = [[
  {
    entity_id: entityId,
    state: "0.10",
    attributes: {},
    last_updated: "2026-01-14T22:45:00Z",
  },
  {
    entity_id: entityId,
    state: "0.20",
    attributes: {},
    last_updated: "2026-01-15T07:15:04Z",
  },
  {
    entity_id: entityId,
    state: "0.30",
    attributes: {
      start: "2026-01-15T11:00:00Z",
      end: "2026-01-15T11:15:00Z",
    },
    last_updated: "2026-01-15T11:00:03Z",
  },
]];
const periods = parseHistoryPeriods(
  response,
  { electricity: entityId },
  {},
  "2026-01-15",
  "Europe/Zurich",
);
const priceAt = (timestamp) =>
  periods.find((period) => period.startTime === Date.parse(timestamp))
    ?.electricity;
const card = new SwissDynamicTariffsCard();
card._hass = { locale: { language: "en" } };
let dayClick;
let renderCount = 0;
const dayButton = {
  dataset: { dayOffset: "1" },
  disabled: false,
  addEventListener(type, callback) {
    if (type === "click") dayClick = callback;
  },
};
card.shadowRoot.querySelectorAll = () => [dayButton];
card._render = () => { renderCount += 1; };
card._bindDayNavigation();
dayClick();
const mobileDimensions = chartDimensions(360);
const desktopDimensions = chartDimensions(768);
const sharedPanel = new SwissDynamicTariffsPanel();
const sharedCardA = {};
const sharedCardB = {};
sharedPanel._cards = new Map([
  ["a", sharedCardA],
  ["b", sharedCardB],
]);
sharedPanel._updateSharedYAxis("a", { minimum: -0.021, maximum: 0.23 });
sharedPanel._updateSharedYAxis("b", { minimum: 0.04, maximum: 0.46 });
const generatedDashboard = await SwissDynamicTariffsDashboardStrategy.generate(
  {},
  {
    locale: { language: "en" },
    states: {
      "sensor.test_forecast": {
        entity_id: "sensor.test_forecast",
        attributes: {
          prices: [],
          available_from: "2026-01-15T12:15:00Z",
          available_until: "2026-01-16T00:00:00Z",
        },
      },
    },
  },
);
process.stdout.write(JSON.stringify({
  winterStart: new Date(
    calendarDateStart("2026-01-15", "Europe/Zurich"),
  ).toISOString(),
  summerStart: new Date(
    calendarDateStart("2026-07-15", "Europe/Zurich"),
  ).toISOString(),
  beforeChange: priceAt("2026-01-15T07:00:00Z"),
  afterChange: priceAt("2026-01-15T07:15:00Z"),
  exactPeriod: priceAt("2026-01-15T11:00:00Z"),
  axisPrice: card._formatAxisPrice(0.12345),
  separatePanelCard:
    customElements.get(CARD_TAG) !== customElements.get(PANEL_CARD_TAG),
  stableDashboardPanel:
    customElements.get(DASHBOARD_PANEL_TAG) !== undefined &&
    customElements.get(DASHBOARD_PANEL_TAG) !== customElements.get(PANEL_TAG) &&
    customElements.get(DASHBOARD_PANEL_TAG) !== customElements.get(CARD_TAG),
  mobileDimensions,
  desktopDimensions,
  desktopCardWidths: {
    referenceScreen: desktopCardWidth(1920),
    largerScreen: desktopCardWidth(2560),
    fallback: desktopCardWidth(undefined),
  },
  axes: {
    positive: priceAxisBounds([0.01, 0.27]),
    negative: priceAxisBounds([-0.121, 0.31]),
    exactNegativeStep: priceAxisBounds([-0.05, 0.1]),
    grid: priceGridTicks(-0.15, 0.4),
    shared: sharedPanel._sharedYAxis,
    firstCard: sharedCardA.sharedYAxis,
    secondCard: sharedCardB.sharedYAxis,
  },
  dashboardLayout: {
    viewType: generatedDashboard.views[0].type,
    cardType: generatedDashboard.views[0].cards[0].type,
  },
  textKeysMatch: Object.values(TEXT).every(
    (translation) =>
      JSON.stringify(Object.keys(translation).sort()) ===
      JSON.stringify(Object.keys(TEXT.en).sort()),
  ),
  localizedLegend: {
    de: TEXT.de.legend,
    en: TEXT.en.legend,
    fr: TEXT.fr.legend,
    it: TEXT.it.legend,
  },
  dayInteraction: {
    selectedOffset: card._selectedDayOffset,
    renderCount,
  },
}));
})();
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [node, str(runner)],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)

    assert data == {
        "winterStart": "2026-01-14T23:00:00.000Z",
        "summerStart": "2026-07-14T22:00:00.000Z",
        "beforeChange": 0.1,
        "afterChange": 0.2,
        "exactPeriod": 0.3,
        "axisPrice": "0.12",
        "separatePanelCard": True,
        "stableDashboardPanel": True,
        "mobileDimensions": {
            "compact": True,
            "width": 336,
            "height": 242,
            "plot": {"left": 62, "right": 12, "top": 24, "bottom": 54},
        },
        "desktopDimensions": {
            "compact": False,
            "width": 724,
            "height": 320,
            "plot": {"left": 78, "right": 20, "top": 24, "bottom": 58},
        },
        "desktopCardWidths": {
            "referenceScreen": 768,
            "largerScreen": 1024,
            "fallback": 480,
        },
        "axes": {
            "positive": {"minimum": 0, "maximum": 0.3},
            "negative": {"minimum": -0.15, "maximum": 0.4},
            "exactNegativeStep": {"minimum": -0.05, "maximum": 0.1},
            "grid": [-0.1, 0, 0.1, 0.2, 0.3, 0.4],
            "shared": {"minimum": -0.05, "maximum": 0.5},
            "firstCard": {"minimum": -0.05, "maximum": 0.5},
            "secondCard": {"minimum": -0.05, "maximum": 0.5},
        },
        "dashboardLayout": {
            "viewType": "panel",
            "cardType": "custom:swiss-dynamic-tariffs-panel-0-5-8",
        },
        "textKeysMatch": True,
        "localizedLegend": {
            "de": "Legende",
            "en": "Legend",
            "fr": "Légende",
            "it": "Legenda",
        },
        "dayInteraction": {"selectedOffset": 1, "renderCount": 1},
    }
