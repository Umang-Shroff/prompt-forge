from __future__ import annotations

import re

from models import (
    IntentType,
    PromptData,
)


ROLE_PATTERNS = (
    r"\bact as\b",
    r"\byou are\b",
    r"\bassume the role\b",
)

DEBUG_PATTERNS = (
    r"\berror\b",
    r"\bexception\b",
    r"\bstack trace\b",
    r"\btraceback\b",
    r"\bbug\b",
    r"\bfix\b",
)

PLAN_PATTERNS = (
    r"\bplan\b",
    r"\broadmap\b",
    r"\bphase\b",
    r"\bmilestone\b",
    r"\bstep\b",
)

EXPLANATION_PATTERNS = (
    r"\bwhy\b",
    r"\bexplain\b",
    r"\breason\b",
    r"\bbecause\b",
    r"\btrade[- ]?off\b",
)

INSTRUCTION_PATTERNS = (
    r"\bmust\b",
    r"\bshould\b",
    r"\brequired\b",
    r"\bensure\b",
    r"\bprovide\b",
    r"\binclude\b",
    r"\bexplain\b",
)

EXAMPLE_PATTERNS = (
    r"\bexample\b",
    r"\bfor example\b",
    r"\be\.g\.\b",
)


def score_chunk(
    chunk: str,
    index: int,
    total_chunks: int,
    prompt: PromptData,
) -> float:
    """
    Computes an importance score in the range [0.1, 1.0].
    """

    score = 0.50

    lower = chunk.lower()

    # -------------------------------
    # Position
    # -------------------------------

    if index == 0:
        score += 0.20

    elif index == total_chunks - 1:
        score += 0.10

    # -------------------------------
    # Role
    # -------------------------------

    if prompt.intent.has(IntentType.ROLE):

        if any(
            re.search(
                pattern,
                lower,
            )
            for pattern in ROLE_PATTERNS
        ):
            score += 0.35

    # -------------------------------
    # Debugging
    # -------------------------------

    if prompt.intent.has(IntentType.DEBUG):

        if any(
            re.search(
                pattern,
                lower,
            )
            for pattern in DEBUG_PATTERNS
        ):
            score += 0.20

    # -------------------------------
    # Planning
    # -------------------------------

    if prompt.intent.has(IntentType.PLAN):

        if any(
            re.search(
                pattern,
                lower,
            )
            for pattern in PLAN_PATTERNS
        ):
            score += 0.20

    # -------------------------------
    # Explanation
    # -------------------------------

    if prompt.intent.has(IntentType.EXPLAIN):

        if any(
            re.search(
                pattern,
                lower,
            )
            for pattern in EXPLANATION_PATTERNS
        ):
            score += 0.20

    # -------------------------------
    # Instructions
    # -------------------------------

    if any(
        re.search(
            pattern,
            lower,
        )
        for pattern in INSTRUCTION_PATTERNS
    ):
        score += 0.15

    # -------------------------------
    # Code
    # -------------------------------

    if prompt.analysis.contains_code:

        if (
            "```" in chunk
            or "def " in chunk
            or "class " in chunk
            or "import " in chunk
        ):
            score += 0.25

    # -------------------------------
    # Examples
    # -------------------------------

    if any(
        re.search(
            pattern,
            lower,
        )
        for pattern in EXAMPLE_PATTERNS
    ):
        score -= 0.10

    # -------------------------------
    # Length
    # -------------------------------

    if len(chunk) < 60:
        score -= 0.05

    elif len(chunk) > 400:
        score += 0.05

    return max(
        0.10,
        min(
            score,
            1.0,
        ),
    )