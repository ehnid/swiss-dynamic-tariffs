# Swiss Dynamic Tariffs

<p align="center">
  <img src="https://raw.githubusercontent.com/ehnid/swiss-dynamic-tariffs/main/custom_components/swiss_dynamic_tariffs/brand/logo.png" alt="Swiss Dynamic Tariffs logo" width="220">
</p>

[![GitHub release](https://img.shields.io/github/v/release/ehnid/swiss-dynamic-tariffs)](https://github.com/ehnid/swiss-dynamic-tariffs/releases)
[![Tests](https://github.com/ehnid/swiss-dynamic-tariffs/actions/workflows/tests.yaml/badge.svg)](https://github.com/ehnid/swiss-dynamic-tariffs/actions/workflows/tests.yaml)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Swiss Dynamic Tariffs brings quarter-hourly prices from supported Swiss energy
providers into Home Assistant. It creates translated sensors and a
user-managed, interactive tariff dashboard without requiring YAML or an
additional chart card.

## Motivation

The project was started by an electrical engineer as a practical way to
experiment with home automation and to support the shift towards dynamic
electricity prices in Switzerland. Making tariff signals visible and usable in
Home Assistant should help households move flexible consumption away from peak
periods.

The initiator's engineering conviction is that widespread, tariff-driven load
shifting can avoid or defer a substantial share of grid reinforcement,
particularly on Swiss distribution grid levels 5 and 7. This is the motivation
behind the project rather than a quantified promise: the actual effect depends
on adoption, local grid constraints, simultaneous behaviour and network
planning.

## Features

- Multiple tariff options from the same provider can be configured separately.
- Current, next, minimum, maximum and average price sensors are created for
  every available price component.
- A forecast sensor exposes every quarter-hour period published by the provider.
- The user-managed dashboard combines the complete provider-published window
  with Recorder values that are no longer available from the provider.
- Day buttons cover every available forecast date, including data beyond
  24 hours.
- The compact chart includes labelled axes, values on hover and an expandable
  quarter-hour table.
- Sensor and dashboard text is available in German, English, French and Italian.

## Supported tariffs

These names are shown in the Home Assistant configuration flow:

| Flow option                                    | Price components                          |
| ---------------------------------------------- | ----------------------------------------- |
| BKW – dynamische Einspeisevergütung            | Feed-in                                   |
| CKW – Home Dynamic                             | Electricity, grid usage, grid, integrated |
| CKW – Business Dynamic                         | Electricity, grid usage, grid, integrated |
| Groupe E – Vario                               | Grid, integrated                          |
| Primeo Energie – Netz dynamisch                | Electricity, grid usage, grid, integrated |
| Primeo Energie – Netz dynamisch (AVAG)         | Electricity, grid usage, grid, integrated |
| Primeo Energie – Netz dynamisch (ELAG)         | Electricity, grid usage, grid, integrated |
| EKZ – Energie Dynamisch + Netz 400D            | Integrated                                |
| EKZ Einsiedeln – Energie Dynamisch + Netz 400D | Integrated                                |

No tariff is preselected. The user must explicitly choose the required
provider/tariff combination.

The amount and horizon of data are controlled by each provider. The integration
shows all periods returned by the provider and does not invent missing prices.

## Installation

### HACS

[![Open your Home Assistant instance and add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ehnid&repository=swiss-dynamic-tariffs&category=integration)

1. Add this repository to HACS as an integration.
2. Install **Swiss Dynamic Tariffs**.
3. Restart Home Assistant.
4. Open **Settings → Devices & services → Add integration**.
5. Search for **Swiss Dynamic Tariffs** and select a tariff.

Tagged releases contain the `swiss_dynamic_tariffs.zip` package expected by
HACS.

### Manual installation

1. Copy `custom_components/swiss_dynamic_tariffs` into the
   `custom_components` directory of your Home Assistant configuration.
2. Restart Home Assistant.
3. Add **Swiss Dynamic Tariffs** under **Settings → Devices & services**.

## Sensors

For every price component supported by a tariff, the integration creates:

| Sensor                      | Meaning                                                   |
| --------------------------- | --------------------------------------------------------- |
| Current                     | Price of the active quarter-hour period.                  |
| Next                        | Price of the next published quarter-hour period.          |
| Cheapest quarter-hour       | Lowest price among periods that have not ended.           |
| Most expensive quarter-hour | Highest price among periods that have not ended.          |
| Average                     | Average across all published periods that have not ended. |

One additional **Tariff forecast** sensor contains the complete period window
currently published by the provider. This includes earlier periods of the
current day when the provider still returns them:

- its state is the total published duration in hours;
- `prices` contains the quarter-hour periods;
- each period contains ISO 8601 `start` and `end` timestamps;
- `available_from`, `available_until` and `period_count` summarize the range;
- prices use CHF/kWh.

### Price components

| API term      | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| `electricity` | Energy-only price for electricity consumed from the grid.    |
| `feed_in`     | Compensation for electricity exported to the grid.           |
| `grid_usage`  | Dynamic network usage charge without the energy price.       |
| `grid`        | Network charge including provider-reported grid levies.      |
| `integrated`  | Provider-specific combined price, normally energy plus grid. |

Fixed charges, taxes and VAT depend on the provider response and may not be
included. Home Assistant translates display names. Integration unique IDs stay
stable, while users may rename entity IDs normally.

## Dashboard

After the first tariff is configured, **Swiss Dynamic Tariffs** is created as a
regular Home Assistant storage dashboard and added to the sidebar. It appears
under **Settings → Dashboards**, where users can change its title, icon,
visibility and order or delete it. Its stored layout uses a regular bundled
card rather than depending on Lovelace strategy registration, and it contains
one tariff frame for every configured forecast.

The integration creates this dashboard only once. If a user deletes it, the
integration respects that decision and does not recreate it after a restart.
An unchanged strategy-only dashboard created by version 0.5.6 is migrated to
the regular bundled panel card automatically during the next restart. User-edited
dashboard content is never replaced.
To restore it later, add a dashboard manually and select the
**Swiss Dynamic Tariffs** Community strategy.

Each card provides:

- a responsive tariff frame whose desktop maximum is 40% of the current screen
  width and which uses the full available width on phones;
- a chart that scales with its tariff frame instead of using a fixed size;
- today's recorded prices up to the current quarter-hour;
- all currently published future periods;
- one-click navigation through every available forecast day;
- minimum, maximum and current/next values;
- a current-time marker, Y-axis labels with two decimal places and exact values
  on hover;
- one shared Y-axis range across all visible tariff graphs, with a zero-based
  scale unless negative prices require additional space;
- 10-rappen grid intervals from zero and a highlighted zero line;
- an expandable table that remains open during data refreshes.

Today is selected initially. The selection remains unchanged during updates. If
there are no values for the selected day, the card reports this instead of
silently switching dates.

### Historical values

The provider-published window is the first source for today's past values. This
directly preserves complete Primeo Energie, AVAG and ELAG days while their API
continues to return them. If a provider has already removed an earlier period,
the card reads Home Assistant's history for the matching **Current price**
sensors and combines those records with the published window by exact start/end
timestamp. Provider values take precedence where both sources cover a period.

States recorded by releases before 0.5.0 do not contain exact tariff-period
attributes. The dashboard reconstructs those older values from their Recorder
timestamps on a quarter-hour grid; newer exact period boundaries take
precedence wherever available.

This requires Home Assistant Recorder/History to record those sensors. Without
history data, the card still displays every period currently supplied by the
provider.

From version 0.5.3, the current-price sensors advance after every scheduled
15-minute refresh even if the provider returns an unchanged list or two
consecutive periods have the same price. This gives Recorder one state with
exact boundaries per quarter-hour. A gap can be recovered while the provider
still publishes that period; after it disappears from the source, Recorder is
the only historical source.

### Adding the card elsewhere

Add a card by entity and choose a **Tariff forecast** sensor. On supported Home
Assistant versions, the card picker suggests **Swiss Dynamic Tariffs – Tariff
forecast** automatically. The **Swiss Dynamic Tariffs** Community dashboard
strategy is also available under **Settings → Dashboards → Add dashboard**.

## Data behaviour and limitations

- Updates run every 15 minutes.
- Provider timestamps are retained with their timezone information.
- BKW may switch its endpoint to the newly published day. The integration keeps
  already fetched, not-yet-ended periods so the active price does not vanish.
- A provider may publish only tomorrow's values or temporarily return no data.
- Historical chart values are limited by the user's Recorder retention and
  exclusion settings.

## Troubleshooting

### A dashboard update is not visible

Update the integration in HACS and restart Home Assistant. The dashboard's
responsive overview card uses a release-specific component name and frontend
cache key. A manually added card may additionally require a browser refresh or
a reload of the Home Assistant Companion app because browsers cannot replace an
already registered custom element in a running page.

### No past values are shown

Check that Recorder/History is enabled and that the corresponding **Current
price** sensors are not excluded. History can only be displayed after Home
Assistant has recorded sensor states.

### No later day button is shown

The integration creates one button per date actually published by the provider.
If only today and tomorrow are returned, no additional date can be displayed.

## Development documentation

- [Contributing](CONTRIBUTING.md)
- [Architecture](docs/architecture.md)
- [Architecture decision: dashboard time series](docs/adr/0001-dashboard-time-series.md)
- [Architecture decision: user-managed dashboard](docs/adr/0002-user-managed-dashboard.md)

## License

Swiss Dynamic Tariffs is distributed under the [MIT License](LICENSE).
