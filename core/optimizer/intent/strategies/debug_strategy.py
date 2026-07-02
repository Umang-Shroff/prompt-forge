from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..strategy import IntentOptimizationStrategy


class DebugStrategy(IntentOptimizationStrategy):
    """
    Preserves debugging-related terminology.
    """

    def apply(
        self,
        prompt: PromptData,
    ) -> None:

        if not prompt.intent.has(
            IntentType.DEBUG,
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
                "error",
                "exception",
                "traceback",
                "stack",
                "bug",
                "debug",
            }
        )
        
        hints.protected_phrases.update(
            {
                "stack trace",
                "error message",
            }
        )