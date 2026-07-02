from __future__ import annotations

from dataclasses import dataclass

from .intent_type import IntentType


@dataclass(slots=True)
class IntentScore:
    """
    Confidence score for one detected intent.
    """

    intent: IntentType

    confidence: float = 0.0

    evidence: list[str] | None = None

    def __post_init__(self) -> None:

        self.confidence = max(
            0.0,
            min(
                1.0,
                self.confidence,
            ),
        )

        if self.evidence is None:
            self.evidence = []