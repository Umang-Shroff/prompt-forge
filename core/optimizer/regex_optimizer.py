from __future__ import annotations

import re

from .optimizer import Optimizer


class RegexOptimizer(Optimizer):
    """
    Base class for optimizers that perform regex-based
    pattern replacements.

    Subclasses only need to provide a mapping of
    regex patterns to replacement strings.
    """

    REGEX_FLAGS = re.IGNORECASE

    def apply_patterns(
        self,
        text: str,
        patterns: dict[str, str],
    ) -> str:
        """
        Apply regex replacements sequentially.

        This helper is intentionally lightweight.
        Formatting cleanup belongs to the Normalizer stage,
        so this method only fixes whitespace introduced
        directly by replacements.
        """

        for pattern, replacement in patterns.items():

            text = re.sub(
                pattern,
                replacement,
                text,
                flags=self.REGEX_FLAGS,
            )

        # --------------------------------------------------
        # Cleanup only whitespace introduced by replacements
        # --------------------------------------------------

        # Multiple spaces created after removing words
        text = re.sub(r" {2,}", " ", text)

        # Remove spaces before punctuation
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)

        # Remove spaces immediately inside parentheses
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)

        # Collapse 3+ blank lines to 2.
        # (2 blank lines are preserved because the
        # BlankLineNormalizer already decided that format.)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text