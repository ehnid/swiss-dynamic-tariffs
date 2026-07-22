[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

<p align="center">
  <img src="https://raw.githubusercontent.com/ehnid/swiss-dynamic-tariffs/main/custom_components/swiss_dynamic_tariffs/brand/logo.png" alt="Swiss Dynamic Tariffs logo" width="220">
</p>

**This component will set up the following platforms.**

| Platform | Description                                               |
| -------- | --------------------------------------------------------- |
| `sensor` | Current, next, min/max, average and forecast tariff data. |

Supported provider/tariff combinations:

| Provider       | Tariffs                                                   |
| -------------- | --------------------------------------------------------- |
| BKW            | `feed_in`                                                 |
| CKW            | `home_dynamic`, `business_dynamic`                        |
| Groupe E       | `VARIO`                                                   |
| Primeo Energie | `NetzDynamisch`, `NetzDynamischAVAG`, `NetzDynamischELAG` |
| EKZ            | `integrated_400D`, `integrated_400D_E` (Einsiedeln)       |

Every tariff is available as its own option in the configuration flow, so
more than one tariff from the same provider can be configured.

{% if not installed %}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Swiss Dynamic Tariffs".

{% endif %}

## Configuration is done in the UI

<!---->

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[commits]: https://github.com/ehnid/swiss-dynamic-tariffs/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/ehnid/swiss-dynamic-tariffs/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ehnid-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ehnid/swiss-dynamic-tariffs.svg?style=for-the-badge
[releases]: https://github.com/ehnid/swiss-dynamic-tariffs/releases
[user_profile]: https://github.com/ehnid
