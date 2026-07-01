from __future__ import annotations

import re

from PromptOptimizer.core.analyzer.config import MARKDOWN_MATCH_WEIGHT, MIN_MARKDOWN_CONFIDENCE, MAX_CONFIDENCE
from models import PromptData
from .patterns import MARKDOWN_PATTERNS
from .detector import Detector


class MarkdownDetector(Detector):
    """
    Detects Markdown formatting.
    """

    @property
    def priority(self) -> int:
        return 40

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt

        score = 0

        for pattern in MARKDOWN_PATTERNS:

            if re.search(pattern, text, re.MULTILINE):
                score += MARKDOWN_MATCH_WEIGHT

        confidence = min(
            score / len(MARKDOWN_PATTERNS),
            MAX_CONFIDENCE,
        )

        if confidence >= MIN_MARKDOWN_CONFIDENCE:

            prompt.analysis.contains_markdown = True

            prompt.analysis.set_confidence(
                "markdown",
                min(score / len(MARKDOWN_PATTERNS), 1.0),
            )