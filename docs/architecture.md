# Architecture

This document describes the stable structure and data contracts of Swiss
Dynamic Tariffs. Design choices and their alternatives are recorded separately
under [`docs/adr`](adr/).

## Project intent

The integration exists to make Swiss dynamic tariffs usable for practical home
automation and load-shifting experiments. Its motivating engineering thesis is
that sufficiently broad, price-responsive consumption can lower coincident
peaks and avoid or defer substantial reinforcement of distribution grid levels
5 and 7.

The software cannot measure or guarantee that system-level outcome. Adoption,
local bottlenecks, simultaneous customer behaviour and the network operator's
planning criteria remain outside the integration. The technical design
therefore concentrates on a narrower contribution: exposing provider data
faithfully, transparently and in a form that Home Assistant automations can
use.

## Responsibilities

The integration has three boundaries:

1. **Providers** translate external EVU APIs into a common tariff model.
2. **Home Assistant entities** expose current, derived and forecast values.
3. **The frontend** presents recorded and forecast values without changing the
   tariff data.

Keeping these boundaries separate allows a provider to be added without
rewriting the coordinator, sensors or dashboard.

```mermaid
flowchart LR
    EVU["EVU API"] --> Provider["TariffProvider"]
    Provider --> Model["TariffPeriod list"]
    Model --> Coordinator["DataUpdateCoordinator"]
    Coordinator --> Sensors["Price sensors"]
    Coordinator --> Forecast["Forecast sensor"]
    Sensors --> Recorder["Home Assistant Recorder"]
    Recorder --> Card["Tariff dashboard card"]
    Forecast --> Card
```

## Backend data flow

### Provider layer

`providers/base.py` defines the `TariffProvider` contract. Implementations:

- perform asynchronous network requests;
- parse provider-specific payloads;
- return timezone-aware `TariffPeriod` objects;
- populate only price components supplied by the provider;
- express prices in CHF/kWh.

`providers/registry.py` is the single source of truth for configuration-flow
options. A tariff variant gets its own `TariffOption`, even when it shares a
provider implementation with other variants.

### Common model

`models.py` defines `TariffPeriod`. Each period has an exact `start`, `end` and
optional values for:

- `electricity`;
- `feed_in`;
- `grid_usage`;
- `grid`;
- `integrated`.

Missing components remain `None`. They are never inferred from unrelated
values.

### Coordinator

`coordinator.py` refreshes provider data every 15 minutes and supplies all
entities from one cached response.

New provider data is merged with previously fetched periods that have not
ended. This specifically prevents the active BKW period from disappearing when
the endpoint switches to a newly published day. Expired periods are not kept in
the coordinator; historical retention belongs to Home Assistant Recorder.

Derived minimum, maximum and average values use periods that have not ended, so
their results remain actionable.

## Entity contracts

`sensor.py` creates five sensors for every component supported by the provider:

- current;
- next;
- minimum;
- maximum;
- average.

Unique IDs contain the config-entry ID, component and sensor role. Existing
unique IDs are a compatibility contract and must not be renamed.

Price sensor attributes include:

| Attribute          | Purpose                                                     |
| ------------------ | ----------------------------------------------------------- |
| `start`, `end`     | Exact period represented by the state, when applicable.     |
| `tariff_component` | Component represented by the entity.                        |
| `tariff_role`      | Current, next, minimum, maximum or average role.            |
| `tariff_entry_id`  | Stable link between entities belonging to one tariff entry. |

The forecast sensor exposes all future periods under `prices`. Its state is the
sum of their durations in hours. `tariff_entry_id` links it to the corresponding
current-price sensors without depending on user-editable entity IDs or names.

The linking attributes are intentionally data, not presentation: the frontend
can discover renamed entities while provider and entity code remain unaware of
dashboard layout.

## Frontend data flow

The bundled JavaScript registers:

- a custom tariff card;
- the automatic sidebar panel;
- a dashboard strategy;
- card-picker metadata.

For each card:

1. Forecast periods are parsed from the forecast sensor.
2. Current-price sensors belonging to the same `tariff_entry_id` are found.
3. Home Assistant History is queried for the current day.
4. Historical states with recorded `start`/`end` attributes retain those exact
   boundaries.
