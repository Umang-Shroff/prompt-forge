from __future__ import annotations

from core.intent.detector import IntentDetector

from models.intent_document import IntentDocument
from models.intent_score import IntentScore
from models.intent_type import IntentType


class RoleDetector(IntentDetector):

    _PATTERNS = (
        "act as",
        "assume the role",
        "you are",
        "behave as",
        "expert",
        "senior",
        "architect",
        "consultant",
    )

    @property
    def name(self) -> str:
        return "RoleDetector"

    def detect(
        self,
        document: IntentDocument,
    ) -> IntentScore:

        score = 0.0
        evidence = []

        text = document.normalized_text

        for pattern in self._PATTERNS:

            if pattern in text:
                score += 0.15
                evidence.append(pattern)

        return IntentScore(
            intent=IntentType.ROLE,
            confidence=min(score, 1.0),
            evidence=evidence,
        )