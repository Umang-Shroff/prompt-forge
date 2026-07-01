from __future__ import annotations

from core.stage import Stage
from models import PromptData

from .token_counter import TokenCounter


class TokenCounterStage(Stage):
    """
    Computes token statistics for prompt.
    """

    def __init__(self) -> None:
        self.counter = TokenCounter()

    def execute(self, prompt: PromptData) -> PromptData:

        original = prompt.original_prompt
        current = prompt.current_prompt

        prompt.tokens.original_tokens = self.counter.count(original)
        prompt.tokens.optimized_tokens = self.counter.count(current)

        prompt.tokens.update()

        return prompt