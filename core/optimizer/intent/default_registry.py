from __future__ import annotations
from PromptOptimizer.core.optimizer.intent.strategies.plan_strategy import PlanStrategy
from .registry import StrategyRegistry
from .strategies.explain_strategy import ExplainStrategy
from .strategies.role_strategy import RoleStrategy
from .strategies.code_strategy import CodeStrategy
from .strategies.debug_strategy import DebugStrategy


def create_default_registry() -> StrategyRegistry:

    registry = StrategyRegistry()

    registry.register(
        RoleStrategy(),
    )

    registry.register(
        PlanStrategy(),
    )

    registry.register(
        ExplainStrategy(),
    )

    registry.register(
        CodeStrategy(),
    )

    registry.register(
        DebugStrategy(),
    )

    return registry