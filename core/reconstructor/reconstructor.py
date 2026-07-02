from __future__ import annotations

from abc import ABC, abstractmethod


class Reconstructor(ABC):
    """
    Base class for all prompt reconstructors.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def priority(self) -> int:
        return 100

    @abstractmethod
    def reconstruct(
        self,
        text: str,
    ) -> str:
        raise NotImplementedError