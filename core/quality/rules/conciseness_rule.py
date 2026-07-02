from __future__ import annotations

from models import PromptData

from ..rule import QualityRule


class ConcisenessRule(QualityRule):
    """
    Scores prompt conciseness.
    """

    @property
    def priority(self) -> int:
        return 30

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        words = len(
            prompt.current_prompt.split()
        )

        if words < 50:
            score = 100.0

        elif words < 100:
            score = 90.0

        elif words < 200:
            score = 75.0

        else:
            score = 60.0

        prompt.quality.conciseness = score

        return score