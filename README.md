# Swiss Dynamic Tariffs

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

| Platform | Description                                                 |
| -------- | ----------------------------------------------------------- |
| `sensor` | Current, next, min/max and average tariff values (CHF/kWh). |

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
feed-in, grid usage, or an all-in/"integrated" price), five sensors are
created. The public BKW endpoint currently publishes the dynamic feed-in
tariff, so a BKW configuration creates five feed-in sensors:

| Sensor                      | Meaning                                                |
| --------------------------- | ------------------------------------------------------ |
| Current                     | Price of the currently active quarter hour.            |
| Next                        | Price of the quarter hour right after the current one. |
| Cheapest Quarter Hour       | Lowest upcoming price and when it occurs.              |
| Most Expensive Quarter Hour | Highest upcoming price and when it occurs.             |
| Average                     | Average price across all known upcoming quarter hours. |

"Cheapest" and "most expensive" are computed over every quarter hour
the provider has already published that hasn't ended yet - this
covers the rest of today plus tomorrow once a provider publishes
next-day prices.

When BKW switches the endpoint to the newly published day, the integration
retains previously fetched periods until they end. This keeps the current
tariff available while Home Assistant is running.

![example][exampleimg]

## Installation

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
custom_components/swiss_dynamic_tariffs/translations/nb.json
custom_components/swiss_dynamic_tariffs/__init__.py
custom_components/swiss_dynamic_tariffs/config_flow.py
custom_components/swiss_dynamic_tariffs/const.py
custom_components/swiss_dynamic_tariffs/coordinator.py
custom_components/swiss_dynamic_tariffs/entity.py
custom_components/swiss_dynamic_tariffs/exceptions.py
custom_components/swiss_dynamic_tariffs/manifest.json
custom_components/swiss_dynamic_tariffs/models.py
custom_components/swiss_dynamic_tariffs/sensor.py
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

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/ehnid
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ehnid/swiss-dynamic-tariffs-template.svg?style=for-the-badge
[commits]: https://github.com/ehnid/swiss-dynamic-tariffs-template/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/ehnid/swiss-dynamic-tariffs-template.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ehnid-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ehnid/swiss-dynamic-tariffs-template.svg?style=for-the-badge
[releases]: https://github.com/ehnid/swiss-dynamic-tariffs-template/releases
[user_profile]: https://github.com/ehnid
