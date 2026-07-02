from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..rule import QualityRule


class SpecificityRule(QualityRule):
    """
    Scores how specific the prompt is.
    """

    @property
    def priority(self) -> int:
        return 50

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        score = 60.0

        # -----------------------------
        # Explicit role
        # -----------------------------

        if prompt.intent.has(IntentType.ROLE):
            score += 15

        # -----------------------------
        # Important keywords
        # -----------------------------

        if prompt.optimization_hints.preferred_keywords:
            score += 15

        # -----------------------------
        # Structured prompt
        # -----------------------------



        score = min(
            100.0,
            score,
        )

        prompt.quality.specificity = score

        return score