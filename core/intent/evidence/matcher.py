from __future__ import annotations

import re

from .evidence import Evidence
from .feature import Feature
from .weights import EvidenceWeights

from models import IntentDocument


class EvidenceMatcher:
    """
    Extracts weighted evidence from an IntentDocument.

    Detectors never search text directly.
    They simply declare the words and phrases they care about.
    """

    def __init__(
        self,
        document: IntentDocument,
        weights: EvidenceWeights | None = None,
    ) -> None:

        self._document = document

        self._weights = weights or EvidenceWeights()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        *,
        keywords: list[tuple[str, float]] | None = None,
        phrases: list[tuple[str, float]] | None = None,
    ) -> Evidence:

        evidence = Evidence()

        if keywords:

            for keyword, weight in keywords:

                self._collect_keyword(
                    evidence,
                    keyword,
                    weight,
                )

        if phrases:

            for phrase, weight in phrases:

                self._collect_phrase(
                    evidence,
                    phrase,
                    weight,
                )

        evidence.confidence = min(
            evidence.confidence,
            1.0,
        )

        return evidence

    # ---------------------------------------------------------
    # Keyword
    # ---------------------------------------------------------

    def _collect_keyword(
        self,
        evidence: Evidence,
        keyword: str,
        weight: float,
    ) -> None:

        pattern = re.compile(
            rf"\b{re.escape(keyword)}\b",
            flags=re.IGNORECASE,
        )

        matches = list(
            pattern.finditer(
                self._document.raw_text,
            )
        )

        if not matches:
            return

        multiplier = self._sentence_multiplier(
            matches[0].start(),
        )

        confidence = min(
            weight * len(matches) * multiplier,
            weight * 2.0,
        )

        evidence.confidence += confidence

        evidence.add(
            Feature(
                value=keyword,
                occurrences=len(matches),
                sentence=self._sentence_index(
                    matches[0].start(),
                ),
                position=matches[0].start(),
            )
        )

    # ---------------------------------------------------------
    # Phrase
    # ---------------------------------------------------------

    def _collect_phrase(
        self,
        evidence: Evidence,
        phrase: str,
        weight: float,
    ) -> None:

        pattern = re.compile(
            re.escape(phrase),
            flags=re.IGNORECASE,
        )

        matches = list(
            pattern.finditer(
                self._document.raw_text,
            )
        )

        if not matches:
            return

        multiplier = self._sentence_multiplier(
            matches[0].start(),
        )

        confidence = min(
            weight * len(matches) * multiplier,
            weight * 2.0,
        )

        evidence.confidence += confidence

        evidence.add(
            Feature(
                value=phrase,
                occurrences=len(matches),
                sentence=self._sentence_index(
                    matches[0].start(),
                ),
                position=matches[0].start(),
            )
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _sentence_index(
        self,
        position: int,
    ) -> int:

        current = 0

        for index, sentence in enumerate(
            self._document.sentences,
        ):

            current += len(sentence)

            if position <= current:

                return index

        return len(self._document.sentences) - 1

    def _sentence_multiplier(
        self,
        position: int,
    ) -> float:

        sentence = self._sentence_index(
            position,
        )

        if sentence == 0:
            return self._weights.first_sentence_multiplier

        if sentence == 1:
            return self._weights.second_sentence_multiplier

        return self._weights.remaining_sentence_multiplier