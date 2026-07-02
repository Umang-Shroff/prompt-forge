from __future__ import annotations

from dataclasses import dataclass

from .prompt_data import AnalysisResult


@dataclass(slots=True)
class IntentDocument:
    """
    Shared document passed to every intent detector.

    Preprocessed once to avoid repeated work.
    """

    raw_text: str

    normalized_text: str

    words: list[str]

    sentences: list[str]

    analysis: AnalysisResult