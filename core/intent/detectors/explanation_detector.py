from __future__ import annotations

from core.intent.detector import IntentDetector


from models.intent_document import IntentDocument
from models.intent_score import IntentScore
from models.intent_type import IntentType


class ExplanationDetector(IntentDetector):

    _KEYWORDS = (
        "explain",
        "why",
        "how",
        "teach",
        "describe",
        "walk through",
        "step by step",
    )

    @property
    def name(self) -> str:
        return "ExplanationDetector"

    def detect(
        self,
        document: IntentDocument,
    ) -> IntentScore:

        score = 0.0
        evidence = []

        text = document.normalized_text

        for keyword in self._KEYWORDS:

            if keyword in text:
                score += 0.15
                evidence.append(keyword)

        return IntentScore(
            intent=IntentType.EXPLAIN,
            confidence=min(score, 1.0),
            evidence=evidence,
        )