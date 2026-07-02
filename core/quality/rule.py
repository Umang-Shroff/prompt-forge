from __future__ import annotations

from abc import ABC, abstractmethod

from models import PromptData


class QualityRule(ABC):
    """
    Base class for every quality scoring rule.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def priority(self) -> int:
        return 100

    @abstractmethod
    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:
        """
        Returns a score in the range [0,100].
        """
        raise NotImplementedError