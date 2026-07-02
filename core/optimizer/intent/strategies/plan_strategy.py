from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..strategy import IntentOptimizationStrategy


class PlanStrategy(IntentOptimizationStrategy):
    """
    Preserves planning and architecture terminology.
    """

    def apply(
        self,
        prompt: PromptData,
    ) -> None:

        if not prompt.intent.has(
            IntentType.PLAN,
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
                "architecture",
                "roadmap",
                "implementation",
                "deployment",
                "workflow",
                "design",
            }
        )