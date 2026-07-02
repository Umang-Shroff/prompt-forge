from __future__ import annotations

from models import PromptData

from .default_registry import create_default_registry
from .registry import StrategyRegistry


class StrategyExecutor:
    """
    Executes every registered intent optimization strategy.
    """

    def __init__(
        self,
        registry: StrategyRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

    def execute(
        self,
        prompt: PromptData,
    ) -> None:

        prompt.optimization_hints.clear()

        for strategy in self._registry.strategies:

            strategy.apply(
                prompt,
            )