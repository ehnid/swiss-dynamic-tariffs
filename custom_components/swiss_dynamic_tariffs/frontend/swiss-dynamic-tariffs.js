const CARD_TAG = "swiss-dynamic-tariffs-card";
const CARD_TYPE = `custom:${CARD_TAG}`;
const STRATEGY_TYPE = "swiss-dynamic-tariffs";
const FORECAST_ATTRIBUTES = ["prices", "available_from", "available_until"];

const COMPONENTS = [
  {
    key: "integrated",
    color: "#8b5cf6",
    labels: {
      de: "Gesamtpreis",
      en: "Integrated price",
      fr: "Prix total",
      it: "Prezzo totale",
    },
  },
  {
    key: "electricity",
    color: "#00a6d6",
    labels: {
      de: "Energie",
      en: "Electricity",
      fr: "Énergie",
      it: "Energia",
    },
  },
  {
    key: "grid_usage",
    color: "#f59e0b",
    labels: {
      de: "Netznutzung",
      en: "Grid usage",
      fr: "Utilisation du réseau",
      it: "Utilizzo della rete",
    },
  },
  {
    key: "grid",
    color: "#ef4444",
    labels: {
      de: "Netz inkl. Abgaben",
      en: "Grid incl. levies",
      fr: "Réseau, taxes comprises",
      it: "Rete, tasse incluse",
    },
  },
  {
    key: "feed_in",
    color: "#22c55e",
    labels: {
      de: "Einspeisevergütung",
      en: "Feed-in tariff",
      fr: "Rétribution d’injection",
      it: "Tariffa di immissione",
    },
  },
];

const TEXT = {
  de: {
    title: "Tarifprognose",
    dashboardTitle: "Dynamische Stromtarife",
    dashboardDescription:
      "Automatische Preisdiagramme für alle Tarifprognosen.",
    noData: "Noch keine zukünftigen Tarifdaten verfügbar.",
    unavailable: "Der Tarifprognose-Sensor ist nicht verfügbar.",
    chooseEntity: "Tarifprognose-Sensor",
    priceAxis: "Preis [CHF/kWh]",
    timeAxis: "Zeit",
    current: "Aktuell",
    minimum: "Günstigste",
    maximum: "Teuerste",
    period: "Verfügbarer Zeitraum",
    until: "bis",
    periods: "Viertelstunden",
    now: "Jetzt",
    showData: "Viertelstundenwerte anzeigen",
    time: "Zeitfenster",
    noForecasts:
      "Noch keine Tarifprognose gefunden. Richten Sie zuerst einen dynamischen Tarif ein.",
  },
  en: {
    title: "Tariff forecast",
    dashboardTitle: "Dynamic electricity tariffs",
    dashboardDescription: "Automatic price charts for all tariff forecasts.",
    noData: "No future tariff data is available yet.",
    unavailable: "The tariff forecast sensor is unavailable.",
    chooseEntity: "Tariff forecast sensor",
    priceAxis: "Price [CHF/kWh]",
    timeAxis: "Time",
    current: "Current",
    minimum: "Cheapest",
    maximum: "Most expensive",
    period: "Available period",
    until: "to",
    periods: "quarter-hours",
    now: "Now",
    showData: "Show quarter-hour values",
    time: "Time window",
    noForecasts: "No tariff forecast found yet. Set up a dynamic tariff first.",
  },
  fr: {
    title: "Prévision tarifaire",
    dashboardTitle: "Tarifs dynamiques de l’électricité",
    dashboardDescription:
      "Graphiques automatiques pour toutes les prévisions tarifaires.",
    noData: "Aucune donnée tarifaire future n’est encore disponible.",
    unavailable: "Le capteur de prévision tarifaire n’est pas disponible.",
    chooseEntity: "Capteur de prévision tarifaire",
    priceAxis: "Prix [CHF/kWh]",
    timeAxis: "Heure",
    current: "Actuel",
    minimum: "Le moins cher",
    maximum: "Le plus cher",
    period: "Période disponible",
    until: "à",
    periods: "quarts d’heure",
    now: "Maintenant",
    showData: "Afficher les valeurs par quart d’heure",
    time: "Plage horaire",
    noForecasts:
      "Aucune prévision tarifaire trouvée. Configurez d’abord un tarif dynamique.",
  },
  it: {
    title: "Previsione tariffaria",
    dashboardTitle: "Tariffe elettriche dinamiche",
    dashboardDescription:
      "Grafici automatici per tutte le previsioni tariffarie.",
    noData: "Non sono ancora disponibili dati tariffari futuri.",
    unavailable: "Il sensore della previsione tariffaria non è disponibile.",
    chooseEntity: "Sensore della previsione tariffaria",
    priceAxis: "Prezzo [CHF/kWh]",
    timeAxis: "Ora",
    current: "Attuale",
    minimum: "Più conveniente",
    maximum: "Più costoso",
    period: "Periodo disponibile",
    until: "a",
    periods: "quarti d’ora",
    now: "Adesso",
    showData: "Mostra i valori ogni quarto d’ora",
    time: "Intervallo",
    noForecasts:
      "Nessuna previsione tariffaria trovata. Configurare prima una tariffa dinamica.",
  },
};

