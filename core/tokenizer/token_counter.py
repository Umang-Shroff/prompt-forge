from __future__ import annotations

from transformers import PreTrainedTokenizerBase

from models import CompressionConfig

from .tokenizer_cache import TokenizerCache


class TokenCounter:
    """
    Counts tokens using the tokenizer associated with the
    configured compression model.
    """

    def __init__(
        self,
        config: CompressionConfig,
    ) -> None:

        self._config = config

        self._tokenizer: PreTrainedTokenizerBase = (
            TokenizerCache.get(config)
        )

    def count(
        self,
        text: str,
    ) -> int:
        """
        Return the number of tokens in the text.
        """

        return len(
            self._tokenizer.encode(
                text,
                add_special_tokens=False,
            )
        )