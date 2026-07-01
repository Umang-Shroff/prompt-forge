from __future__ import annotations

from abc import ABC, abstractmethod

from models import OptimizationContext


class Optimizer(ABC):
    """
    Base class for every semantic optimizer.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def priority(self) -> int:
        return 100

    @property
    def enabled(self) -> bool:
        return True

    @abstractmethod
    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:
        raise NotImplementedError