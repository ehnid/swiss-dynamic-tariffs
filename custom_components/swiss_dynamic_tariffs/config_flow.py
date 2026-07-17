from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN


class SwissDynamicTariffsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    async def async_step_user(self, user_input=None):
        """Handle user setup."""

        if user_input:
            return self.async_create_entry(
                title="Swiss Dynamic Tariffs",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
        )
