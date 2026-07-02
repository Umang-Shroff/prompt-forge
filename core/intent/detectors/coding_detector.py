from __future__ import annotations

from core.intent.detector import IntentDetector

from models.intent_document import IntentDocument
from models.intent_score import IntentScore
from models.intent_type import IntentType

class CodingDetector(IntentDetector):

    _KEYWORDS = (
        "write code",
        "implement",
        "create",
        "build",
        "python",
        "java",
        "react",
        "fastapi",
        "api",
        "function",
        "class",
    )

    @property
    def name(self) -> str:
        return "CodingDetector"

    def detect(
        self,
        document: IntentDocument,
    ) -> IntentScore:

        score = 0.0
        evidence = []

        text = document.normalized_text

        for keyword in self._KEYWORDS:

            if keyword in text:
                score += 0.12
                evidence.append(keyword)

        return IntentScore(
            intent=IntentType.GENERATE_CODE,
            confidence=min(score, 1.0),
            evidence=evidence,
        )