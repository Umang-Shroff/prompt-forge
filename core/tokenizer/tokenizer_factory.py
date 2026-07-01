from __future__ import annotations

import tiktoken

from .tokenizer_config import TokenizerConfig


class TokenizerFactory:
    """
    Creates tiktoken encoders.

    Future versions can create Claude, Gemini,
    Llama or custom tokenizers without changing
    the rest of the pipeline.
    """

    @staticmethod
    def create(config: TokenizerConfig):

        try:

            return tiktoken.encoding_for_model(
                config.model_name,
            )

        except KeyError:

            return tiktoken.get_encoding(
                config.fallback_encoding,
            )