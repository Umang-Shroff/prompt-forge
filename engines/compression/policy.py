from __future__ import annotations

from dataclasses import dataclass

from models import OptimizationMode


@dataclass(slots=True, frozen=True)
class CompressionPolicy:
    """
    Defines target compression behaviour.

    The engine should never know what
    "Balanced" or "Aggressive" means.

    It simply asks the policy.
    """

    target_ratio: float

    context_budget: str

    token_budget_ratio: float


class PolicyFactory:

    @staticmethod
    def create(
        mode: OptimizationMode,
    ) -> CompressionPolicy:

        if mode == OptimizationMode.CONSERVATIVE:

            return CompressionPolicy(
                target_ratio=0.80,
                context_budget="+200",
                token_budget_ratio=1.6,
            )

        if mode == OptimizationMode.AGGRESSIVE:

            return CompressionPolicy(
                target_ratio=0.35,
                context_budget="+50",
                token_budget_ratio=1.2,
            )

        return CompressionPolicy(
            target_ratio=0.60,
            context_budget="+100",
            token_budget_ratio=1.4,
        )