from __future__ import annotations

from abc import ABC, abstractmethod

from models import NormalizationContext


class Normalizer(ABC):
    """
    Base class for every normalizer.

    Normalizers receive the current prompt text,
    transform it, and return the updated text.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def priority(self) -> int:
        """
        Lower values execute first.
        """
        return 100

    @property
    def enabled(self) -> bool:
        return True

    @abstractmethod
    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:
        """
        Normalize the supplied text.
        """
        raise NotImplementedError