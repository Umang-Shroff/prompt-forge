from __future__ import annotations

from .registry import ReconstructorRegistry
from .sentence_reconstructor import SentenceReconstructor
from .list_reconstructor import ListReconstructor


def create_default_registry() -> ReconstructorRegistry:

    registry = ReconstructorRegistry()

    registry.register(
        SentenceReconstructor(),
    )
    registry.register(
        ListReconstructor(),
    )

    return registry