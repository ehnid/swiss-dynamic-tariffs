from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN

import voluptuous as vol


class SwissDynamicTariffsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ):
        """Handle the initial setup."""

        if user_input is not None:
            provider = user_input["provider"]

            await self.async_set_unique_id(f"{DOMAIN}_{provider}")

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="BKW Dynamic Tariffs",
                data={
                    "provider": provider,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("provider"): vol.In(["bkw"])}),
        )
