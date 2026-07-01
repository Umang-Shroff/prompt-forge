from __future__ import annotations

import re

from models import PromptData

from .config import (
    LOG_MATCH_WEIGHT,
    MAX_CONFIDENCE,
    MIN_LOG_CONFIDENCE,
)
from .detector import Detector
from .patterns import LOG_PATTERNS


class LogsDetector(Detector):
    """
    Detects console output and log files.
    """

    @property
    def priority(self) -> int:
        return 50

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt

        score = 0.0

        for pattern in LOG_PATTERNS:

            if re.search(pattern, text):
                score += LOG_MATCH_WEIGHT

        confidence = min(
            score / len(LOG_PATTERNS),
            MAX_CONFIDENCE,
        )

        if confidence >= MIN_LOG_CONFIDENCE:

            prompt.analysis.mark_detected(
                "logs",
                confidence,
            )