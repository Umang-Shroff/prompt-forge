from __future__ import annotations

from typing import Iterable

from .reconstructor import Reconstructor


class ReconstructorRegistry:

    def __init__(self) -> None:

        self._reconstructors: list[Reconstructor] = []

    def register(
        self,
        reconstructor: Reconstructor,
    ) -> None:

        self._reconstructors.append(reconstructor)

        self._reconstructors.sort(
            key=lambda r: r.priority,
        )

    def extend(
        self,
        reconstructors: Iterable[Reconstructor],
    ) -> None:

        for reconstructor in reconstructors:
            self.register(reconstructor)

    @property
    def reconstructors(
        self,
    ) -> tuple[Reconstructor, ...]:

        return tuple(self._reconstructors)