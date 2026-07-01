from __future__ import annotations

import re

from models import (
    OptimizationContext,
    OptimizationMode,
)

from .regex_optimizer import RegexOptimizer
from .patterns import FILLER_PATTERNS


class FillerOptimizer(RegexOptimizer):
    """
    Removes conversational filler phrases.
    """

    @property
    def priority(self) -> int:
        return 10

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_structured:
            return text

        patterns = dict(FILLER_PATTERNS)

        if context.mode == OptimizationMode.CONSERVATIVE:
            patterns.pop(
                r"\bi would like you to\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
        )