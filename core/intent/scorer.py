from __future__ import annotations
from unittest import result

from models import (
    IntentDocument,
    IntentResult,
)

from .registry import IntentRegistry
from .config import (
    MAX_INTENTS,
    MIN_INTENT_CONFIDENCE,
)


class IntentScorer:
    """
    Executes every registered detector and
    aggregates the results.
    """

    def __init__(
        self,
        registry: IntentRegistry,
    ) -> None:

        self._registry = registry

    def score(
        self,
        document: IntentDocument,
    ) -> IntentResult:

        result = IntentResult()

        for detector in self._registry.detectors:

            score = detector.detect(
                document,
            )

            if score.confidence >= MIN_INTENT_CONFIDENCE:

                result.add(
                    score,
                )

        result.scores.sort(
            key=lambda score: score.confidence,
            reverse=True,
        )

        result.scores = result.scores[:MAX_INTENTS]
    
        return result