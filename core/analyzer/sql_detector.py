from __future__ import annotations

import re

from models import PromptData

from .config import (
    MAX_CONFIDENCE,
    MIN_SQL_CONFIDENCE,
    SQL_MATCH_WEIGHT,
)
from .detector import Detector
from .patterns import SQL_PATTERNS


class SqlDetector(Detector):
    """
    Detects SQL queries or SQL scripts.
    """

    @property
    def priority(self) -> int:
        return 35

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt

        matches = sum(
            bool(re.search(pattern, text, re.IGNORECASE))
            for pattern in SQL_PATTERNS
        )

        confidence = min(
            (matches * SQL_MATCH_WEIGHT) / len(SQL_PATTERNS),
            MAX_CONFIDENCE,
        )

        if confidence >= MIN_SQL_CONFIDENCE:

            prompt.analysis.mark_detected(
                "sql",
                confidence,
            )