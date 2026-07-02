from __future__ import annotations

from core.stage import Stage

from models import (
    OptimizationContext,
    PromptData,
)

from .default_registry import create_default_registry
from .intent.executor import StrategyExecutor
from .planner import OptimizationPlanner
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

        self._strategy_executor = StrategyExecutor()

        self._planner = OptimizationPlanner()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        # -----------------------------------------
        # Execute intent-specific optimization
        # strategies before generic optimizers.
        # -----------------------------------------

        self._strategy_executor.execute(
            prompt,
        )

        # -----------------------------------------
        # Build optimization plan.
        # -----------------------------------------

        plan = self._planner.build(
            prompt,
        )

        # -----------------------------------------
        # Build shared optimization context.
        #
        # NOTE:
        # This context will be expanded later to
        # include quality, intent and plan.
        # -----------------------------------------

        context = OptimizationContext(
            mode=prompt.mode,
            analysis=prompt.analysis,
            intent=prompt.intent,
            quality=prompt.quality,
            normalization=prompt.normalization,
            optimization_hints=prompt.optimization_hints,
            plan=plan,
        )

        text = prompt.current_prompt

        # -----------------------------------------
        # Execute enabled optimizers.
        # -----------------------------------------

        for optimizer in self._registry.optimizers:

            if not optimizer.enabled:
                continue

            if not plan.is_enabled(
                optimizer.optimizer_type,
            ):
                continue

            before = text

            after = optimizer.optimize(
                text,
                context,
            )

            if before != after:

                prompt.optimization.add_step(
                    name=optimizer.name,
                    before=before,
                    after=after,
                )

            text = after

        prompt.current_prompt = text

        return prompt