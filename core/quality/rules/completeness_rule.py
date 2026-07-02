from __future__ import annotations

from models import PromptData

from ..rule import QualityRule


class CompletenessRule(QualityRule):
    """
    Scores whether the prompt contains enough information
    for the model to perform the requested task.
    """

    @property
    def priority(self) -> int:
        return 40

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        score = 50.0

        # -----------------------------
        # Intent detected
        # -----------------------------



        # -----------------------------
        # Protected phrases
        # -----------------------------

        if prompt.optimization_hints.protected_phrases:
            score += 10

        # -----------------------------
        # Preferred keywords
        # -----------------------------

        if prompt.optimization_hints.preferred_keywords:
            score += 10

        score = min(
            100.0,
            score,
        )

        prompt.quality.completeness = score

        return score