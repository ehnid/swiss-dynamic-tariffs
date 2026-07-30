# ADR 0001: Compose dashboard time series from Recorder and forecast data

- **Status:** Accepted
- **Date:** 2026-07-25
- **Scope:** Dashboard history, forecast horizon and entity linkage

## Context

Provider APIs primarily describe current and future tariffs. Some providers
stop returning periods that have already ended, and some switch entirely to a
newly published day. The forecast sensor therefore cannot reliably reconstruct
the beginning of the current day.

Users need one continuous daily view containing:

- prices already observed today;
- the active quarter-hour;
- every future period currently published;
- additional forecast days when a provider supplies more than 24 hours.

The solution must also support entities renamed by users, avoid duplicate
periods and continue working when Recorder is disabled.

## Decision

1. The forecast sensor remains the authoritative source for future periods.
2. The dashboard reads today's past values from Home Assistant History for the
   matching **Current price** sensors.
3. Price and forecast sensors expose `tariff_entry_id`; price sensors also
   expose `tariff_component` and `tariff_role`.
4. The frontend discovers current-price sensors through these stable attributes,
   not through entity names.
5. Historical states carrying period attributes retain their exact boundaries.
   Legacy states recorded before those attributes existed are reconstructed
   from their state-change timestamps on a quarter-hour grid.
6. Historical and forecast periods are merged by exact start/end timestamp.
   Exact attributes and forecast values overwrite inferred values for the same
   component and period.
7. History requests include non-significant state changes so equal consecutive
   prices are not lost.
8. Calendar days are calculated in Home Assistant's configured timezone.
9. Day navigation is derived from all available dates and has no fixed
   24-hour limit.
10. History is an optional enhancement; failures fall back to forecast-only
    rendering.
11. The coordinator notifies sensor listeners after every scheduled tariff
    refresh, even when the provider payload compares equal to the previous
    response. The current period is time-dependent and must therefore advance
    independently of payload changes.
12. Visible tariff cards publish their raw price extrema to the overview. The
    overview applies one shared Y-axis range to all cards: zero as the normal
    lower bound, the next negative CHF 0.05 step when needed, and the next
    CHF 0.10 step for the upper bound. Grid lines use CHF 0.10 intervals from a
    highlighted zero line.

## Why this location

Recorder already owns historical state retention, exclusion rules and database
lifecycle. Reusing it avoids creating a second persistence system inside the
custom integration.

The merge belongs in the frontend because it is a presentation-specific view:
backend sensor semantics remain clear—current sensors describe the active
period and the forecast sensor describes future periods. Provider and
coordinator code do not become coupled to a dashboard requirement.

Stable linking metadata belongs on entities because entity IDs and friendly
names can be changed by users. A config-entry identifier and explicit role are
machine-readable and independent of translations.

## Alternatives considered

### Keep all expired periods in the coordinator

Rejected as the primary history mechanism. It would lose data after a Home
Assistant restart, duplicate Recorder responsibilities and increase retained
memory. The coordinator keeps only not-yet-ended periods needed for live sensor
continuity.

### Persist a custom tariff database

Rejected. It would add migrations, retention settings, storage failure modes and
privacy responsibilities for data already handled by Recorder.

### Infer current sensors from entity IDs or friendly names

Rejected. Both can be changed by users, and friendly names vary by language.

### Use long-term statistics

Rejected for the daily quarter-hour chart. Statistics may aggregate values and
do not preserve the exact tariff period attributes needed for step boundaries.

### Require a third-party chart card

Rejected. Automatic discovery and a bundled card are core usability goals, and
external cards cannot reliably know the integration-specific merge rules.

## Consequences

### Positive

- The chart can show the full recorded current day.
- History recorded before version 0.5.0 remains usable without a migration.
- Restart-safe history is delegated to Home Assistant.
- User-renamed entities continue to work.
- Forecasts longer than 24 hours appear automatically.
- Duplicate historical/forecast periods are deterministic.
- Forecast-only use remains available without Recorder.
- Recorder receives one state with exact boundaries for every quarter-hour,
  including when consecutive periods have the same price or the provider
  response remains unchanged.
- Equal Y-axis ranges make simultaneous tariff graphs directly comparable.

### Trade-offs

- The first chart render may briefly contain forecast data only while History
  loads.
- Past values depend on Recorder retention and exclusion settings.
- The frontend performs one History request per active quarter-hour and tariff
  card.
- Entity state attributes include internal linkage metadata.

## Invariants for future changes

- Do not derive entity linkage from names.
- Do not silently substitute tomorrow when today is selected.
- Do not cap provider forecasts at 24 hours.
- Do not make Recorder a hard integration dependency.
- Preserve exact timezone-aware period boundaries.
- Preserve forecast-over-history precedence for duplicate periods.
- Keep coordinator listener updates independent of provider-payload equality;
  current-period sensor values and attributes change with time.
- Synchronize visible dashboard-card axes from raw extrema and keep grid
  intervals anchored to zero.
- Keep public and versioned internal custom-element constructors distinct.
- Derive chart dimensions from the rendered tariff-frame width.
