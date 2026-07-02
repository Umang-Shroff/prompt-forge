from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..strategy import IntentOptimizationStrategy

class CodeStrategy(IntentOptimizationStrategy):
    """
    Preserves code-related identifiers and keywords.
    """

    def apply(
        self,
        prompt: PromptData,
    ) -> None:

        if not prompt.intent.has(
            IntentType.GENERATE_CODE,
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
                "function",
                "class",
                "method",
                "api",
                "database",
                "algorithm",
                "implementation",
            }
        )