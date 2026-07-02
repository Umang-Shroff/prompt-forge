from __future__ import annotations

from abc import ABC, abstractmethod

from ...models.intent_score import IntentScore

from ...models.intent_document import IntentDocument


class IntentDetector(ABC):
    """
    Base class for all intent detectors.

    Each detector analyzes the prompt and returns
    a confidence score for one intent.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Detector name.
        """

    @abstractmethod
    def detect(
        self,
        document: IntentDocument,
    ) -> IntentScore:
        """
        Detect intent from the shared document.
        """