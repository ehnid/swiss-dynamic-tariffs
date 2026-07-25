# Swiss Dynamic Tariffs

<p align="center">
  <img src="https://raw.githubusercontent.com/ehnid/swiss-dynamic-tariffs/main/custom_components/swiss_dynamic_tariffs/brand/logo.png" alt="Swiss Dynamic Tariffs logo" width="220">
</p>

Swiss Dynamic Tariffs imports quarter-hourly prices from supported Swiss energy
providers into Home Assistant. Configuration is completed in the UI; no YAML or
third-party chart card is required.

The project was started by an electrical engineer to experiment with home
automation and support Switzerland's shift towards dynamic electricity prices.
It is driven by the conviction that broad use of tariff-based load shifting can
avoid or defer a substantial share of grid reinforcement, especially on
distribution grid levels 5 and 7. The actual effect depends on adoption, local
constraints and network planning.

## Supported tariffs

- BKW – dynamische Einspeisevergütung
- CKW – Home Dynamic
- CKW – Business Dynamic
- Groupe E – Vario
- Primeo Energie – Netz dynamisch
- Primeo Energie – Netz dynamisch (AVAG)
- Primeo Energie – Netz dynamisch (ELAG)
- EKZ – Energie Dynamisch + Netz 400D
- EKZ Einsiedeln – Energie Dynamisch + Netz 400D

Every tariff is a separate configuration-flow option, so multiple tariffs from
the same provider can be added.

## Sensors and dashboard

The integration creates current, next, minimum, maximum and average sensors for
every price component supplied by the selected tariff. A forecast sensor exposes
all published future quarter-hour periods.

The automatic sidebar dashboard provides:

- a compact chart with labelled time and price axes;
- today's recorded current-price values, including legacy Recorder states,
  combined with the forecast;
- Y-axis labels limited to two decimal places while detail values retain their
  precision;
- all dates published by the provider, including forecasts beyond 24 hours;
- exact hover values and minimum/maximum annotations;
- an expandable quarter-hour table that remains open during updates.

Past chart values require Home Assistant Recorder/History to record the
corresponding **Current price** sensors. Forecast display continues to work when
history is unavailable.

{% if not installed %}

## Installation

1. Install **Swiss Dynamic Tariffs** through HACS.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration**.
4. Search for **Swiss Dynamic Tariffs** and select a tariff.

{% else %}

## Configuration

Open **Settings → Devices & services → Add integration**, search for
**Swiss Dynamic Tariffs** and select the required provider/tariff combination.

{% endif %}

## More information

- [Complete user guide](README.md)
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)
- [MIT License](LICENSE)
