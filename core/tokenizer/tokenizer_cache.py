from __future__ import annotations

from transformers import (
    AutoTokenizer,
    PreTrainedTokenizerBase,
)

from models import CompressionConfig


class TokenizerCache:
    """
    Lazily loads and caches Hugging Face tokenizers.

    One tokenizer is created for each unique compression
    configuration and reused throughout the application.
    """

    _cache: dict[tuple, PreTrainedTokenizerBase] = {}

    
    @classmethod
    def get(
        cls,
        config: CompressionConfig,
    ) -> PreTrainedTokenizerBase:

        key = config.cache_key

        if key not in cls._cache:

            cls._cache[key] = AutoTokenizer.from_pretrained(
                config.model_name,
                cache_dir=config.cache_dir,
                trust_remote_code=True,
            )

        return cls._cache[key]

    @classmethod
    def clear(cls) -> None:
        """
        Remove all cached tokenizer instances.

        Primarily useful during testing.
        """

        cls._cache.clear()