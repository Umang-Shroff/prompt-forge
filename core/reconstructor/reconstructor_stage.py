from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .default_registry import create_default_registry
from .registry import ReconstructorRegistry


class ReconstructorStage(Stage):

    def __init__(
        self,
        registry: ReconstructorRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        text = prompt.current_prompt

        for reconstructor in self._registry.reconstructors:

            text = reconstructor.reconstruct(
                text,
            )

        prompt.current_prompt = text

        return prompt