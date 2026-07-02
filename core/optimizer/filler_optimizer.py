from __future__ import annotations

import re

from models import OptimizationContext

from .optimizer_type import OptimizerType
from .patterns import FILLER_PATTERNS
from .regex_optimizer import RegexOptimizer


class FillerOptimizer(RegexOptimizer):
    """
    Removes conversational filler phrases while adapting
    to prompt quality and optimization mode.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.FILLER

    @property
    def priority(self) -> int:
        return 10

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        # -----------------------------------------
        # Never modify structured or code prompts.
        # -----------------------------------------

        if (
            context.is_structured
            or context.contains_code
        ):
            return text

        # -----------------------------------------
        # If the entire text contains protected
        # terms, leave it untouched.
        # -----------------------------------------

        if self.is_protected(
            text,
            context,
        ):
            return text

        patterns = dict(
            FILLER_PATTERNS,
        )

        # -----------------------------------------
        # Conservative mode keeps more natural
        # language.
        # -----------------------------------------

        if context.is_conservative:

            patterns.pop(
                r"\bi would like you to\b",
                None,
            )

            patterns.pop(
                r"\bplease\b",
                None,
            )

        # -----------------------------------------
        # High-quality prompts receive minimal
        # cleanup even in balanced mode.
        # -----------------------------------------

        elif (
            context.is_balanced
            and context.quality_score >= 85
        ):

            patterns.pop(
                r"\bi would like you to\b",
                None,
            )

        # -----------------------------------------
        # Preserve preferred keywords.
        # -----------------------------------------

        for keyword in context.optimization_hints.preferred_keywords:

            patterns.pop(
                rf"\b{re.escape(keyword)}\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
            context.optimization_hints.preserve_terms,
            context.optimization_hints.protected_phrases,
        )