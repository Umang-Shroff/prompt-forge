from __future__ import annotations

from dataclasses import dataclass

from .intent_type import IntentType
from dataclasses import dataclass, field


@dataclass(slots=True)
class IntentScore:
    """
    Confidence score for one detected intent.
    """

    intent: IntentType

    confidence: float = 0.0

    evidence: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self) -> None:

        self.confidence = max(
            0.0,
            min(
                1.0,
                self.confidence,
            ),
        )
