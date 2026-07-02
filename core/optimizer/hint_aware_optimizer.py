from __future__ import annotations

import re

from models import OptimizationContext

from .optimizer import Optimizer


class HintAwareOptimizer(Optimizer):
    """
    Protects intent-critical terms from downstream optimizers.

    Protected terms are temporarily replaced with placeholders
    before other optimizers execute and restored afterwards.
    """

    _PATTERN = "__PF_PROTECTED_{}__"

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        hints = context.optimization_hints

        if not hints.preserve_terms:
            return text

        replacements: dict[str, str] = {}

        protected = sorted(
            hints.preserve_terms,
            key=len,
            reverse=True,
        )

        # Protect
        for index, term in enumerate(protected):

            placeholder = self._PATTERN.format(index)

            pattern = re.compile(
                rf"\b{re.escape(term)}\b",
                re.IGNORECASE,
            )

            if pattern.search(text):

                replacements[placeholder] = term

                text = pattern.sub(
                    placeholder,
                    text,
                )

        # Restore immediately.
        # Later we can split protect/restore into two stages.

        for placeholder, original in replacements.items():

            text = text.replace(
                placeholder,
                original,
            )

        return text