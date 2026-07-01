from __future__ import annotations

from models import PromptData

from .stage import Stage


class Pipeline:
    """
    Executes pipeline stages sequentially.
    """

    def __init__(self, stages: list[Stage]) -> None:
        self._stages = stages

    @property
    def stages(self) -> tuple[Stage, ...]:
        """
        Immutable view of registered stages.
        """
        return tuple(self._stages)

    def run(self, prompt: PromptData) -> PromptData:
        """
        Execute every pipeline stage in order.
        """

        for stage in self._stages:

            prompt = stage.execute(prompt)

            prompt.metadata.mark_stage_completed(stage.name)

            if prompt.diagnostics.has_errors:
                break

        prompt.metadata.finish()

        return prompt