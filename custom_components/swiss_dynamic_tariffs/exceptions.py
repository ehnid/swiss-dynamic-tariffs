"""Exceptions for Swiss Dynamic Tariffs."""


class SwissDynamicTariffsError(Exception):
    """Base exception for the integration."""


class ProviderConnectionError(SwissDynamicTariffsError):
    """Raised when a provider cannot be reached."""


class ProviderAuthenticationError(SwissDynamicTariffsError):
    """Raised when authentication fails."""


class ProviderDataError(SwissDynamicTariffsError):
    """Raised when provider data is invalid or incomplete."""
