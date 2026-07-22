# Swiss Dynamic Tariffs

<p align="center">
  <img src="https://raw.githubusercontent.com/ehnid/swiss-dynamic-tariffs/main/custom_components/swiss_dynamic_tariffs/brand/logo.png" alt="Swiss Dynamic Tariffs logo" width="220">
</p>

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

| Platform | Description                                               |
| -------- | --------------------------------------------------------- |
| `sensor` | Current, next, min/max, average and forecast tariff data. |

Currently selectable provider/tariff combinations:

| Provider       | Tariff              | Available price components                |
| -------------- | ------------------- | ----------------------------------------- |
| BKW            | `feed_in`           | Feed-in                                   |
| CKW            | `home_dynamic`      | Electricity, grid usage, grid, integrated |
| CKW            | `business_dynamic`  | Electricity, grid usage, grid, integrated |
| Groupe E       | `VARIO`             | Grid, integrated                          |
| Primeo Energie | `NetzDynamisch`     | Electricity, grid usage, grid, integrated |
| Primeo Energie | `NetzDynamischAVAG` | Electricity, grid usage, grid, integrated |
| Primeo Energie | `NetzDynamischELAG` | Electricity, grid usage, grid, integrated |
| EKZ            | `integrated_400D`   | Integrated                                |
| EKZ Einsiedeln | `integrated_400D_E` | Integrated                                |

Each provider/tariff combination is a separate option in the configuration
flow. Multiple tariffs from the same provider can therefore be added as
separate integration entries.

For every price component supported by the selected provider (consumption,
feed-in, grid usage, or an all-in/"integrated" price), five price sensors are
created. One additional **Tariff forecast** sensor combines every published
future quarter hour and all available price components. The public BKW
endpoint currently publishes the dynamic feed-in tariff, so a BKW
configuration creates five feed-in price sensors plus the forecast sensor:

| Sensor                      | Meaning                                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| Current                     | Price of the currently active quarter hour.                                                     |
| Next                        | Price of the next quarter hour.                                                                 |
| Cheapest Quarter Hour       | Lowest upcoming price and when it occurs.                                                       |
| Most Expensive Quarter Hour | Highest upcoming price and when it occurs.                                                      |
| Average                     | Average price across all known upcoming quarter hours.                                          |
| Tariff forecast             | Number of future hours available; all quarter-hour prices are stored in the `prices` attribute. |

"Cheapest" and "most expensive" are computed over every quarter hour
the provider has already published that hasn't ended yet - this
covers the rest of today plus tomorrow once a provider publishes
next-day prices.

The **Tariff forecast** sensor state shows how many future hours are currently
available. Its `prices` attribute contains every published future quarter hour.
Each list item provides `start`, `end`, and every price component supplied by
the selected provider. Timestamps use ISO 8601 and prices use CHF/kWh. The
attributes `available_from`, `available_until`, and `period_count` summarize
the available range.

### Price component terminology

The provider APIs use the following English terms. Not every provider supplies
every component, and fixed monthly charges or VAT may not be included:

| API term      | Meaning                                                                    |
| ------------- | -------------------------------------------------------------------------- |
| `electricity` | Energy-only price for electricity consumed from the grid.                  |
| `feed_in`     | Compensation paid for electricity exported to the grid.                    |
| `grid_usage`  | Dynamic usage-based network charge without the energy price.               |
| `grid`        | Network charge including the grid-related levies reported by the provider. |
| `integrated`  | Provider-specific combined price, normally `electricity` plus `grid`.      |

Sensor display names are translated by Home Assistant into the configured
system language. Their technical entity IDs remain stable and use the English
API terms above.

When BKW switches the endpoint to the newly published day, the integration
retains previously fetched periods until they end. This keeps the current
tariff available while Home Assistant is running.

## Installation

### HACS

[![Open your Home Assistant instance and add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ehnid&repository=swiss-dynamic-tariffs&category=integration)

Releases tagged with `v*` are automatically packaged for HACS. HACS then
installs the matching `swiss_dynamic_tariffs.zip` release asset.

### Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `swiss_dynamic_tariffs`.
4. Download _all_ the files from the `custom_components/swiss_dynamic_tariffs/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Swiss Dynamic Tariffs"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/swiss_dynamic_tariffs/translations/en.json
custom_components/swiss_dynamic_tariffs/translations/de.json
custom_components/swiss_dynamic_tariffs/translations/fr.json
custom_components/swiss_dynamic_tariffs/translations/it.json
custom_components/swiss_dynamic_tariffs/brand/icon.png
custom_components/swiss_dynamic_tariffs/brand/logo.png
custom_components/swiss_dynamic_tariffs/__init__.py
custom_components/swiss_dynamic_tariffs/config_flow.py
custom_components/swiss_dynamic_tariffs/const.py
custom_components/swiss_dynamic_tariffs/coordinator.py
custom_components/swiss_dynamic_tariffs/entity.py
custom_components/swiss_dynamic_tariffs/exceptions.py
custom_components/swiss_dynamic_tariffs/manifest.json
custom_components/swiss_dynamic_tariffs/models.py
custom_components/swiss_dynamic_tariffs/sensor.py
custom_components/swiss_dynamic_tariffs/strings.json
custom_components/swiss_dynamic_tariffs/providers/__init__.py
custom_components/swiss_dynamic_tariffs/providers/base.py
custom_components/swiss_dynamic_tariffs/providers/bkw.py
custom_components/swiss_dynamic_tariffs/providers/ckw.py
custom_components/swiss_dynamic_tariffs/providers/ekz.py
custom_components/swiss_dynamic_tariffs/providers/groupe_e.py
custom_components/swiss_dynamic_tariffs/providers/parser.py
custom_components/swiss_dynamic_tariffs/providers/primeo.py
custom_components/swiss_dynamic_tariffs/providers/registry.py
custom_components/swiss_dynamic_tariffs/providers/standard.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## License

Swiss Dynamic Tariffs is distributed under the [MIT License](LICENSE).

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/ehnid
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[commits]: https://github.com/ehnid/swiss-dynamic-tariffs/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ehnid-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[releases]: https://github.com/ehnid/swiss-dynamic-tariffs/releases
[user_profile]: https://github.com/ehnid
