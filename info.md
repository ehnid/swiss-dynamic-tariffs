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
the same provider can be added. The selection starts empty and requires an
explicit provider/tariff choice.

## Sensors and dashboard

The integration creates current, next, minimum, maximum and average sensors for
every price component supplied by the selected tariff. A forecast sensor exposes
the complete quarter-hour window currently published by the provider, including
earlier periods that remain available from the source.

The integration creates a regular user-managed Home Assistant dashboard. It can
be reordered, renamed, hidden from the sidebar or deleted under
**Settings → Dashboards**. A deleted dashboard is not recreated automatically.

The dashboard provides:

- a responsive tariff frame capped at 40% of the current screen width on
  desktops and using the full available width on phones;
- a chart with labelled time and price axes that follows the frame size;
- today's provider-published values combined with Recorder states for periods
  no longer returned by the source;
- Y-axis labels limited to two decimal places while detail values retain their
  precision;
- a synchronized Y-axis range for all visible tariff graphs, starting at zero
  unless negative values require a lower bound;
- a highlighted zero line and grid lines every CHF 0.10, measured from zero;
- all dates published by the provider, including forecasts beyond 24 hours;
- exact hover values and minimum/maximum annotations;
- an expandable quarter-hour table that remains open during updates.

Past values that remain in a provider response do not require Recorder. For
periods already removed by the provider, Home Assistant Recorder/History must
record the corresponding **Current price** sensors. Version 0.5.3 ensures that
Recorder receives every scheduled quarter-hour even when the provider payload
or consecutive prices are unchanged.

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
