from __future__ import annotations

from abc import ABC, abstractmethod

from models import PromptData


class Detector(ABC):
    """
    Base class for all prompt detectors.

    Every detector is responsible for recognizing
    exactly one characteristic of a prompt and
    updating PromptData.analysis.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def priority(self) -> int:
        """
        Lower priority executes first.

        Example:

        CodeDetector      -> 10

        MarkdownDetector  -> 20

        MixedDetector     -> 100
        """

        return 100

    @property
    def enabled(self) -> bool:
        """
        Allows detectors to be disabled
        without removing them.
        """

        return True

    @abstractmethod
    def detect(self, prompt: PromptData) -> None:
        """
        Analyze the prompt.

        Update PromptData in-place.
        """

        raise NotImplementedError