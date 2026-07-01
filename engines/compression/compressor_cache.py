from __future__ import annotations

from typing import Any

from models import CompressionConfig

from .loader import CompressorLoader


class CompressorCache:
    """
    Lazily creates and caches PromptCompressor instances.

    One PromptCompressor is created for each unique
    CompressionConfig and reused throughout the application.
    """

    _cache: dict[tuple, Any] = {}


    @classmethod
    def get(
        cls,
        config: CompressionConfig,
    ) -> Any:

        key = config.cache_key

        if key not in cls._cache:

            loader = CompressorLoader(config)

            cls._cache[key] = loader.load()

        return cls._cache[key]

    @classmethod
    def clear(cls) -> None:
        """
        Remove all cached PromptCompressor instances.

        Primarily useful during testing.
        """

        cls._cache.clear()