from __future__ import annotations

from models import PromptData

from ..constants import STRUCTURE_MARKERS
from ..rule import QualityRule


class StructureRule(QualityRule):
    """
    Scores how well the prompt is structured.
    """

    @property
    def priority(self) -> int:
        return 20

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        text = prompt.current_prompt

        score = 60.0

        if "\n" in text:
            score += 20

        if any(
            marker in text
            for marker in STRUCTURE_MARKERS
        ):
            score += 20

        prompt.quality.structure = min(
            100.0,
            score,
        )

        return prompt.quality.structure