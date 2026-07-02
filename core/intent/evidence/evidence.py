from __future__ import annotations

from dataclasses import dataclass, field

from .feature import Feature


@dataclass(slots=True)
class Evidence:
    """
    Collection of extracted features supporting
    one intent.
    """

    confidence: float = 0.0

    features: list[Feature] = field(
        default_factory=list,
    )

    def add(
        self,
        feature: Feature,
    ) -> None:

        self.features.append(
            feature,
        )