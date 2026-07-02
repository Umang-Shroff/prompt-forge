from __future__ import annotations
import re
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
        raise NotImplementedError