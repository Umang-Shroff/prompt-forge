from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..strategy import IntentOptimizationStrategy


class ExplainStrategy(IntentOptimizationStrategy):
    """
    Preserves explanation-related terminology.
    """

    def apply(
        self,
        prompt: PromptData,
    ) -> None:

        if not prompt.intent.has(
            IntentType.EXPLAIN,
        ):
            return

        score = prompt.intent.primary_score

        if score is None:
            return

        hints = prompt.optimization_hints

        hints.preserve_terms.update(
            score.evidence or [],
        )

        hints.preferred_keywords.update(
            {
                "explain",
                "reason",
                "because",
                "example",
                "step-by-step",
            }
        )