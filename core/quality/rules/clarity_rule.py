from __future__ import annotations

import re

from models import PromptData
from ..constants import VAGUE_WORDS
from ..rule import QualityRule


class ClarityRule(QualityRule):
    """
    Scores prompt clarity by penalizing vague wording.
    """

    @property
    def priority(self) -> int:
        return 10

    def evaluate(
        self,
        prompt: PromptData,
    ) -> float:

        text = prompt.current_prompt

        score = 100.0

        for word in VAGUE_WORDS:

            if re.search(
                rf"\b{re.escape(word)}\b",
                text,
                re.IGNORECASE,
            ):
                score -= 10

        prompt.quality.clarity = max(
            0.0,
            score,
        )

        return prompt.quality.clarity