5. Older states without period attributes are expanded from their Recorder
   timestamps onto the quarter-hour grid. This preserves history written before
   the linkage attributes were introduced in version 0.5.0.
6. Exact history and forecast periods are merged by start/end timestamp.
7. The result is split into calendar days in the configured Home Assistant
   timezone.

The later data source wins during a merge. Forecast data is applied after
history, making the latest provider payload authoritative if both sources cover
the same period.

History loading is cached by date, entity ID and current period start. This
avoids a Recorder query for every Home Assistant state refresh while ensuring a
new query occurs when the active quarter-hour changes.

Although a provider may return the same full tariff list throughout the day,
the coordinator notifies its sensor listeners after every scheduled 15-minute
refresh. The current-price sensor is time-dependent: its value and exact
`start`/`end` attributes must advance to the active period even when the fetched
list compares equal. Recorder can therefore retain every quarter-hour,
including consecutive periods with identical prices.

History is optional. If the endpoint is unavailable or Recorder excludes the
current-price sensors, the card continues with forecast data only.

See
[ADR 0001: Dashboard time-series composition](adr/0001-dashboard-time-series.md)
for the rationale and alternatives.

## Time and forecast horizon

All comparisons use absolute timestamps. Calendar grouping and labels use
Home Assistant's configured timezone.

Today and tomorrow are always available as navigation choices. Additional
buttons are created for every further date present in the provider data; there
is no hard-coded 24-hour forecast limit.

The automatic panel caps each complete tariff card—not just its SVG—at 40% of
`window.screen.width` on desktop. The limit therefore follows the user's screen,
not the width of the Home Assistant content frame. On the 1920 × 1080 reference
screen this is 768 pixels. If the browser window is narrowed, that same maximum
occupies a progressively larger proportion of the window. Cards wrap when
several tariffs are configured. At viewport widths of 800 pixels or less, every
card uses the full available panel width.

The SVG has no fixed CSS width or height. Its logical view box is recalculated
from the measured card width, and its height follows a bounded aspect ratio.
This keeps text and touch targets legible on phones without letting a desktop
chart dominate the page. `ResizeObserver` follows orientation and layout
changes; older WebViews receive a one-time post-attachment measurement instead.
Y-axis tick labels use exactly two decimal places; tooltips and table cells
retain the provider precision.

## Frontend state preservation

The card is re-rendered when Home Assistant state changes. User interaction is
stored on the card instance:

- selected day;
- expanded/collapsed table state.

These values are read before replacing the shadow DOM and applied to the new
markup, preventing automatic updates from resetting the interface.

## Error handling

- Provider failures become `UpdateFailed` and preserve coordinator semantics.
- Initial provider failures raise `ConfigEntryNotReady`.
- A missing History response affects only past chart values.
- Missing values for a selected day produce an explicit empty state.
- Unsupported price components are omitted rather than displayed as zero.

## Frontend delivery and caching

The JavaScript file is served through Home Assistant's static-path support. The
query-string cache key is read from `manifest.json`, so every integration
version loads a matching frontend bundle.

The automatic sidebar panel and its internal card also use a component name
derived from that version. Browsers cannot redefine an existing custom element,
so versioning the element prevents a Home Assistant reconnect from silently
retaining the previous graph implementation. The public custom-card tag remains
stable for Lovelace compatibility and may require a page reload after an
upgrade.

The public card and versioned internal card must use distinct JavaScript
constructors. The Custom Elements registry rejects registering one constructor
under two names; violating this rule aborts module evaluation and leaves a fresh
panel blank. The internal card therefore uses a dedicated subclass even though
it shares all behaviour.

The manifest version, JavaScript `FRONTEND_VERSION` and panel component name
must be changed together for each published frontend change. A regression test
enforces this contract and emulates the browser's constructor-uniqueness rule.

## Validation

The required local checks are:

```bash
pre-commit run --all-files
pytest --cov=custom_components.swiss_dynamic_tariffs
node --check custom_components/swiss_dynamic_tariffs/frontend/swiss-dynamic-tariffs.js
```

GitHub Actions additionally runs HACS and Hassfest validation. A `v*` tag
triggers the release workflow, which verifies the tag/version match and builds
the HACS ZIP.
