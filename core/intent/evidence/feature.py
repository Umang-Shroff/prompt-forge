from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Feature:
    """
    A single feature that contributes towards
    intent detection.
    """

    value: str

    occurrences: int

    sentence: int

    position: int