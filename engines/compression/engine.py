from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import PromptData
    from core.compressor.context import CompressionContext
    from engines.compression.policy import CompressionPolicy

class CompressionEngine(ABC):
    """
    Base interface for compression engines.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def compress(
        self,
        text: str,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
    ) -> str:
        raise NotImplementedError