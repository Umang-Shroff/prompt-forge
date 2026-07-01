from __future__ import annotations

from engines.compression.longllmlingua_engine import LongLLMLinguaEngine

from .registry import CompressionRegistry


def create_default_registry() -> CompressionRegistry:
    """
    Create the default compression registry.
    """

    registry = CompressionRegistry()

    registry.register(
        LongLLMLinguaEngine(),
    )

    return registry