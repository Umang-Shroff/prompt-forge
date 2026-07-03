from __future__ import annotations

import re

from models import PromptData


class ImportanceScorer:
    """
    Scores each chunk for LongLLMLingua.
    Higher score = preserve more.
    """

    ROLE_PATTERNS = (
        "act as",
        "you are",
        "assume the role",
    )

    REASONING_PATTERNS = (
        "think carefully",
        "step by step",
        "reason",
        "do not rush",
        "carefully",
    )

    OUTPUT_PATTERNS = (
        "summarize",
        "summary",
        "checklist",
        "output",
        "format",
        "json",
        "markdown",
        "table",
    )

    REQUIREMENT_PATTERNS = (
        "must",
        "should",
        "required",
        "requirements",
        "important",
        "critical",
    )

    CODE_PATTERNS = (
        "def ",
        "class ",
        "import ",
        "{",
        "}",
        "<",
        ">",
    )

    def score(
        self,
        chunks: list[str],
        prompt: PromptData,
    ) -> list[float]:

        return [
            self._score_chunk(chunk)
            for chunk in chunks
        ]

    def _score_chunk(
        self,
        text: str,
    ) -> float:

        lower = text.lower()

        score = 0.30

        if any(p in lower for p in self.ROLE_PATTERNS):
            score += 0.50

        if any(p in lower for p in self.REASONING_PATTERNS):
            score += 0.40

        if any(p in lower for p in self.OUTPUT_PATTERNS):
            score += 0.35

        if any(p in lower for p in self.REQUIREMENT_PATTERNS):
            score += 0.30

        if any(p in text for p in self.CODE_PATTERNS):
            score += 0.35

        if re.search(r"^\s*[-*]\s", text, re.MULTILINE):
            score += 0.20

        if re.search(r"^\s*\d+\.", text, re.MULTILINE):
            score += 0.20

        if len(text) > 1200:
            score -= 0.15

        return max(
            0.10,
            min(score, 1.0),
        )