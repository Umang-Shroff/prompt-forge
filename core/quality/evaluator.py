from __future__ import annotations

from .registry import QualityRegistry


class QualityEvaluator:
    """
    Executes all registered quality rules.
    """

    def __init__(
        self,
        registry: QualityRegistry,
    ) -> None:

        self._registry = registry

    def evaluate(
        self,
        prompt,
    ) -> None:

        for rule in self._registry.rules:
            rule.evaluate(prompt)