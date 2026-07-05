from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProtectedRegionStore:

    placeholders: dict[str, str]

    def __init__(self) -> None:

        self.placeholders = {}

    def add(
        self,
        text: str,
    ) -> str:

        key = f"__PF_CODE_{len(self.placeholders)}__"

        self.placeholders[key] = text

        return key

    def restore(
        self,
        text: str,
    ) -> str:

        for key, value in self.placeholders.items():

            text = text.replace(
                key,
                value,
            )

        return text