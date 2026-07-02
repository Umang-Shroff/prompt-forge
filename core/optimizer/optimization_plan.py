from __future__ import annotations

from dataclasses import dataclass, field

from .optimizer_type import OptimizerType


@dataclass(slots=True)
class OptimizationPlan:
    """
    Describes how each optimizer category should behave.
    """

    enabled_optimizers: set[OptimizerType] = field(
        default_factory=lambda: {
            OptimizerType.ROLE,
            OptimizerType.INSTRUCTION,
            OptimizerType.SENTENCE,
            OptimizerType.REDUNDANCY,
            OptimizerType.REPETITION,
            OptimizerType.FILLER,
        }
    )

    aggressive: bool = False

    preserve_structure: bool = False

    preserve_examples: bool = False

    preserve_code: bool = False

    notes: list[str] = field(
        default_factory=list,
    )

    def enable(
        self,
        optimizer: OptimizerType,
    ) -> None:

        self.enabled_optimizers.add(
            optimizer,
        )

    def disable(
        self,
        optimizer: OptimizerType,
    ) -> None:

        self.enabled_optimizers.discard(
            optimizer,
        )

    def is_enabled(
        self,
        optimizer: OptimizerType,
    ) -> bool:

        return optimizer in self.enabled_optimizers