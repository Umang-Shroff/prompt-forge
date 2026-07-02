from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .default_registry import create_default_registry
from .document_builder import IntentDocumentBuilder
from .registry import IntentRegistry
from .scorer import IntentScorer


class IntentStage(Stage):
    """
    Detects the user's intent.

    The detected intents are stored in PromptData.intent.
    """

    def __init__(
        self,
        registry: IntentRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

        self._builder = IntentDocumentBuilder()

        self._scorer = IntentScorer(
            self._registry,
        )

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        document = self._builder.build(
            prompt.current_prompt,
            prompt.analysis,
        )

        prompt.intent = self._scorer.score(
            document,
        )

        return prompt