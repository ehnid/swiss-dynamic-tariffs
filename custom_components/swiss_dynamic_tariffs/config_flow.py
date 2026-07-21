import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .const import CONF_PROVIDER, DOMAIN
from .providers.registry import PROVIDERS


class SwissDynamicTariffsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ):
        """Handle the initial setup."""

        if user_input is not None:
            provider = user_input[CONF_PROVIDER]
            provider_class = PROVIDERS[provider]

            await self.async_set_unique_id(f"{DOMAIN}_{provider}")

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"{provider_class.name} Dynamic Tariffs",
                data={
                    CONF_PROVIDER: provider,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PROVIDER): vol.In(
                        {key: provider.name for key, provider in PROVIDERS.items()}
                    )
                }
            ),
        )
