# AI Agent Instructions for Swiss Dynamic Tariffs

This is a Home Assistant custom component providing dynamic tariff pricing data from Swiss energy providers. This document helps AI agents understand the codebase structure and conventions.

## Quick Start

**Testing:** `pytest --cov=custom_components.swiss_dynamic_tariffs`
**Code style:** `black .` + `isort .` (or use `pre-commit run --all-files`)
**Dev container:** Available in VS Code with tasks to run Home Assistant locally

## Architecture Overview

### Core Pattern: Provider System

The integration follows an **extensible provider pattern**:

- **Base class:** [`providers/base.py`](custom_components/swiss_dynamic_tariffs/providers/base.py) — Abstract `TariffProvider` interface
- **Implementations:** [`providers/bkw.py`](custom_components/swiss_dynamic_tariffs/providers/bkw.py) and others
- **Registry:** [`providers/registry.py`](custom_components/swiss_dynamic_tariffs/providers/registry.py) — Dynamic provider lookup

To add a new provider: Implement the `TariffProvider` interface and register it in `registry.py`.

### Data Flow

1. **Configuration:** User selects provider in config flow ([`config_flow.py`](custom_components/swiss_dynamic_tariffs/config_flow.py))
2. **Setup:** [`__init__.py`](custom_components/swiss_dynamic_tariffs/__init__.py) instantiates the chosen provider
3. **Updates:** [`coordinator.py`](custom_components/swiss_dynamic_tariffs/coordinator.py) — Uses Home Assistant's `DataUpdateCoordinator` to fetch and cache tariff data at intervals
4. **Entities:** [`sensor.py`](custom_components/swiss_dynamic_tariffs/sensor.py) — Creates Home Assistant sensor entities that expose tariff data

### Key Models

[`models.py`](custom_components/swiss_dynamic_tariffs/models.py) defines data structures like `TariffPeriod`.

## File Organization

```
custom_components/swiss_dynamic_tariffs/
├── __init__.py           # Integration setup & async_setup_entry
├── config_flow.py        # UI configuration flow
├── coordinator.py        # DataUpdateCoordinator for data fetching
├── api.py                # Legacy API client (consider using providers directly)
├── sensor.py             # Sensor entity definitions
├── entity.py             # Base entity class
├── models.py             # Data models (TariffPeriod, etc.)
├── const.py              # Constants (DOMAIN, PLATFORMS, defaults)
├── exceptions.py         # Custom exceptions
├── manifest.json         # Integration metadata
├── providers/
│   ├── base.py          # TariffProvider abstract base class
│   ├── registry.py      # Provider registry & lookup
│   └── bkw.py           # BKW provider implementation
└── translations/        # Multi-language strings
```

## Development Conventions

### Async/Await

All network I/O and Home Assistant interactions are async. Use `async def` for coordinator updates and provider methods.

### Typing

Type hints are used throughout. Use `from __future__ import annotations` for forward references.

### Logging

- Import: `import logging` and `_LOGGER = logging.getLogger(__name__)`
- Use `_LOGGER.debug()`, `.info()`, `.warning()`, `.error()`

### Constants

All hardcoded values go in [`const.py`](custom_components/swiss_dynamic_tariffs/const.py) with the `DOMAIN` and `PLATFORMS` defined there.

### Testing

Tests are in the `tests/` folder using pytest. See [CONTRIBUTING.md](CONTRIBUTING.md) for test execution.

## Common Tasks

### Adding a new provider

1. Create `providers/my_provider.py` inheriting from `TariffProvider`
2. Implement `async_get_tariffs()` returning `list[TariffPeriod]`
3. Register in [`providers/registry.py`](custom_components/swiss_dynamic_tariffs/providers/registry.py)
4. Add to config flow choices in [`config_flow.py`](custom_components/swiss_dynamic_tariffs/config_flow.py)

### Adding a new sensor

1. Define the sensor class in [`sensor.py`](custom_components/swiss_dynamic_tariffs/sensor.py) inheriting from `CoordinatorEntity`
2. Reference the coordinator data via `self.coordinator.data`
3. Update `PLATFORMS` in [`const.py`](custom_components/swiss_dynamic_tariffs/const.py) if adding a new platform

### Updating translations

Add/update keys in `translations/{lang}.json` files. See CONTRIBUTING.md for details.

## Key Dependencies

- **homeassistant** — Home Assistant core
- **aiohttp** — Async HTTP client (via Home Assistant)
- **pytest-homeassistant-custom-component** — Testing utilities

## Code Style & Linting

Enforced via pre-commit hooks:

- **Black** — Code formatting
- **isort** — Import sorting
- **flake8** — Linting (see `setup.cfg` for ignore rules)

Configuration in [`setup.cfg`](setup.cfg): max line length 88, isort configured for Home Assistant conventions.

## Links

- [Contribution Guidelines](CONTRIBUTING.md)
- [Home Assistant Developer Docs](https://developers.home-assistant.io)
- [Integration Blueprint Template](https://github.com/custom-components/integration_blueprint)
