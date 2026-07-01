from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompressionBudget:
    """
    Defines how aggressively compression should behave.
    """

    original_tokens: int
    target_tokens: int

    @property
    def reduction_required(self) -> float:
        if self.original_tokens == 0:
            return 0.0

        return (
            self.original_tokens - self.target_tokens
        ) / self.original_tokens * 100

    @property
    def is_high_pressure(self) -> bool:
        return self.reduction_required > 50

    @property
    def is_medium_pressure(self) -> bool:
        return 20 < self.reduction_required <= 50

    @property
    def is_low_pressure(self) -> bool:
        return self.reduction_required <= 20