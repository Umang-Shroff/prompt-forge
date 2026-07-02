from __future__ import annotations

from dataclasses import dataclass, field

from .intent_score import IntentScore
from .intent_type import IntentType
from core.intent.config import STRONG_INTENT_CONFIDENCE

@dataclass(slots=True)
class IntentResult:
    """
    Stores all detected intents ordered by confidence.
    """

    scores: list[IntentScore] = field(
        default_factory=list,
    )

    @property
    def primary(self) -> IntentType:

        if not self.scores:
            return IntentType.UNKNOWN

        return self.scores[0].intent

    @property
    def primary_score(self) -> IntentScore | None:

        if not self.scores:
            return None

        return self.scores[0]

    @property
    def confidence(self) -> float:

        if not self.scores:
            return 0.0

        return self.scores[0].confidence

    @property
    def secondary(self) -> list[IntentType]:

        return [
            score.intent
            for score in self.scores[1:]
        ]

    def add(
        self,
        score: IntentScore,
    ) -> None:

        self.scores.append(score)

    def has(
        self,
        intent: IntentType,
        threshold: float = STRONG_INTENT_CONFIDENCE
    ) -> bool:

        return any(
            score.intent == intent
            and score.confidence >= threshold
            for score in self.scores
        )

    def top(
        self,
        limit: int = 3,
    ) -> list[IntentScore]:

        return self.scores[:limit]