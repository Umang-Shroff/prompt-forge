from __future__ import annotations

from core.stage import Stage

from models import (
    CompressionConfig,
    PromptData,
)

from .token_counter_cache import TokenCounterCache


class TokenCounterStage(Stage):
    """
    Computes token statistics for the prompt.

    The original prompt is tokenized only once, while the
    current prompt is tokenized on every execution so the
    latest optimization statistics are always available.
    """

    def __init__(self) -> None:

        self.counter = TokenCounterCache.get(
            CompressionConfig(),
        )

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        # Count the original prompt only once.
        if prompt.tokens.original_tokens == 0:

            prompt.tokens.original_tokens = self.counter.count(
                prompt.original_prompt,
            )

        # Always recount the current prompt since it may have
        # changed after optimization or compression.
        prompt.tokens.optimized_tokens = self.counter.count(
            prompt.current_prompt,
        )

        prompt.tokens.update()

        return prompt