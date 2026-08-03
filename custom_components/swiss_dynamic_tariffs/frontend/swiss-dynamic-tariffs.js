const CARD_TAG = "swiss-dynamic-tariffs-card";
const CARD_TYPE = `custom:${CARD_TAG}`;
const STRATEGY_TYPE = "swiss-dynamic-tariffs";
const FRONTEND_VERSION = "0.5.9";
const DASHBOARD_PANEL_TAG = "swiss-dynamic-tariffs-panel";
const PANEL_TAG = `swiss-dynamic-tariffs-panel-${FRONTEND_VERSION.replaceAll(
  ".",
  "-",
)}`;
const PANEL_CARD_TAG = `${PANEL_TAG}-card`;
const AXIS_EXTENT_EVENT = "swiss-dynamic-tariffs-axis-extent";
const FORECAST_ATTRIBUTES = ["prices", "available_from", "available_until"];
const QUARTER_HOUR_MS = 15 * 60 * 1000;
const PRICE_GRID_STEP = 0.1;
const NEGATIVE_AXIS_STEP = 0.05;
const ROUNDING_EPSILON = 1e-9;

const COMPONENTS = [
  {
    key: "integrated",
    color: "#8b5cf6",
    labels: {
      de: "Gesamtpreis",
      en: "Total price",
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
      en: "Feed-in remuneration",
      fr: "Rétribution de l’injection",
      it: "Remunerazione per l’immissione",
    },
  },
];

