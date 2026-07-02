from __future__ import annotations

from models import OptimizationContext

from .optimizer_type import OptimizerType
from .regex_optimizer import RegexOptimizer
from .patterns import SENTENCE_PATTERNS


class SentenceOptimizer(RegexOptimizer):
    """
    Simplifies verbose sentence constructions.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.SENTENCE

    @property
    def priority(self) -> int:
        return 30

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if (
            context.is_structured
            or context.contains_code
        ):
            return text

        if self.is_protected(
            text,
            context,
        ):
            return text

        patterns = dict(
            SENTENCE_PATTERNS,
        )

        if context.is_conservative:

            patterns.pop(
                r"\bdue to the fact that\b",
                None,
            )

            patterns.pop(
                r"\bin order to\b",
                None,
            )

        elif (
            context.is_balanced
            and context.quality_score >= 85
        ):

            patterns.pop(
                r"\bdue to the fact that\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
            context.optimization_hints.preserve_terms,
            context.optimization_hints.protected_phrases,
        )