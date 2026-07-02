from __future__ import annotations

import re
from models.intent_document import IntentDocument

from models import AnalysisResult


class IntentDocumentBuilder:
    """
    Builds the shared IntentDocument used by all
    intent detectors.

    This performs only lightweight preprocessing.
    It intentionally does not depend on the
    NormalizerStage.
    """

    _sentence_pattern = re.compile(r"[.!?\n]+")

    _whitespace_pattern = re.compile(r"\s+")

    def build(
        self,
        text: str,
        analysis: AnalysisResult,
    ) -> IntentDocument:

        normalized = self._whitespace_pattern.sub(
            " ",
            text.strip(),
        ).lower()

        words = normalized.split()

        sentences = [
            sentence.strip()
            for sentence in self._sentence_pattern.split(text)
            if sentence.strip()
        ]

        return IntentDocument(
            raw_text=text,
            normalized_text=normalized,
            words=words,
            sentences=sentences,
            analysis=analysis,
        )