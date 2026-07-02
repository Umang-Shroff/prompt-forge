from __future__ import annotations

from models import (
    OptimizationContext,
    IntentType,
)

from .patterns import ROLE_PATTERNS
from .regex_optimizer import RegexOptimizer
from .optimizer_type import OptimizerType


class RoleOptimizer(RegexOptimizer):
    """
    Compresses verbose role descriptions while
    preserving role intent.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.ROLE

    @property
    def priority(self) -> int:
        return 40

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

        # Preserve role wording for non-role prompts.
        if context.primary_intent != IntentType.ROLE:
            return text

        patterns = dict(
            ROLE_PATTERNS,
        )

        if context.is_conservative:

            patterns.pop(
                r"you are an expert software engineer specializing in python development",
                None,
            )

        elif (
            context.is_balanced
            and context.quality_score >= 90
        ):

            patterns.pop(
                r"you are an expert software engineer specializing in python development",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
            context.optimization_hints.preserve_terms,
            context.optimization_hints.protected_phrases,
        )