"""Registry for tariff providers."""

from __future__ import annotations

from .base import BaseProvider

# Registry of available providers.
#
# The key is the provider identifier used in the configuration.
# The value will be the provider class.
#
# Provider implementations will be added in later phases.
PROVIDERS: dict[str, type[BaseProvider]] = {}
