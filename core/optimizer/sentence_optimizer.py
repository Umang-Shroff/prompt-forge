from __future__ import annotations

import re

from .regex_optimizer import RegexOptimizer
from models import (
    OptimizationContext,
    OptimizationMode,
)

from .optimizer import Optimizer
from .patterns import SENTENCE_PATTERNS


class SentenceOptimizer(RegexOptimizer):
    """
    Shortens verbose sentence constructions.
    """

    @property
    def priority(self) -> int:
        return 30

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_structured:
            return text

        patterns = dict(SENTENCE_PATTERNS)

        if context.mode == OptimizationMode.CONSERVATIVE:

            patterns.pop(
                r"\bdue to the fact that\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
        )