const TEXT = {
  de: {
    title: "Tarifprognose",
    dashboardTitle: "Dynamische Stromtarife",
    dashboardDescription:
      "Automatische Preisdiagramme für alle Tarifprognosen.",
    cardPickerName: "Swiss Dynamic Tariffs – Tarifprognose",
    cardPickerDescription:
      "Interaktive Zeitleiste für aufgezeichnete und prognostizierte Viertelstundenpreise.",
    strategyDescription:
      "Automatische Diagramme für aufgezeichnete und prognostizierte Tarifpreise.",
    noData: "Noch keine zukünftigen Tarifdaten verfügbar.",
    noDataForDay: "Für diesen Tag sind keine Tarifdaten verfügbar.",
    unavailable: "Der Tarifprognose-Sensor ist nicht verfügbar.",
    chooseEntity: "Tarifprognose-Sensor",
    priceAxis: "Preis [CHF/kWh]",
    timeAxis: "Zeit",
    legend: "Legende",
    current: "Aktueller Wert",
    next: "Nächster Wert",
    minimum: "Minimum",
    maximum: "Maximum",
    period: "Verfügbarer Zeitraum",
    until: "bis",
    periods: "Viertelstunden",
    now: "Jetzt",
    today: "Heute",
    tomorrow: "Morgen",
    selectDay: "Tag auswählen",
    first: "Erster Wert",
    showData: "Viertelstundenwerte anzeigen",
    time: "Zeitfenster",
    noForecasts:
      "Noch keine Tarifprognose gefunden. Richten Sie zuerst einen dynamischen Tarif ein.",
  },
  en: {
    title: "Tariff forecast",
    dashboardTitle: "Dynamic electricity tariffs",
    dashboardDescription: "Automatic price charts for all tariff forecasts.",
    cardPickerName: "Swiss Dynamic Tariffs – Tariff forecast",
    cardPickerDescription:
      "Interactive timeline for recorded and forecast quarter-hour prices.",
    strategyDescription:
      "Automatic charts for recorded and forecast tariff prices.",
    noData: "No future tariff data is available yet.",
    noDataForDay: "No tariff data is available for this day.",
    unavailable: "The tariff forecast sensor is unavailable.",
    chooseEntity: "Tariff forecast sensor",
    priceAxis: "Price [CHF/kWh]",
    timeAxis: "Time",
    legend: "Legend",
    current: "Current value",
    next: "Next value",
    minimum: "Minimum",
    maximum: "Maximum",
    period: "Available period",
    until: "to",
    periods: "quarter-hours",
    now: "Now",
    today: "Today",
    tomorrow: "Tomorrow",
    selectDay: "Select a day",
    first: "First value",
    showData: "Show quarter-hour values",
    time: "Time window",
    noForecasts: "No tariff forecast found yet. Set up a dynamic tariff first.",
  },
  fr: {
    title: "Prévision tarifaire",
    dashboardTitle: "Tarifs dynamiques de l’électricité",
    dashboardDescription:
      "Graphiques automatiques pour toutes les prévisions tarifaires.",
    cardPickerName: "Swiss Dynamic Tariffs – Prévision tarifaire",
    cardPickerDescription:
      "Graphique chronologique interactif des prix quart-horaires enregistrés et prévisionnels.",
    strategyDescription:
      "Graphiques automatiques des tarifs enregistrés et prévisionnels.",
    noData: "Aucune donnée tarifaire future n’est encore disponible.",
    noDataForDay: "Aucune donnée tarifaire n’est disponible pour ce jour.",
    unavailable: "Le capteur de prévision tarifaire n’est pas disponible.",
    chooseEntity: "Capteur de prévision tarifaire",
    priceAxis: "Prix [CHF/kWh]",
    timeAxis: "Heure",
    legend: "Légende",
    current: "Valeur actuelle",
    next: "Valeur suivante",
    minimum: "Minimum",
    maximum: "Maximum",
    period: "Période disponible",
    until: "à",
    periods: "quarts d’heure",
    now: "Maintenant",
    today: "Aujourd’hui",
    tomorrow: "Demain",
    selectDay: "Sélectionner un jour",
    first: "Première valeur",
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
    cardPickerName: "Swiss Dynamic Tariffs – Previsione tariffaria",
    cardPickerDescription:
      "Grafico temporale interattivo dei prezzi quartorari registrati e previsti.",
    strategyDescription:
      "Grafici automatici dei prezzi tariffari registrati e previsti.",
    noData: "Non sono ancora disponibili dati tariffari futuri.",
    noDataForDay: "Non sono disponibili dati tariffari per questo giorno.",
    unavailable: "Il sensore della previsione tariffaria non è disponibile.",
    chooseEntity: "Sensore della previsione tariffaria",
    priceAxis: "Prezzo [CHF/kWh]",
    timeAxis: "Ora",
    legend: "Legenda",
    current: "Valore attuale",
    next: "Valore successivo",
    minimum: "Minimo",
    maximum: "Massimo",
    period: "Periodo disponibile",
    until: "a",
    periods: "quarti d’ora",
    now: "Adesso",
    today: "Oggi",
    tomorrow: "Domani",
    selectDay: "Seleziona il giorno",
    first: "Primo valore",
    showData: "Mostra i valori ogni quarto d’ora",
    time: "Intervallo",
    noForecasts:
      "Nessuna previsione tariffaria trovata. Configura prima una tariffa dinamica.",
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

function textForBrowser() {
  const language =
    typeof navigator === "undefined" ? "en" : navigator.language || "en";
  const shortLanguage = language.split("-")[0].toLowerCase();
  return TEXT[shortLanguage] || TEXT.en;
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

/**
 * Find current-price sensors by stable integration metadata.
 *
 * Entity IDs and friendly names are user-editable, so neither is suitable for
 * linking a forecast card to the sensors whose Recorder history it needs.
 */
function currentPriceEntities(hass, forecastState) {
  const entryId = forecastState?.attributes?.tariff_entry_id;
  if (!entryId) {
    return {};
  }

  return Object.values(hass?.states || {}).reduce((entities, state) => {
    const attributes = state.attributes || {};
    if (
      attributes.tariff_entry_id === entryId &&
      attributes.tariff_role === "current_price" &&
      COMPONENTS.some(
        (component) => component.key === attributes.tariff_component,
      )
    ) {
      entities[attributes.tariff_component] = state.entity_id;
    }
    return entities;
  }, {});
}

/**
 * Convert Recorder states into the same period shape used by the forecast.
 *
 * Live states are included because Recorder writes can lag slightly behind the
 * active quarter-hour. States outside today's Home Assistant calendar date are
 * deliberately ignored.
 */
function parseHistoryPeriods(
  historyResponse,
  componentEntities,
  currentStates,
  todayKey,
  timeZone,
) {
  const entityComponents = Object.fromEntries(
    Object.entries(componentEntities).map(([component, entityId]) => [
      entityId,
      component,
    ]),
  );
  const recordedStates = Array.isArray(historyResponse)
    ? historyResponse.flat()
    : [];
  const liveStates = Object.values(componentEntities)
    .map((entityId) => currentStates?.[entityId])
    .filter(Boolean);
  const exactPeriods = new Map();
  const historyEvents = new Map();
  const now = Date.now();
  const dayStart = calendarDateStart(todayKey, timeZone);
  const dayEnd = calendarDateStart(shiftCalendarDateKey(todayKey, 1), timeZone);

  for (const state of [...recordedStates, ...liveStates]) {
    const component = entityComponents[state.entity_id];
    const attributes = state.attributes || {};
    const startTime = Date.parse(attributes.start);
    const endTime = Date.parse(attributes.end);
    const value = Number(state.state);
    const updatedTime = Date.parse(state.last_updated || state.last_changed);

    if (component && Number.isFinite(updatedTime)) {
      const events = historyEvents.get(component) || [];
      events.push({
        timestamp: updatedTime,
        value: Number.isFinite(value) ? value : null,
      });
      historyEvents.set(component, events);
    }

    if (
      !component ||
      !Number.isFinite(startTime) ||
      !Number.isFinite(endTime) ||
      !Number.isFinite(value) ||
      startTime > now ||
      endTime <= startTime ||
      startTime >= dayEnd ||
      endTime <= dayStart
    ) {
      continue;
    }

    const key = `${startTime}:${endTime}`;
    const period = exactPeriods.get(key) || {
      start: attributes.start,
      end: attributes.end,
      startTime,
      endTime,
    };
    period[component] = value;
    exactPeriods.set(key, period);
  }

  /*
   * Releases before 0.5.0 did not record exact period boundaries. Reconstruct
   * their held sensor states on a quarter-hour grid so an update does not make
   * all earlier values from the same day disappear. Exact attributes, when
   * present, are merged afterwards and therefore remain authoritative.
   */
  const inferredPeriods = new Map();
  const historyEnd = Math.min(now, dayEnd);
  for (const [component, events] of historyEvents) {
    events.sort((left, right) => left.timestamp - right.timestamp);
    let eventIndex = 0;
    let activeValue = null;

    while (
      eventIndex < events.length &&
      events[eventIndex].timestamp < dayStart
    ) {
      activeValue = events[eventIndex].value;
      eventIndex += 1;
    }

    for (
      let startTime = dayStart;
      startTime < historyEnd;
      startTime += QUARTER_HOUR_MS
    ) {
      while (
        eventIndex < events.length &&
        Math.floor(events[eventIndex].timestamp / QUARTER_HOUR_MS) *
          QUARTER_HOUR_MS <=
          startTime
      ) {
        activeValue = events[eventIndex].value;
        eventIndex += 1;
      }

      if (!Number.isFinite(activeValue)) {
        continue;
      }

      const endTime = Math.min(startTime + QUARTER_HOUR_MS, dayEnd);
      const key = `${startTime}:${endTime}`;
      const period = inferredPeriods.get(key) || {
        start: new Date(startTime).toISOString(),
        end: new Date(endTime).toISOString(),
        startTime,
        endTime,
      };
      period[component] = activeValue;
      inferredPeriods.set(key, period);
    }
  }

  return mergePeriods(
    [...inferredPeriods.values()],
    [...exactPeriods.values()],
  );
}

/**
 * Merge equal time windows without creating duplicate chart points.
 *
 * Later sources win component by component. Callers pass history first and the
 * latest provider forecast second, making fresh provider data authoritative.
 */
function mergePeriods(...periodSets) {
  const periods = new Map();
  for (const period of periodSets.flat()) {
    const key = `${period.startTime}:${period.endTime}`;
    periods.set(key, { ...(periods.get(key) || {}), ...period });
  }
  return [...periods.values()].sort(
    (left, right) => left.startTime - right.startTime,
  );
}

function calendarDateKey(timestamp, timeZone) {
  const parts = new Intl.DateTimeFormat("en", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date(timestamp));
  const value = (type) => parts.find((part) => part.type === type)?.value;
  return `${value("year")}-${value("month")}-${value("day")}`;
}

function shiftCalendarDateKey(dateKey, days) {
  const [year, month, day] = dateKey.split("-").map(Number);
  const shifted = new Date(Date.UTC(year, month - 1, day + days));
  return [
    shifted.getUTCFullYear(),
    String(shifted.getUTCMonth() + 1).padStart(2, "0"),
    String(shifted.getUTCDate()).padStart(2, "0"),
  ].join("-");
}

/**
 * Resolve midnight for a Home Assistant calendar date in its configured zone.
 *
 * Date.parse("YYYY-MM-DD") always means UTC, which is not midnight in
 * Europe/Zurich. Iterating the formatted wall-clock difference avoids a
 * dependency on the browser's own timezone and also handles DST transitions.
 */
function calendarDateStart(dateKey, timeZone) {
  const [year, month, day] = dateKey.split("-").map(Number);
  const targetWallTime = Date.UTC(year, month - 1, day);
  const formatter = new Intl.DateTimeFormat("en", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  });
  let timestamp = targetWallTime;

  for (let attempt = 0; attempt < 3; attempt += 1) {
    const parts = formatter.formatToParts(new Date(timestamp));
    const value = (type) =>
      Number(parts.find((part) => part.type === type)?.value);
    const representedWallTime = Date.UTC(
      value("year"),
      value("month") - 1,
      value("day"),
      value("hour"),
      value("minute"),
      value("second"),
    );
    const correction = targetWallTime - representedWallTime;
    timestamp += correction;
    if (correction === 0) {
      break;
    }
  }

  return timestamp;
}

function calendarDayDifference(startDateKey, endDateKey) {
  const toUtc = (dateKey) => {
    const [year, month, day] = dateKey.split("-").map(Number);
    return Date.UTC(year, month - 1, day);
  };
  return Math.round(
    (toUtc(endDateKey) - toUtc(startDateKey)) / (24 * 60 * 60 * 1000),
  );
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

function priceAxisBounds(values) {
  const finiteValues = values.map(Number).filter(Number.isFinite);
  if (!finiteValues.length) {
    return { minimum: 0, maximum: PRICE_GRID_STEP };
  }

  const rawMinimum = Math.min(...finiteValues);
  const rawMaximum = Math.max(...finiteValues);
  const minimum =
    rawMinimum < 0
      ? Math.floor((rawMinimum + ROUNDING_EPSILON) / NEGATIVE_AXIS_STEP) *
        NEGATIVE_AXIS_STEP
      : 0;
  let maximum =
    rawMaximum > 0
      ? Math.ceil((rawMaximum - ROUNDING_EPSILON) / PRICE_GRID_STEP) *
        PRICE_GRID_STEP
      : 0;

  if (maximum <= minimum) {
    maximum = minimum + PRICE_GRID_STEP;
  }

  return {
    minimum: Number(minimum.toFixed(10)),
    maximum: Number(maximum.toFixed(10)),
  };
}

function priceGridTicks(minimum, maximum) {
  const ticks = [0];

  for (
    let value = PRICE_GRID_STEP;
    value <= maximum + ROUNDING_EPSILON;
    value += PRICE_GRID_STEP
  ) {
    ticks.push(Number(value.toFixed(10)));
  }

  for (
    let value = -PRICE_GRID_STEP;
    value >= minimum - ROUNDING_EPSILON;
    value -= PRICE_GRID_STEP
  ) {
    ticks.push(Number(value.toFixed(10)));
  }

  return ticks.sort((left, right) => left - right);
}

function equalAxisBounds(left, right) {
  return left?.minimum === right?.minimum && left?.maximum === right?.maximum;
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

function timeTicks(minimum, maximum, count) {
  return Array.from(
    { length: count },
    (_, index) => minimum + ((maximum - minimum) * index) / (count - 1),
  );
}

function chartDimensions(measuredHostWidth) {
  // The first render happens before a dashboard overview card is attached.
  // A moderate fallback is replaced immediately by ResizeObserver.
  const hostWidth = measuredHostWidth > 0 ? measuredHostWidth : 560;
  const compact = hostWidth <= 600;
  const horizontalPadding = compact ? 24 : 44;
  const width = Math.max(280, hostWidth - horizontalPadding);
  const height = Math.round(
    Math.max(
      compact ? 240 : 250,
      Math.min(compact ? 300 : 320, width * (compact ? 0.72 : 0.55)),
    ),
  );
  const plot = compact
    ? { left: 62, right: 12, top: 24, bottom: 54 }
    : { left: 78, right: 20, top: 24, bottom: 58 };

  return { compact, width, height, plot };
}

function desktopCardWidth(screenWidth) {
  const width = Number(screenWidth);
  return Number.isFinite(width) && width > 0 ? Math.round(width * 0.4) : 480;
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
    this._detailsOpen = false;
    this._selectedDayOffset = 0;
    this._historyPeriods = [];
    this._historyLoadingKey = undefined;
    this._historyLoadedKey = undefined;
    this._historyRetryAfter = 0;
    this._renderedHostWidth = undefined;
    this._sharedYAxis = undefined;
    this._resizeObserver =
      typeof ResizeObserver === "undefined"
        ? undefined
        : new ResizeObserver(([entry]) => {
            const hostWidth = Math.round(entry.contentRect.width);
            if (
              hostWidth > 0 &&
              Math.abs(hostWidth - (this._renderedHostWidth || 0)) >= 8
            ) {
              this._renderedHostWidth = hostWidth;
              this._render();
            }
          });
  }

  connectedCallback() {
    if (this._resizeObserver) {
      this._resizeObserver.observe(this);
      return;
    }

    /*
     * Older companion-app WebViews may not expose ResizeObserver. Measure once
     * after attachment so the card remains usable instead of failing entirely.
     */
    requestAnimationFrame(() => {
      this._renderedHostWidth = Math.round(this.getBoundingClientRect().width);
      this._render();
    });
  }

  disconnectedCallback() {
    this._resizeObserver?.disconnect();
  }

  setConfig(config) {
    if (!config?.entity) {
      throw new Error("Please select a tariff forecast sensor.");
    }

    this._config = { ...config };
    this._scheduleHistoryLoad();
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._scheduleHistoryLoad();
    this._render();
  }

  set sharedYAxis(bounds) {
    const nextBounds =
      bounds &&
      Number.isFinite(bounds.minimum) &&
      Number.isFinite(bounds.maximum) &&
      bounds.maximum > bounds.minimum
        ? { minimum: bounds.minimum, maximum: bounds.maximum }
        : undefined;
    if (equalAxisBounds(this._sharedYAxis, nextBounds)) {
      return;
    }
    this._sharedYAxis = nextBounds;
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

  _formatAxisPrice(value) {
    return new Intl.NumberFormat(languageFromHass(this._hass), {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  }

  _formatDateTime(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      timeZone: this._hass.config.time_zone,
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp));
  }

  _formatTime(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      timeZone: this._hass.config.time_zone,
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp));
  }

  _formatDate(timestamp) {
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      timeZone: this._hass.config.time_zone,
      day: "2-digit",
      month: "2-digit",
    }).format(new Date(timestamp));
  }

  _formatCalendarDay(dateKey) {
    const [year, month, day] = dateKey.split("-").map(Number);
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      timeZone: "UTC",
      weekday: "short",
      day: "2-digit",
      month: "2-digit",
    }).format(new Date(Date.UTC(year, month - 1, day, 12)));
  }

  _formatCalendarWeekday(dateKey) {
    const [year, month, day] = dateKey.split("-").map(Number);
    return new Intl.DateTimeFormat(languageFromHass(this._hass), {
      timeZone: "UTC",
      weekday: "long",
    }).format(new Date(Date.UTC(year, month - 1, day, 12)));
  }

  _scheduleHistoryLoad() {
    if (!this._hass || !this._config?.entity) {
      return;
    }

    const state = this._hass.states[this._config.entity];
    const componentEntities = currentPriceEntities(this._hass, state);
    const entityIds = Object.values(componentEntities).sort();
    if (!entityIds.length || typeof this._hass.callApi !== "function") {
      this._historyPeriods = [];
      return;
    }

    const timeZone = this._hass.config.time_zone;
    const todayKey = calendarDateKey(Date.now(), timeZone);
    const currentPeriodKeys = entityIds.map((entityId) => {
      const currentState = this._hass.states[entityId];
      return `${entityId}:${
        currentState?.attributes?.start ||
        currentState?.last_updated ||
        currentState?.state ||
        ""
      }`;
    });
    const requestKey = `${todayKey}:${currentPeriodKeys.join("|")}`;
    // Home Assistant pushes state updates frequently. Reload history only when
    // the date, linked entities or active quarter-hour changes.
    if (
      requestKey === this._historyLoadingKey ||
      requestKey === this._historyLoadedKey ||
      Date.now() < this._historyRetryAfter
    ) {
      return;
    }

    this._historyLoadingKey = requestKey;
    this._loadHistory(componentEntities, todayKey, timeZone)
      .then((periods) => {
        if (this._historyLoadingKey !== requestKey) {
          return;
        }
        this._historyPeriods = periods;
        this._historyLoadedKey = requestKey;
        this._historyLoadingKey = undefined;
        this._historyRetryAfter = 0;
        this._render();
      })
      .catch((error) => {
        if (this._historyLoadingKey === requestKey) {
          this._historyLoadingKey = undefined;
          this._historyRetryAfter = Date.now() + 60_000;
        }
        console.warn("Swiss Dynamic Tariffs could not load history", error);
      });
  }

  async _loadHistory(componentEntities, todayKey, timeZone) {
    const now = new Date();
    const historyStart = new Date(calendarDateStart(todayKey, timeZone));
    const entityIds = Object.values(componentEntities);
    const path =
      `history/period/${encodeURIComponent(historyStart.toISOString())}` +
      `?filter_entity_id=${encodeURIComponent(entityIds.join(","))}` +
      `&end_time=${encodeURIComponent(now.toISOString())}` +
      "&significant_changes_only=0";
    const response = await this._hass.callApi("GET", path);
    return parseHistoryPeriods(
      response,
      componentEntities,
      this._hass.states,
      todayKey,
      timeZone,
    );
  }

  _renderDayNavigation(dayOptions) {
    return dayOptions
      .map(
        (option) => `
          <button
            type="button"
            class="day-button ${
              option.offset === this._selectedDayOffset ? "active" : ""
            }"
            data-day-offset="${option.offset}"
            role="tab"
            aria-selected="${
              option.offset === this._selectedDayOffset ? "true" : "false"
            }"
          >
            <span>${escapeHtml(option.label)}</span>
            <strong>${escapeHtml(
              this._formatCalendarDay(option.dateKey),
            )}</strong>
          </button>
        `,
      )
      .join("");
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
    this._publishAxisExtent();
  }

  _emptyDayCard(title, selectedDay, dayNavigation, message) {
    const text = textFor(this._hass);

    this.shadowRoot.innerHTML = `
      <style>${this._styles()}</style>
      <ha-card>
        <div class="card-header">
          <div>
            <div class="eyebrow">Swiss Dynamic Tariffs</div>
            <h2>${escapeHtml(title)}</h2>
            <p>${escapeHtml(this._formatCalendarDay(selectedDay.dateKey))}</p>
          </div>
          <ha-icon icon="mdi:chart-timeline-variant"></ha-icon>
        </div>
        <div
          class="day-navigation"
          role="tablist"
          aria-label="${escapeHtml(text.selectDay)}"
        >
          ${dayNavigation}
        </div>
        <div class="empty-state">
          <ha-icon icon="mdi:calendar-alert"></ha-icon>
          <p>${escapeHtml(message)}</p>
        </div>
      </ha-card>
    `;
    this._bindDayNavigation();
    this._publishAxisExtent();
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) {
      return;
    }

    const existingDetails = this.shadowRoot.querySelector("details");
    if (existingDetails) {
      this._detailsOpen = existingDetails.open;
    }

    const text = textFor(this._hass);
    const state = this._hass.states[this._config.entity];
    if (!state || ["unknown", "unavailable"].includes(state.state)) {
      this._emptyCard(text.unavailable);
      return;
    }

    const allPeriods = mergePeriods(this._historyPeriods, parsePeriods(state));
    const timeZone = this._hass.config.time_zone;
    const todayKey = calendarDateKey(Date.now(), timeZone);
    // Always expose today and tomorrow, then add every further date actually
    // supplied by a provider instead of imposing a 24-hour horizon.
    const dayOffsets = [
      ...new Set([
        0,
        1,
        ...allPeriods
          .map((period) =>
            calendarDayDifference(
              todayKey,
              calendarDateKey(period.startTime, timeZone),
            ),
          )
          .filter((offset) => offset >= 0),
      ]),
    ].sort((left, right) => left - right);
    const dayOptions = dayOffsets.map((offset) => {
      const dateKey = shiftCalendarDateKey(todayKey, offset);
      const periods = allPeriods.filter(
        (period) => calendarDateKey(period.startTime, timeZone) === dateKey,
      );
      return {
        offset,
        dateKey,
        periods,
        label:
          offset === 0
            ? text.today
            : offset === 1
              ? text.tomorrow
              : this._formatCalendarWeekday(dateKey),
      };
    });
    let selectedDay = dayOptions.find(
      (option) => option.offset === this._selectedDayOffset,
    );
    if (!selectedDay) {
      selectedDay = dayOptions[0];
      this._selectedDayOffset = selectedDay.offset;
    }
    const title =
      this._config.title || state.attributes.friendly_name || text.title;
    const dayNavigation = this._renderDayNavigation(dayOptions);
    if (!selectedDay.periods.length) {
      this._emptyDayCard(
        title,
        selectedDay,
        dayNavigation,
        allPeriods.length ? text.noDataForDay : text.noData,
      );
      return;
    }

    const periods = selectedDay.periods;
    const components = availableComponents(periods, this._config.components);
    if (!components.length) {
      this._emptyCard(text.noData);
      return;
    }

    const measuredHostWidth =
      this._renderedHostWidth || Math.round(this.getBoundingClientRect().width);
    const { compact, width, height, plot } = chartDimensions(measuredHostWidth);
    const plotWidth = width - plot.left - plot.right;
    const plotHeight = height - plot.top - plot.bottom;
    const xMinimum = periods[0].startTime;
    const xMaximum = periods[periods.length - 1].endTime;
    const values = priceValues(periods, components);
    const rawMinimum = Math.min(...values);
    const rawMaximum = Math.max(...values);
    const localYAxis = priceAxisBounds(values);
    const { minimum: yMinimum, maximum: yMaximum } =
      this._sharedYAxis || localYAxis;
    const xScale = (timestamp) =>
      plot.left + ((timestamp - xMinimum) / (xMaximum - xMinimum)) * plotWidth;
    const yScale = (value) =>
      plot.top + ((yMaximum - value) / (yMaximum - yMinimum)) * plotHeight;
    const yTicks = priceGridTicks(yMinimum, yMaximum);
    const xTicks = timeTicks(xMinimum, xMaximum, compact ? 4 : 6);
    const primaryComponent = components[0];
    const primaryPeriods = periods.filter((period) =>
      Number.isFinite(Number(period[primaryComponent.key])),
    );
    const now = Date.now();
    const activePeriod = primaryPeriods.find(
      (period) => period.startTime <= now && now < period.endTime,
    );
    const headlinePeriod = activePeriod || primaryPeriods[0];
    const headlineLabel = activePeriod
      ? text.current
      : this._selectedDayOffset === 0
        ? text.next
        : text.first;
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
    const coverageHours = (xMaximum - xMinimum) / 3_600_000;

    const gridLines = yTicks
      .map((tick) => {
        const y = yScale(tick);
        return `
          <line class="grid-line ${
            Math.abs(tick) < ROUNDING_EPSILON ? "zero-line" : ""
          }" x1="${plot.left}" y1="${y}" x2="${
            width - plot.right
          }" y2="${y}"></line>
          <text class="axis-tick y-tick" x="${plot.left - 12}" y="${
            y + 4
          }">${escapeHtml(this._formatAxisPrice(tick))}</text>
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
        label: headlineLabel,
        value: `${this._formatPrice(
          Number(headlinePeriod[primaryComponent.key]),
        )} CHF/kWh`,
        detail: this._formatTime(headlinePeriod.startTime),
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

        <div
          class="day-navigation"
          role="tablist"
          aria-label="${escapeHtml(text.selectDay)}"
        >
          ${dayNavigation}
        </div>

        <div class="summary-grid">${summary}</div>
        <div class="legend" aria-label="${escapeHtml(
          text.legend,
        )}">${legend}</div>

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

        <details ${this._detailsOpen ? "open" : ""}>
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
    this._bindDayNavigation();
    this._bindChartInteractions();
    this._bindDetailsInteraction();
    this._publishAxisExtent({ minimum: rawMinimum, maximum: rawMaximum });
  }

  _publishAxisExtent(extent) {
    this.dispatchEvent(
      new CustomEvent(AXIS_EXTENT_EVENT, {
        bubbles: false,
        detail: extent || null,
      }),
    );
  }

  _bindDayNavigation() {
    for (const button of this.shadowRoot.querySelectorAll(".day-button")) {
      button.addEventListener("click", () => {
        const offset = Number(button.dataset.dayOffset);
        if (
          Number.isInteger(offset) &&
          offset !== this._selectedDayOffset &&
          !button.disabled
        ) {
          this._selectedDayOffset = offset;
          this._render();
        }
      });
    }
  }

  _bindChartInteractions() {
    const chart = this.shadowRoot.querySelector(".chart");
    if (!chart) {
      return;
    }

    chart.addEventListener("pointermove", (event) => this._showTooltip(event));
    chart.addEventListener("pointerleave", () => this._hideTooltip());
  }

  _bindDetailsInteraction() {
    const details = this.shadowRoot.querySelector("details");
    details?.addEventListener("toggle", () => {
      this._detailsOpen = details.open;
    });
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
        padding: 18px;
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
        margin-bottom: 14px;
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

      .day-navigation {
        display: flex;
        width: fit-content;
        max-width: 100%;
        box-sizing: border-box;
        gap: 4px;
        margin: 0 0 16px;
        padding: 4px;
        overflow-x: auto;
        border: 1px solid var(--sdt-border);
        border-radius: 14px;
        background: color-mix(
          in srgb,
          var(--primary-text-color) 5%,
          transparent
        );
        scrollbar-width: thin;
      }

      .day-button {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
        flex: 0 0 auto;
        min-width: 116px;
        padding: 8px 13px;
        border: 0;
        border-radius: 10px;
        color: var(--sdt-muted);
        background: transparent;
        font: inherit;
        text-align: left;
        cursor: pointer;
      }

      .day-button span {
        font-size: 0.72rem;
        font-weight: 600;
      }

      .day-button strong {
        color: var(--primary-text-color);
        font-size: 0.86rem;
      }

      .day-button.active {
        color: var(--primary-color);
        background: var(--card-background-color);
        box-shadow: 0 1px 5px color-mix(in srgb, #000 18%, transparent);
      }

      .day-button.active strong {
        color: var(--primary-color);
      }

      .day-button:focus-visible {
        outline: 2px solid var(--primary-color);
        outline-offset: 1px;
      }

      .summary-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
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
        width: 100%;
        box-sizing: border-box;
        gap: 8px 14px;
        margin: 0 auto 5px;
        padding-left: 66px;
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
        margin: 0 auto;
      }

      .chart {
        display: block;
        width: 100%;
        height: auto;
        overflow: visible;
      }

      .grid-line {
        stroke: var(--divider-color);
        stroke-width: 1;
        stroke-dasharray: 3 5;
      }

      .grid-line.zero-line {
        stroke: color-mix(
          in srgb,
          var(--primary-text-color) 76%,
          transparent
        );
        stroke-width: 2.5;
        stroke-dasharray: none;
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
        min-height: 44px;
        box-sizing: border-box;
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
          padding: 14px 10px;
        }

        .day-navigation {
          width: 100%;
        }

        .legend {
          padding-left: 52px;
        }

        .card-header > ha-icon {
          --mdc-icon-size: 28px;
          padding: 8px;
        }
      }
    `;
  }
}

