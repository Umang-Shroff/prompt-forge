from __future__ import annotations

from models import (
    IntentScore,
    IntentType,
)

from .vocabulary import VocabularyEntry
from .config import MAX_EVIDENCE_ITEMS
from .evidence.matcher import EvidenceMatcher


class IntentBuilder:
    """
    Fluent builder used by intent detectors.

    Detectors only describe the signals that indicate
    an intent. The builder delegates evidence extraction
    to EvidenceMatcher and produces the final IntentScore.
    """

    def __init__(
        self,
        intent: IntentType,
        matcher: EvidenceMatcher,
    ) -> None:

        self._intent = intent
        self._matcher = matcher

        self._keywords: list[tuple[str, float]] = []
        self._phrases: list[tuple[str, float]] = []

    # -----------------------------------------------------

    def keyword(
        self,
        value: str,
        weight: float,
    ) -> "IntentBuilder":

        self._keywords.append(
            (
                value,
                weight,
            )
        )

        return self

    # -----------------------------------------------------

    def keywords(
        self,
        *values: tuple[str, float],
    ) -> "IntentBuilder":

        self._keywords.extend(values)

        return self

    # -----------------------------------------------------

    def phrase(
        self,
        value: str,
        weight: float,
    ) -> "IntentBuilder":

        self._phrases.append(
            (
                value,
                weight,
            )
        )

        return self

    # -----------------------------------------------------

    def phrases(
        self,
        *values: tuple[str, float],
    ) -> "IntentBuilder":

        self._phrases.extend(values)

        return self

    # -----------------------------------------------------

    def use(
        self,
        vocabulary: VocabularyEntry,
    ) -> "IntentBuilder":

        self._keywords.extend(
            vocabulary.keywords,
        )

        self._phrases.extend(
            vocabulary.phrases,
        )

        return self

    # -----------------------------------------------------

    def build(
        self,
    ) -> IntentScore:

        evidence = self._matcher.build(
            keywords=self._keywords,
            phrases=self._phrases,
        )

        return IntentScore(
            intent=self._intent,
            confidence=evidence.confidence,
            evidence=[
                feature.value
                for feature in evidence.features[:MAX_EVIDENCE_ITEMS]
            ],
        )