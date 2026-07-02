from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ImportanceScore:
    """
    Importance assigned by one detector.
    """

    confidence: float

    evidence: list[str] = field(
        default_factory=list,
    )

    def __post_init__(
        self,
    ) -> None:

        self.confidence = max(
            0.0,
            min(
                1.0,
                self.confidence,
            ),
        )