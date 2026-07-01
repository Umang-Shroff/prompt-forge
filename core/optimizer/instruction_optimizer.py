from __future__ import annotations

from models import OptimizationContext

from .patterns import INSTRUCTION_PATTERNS
from .regex_optimizer import RegexOptimizer


class InstructionOptimizer(RegexOptimizer):
    """
    Compress verbose instruction wording while preserving intent.
    """

    @property
    def priority(self) -> int:
        return 20

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_structured:
            return text

        patterns = dict(INSTRUCTION_PATTERNS)

        if context.is_conservative:

            patterns.pop(
                r"\bprovide a detailed explanation of\b",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
        )