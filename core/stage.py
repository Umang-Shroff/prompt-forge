from __future__ import annotations

from abc import ABC, abstractmethod

from models import PromptData


class Stage(ABC):
    """
    Base class for every pipeline stage.

    Each stage receives the shared PromptData object,
    performs its operation, and returns the same object.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(self, prompt: PromptData) -> PromptData:
        """
        Execute this stage.
        """
        raise NotImplementedError