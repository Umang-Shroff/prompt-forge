from __future__ import annotations

from abc import ABC, abstractmethod

from models import OptimizationContext

from .optimizer_type import OptimizerType


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

    @property
    @abstractmethod
    def optimizer_type(
        self,
    ) -> OptimizerType:
        """
        Returns the category of optimizer.

        This allows OptimizerStage to make decisions without
        relying on fragile class names.
        """
        raise NotImplementedError

    def is_protected(
        self,
        text: str,
        context: OptimizationContext,
    ) -> bool:
        """
        Returns True if the text contains a protected term.
        """

        protected = context.optimization_hints.preserve_terms

        if not protected:
            return False

        lowered = text.lower()

        return any(
            term.lower() in lowered
            for term in protected
        )

    @abstractmethod
    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:
        """
        Optimize the supplied text.
        """
        raise NotImplementedError