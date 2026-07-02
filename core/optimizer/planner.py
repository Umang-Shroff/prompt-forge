from __future__ import annotations

from models import (
    IntentType,
    PromptData,
)
from .optimization_plan import OptimizationPlan
from .optimizer_type import OptimizerType


class OptimizationPlanner:
    """
    Builds an optimization plan using all analysis
    performed earlier in the pipeline.
    """

    def build(
        self,
        prompt: PromptData,
    ) -> OptimizationPlan:

        plan = OptimizationPlan()

        quality = prompt.quality.overall

        # -----------------------------
        # Quality
        # -----------------------------

        if quality >= 90:

            plan.disable(
                OptimizerType.SENTENCE,
            )
            plan.aggressive = False

        elif quality < 70:

            plan.aggressive = True

        # -----------------------------
        # Code
        # -----------------------------

        if prompt.analysis.contains_code:

            plan.preserve_code = True

        # -----------------------------
        # Markdown
        # -----------------------------

        if prompt.analysis.contains_markdown:

            plan.preserve_structure = True

        # -----------------------------
        # Role prompts
        # -----------------------------

        if prompt.intent.has(IntentType.ROLE):

            plan.notes.append(
                "Preserve system role."
            )

        # -----------------------------
        # Planning prompts
        # -----------------------------

        if prompt.intent.has(IntentType.PLAN):

            plan.preserve_structure = True

        return plan