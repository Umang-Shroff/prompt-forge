from __future__ import annotations

from enum import Enum


class OptimizerType(str, Enum):
    """
    Categories of optimizers.
    """

    ROLE = "role"

    INSTRUCTION = "instruction"

    SENTENCE = "sentence"

    REGEX = "regex"

    KEYWORD = "keyword"

    REDUNDANCY = "redundancy"

    REPETITION = "repetition"

    FILLER = "filler"

    OTHER = "other"