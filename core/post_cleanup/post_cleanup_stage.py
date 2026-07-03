from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .cleanup import PostCompressionCleanup


class PostCleanupStage(Stage):

    def __init__(self) -> None:
        self._cleanup = PostCompressionCleanup()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        prompt.current_prompt = self._cleanup.clean(
            prompt.current_prompt,
        )

        return prompt