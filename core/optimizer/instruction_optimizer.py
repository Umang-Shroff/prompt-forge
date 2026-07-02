from __future__ import annotations

from models import (
    OptimizationContext,
    IntentType,
)

from .optimizer_type import OptimizerType
from .patterns import INSTRUCTION_PATTERNS
from .regex_optimizer import RegexOptimizer


class InstructionOptimizer(RegexOptimizer):
    """
    Compresses verbose instruction wording while preserving intent.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.OTHER

    @property
    def priority(self) -> int:
        return 20

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
            INSTRUCTION_PATTERNS,
        )

        if context.is_conservative:

            patterns.pop(
                r"\bprovide a detailed explanation of\b",
                None,
            )

        elif (
            context.primary_intent == IntentType.EXPLAIN
            and context.quality_score >= 90
        ):

            patterns.pop(
                r"\bprovide a detailed explanation of\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
            context.optimization_hints.preserve_terms,
            context.optimization_hints.protected_phrases,
        )