function languageFromHass(hass) {
  const language = hass?.locale?.language || hass?.language || "en";
  const shortLanguage = language.split("-")[0].toLowerCase();
  return TEXT[shortLanguage] ? shortLanguage : "en";
}

function textFor(hass) {
  return TEXT[languageFromHass(hass)];
}

function componentLabel(component, hass) {
  const language = languageFromHass(hass);
  return component.labels[language] || component.labels.en;
}

function isForecastState(state) {
  return (
    state?.entity_id?.startsWith("sensor.") &&
    FORECAST_ATTRIBUTES.every((attribute) =>
      Object.prototype.hasOwnProperty.call(state.attributes || {}, attribute),
    ) &&
    Array.isArray(state.attributes.prices)
  );
}

function forecastEntities(hass) {
  return Object.values(hass?.states || {})
    .filter(isForecastState)
    .sort((left, right) =>
      String(left.attributes.friendly_name || left.entity_id).localeCompare(
        String(right.attributes.friendly_name || right.entity_id),
      ),
    );
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function parsePeriods(state) {
  return (state?.attributes?.prices || [])
    .map((period) => ({
      ...period,
      startTime: Date.parse(period.start),
      endTime: Date.parse(period.end),
    }))
    .filter(
      (period) =>
        Number.isFinite(period.startTime) &&
        Number.isFinite(period.endTime) &&
        period.endTime > period.startTime,
    )
    .sort((left, right) => left.startTime - right.startTime);
}

function availableComponents(periods, configuredComponents) {
  const requested = Array.isArray(configuredComponents)
    ? new Set(configuredComponents)
    : null;

  return COMPONENTS.filter(
    (component) =>
      (!requested || requested.has(component.key)) &&
      periods.some(
        (period) =>
          period[component.key] !== undefined &&
          period[component.key] !== null &&
          Number.isFinite(Number(period[component.key])),
      ),
  );
}

function priceValues(periods, components) {
  return periods.flatMap((period) =>
    components
      .map((component) => Number(period[component.key]))
      .filter(Number.isFinite),
  );
}

function stepPath(periods, component, xScale, yScale) {
  let path = "";
  let previousEnd = null;
  let hasPath = false;

  for (const period of periods) {
    const value = Number(period[component.key]);
    if (!Number.isFinite(value)) {
      hasPath = false;
      previousEnd = null;
      continue;
    }

    const startX = xScale(period.startTime);
    const endX = xScale(period.endTime);
    const y = yScale(value);
    const continuous = hasPath && previousEnd === period.startTime;

    path += continuous
      ? ` V ${y.toFixed(2)} H ${endX.toFixed(2)}`
      : ` M ${startX.toFixed(2)} ${y.toFixed(2)} H ${endX.toFixed(2)}`;

    hasPath = true;
    previousEnd = period.endTime;
  }

  return path.trim();
}

function numericTicks(minimum, maximum, count) {
  if (minimum === maximum) {
    return [minimum];
  }

  return Array.from(
    { length: count },
    (_, index) => minimum + ((maximum - minimum) * index) / (count - 1),
  );
}

function timeTicks(minimum, maximum, count) {
  return Array.from(
    { length: count },
    (_, index) => minimum + ((maximum - minimum) * index) / (count - 1),
  );
}

class SwissDynamicTariffsCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("swiss-dynamic-tariffs-card-editor");
  }

  static getStubConfig(hass) {
    return {
      entity: forecastEntities(hass)[0]?.entity_id || "",
    };
  }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = undefined;
    this._config = undefined;
    this._chartModel = undefined;
    this._renderedHostWidth = undefined;
    this._resizeObserver = new ResizeObserver(([entry]) => {
      const hostWidth = Math.round(entry.contentRect.width);
      if (
        hostWidth > 0 &&
        Math.abs(hostWidth - (this._renderedHostWidth || 0)) >= 16
      ) {
        this._renderedHostWidth = hostWidth;
        this._render();
      }
    });
  }

  connectedCallback() {
    this._resizeObserver.observe(this);
  }

  disconnectedCallback() {
    this._resizeObserver.disconnect();
  }

  setConfig(config) {
    if (!config?.entity) {
      throw new Error("Please select a tariff forecast sensor.");
    }

    this._config = { ...config };
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return 6;
  }

  _formatPrice(value) {
    return new Intl.NumberFormat(languageFromHass(this._hass), {
      minimumFractionDigits: 3,
      maximumFractionDigits: 5,
    }).format(value);
  }

  _formatDateTime(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp));
  }

  _formatTime(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp));
  }

  _formatDate(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      day: "2-digit",
      month: "2-digit",
    }).format(new Date(timestamp));
  }

  _emptyCard(message) {
    const text = textFor(this._hass);
    const title = this._config?.title || text.title;

    this.shadowRoot.innerHTML = `
      <style>${this._styles()}</style>
      <ha-card>
        <div class="card-header">
          <div>
            <div class="eyebrow">Swiss Dynamic Tariffs</div>
            <h2>${escapeHtml(title)}</h2>
          </div>
          <ha-icon icon="mdi:chart-timeline-variant"></ha-icon>
        </div>
        <div class="empty-state">
          <ha-icon icon="mdi:chart-line-variant"></ha-icon>
          <p>${escapeHtml(message)}</p>
        </div>
      </ha-card>
    `;
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) {
      return;
    }

    const text = textFor(this._hass);
    const state = this._hass.states[this._config.entity];
    if (!state || ["unknown", "unavailable"].includes(state.state)) {
      this._emptyCard(text.unavailable);
      return;
    }

    const periods = parsePeriods(state);
    const components = availableComponents(periods, this._config.components);
    if (!periods.length || !components.length) {
      this._emptyCard(text.noData);
      return;
    }

    const hostWidth =
      this._renderedHostWidth || Math.round(this.getBoundingClientRect().width);
    const compact = hostWidth > 0 && hostWidth <= 500;
    const horizontalPadding = compact ? 24 : 44;
    const width = Math.min(
      760,
      Math.max(320, (hostWidth || 804) - horizontalPadding),
    );
    const height = compact ? 300 : 330;
    const plot = compact
      ? { left: 62, right: 12, top: 26, bottom: 58 }
      : { left: 82, right: 24, top: 26, bottom: 62 };
    const plotWidth = width - plot.left - plot.right;
    const plotHeight = height - plot.top - plot.bottom;
    const xMinimum = periods[0].startTime;
    const xMaximum = periods[periods.length - 1].endTime;
    const values = priceValues(periods, components);
    const rawMinimum = Math.min(...values);
    const rawMaximum = Math.max(...values);
    const valueRange =
      rawMaximum - rawMinimum || Math.max(Math.abs(rawMaximum), 1);
    const yMinimum = rawMinimum - valueRange * 0.12;
    const yMaximum = rawMaximum + valueRange * 0.12;
    const xScale = (timestamp) =>
      plot.left + ((timestamp - xMinimum) / (xMaximum - xMinimum)) * plotWidth;
    const yScale = (value) =>
      plot.top + ((yMaximum - value) / (yMaximum - yMinimum)) * plotHeight;
    const yTicks = numericTicks(yMinimum, yMaximum, 5);
    const xTicks = timeTicks(xMinimum, xMaximum, compact ? 4 : 6);
    const primaryComponent = components[0];
    const primaryPeriods = periods.filter((period) =>
      Number.isFinite(Number(period[primaryComponent.key])),
    );
    const now = Date.now();
    const currentPeriod =
      primaryPeriods.find(
        (period) => period.startTime <= now && now < period.endTime,
      ) || primaryPeriods[0];
    const minimumPeriod = primaryPeriods.reduce((selected, period) =>
      Number(period[primaryComponent.key]) <
      Number(selected[primaryComponent.key])
        ? period
        : selected,
    );
    const maximumPeriod = primaryPeriods.reduce((selected, period) =>
      Number(period[primaryComponent.key]) >
      Number(selected[primaryComponent.key])
        ? period
        : selected,
    );
    const title =
      this._config.title || state.attributes.friendly_name || text.title;
    const coverageHours = (xMaximum - xMinimum) / 3_600_000;

    const gridLines = yTicks
      .map((tick) => {
        const y = yScale(tick);
        return `
          <line class="grid-line" x1="${plot.left}" y1="${y}" x2="${
            width - plot.right
          }" y2="${y}"></line>
          <text class="axis-tick y-tick" x="${plot.left - 12}" y="${
            y + 4
          }">${escapeHtml(this._formatPrice(tick))}</text>
        `;
      })
      .join("");

    const xAxisTicks = xTicks
      .map((tick) => {
        const x = xScale(tick);
        return `
          <line class="x-tick-line" x1="${x}" y1="${
            height - plot.bottom
          }" x2="${x}" y2="${height - plot.bottom + 6}"></line>
          <text class="axis-tick x-tick" x="${x}" y="${
            height - plot.bottom + 22
          }">
            <tspan x="${x}" dy="0">${escapeHtml(this._formatTime(tick))}</tspan>
            <tspan class="date-label" x="${x}" dy="15">${escapeHtml(
              this._formatDate(tick),
            )}</tspan>
          </text>
        `;
      })
      .join("");

    const seriesPaths = components
      .map(
        (component) => `
          <path
            class="price-line"
            d="${stepPath(periods, component, xScale, yScale)}"
            style="stroke: ${component.color}"
          ></path>
        `,
      )
      .join("");

    const nowLine =
      now >= xMinimum && now <= xMaximum
        ? `
          <line class="now-line" x1="${xScale(now)}" y1="${plot.top}" x2="${xScale(
            now,
          )}" y2="${height - plot.bottom}"></line>
          <text class="now-label" x="${xScale(now)}" y="${
            plot.top - 8
          }">${escapeHtml(text.now)}</text>
        `
        : "";

    const annotation = (period, label, below = false) => {
      const value = Number(period[primaryComponent.key]);
      const x = xScale(
        period.startTime + (period.endTime - period.startTime) / 2,
      );
      const y = yScale(value);
      const anchor =
        x > width - 145 ? "end" : x < plot.left + 100 ? "start" : "middle";
      const labelX = anchor === "end" ? x - 8 : anchor === "start" ? x + 8 : x;
      const labelY = below ? y + 24 : y - 14;
      return `
        <circle cx="${x}" cy="${y}" r="5" style="fill: ${
          primaryComponent.color
        }"></circle>
        <text class="annotation" text-anchor="${anchor}" x="${labelX}" y="${labelY}">
          ${escapeHtml(label)} ${escapeHtml(this._formatPrice(value))}
        </text>
      `;
    };

    const legend = components
      .map(
        (component) => `
          <span class="legend-item">
            <span class="legend-color" style="background: ${
              component.color
            }"></span>
            ${escapeHtml(componentLabel(component, this._hass))}
          </span>
        `,
      )
      .join("");

    const summary = [
      {
        label: text.current,
        value: `${this._formatPrice(
          Number(currentPeriod[primaryComponent.key]),
        )} CHF/kWh`,
        detail: this._formatTime(currentPeriod.startTime),
        icon: "mdi:flash",
      },
      {
        label: text.minimum,
        value: `${this._formatPrice(
          Number(minimumPeriod[primaryComponent.key]),
        )} CHF/kWh`,
        detail: this._formatDateTime(minimumPeriod.startTime),
        icon: "mdi:arrow-down-bold",
      },
      {
        label: text.maximum,
        value: `${this._formatPrice(
          Number(maximumPeriod[primaryComponent.key]),
        )} CHF/kWh`,
        detail: this._formatDateTime(maximumPeriod.startTime),
        icon: "mdi:arrow-up-bold",
      },
      {
        label: text.period,
        value: `${coverageHours.toFixed(1)} h`,
        detail: `${periods.length} ${text.periods}`,
        icon: "mdi:clock-outline",
      },
    ]
      .map(
        (item) => `
          <div class="summary-item">
            <ha-icon icon="${item.icon}"></ha-icon>
            <div>
              <span>${escapeHtml(item.label)}</span>
              <strong>${escapeHtml(item.value)}</strong>
              <small>${escapeHtml(item.detail)}</small>
            </div>
          </div>
        `,
      )
      .join("");

    const tableRows = periods
      .map(
        (period) => `
          <tr>
            <td>
              ${escapeHtml(this._formatDateTime(period.startTime))}
              – ${escapeHtml(this._formatTime(period.endTime))}
            </td>
            ${components
              .map((component) => {
                const value = Number(period[component.key]);
                return `<td>${
                  Number.isFinite(value)
                    ? `${escapeHtml(this._formatPrice(value))} CHF/kWh`
                    : "–"
                }</td>`;
              })
              .join("")}
          </tr>
        `,
      )
      .join("");

    this.shadowRoot.innerHTML = `
      <style>${this._styles()}</style>
      <ha-card>
        <div class="card-header">
          <div>
            <div class="eyebrow">Swiss Dynamic Tariffs</div>
            <h2>${escapeHtml(title)}</h2>
            <p>
              ${escapeHtml(this._formatDateTime(xMinimum))}
              ${escapeHtml(text.until)}
              ${escapeHtml(this._formatDateTime(xMaximum))}
            </p>
          </div>
          <ha-icon icon="mdi:chart-timeline-variant"></ha-icon>
        </div>

        <div class="summary-grid">${summary}</div>
        <div class="legend" aria-label="Legend">${legend}</div>

        <div class="chart-wrap">
          <svg
            class="chart"
            viewBox="0 0 ${width} ${height}"
            role="img"
            aria-label="${escapeHtml(text.priceAxis)}"
          >
            ${gridLines}
            <line class="axis-line" x1="${plot.left}" y1="${
              height - plot.bottom
            }" x2="${width - plot.right}" y2="${height - plot.bottom}"></line>
            ${xAxisTicks}
            ${seriesPaths}
            ${nowLine}
            ${annotation(minimumPeriod, text.minimum)}
            ${annotation(maximumPeriod, text.maximum, true)}
            <text
              class="axis-label y-axis-label"
              transform="translate(20 ${plot.top + plotHeight / 2}) rotate(-90)"
            >${escapeHtml(text.priceAxis)}</text>
            <text
              class="axis-label x-axis-label"
              x="${plot.left + plotWidth / 2}"
              y="${height - 4}"
            >${escapeHtml(text.timeAxis)}</text>
            <line class="hover-line" x1="0" y1="${plot.top}" x2="0" y2="${
              height - plot.bottom
            }"></line>
            <rect
              class="interaction-layer"
              x="${plot.left}"
              y="${plot.top}"
              width="${plotWidth}"
              height="${plotHeight}"
            ></rect>
          </svg>
          <div class="tooltip" role="status" aria-live="polite"></div>
        </div>

        <details>
          <summary>
            <ha-icon icon="mdi:table-clock"></ha-icon>
            ${escapeHtml(text.showData)}
          </summary>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>${escapeHtml(text.time)}</th>
                  ${components
                    .map(
                      (component) =>
                        `<th>${escapeHtml(
                          componentLabel(component, this._hass),
                        )}</th>`,
                    )
                    .join("")}
                </tr>
              </thead>
              <tbody>${tableRows}</tbody>
            </table>
          </div>
        </details>
      </ha-card>
    `;

    this._chartModel = {
      width,
      plot,
      plotWidth,
      xMinimum,
      xMaximum,
      xScale,
      periods,
      components,
    };
    this._bindChartInteractions();
  }

  _bindChartInteractions() {
    const chart = this.shadowRoot.querySelector(".chart");
    if (!chart) {
      return;
    }

    chart.addEventListener("pointermove", (event) => this._showTooltip(event));
    chart.addEventListener("pointerleave", () => this._hideTooltip());
  }

  _showTooltip(event) {
    const model = this._chartModel;
    const chart = this.shadowRoot.querySelector(".chart");
    const tooltip = this.shadowRoot.querySelector(".tooltip");
    const hoverLine = this.shadowRoot.querySelector(".hover-line");
    if (!model || !chart || !tooltip || !hoverLine) {
      return;
    }

    const bounds = chart.getBoundingClientRect();
    const svgX = ((event.clientX - bounds.left) / bounds.width) * model.width;
    const clampedX = Math.min(
      model.plot.left + model.plotWidth,
      Math.max(model.plot.left, svgX),
    );
    const timestamp =
      model.xMinimum +
      ((clampedX - model.plot.left) / model.plotWidth) *
        (model.xMaximum - model.xMinimum);
    const period =
      model.periods.find(
        (candidate) =>
          candidate.startTime <= timestamp && timestamp < candidate.endTime,
      ) ||
      model.periods.reduce((selected, candidate) =>
        Math.abs(candidate.startTime - timestamp) <
        Math.abs(selected.startTime - timestamp)
          ? candidate
          : selected,
      );
    const lineX = model.xScale(period.startTime);

    hoverLine.setAttribute("x1", lineX);
    hoverLine.setAttribute("x2", lineX);
    hoverLine.classList.add("visible");

    tooltip.innerHTML = `
      <strong>
        ${escapeHtml(this._formatDateTime(period.startTime))}
        – ${escapeHtml(this._formatTime(period.endTime))}
      </strong>
      ${model.components
        .map((component) => {
          const value = Number(period[component.key]);
          if (!Number.isFinite(value)) {
            return "";
          }
          return `
            <span>
              <i style="background: ${component.color}"></i>
              ${escapeHtml(componentLabel(component, this._hass))}
              <b>${escapeHtml(this._formatPrice(value))} CHF/kWh</b>
            </span>
          `;
        })
        .join("")}
    `;

    const renderedX = (lineX / model.width) * bounds.width;
    tooltip.style.left = `${renderedX}px`;
    tooltip.classList.toggle("align-right", renderedX > bounds.width * 0.65);
    tooltip.classList.add("visible");
  }

  _hideTooltip() {
    this.shadowRoot.querySelector(".tooltip")?.classList.remove("visible");
    this.shadowRoot.querySelector(".hover-line")?.classList.remove("visible");
  }

  _styles() {
    return `
      :host {
        display: block;
        --sdt-border: color-mix(
          in srgb,
          var(--primary-text-color) 14%,
          transparent
        );
        --sdt-muted: var(--secondary-text-color);
      }

      ha-card {
        overflow: hidden;
        padding: 22px;
        background:
          radial-gradient(
            circle at 100% 0%,
            color-mix(in srgb, var(--primary-color) 14%, transparent),
            transparent 34%
          ),
          var(--ha-card-background, var(--card-background-color));
      }

      .card-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 18px;
      }

      .card-header > ha-icon {
        --mdc-icon-size: 34px;
        color: var(--primary-color);
        padding: 10px;
        border-radius: 14px;
        background: color-mix(in srgb, var(--primary-color) 13%, transparent);
      }

      .eyebrow {
        color: var(--primary-color);
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      h2 {
        margin: 3px 0 2px;
        color: var(--primary-text-color);
        font-size: 1.35rem;
        line-height: 1.25;
      }

      .card-header p {
        margin: 0;
        color: var(--sdt-muted);
        font-size: 0.86rem;
      }

      .summary-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 9px;
        margin-bottom: 16px;
      }

      .summary-item {
        min-width: 0;
        display: flex;
        align-items: flex-start;
        gap: 9px;
        padding: 11px;
        border: 1px solid var(--sdt-border);
        border-radius: 13px;
        background: color-mix(
          in srgb,
          var(--card-background-color) 86%,
          transparent
        );
      }

      .summary-item ha-icon {
        --mdc-icon-size: 19px;
        flex: 0 0 auto;
        color: var(--primary-color);
      }

      .summary-item div {
        min-width: 0;
        display: flex;
        flex-direction: column;
      }

      .summary-item span,
      .summary-item small {
        overflow: hidden;
        color: var(--sdt-muted);
        font-size: 0.72rem;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .summary-item strong {
        overflow: hidden;
        margin: 2px 0;
        color: var(--primary-text-color);
        font-size: 0.9rem;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 14px;
        margin: 0 8px 5px 74px;
        color: var(--sdt-muted);
        font-size: 0.76rem;
      }

      .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }

      .legend-color {
        width: 9px;
        height: 9px;
        border-radius: 50%;
      }

      .chart-wrap {
        position: relative;
        width: 100%;
      }

      .chart {
        display: block;
        width: 100%;
        height: auto;
        min-height: 260px;
        overflow: visible;
      }

      .grid-line {
        stroke: var(--divider-color);
        stroke-width: 1;
        stroke-dasharray: 3 5;
      }

      .axis-line,
      .x-tick-line {
        stroke: color-mix(
          in srgb,
          var(--primary-text-color) 40%,
          transparent
        );
        stroke-width: 1;
      }

      .axis-tick,
      .axis-label,
      .annotation,
      .now-label {
        fill: var(--secondary-text-color);
        font-family: var(--paper-font-body1_-_font-family, sans-serif);
      }

      .axis-tick {
        font-size: 11px;
      }

      .y-tick {
        text-anchor: end;
      }

      .x-tick {
        text-anchor: middle;
      }

      .date-label {
        opacity: 0.72;
      }

      .axis-label {
        font-size: 12px;
        font-weight: 600;
        text-anchor: middle;
      }

      .price-line {
        fill: none;
        stroke-width: 3;
        stroke-linecap: round;
        stroke-linejoin: round;
        vector-effect: non-scaling-stroke;
      }

      .now-line {
        stroke: var(--primary-text-color);
        stroke-width: 1.5;
        stroke-dasharray: 5 4;
        opacity: 0.66;
      }

      .now-label {
        font-size: 11px;
        font-weight: 700;
        text-anchor: middle;
      }

      .annotation {
        paint-order: stroke;
        stroke: var(--card-background-color);
        stroke-width: 4px;
        stroke-linejoin: round;
        font-size: 11px;
        font-weight: 700;
      }

      .interaction-layer {
        fill: transparent;
        cursor: crosshair;
      }

      .hover-line {
        visibility: hidden;
        stroke: var(--primary-color);
        stroke-width: 1;
        opacity: 0.7;
        pointer-events: none;
      }

      .hover-line.visible {
        visibility: visible;
      }

      .tooltip {
        position: absolute;
        z-index: 2;
        top: 16px;
        display: none;
        min-width: 205px;
        padding: 10px 12px;
        border: 1px solid var(--sdt-border);
        border-radius: 11px;
        background: var(--card-background-color);
        box-shadow: var(
          --ha-card-box-shadow,
          0 4px 14px rgba(0, 0, 0, 0.18)
        );
        color: var(--primary-text-color);
        font-size: 0.76rem;
        pointer-events: none;
        transform: translateX(10px);
      }

      .tooltip.visible {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }

      .tooltip.align-right {
        transform: translateX(calc(-100% - 10px));
      }

      .tooltip strong {
        margin-bottom: 2px;
      }

      .tooltip span {
        display: grid;
        grid-template-columns: 9px 1fr auto;
        align-items: center;
        gap: 7px;
      }

      .tooltip i {
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }

      .tooltip b {
        font-weight: 700;
      }

      details {
        margin-top: 6px;
        border-top: 1px solid var(--sdt-border);
      }

      summary {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 15px 3px 2px;
        color: var(--primary-color);
        font-size: 0.84rem;
        font-weight: 600;
        cursor: pointer;
        list-style: none;
      }

      summary::-webkit-details-marker {
        display: none;
      }

      summary ha-icon {
        --mdc-icon-size: 18px;
      }

      .table-wrap {
        max-height: 330px;
        margin-top: 12px;
        overflow: auto;
        border: 1px solid var(--sdt-border);
        border-radius: 11px;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        color: var(--primary-text-color);
        font-size: 0.78rem;
        white-space: nowrap;
      }

      th,
      td {
        padding: 9px 11px;
        border-bottom: 1px solid var(--sdt-border);
        text-align: right;
      }

      th:first-child,
      td:first-child {
        position: sticky;
        left: 0;
        text-align: left;
        background: var(--card-background-color);
      }

      th {
        position: sticky;
        top: 0;
        z-index: 1;
        color: var(--sdt-muted);
        background: var(--card-background-color);
        font-weight: 700;
      }

      th:first-child {
        z-index: 2;
      }

      tr:last-child td {
        border-bottom: none;
      }

      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 210px;
        padding: 20px;
        color: var(--sdt-muted);
        text-align: center;
      }

      .empty-state ha-icon {
        --mdc-icon-size: 42px;
        margin-bottom: 10px;
        color: var(--primary-color);
        opacity: 0.7;
      }

      @media (max-width: 700px) {
        ha-card {
          padding: 17px 12px;
        }

        .summary-grid {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .legend {
          margin-left: 50px;
        }

        .chart {
          min-height: 220px;
        }
      }
    `;
  }
}

