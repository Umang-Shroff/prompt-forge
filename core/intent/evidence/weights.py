from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EvidenceWeights:
    """
    Tunable scoring weights for evidence extraction.
    """

    phrase: float = 0.40

    keyword: float = 0.20

    imperative: float = 0.35

    title: float = 0.25

    repeated: float = 0.05

    first_sentence_multiplier: float = 1.60

    second_sentence_multiplier: float = 1.30

    remaining_sentence_multiplier: float = 1.00