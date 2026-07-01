from __future__ import annotations

from models import OptimizationContext

from .patterns import ROLE_PATTERNS
from .regex_optimizer import RegexOptimizer


class RoleOptimizer(RegexOptimizer):
    """
    Compress common role descriptions.
    """

    @property
    def priority(self) -> int:
        return 40

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_structured:
            return text

        patterns = dict(ROLE_PATTERNS)

        if context.is_conservative:

            patterns.pop(
                r"you are an expert software engineer specializing in python development",
                None,
            )

        return self.apply_patterns(
            text,
            patterns,
        )