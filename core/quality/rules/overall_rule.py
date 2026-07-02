from __future__ import annotations

from models import PromptData

from ..rule import QualityRule


class OverallRule(QualityRule):
    """
    Computes the overall prompt quality score.

    This rule should always execute last because it aggregates
    the results of all other quality rules.
    """

    @property
    def priority(self) -> int:
        return 1000

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        quality = prompt.quality

        scores = (
            quality.clarity,
            quality.structure,
            quality.conciseness,
            quality.completeness,
            quality.specificity,
        )

        quality.overall = round(
            sum(scores) / len(scores),
            1,
        )

        return quality.overall