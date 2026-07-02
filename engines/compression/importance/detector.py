from __future__ import annotations

from abc import ABC, abstractmethod

from .score import ImportanceScore


class ChunkImportanceDetector(ABC):
    """
    Base class for every chunk importance detector.
    """

    @abstractmethod
    def detect(
        self,
        chunk: str,
    ) -> ImportanceScore:
        raise NotImplementedError