class SwissDynamicTariffsCardEditor extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = undefined;
    this._config = {};
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = { ...config };
    this._render();
  }

  _render() {
    if (!this._hass) {
      return;
    }

    const picker = document.createElement("ha-entity-picker");
    picker.hass = this._hass;
    picker.value = this._config.entity || "";
    picker.label = textFor(this._hass).chooseEntity;
    picker.includeDomains = ["sensor"];
    picker.allowCustomEntity = false;
    picker.addEventListener("value-changed", (event) => {
      if (!event.detail?.value) {
        return;
      }
      this._config = { ...this._config, entity: event.detail.value };
      this.dispatchEvent(
        new CustomEvent("config-changed", {
          bubbles: true,
          composed: true,
          detail: { config: this._config },
        }),
      );
    });

    this.shadowRoot.replaceChildren(picker);
  }
}

class SwissDynamicTariffsDashboardStrategy extends HTMLElement {
  static getCreateSuggestions(hass) {
    return {
      title: textFor(hass).dashboardTitle,
      icon: "mdi:chart-timeline-variant",
    };
  }

  static async generate(config, hass) {
    const text = textFor(hass);
    const entities = forecastEntities(hass);
    const cards = entities.map((state) => ({
      type: CARD_TYPE,
      entity: state.entity_id,
    }));

    return {
      title: config.title || text.dashboardTitle,
      views: [
        {
          title: text.dashboardTitle,
          path: "tariffs",
          icon: "mdi:chart-timeline-variant",
          cards: cards.length
            ? [
                {
                  type: "grid",
                  columns: 1,
                  square: false,
                  cards,
                },
              ]
            : [
                {
                  type: "markdown",
                  title: text.dashboardTitle,
                  content: text.noForecasts,
                },
              ],
        },
      ],
    };
  }
}

