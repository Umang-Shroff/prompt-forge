from __future__ import annotations

from collections.abc import Iterable

from .rule import QualityRule


class QualityRegistry:

    def __init__(self) -> None:

        self._rules: list[QualityRule] = []

    def register(
        self,
        rule: QualityRule,
    ) -> None:

        self._rules.append(rule)

        self._rules.sort(
            key=lambda rule: rule.priority,
        )

    def extend(
        self,
        rules: Iterable[QualityRule],
    ) -> None:

        for rule in rules:
            self.register(rule)

    @property
    def rules(
        self,
    ) -> tuple[QualityRule, ...]:

        return tuple(self._rules)