/*
 * The Custom Elements registry forbids registering the same constructor under
 * two names. A distinct subclass keeps the public Lovelace card tag stable
 * while allowing the dashboard's internal card to be versioned for caching.
 */
class SwissDynamicTariffsPanelCard extends SwissDynamicTariffsCard {}

class SwissDynamicTariffsPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = undefined;
    this._panel = undefined;
    this._narrow = false;
    this._renderedKey = undefined;
    this._cards = new Map();
    this._axisExtents = new Map();
    this._sharedYAxis = undefined;
    this._handleWindowResize = () => this._updateResponsiveCardWidth();
  }

  connectedCallback() {
    this._updateResponsiveCardWidth();
    window.addEventListener("resize", this._handleWindowResize);
  }

  disconnectedCallback() {
    window.removeEventListener("resize", this._handleWindowResize);
  }

  _updateResponsiveCardWidth() {
    const screenWidth = window.screen?.width || window.innerWidth;
    this.style.setProperty(
      "--sdt-desktop-card-width",
      `${desktopCardWidth(screenWidth)}px`,
    );
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  set panel(panel) {
    this._panel = panel;
    this._render();
  }

  set narrow(narrow) {
    this._narrow = narrow;
    this.toggleAttribute("narrow", narrow);
  }

  set route(route) {
    this._route = route;
  }

  setConfig(config) {
    this._config = config;
  }

  _updateSharedYAxis(entityId, extent) {
    if (
      extent &&
      Number.isFinite(extent.minimum) &&
      Number.isFinite(extent.maximum)
    ) {
      this._axisExtents.set(entityId, extent);
    } else {
      this._axisExtents.delete(entityId);
    }

    const sharedYAxis = this._axisExtents.size
      ? priceAxisBounds(
          [...this._axisExtents.values()].flatMap((value) => [
            value.minimum,
            value.maximum,
          ]),
        )
      : undefined;
    if (equalAxisBounds(this._sharedYAxis, sharedYAxis)) {
      return;
    }

    this._sharedYAxis = sharedYAxis;
    for (const card of this._cards.values()) {
      card.sharedYAxis = sharedYAxis;
    }
  }

  _render() {
    if (!this._hass) {
      return;
    }

    const text = textFor(this._hass);
    const entities = forecastEntities(this._hass);
    const renderedKey = `${languageFromHass(this._hass)}:${entities
      .map((state) => state.entity_id)
      .join(",")}`;

    if (renderedKey === this._renderedKey) {
      for (const card of this._cards.values()) {
        card.hass = this._hass;
      }
      return;
    }

    this._renderedKey = renderedKey;
    this._cards.clear();
    this._axisExtents.clear();
    this._sharedYAxis = undefined;
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          box-sizing: border-box;
          min-height: 100%;
          padding: 24px;
          background:
            radial-gradient(
              circle at 8% 0%,
              color-mix(in srgb, var(--primary-color) 13%, transparent),
              transparent 32rem
            ),
            var(--primary-background-color);
        }

        main {
          width: 100%;
          max-width: 1800px;
          margin: 0 auto;
        }

        header {
          margin: 4px 2px 24px;
        }

        .eyebrow {
          margin-bottom: 5px;
          color: var(--primary-color);
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 0.09em;
          text-transform: uppercase;
        }

        h1 {
          margin: 0;
          color: var(--primary-text-color);
          font-size: clamp(25px, 4vw, 38px);
          line-height: 1.15;
        }

        header p {
          max-width: 700px;
          margin: 8px 0 0;
          color: var(--secondary-text-color);
          font-size: 15px;
          line-height: 1.5;
        }

        .cards {
          display: flex;
          flex-wrap: wrap;
          align-items: flex-start;
          justify-content: center;
          gap: 24px;
        }

        .cards > * {
          width: min(var(--sdt-desktop-card-width, 480px), 100%);
          min-width: min(420px, 100%);
          max-width: var(--sdt-desktop-card-width, 480px);
          flex: 0 1 var(--sdt-desktop-card-width, 480px);
        }

        .empty {
          display: flex;
          align-items: center;
          gap: 13px;
          box-sizing: border-box;
          min-height: 110px;
          padding: 22px;
          border: 1px solid var(--divider-color);
          border-radius: var(--ha-card-border-radius, 12px);
          color: var(--secondary-text-color);
          background: var(--card-background-color);
          box-shadow: var(--ha-card-box-shadow, none);
        }

        .empty ha-icon {
          flex: 0 0 auto;
          color: var(--primary-color);
          --mdc-icon-size: 32px;
        }

        @media (max-width: 800px) {
          :host {
            padding: 12px 8px 24px;
          }

          header {
            margin: 6px 8px 18px;
          }

          header p {
            font-size: 14px;
          }

          .cards {
            gap: 14px;
          }

          .cards > * {
            width: 100%;
            min-width: 0;
            max-width: none;
            flex-basis: 100%;
          }
        }
      </style>
      <main>
        <header>
          <div class="eyebrow">Swiss Dynamic Tariffs</div>
          <h1>${escapeHtml(text.dashboardTitle)}</h1>
          <p>${escapeHtml(text.dashboardDescription)}</p>
        </header>
        ${
          entities.length
            ? '<section class="cards" aria-live="polite"></section>'
            : `
              <div class="empty">
                <ha-icon icon="mdi:chart-line-variant"></ha-icon>
                <span>${escapeHtml(text.noForecasts)}</span>
              </div>
            `
        }
      </main>
    `;

    const cardContainer = this.shadowRoot.querySelector(".cards");
    for (const state of entities) {
      const card = document.createElement(PANEL_CARD_TAG);
      this._cards.set(state.entity_id, card);
      card.addEventListener(AXIS_EXTENT_EVENT, (event) => {
        this._updateSharedYAxis(state.entity_id, event.detail);
      });
      card.setConfig({ entity: state.entity_id });
      cardContainer.append(card);
      card.hass = this._hass;
    }
  }
}

// The automatically provisioned dashboard stores a stable card type instead
// of a Community strategy. A separate subclass is required because the Custom
// Elements registry permits one constructor to be registered under one name.
class SwissDynamicTariffsAutomaticPanel extends SwissDynamicTariffsPanel {}

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
          type: "panel",
          cards: cards.length
            ? [{ type: `custom:${PANEL_TAG}` }]
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

if (!customElements.get(PANEL_CARD_TAG)) {
  customElements.define(PANEL_CARD_TAG, SwissDynamicTariffsPanelCard);
}

if (!customElements.get(PANEL_TAG)) {
  customElements.define(PANEL_TAG, SwissDynamicTariffsPanel);
}

if (!customElements.get(DASHBOARD_PANEL_TAG)) {
  customElements.define(DASHBOARD_PANEL_TAG, SwissDynamicTariffsAutomaticPanel);
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
  const registrationText = textForBrowser();
  window.customCards.push({
    type: CARD_TAG,
    name: registrationText.cardPickerName,
    description: registrationText.cardPickerDescription,
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
  const registrationText = textForBrowser();
  window.customStrategies.push({
    type: STRATEGY_TYPE,
    strategyType: "dashboard",
    name: "Swiss Dynamic Tariffs",
    description: registrationText.strategyDescription,
    documentationURL:
      "https://github.com/ehnid/swiss-dynamic-tariffs#dashboard-visualization",
  });
}
