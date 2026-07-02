from __future__ import annotations

import re

from models import OptimizationContext

from .optimizer import Optimizer
from .optimizer_type import OptimizerType
from .patterns import REDUNDANT_WORD_PATTERN


class RedundancyOptimizer(Optimizer):
    """
    Removes redundant wording while preserving
    important prompt semantics.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.REDUNDANCY

    @property
    def priority(self) -> int:
        return 50

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
        # Respect protected prompts.
        # -----------------------------------------

        if self.is_protected(
            text,
            context,
        ):
            return text

        optimized = re.sub(
            REDUNDANT_WORD_PATTERN,
            r"\1",
            text,
            flags=re.IGNORECASE,
        )

        # -----------------------------------------
        # High-quality prompts receive only minimal
        # cleanup.
        # -----------------------------------------

        if (
            context.is_balanced
            and context.quality_score >= 90
        ):
            return optimized

        # -----------------------------------------
        # Aggressive mode removes redundant spacing
        # left behind after replacements.
        # -----------------------------------------

        if context.needs_aggressive_optimization:

            optimized = re.sub(
                r"\s{2,}",
                " ",
                optimized,
            )

            optimized = re.sub(
                r"\n{3,}",
                "\n\n",
                optimized,
            )

        return optimized.strip()