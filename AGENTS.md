# AI agent guide for Swiss Dynamic Tariffs

Swiss Dynamic Tariffs is a Home Assistant custom integration for
quarter-hourly prices from Swiss energy providers. Preserve the provider data
as published: normalize its shape and units, but do not synthesize missing
prices or extend a provider's forecast horizon.

## Start here

- Architecture and design rationale: [`docs/architecture.md`](docs/architecture.md)
- Contribution and verification workflow:
  [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Tests: `pytest --cov=custom_components.swiss_dynamic_tariffs`
- All repository checks: `pre-commit run --all-files`
- Frontend syntax:

  ```bash
  node --check custom_components/swiss_dynamic_tariffs/frontend/swiss-dynamic-tariffs.js
  ```

The VS Code development container includes Home Assistant, pytest, Ruff,
Prettier, Node.js and pre-commit.

## Architecture

The integration uses an extensible provider system:

- `providers/base.py` defines the provider interface.
- Provider-specific modules fetch or construct tariff periods.
- `providers/registry.py` maps configuration-flow options to providers.
- `coordinator.py` refreshes and caches normalized data.
- `sensor.py` exposes current, statistical and forecast entities.
- `frontend/swiss-dynamic-tariffs.js` renders the automatic sidebar dashboard.

`models.py` owns shared data contracts such as `TariffPeriod`. The dashboard's
history/forecast merge is documented in
[`ADR 0001`](docs/adr/0001-dashboard-time-series.md).

## Implementation conventions

- All network and Home Assistant I/O is asynchronous.
- Use `from __future__ import annotations` and complete type annotations.
- Put shared constants in `const.py`.
- Log through a module-level `_LOGGER = logging.getLogger(__name__)`.
- Keep entity unique IDs backwards compatible.
- Translate user-facing sensor and dashboard text into German, English, French
  and Italian.
- Explain non-obvious provider parsing and frontend state decisions in code.
- Add or update tests whenever behaviour changes.

## Adding a provider or tariff

1. Implement `TariffProvider` in `providers/`.
2. Register every separately selectable tariff in `providers/registry.py`.
3. Add the configuration-flow label to `strings.json` and every translation.
4. Test parsing, units, period boundaries, component names and error handling.
5. Update the supported-tariff tables in `README.md` and `info.md`.

If a source changes its public schema, fail with a clear provider error instead
of silently returning plausible but incorrect prices.

## Documentation decisions

Update `docs/architecture.md` when responsibilities or data flow change. Add an
Architecture Decision Record under `docs/adr/` for decisions that affect public
data contracts, entity identity, provider behaviour or dashboard data sources.
An ADR records the context, alternatives, decision and consequences so later
changes do not accidentally undo an intentional trade-off.
