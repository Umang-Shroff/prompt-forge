from __future__ import annotations

from dataclasses import dataclass

from models import IntentType


@dataclass(slots=True, frozen=True)
class VocabularyEntry:
    """
    Defines the vocabulary associated with a single intent.
    """

    keywords: tuple[tuple[str, float], ...] = ()

    phrases: tuple[tuple[str, float], ...] = ()


class IntentVocabulary:
    """
    Central vocabulary repository.

    Maps IntentType -> VocabularyEntry.
    """

    def __init__(
        self,
        entries: dict[IntentType, VocabularyEntry],
    ) -> None:

        self._entries = entries

    def get(
        self,
        intent: IntentType,
    ) -> VocabularyEntry:

        return self._entries.get(
            intent,
            VocabularyEntry(),
        )