if (!customElements.get(CARD_TAG)) {
  customElements.define(CARD_TAG, SwissDynamicTariffsCard);
}

if (!customElements.get("swiss-dynamic-tariffs-card-editor")) {
  customElements.define(
    "swiss-dynamic-tariffs-card-editor",
    SwissDynamicTariffsCardEditor,
  );
}

const strategyTag = `ll-strategy-dashboard-${STRATEGY_TYPE}`;
if (!customElements.get(strategyTag)) {
  customElements.define(strategyTag, SwissDynamicTariffsDashboardStrategy);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === CARD_TAG)) {
  window.customCards.push({
    type: CARD_TAG,
    name: "Swiss Dynamic Tariffs – Tariff forecast",
    description:
      "Interactive timeline for future quarter-hour electricity prices.",
    preview: true,
    getEntitySuggestion: (hass, entityId) => {
      if (!isForecastState(hass.states[entityId])) {
        return null;
      }
      return {
        config: {
          type: CARD_TYPE,
          entity: entityId,
        },
      };
    },
  });
}

window.customStrategies = window.customStrategies || [];
if (
  !window.customStrategies.some(
    (strategy) =>
      strategy.type === STRATEGY_TYPE && strategy.strategyType === "dashboard",
  )
) {
  window.customStrategies.push({
    type: STRATEGY_TYPE,
    strategyType: "dashboard",
    name: "Swiss Dynamic Tariffs",
    description: "Automatic price charts for all tariff forecasts.",
    documentationURL:
      "https://github.com/ehnid/swiss-dynamic-tariffs#dashboard-visualization",
  });
}
