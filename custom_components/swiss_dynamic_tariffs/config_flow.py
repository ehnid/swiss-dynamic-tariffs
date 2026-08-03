from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_PROVIDER, CONF_TARIFF, DOMAIN
from .dashboard import async_ensure_user_dashboard
from .providers.registry import TARIFF_OPTIONS, get_tariff_option

_LOGGER = logging.getLogger(__name__)


class SwissDynamicTariffsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial setup."""

        if user_input is not None:
            selection = user_input[CONF_PROVIDER]
            option = get_tariff_option(selection)

            await self.async_set_unique_id(f"{DOMAIN}_{option.key}")

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=option.title,
                data={
                    CONF_PROVIDER: option.provider,
                    CONF_TARIFF: option.tariff_name,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PROVIDER): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=key, label=option.title)
                                for key, option in TARIFF_OPTIONS.items()
                            ],
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the integration maintenance options."""

        return SwissDynamicTariffsOptionsFlow()


class SwissDynamicTariffsOptionsFlow(OptionsFlow):
    """Offer user-triggered maintenance actions for the integration."""

    async def async_step_init(
        self,
        user_input: dict | None = None,
    ) -> ConfigFlowResult:
        """Show the integration maintenance menu."""

        return self.async_show_menu(
            step_id="init",
            menu_options=["dashboard"],
        )

    async def async_step_dashboard(
        self,
        user_input: dict | None = None,
    ) -> ConfigFlowResult:
        """Create or restore the user-managed tariff dashboard."""

        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await async_ensure_user_dashboard(self.hass, force=True)
            except Exception:
                _LOGGER.exception("Unable to restore the tariff dashboard")
                errors["base"] = "dashboard_creation_failed"
            else:
                return self.async_create_entry(data=self.config_entry.options)

        return self.async_show_form(
            step_id="dashboard",
            data_schema=vol.Schema({}),
            errors=errors,
        )
