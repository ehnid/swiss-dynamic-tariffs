import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .const import CONF_PROVIDER, CONF_TARIFF, DOMAIN
from .providers.registry import TARIFF_OPTIONS, get_tariff_option


class SwissDynamicTariffsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ):
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
                    vol.Required(CONF_PROVIDER): vol.In(
                        {key: option.title for key, option in TARIFF_OPTIONS.items()}
                    )
                }
            ),
        )
