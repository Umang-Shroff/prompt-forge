from __future__ import annotations

from dataclasses import dataclass

from models import OptimizationMode, AnalysisResult

from .budget import CompressionBudget


@dataclass(frozen=True, slots=True)
class CompressionContext:
    """
    Read-only compression context with budget awareness.
    """

    mode: OptimizationMode
    analysis: AnalysisResult
    budget: CompressionBudget | None = None

    # -----------------------------
    # Mode helpers
    # -----------------------------

    @property
    def is_aggressive(self) -> bool:
        return self.mode == OptimizationMode.AGGRESSIVE

    @property
    def is_balanced(self) -> bool:
        return self.mode == OptimizationMode.BALANCED

    @property
    def is_conservative(self) -> bool:
        return self.mode == OptimizationMode.CONSERVATIVE

    # -----------------------------
    # Budget helpers
    # -----------------------------

    @property
    def has_budget(self) -> bool:
        return self.budget is not None

    @property
    def high_pressure(self) -> bool:
        return self.budget.is_high_pressure if self.budget else False