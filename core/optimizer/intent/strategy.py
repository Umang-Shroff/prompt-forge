from __future__ import annotations

from abc import ABC, abstractmethod

from models import PromptData


class IntentOptimizationStrategy(ABC):
    """
    Applies intent-specific optimizations.
    """

    @abstractmethod
    def apply(
        self,
        prompt: PromptData,
    ) -> None:
        ...