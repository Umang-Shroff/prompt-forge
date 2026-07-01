from __future__ import annotations

from models import CompressionConfig

from .token_counter import TokenCounter


class TokenCounterCache:
    """
    Lazily creates and caches TokenCounter instances.

    One TokenCounter is created per configured model and
    reused throughout the application.
    """

    _cache: dict[str, TokenCounter] = {}

    @classmethod
    def get(
        cls,
        config: CompressionConfig,
    ) -> TokenCounter:

        model = config.model_name

        if model not in cls._cache:

            cls._cache[model] = TokenCounter(
                config=config,
            )

        return cls._cache[model]

    @classmethod
    def clear(cls) -> None:
        """
        Clear all cached counters.

        Primarily useful during testing.
        """

        cls._cache.clear()