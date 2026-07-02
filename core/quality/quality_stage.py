from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .default_registry import create_default_registry
from .evaluator import QualityEvaluator
from .registry import QualityRegistry


class QualityStage(Stage):
    """
    Evaluates prompt quality.
    """

    def __init__(
        self,
        registry: QualityRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

        self._evaluator = QualityEvaluator(
            self._registry,
        )

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        self._evaluator.evaluate(
            prompt,
        )

        return prompt