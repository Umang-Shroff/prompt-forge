from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)

from ..strategy import IntentOptimizationStrategy


class RoleStrategy(IntentOptimizationStrategy):
    """
    Preserves role-related terminology.

    Examples
    --------
    Act as...
    You are...
    Expert...
    Senior...
    Consultant...
    """

    def apply(
        self,
        prompt: PromptData,
    ) -> None:

        if not prompt.intent.has(
            IntentType.ROLE,
        ):
            return

        score = prompt.intent.primary_score

        if score is None:
            return

        hints = prompt.optimization_hints

        hints.preserve_terms.update(
            score.evidence or [],
        )
        
        hints.protected_phrases.update(
            {
                "act as",
                "you are",
                "assume the role",
            }
        )
        
        hints.preferred_keywords.update(
            {
                "expert",
                "architect",
                "engineer",
                "consultant",
                "specialist",
            }
        )