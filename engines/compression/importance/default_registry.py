from __future__ import annotations

from .registry import ImportanceRegistry


def create_default_registry() -> ImportanceRegistry:

    registry = ImportanceRegistry()

    return registry