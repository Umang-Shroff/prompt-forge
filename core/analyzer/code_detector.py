from __future__ import annotations

import re

from .config import CODE_MATCH_WEIGHT, MAX_CONFIDENCE, MIN_CODE_CONFIDENCE
from models import PromptData

from .detector import Detector
from .patterns import CODE_PATTERNS


class CodeDetector(Detector):
    """
    Detects whether the prompt contains source code.
    """

    @property
    def priority(self) -> int:
        return 10

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt

        score = 0.0

        for language, regexes in CODE_PATTERNS.items():

            matches = sum(
                bool(re.search(regex, text))
                for regex in regexes
            )

            if matches:

                prompt.analysis.add_language(language)

                score += matches * CODE_MATCH_WEIGHT

        if score >= MIN_CODE_CONFIDENCE:

            prompt.analysis.mark_detected(
                "code",
                min(score, MAX_CONFIDENCE),
            )