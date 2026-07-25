"""Tests for the bundled tariff dashboard frontend."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from custom_components.swiss_dynamic_tariffs.const import PANEL_COMPONENT_NAME, VERSION

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
  attachShadow() { return {}; }
};
global.ResizeObserver = class {
  observe() {}
  disconnect() {}
};
global.customElements = {
  elements: new Map(),
  get(name) { return this.elements.get(name); },
  define(name, value) { this.elements.set(name, value); },
};
global.window = {};
"""
        + source
        + """
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
}));
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
    }
