from __future__ import annotations

from core.stage import Stage

from models import (
    OptimizationContext,
    PromptData,
)

from .default_registry import create_default_registry
from .registry import OptimizerRegistry


class OptimizerStage(Stage):
    """
    Executes all registered optimizers sequentially
    and records their impact in OptimizationReport.
    """

    def __init__(
        self,
        registry: OptimizerRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        context = OptimizationContext(
            mode=prompt.mode,
            analysis=prompt.analysis,
            normalization=prompt.normalization,
        )

        text = prompt.current_prompt

        optimizers = self._registry.optimizers

        if not optimizers:
            return prompt

        for optimizer in optimizers:

            before = text

            after = optimizer.optimize(
                text,
                context,
            )

            # Record only meaningful changes
            if before != after:
                prompt.optimization.add_step(
                    name=optimizer.name,
                    before=before,
                    after=after,
                )

            text = after

        prompt.current_prompt = text

        return prompt