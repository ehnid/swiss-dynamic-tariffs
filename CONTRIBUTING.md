# Contributing to Swiss Dynamic Tariffs

Contributions are welcome. Please use GitHub issues for bugs and feature
proposals and pull requests for code or documentation changes.

## Before changing code

Read [the architecture guide](docs/architecture.md). Decisions that affect data
contracts, provider behaviour, entity identity or dashboard data sources should
also be documented as an Architecture Decision Record (ADR) under `docs/adr/`.

An ADR explains why a design was selected, which alternatives were considered
and what consequences maintainers must preserve. Use
[ADR 0001](docs/adr/0001-dashboard-time-series.md) as the format example.

## Development environment

The repository includes a VS Code development container with the required
Python and Home Assistant dependencies. A local environment can also be used:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_test.txt
pre-commit install
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Workflow

1. Fork the repository and create a branch from `main`.
2. Keep changes focused and preserve backwards-compatible entity unique IDs.
3. Add or update tests for changed behaviour.
4. Update user documentation and technical documentation where applicable.
5. Run the complete checks.
6. Open a pull request describing the problem, solution and relevant design
   trade-offs.

## Required checks

Run the same formatting and linting hooks used in CI:

```bash
pre-commit run --all-files
```

Run the test suite:

```bash
pytest --cov=custom_components.swiss_dynamic_tariffs
```

For frontend changes, also verify JavaScript syntax:

```bash
node --check custom_components/swiss_dynamic_tariffs/frontend/swiss-dynamic-tariffs.js
```

## Adding or changing a provider

The provider system is intentionally isolated from Home Assistant entities:

1. Implement `TariffProvider` under
   `custom_components/swiss_dynamic_tariffs/providers/`.
2. Return timezone-aware `TariffPeriod` objects with CHF/kWh values.
3. Register the provider and each selectable tariff in `providers/registry.py`.
4. Use the exact user-facing tariff name required in the configuration flow.
5. Add parser, request and config-flow tests.
6. Update the supported-tariff table in `README.md` and `info.md`.

Provider code must not rename existing sensor unique IDs or silently invent
missing price components.

## Documentation responsibilities

- `README.md` is the primary user guide.
- `info.md` is the concise HACS store description.
- `docs/architecture.md` describes stable technical structure and contracts.
- `docs/adr/` records important design decisions and their rationale.
- Code comments explain local, non-obvious constraints; they should not repeat
  what the code already states clearly.

## Bug reports

Please include:

- Home Assistant and integration versions;
- selected provider and tariff;
- expected and actual behaviour;
- relevant logs with secrets removed;
- steps that reproduce the problem;
- screenshots when the dashboard presentation is involved.

## License

By contributing, you agree that your contribution is licensed under the
[MIT License](LICENSE).
