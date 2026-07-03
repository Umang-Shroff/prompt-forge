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

    REGEX_FLAGS: re.RegexFlag = re.IGNORECASE

    def apply_patterns(
        self,
        text: str,
        patterns: dict[str, str],
        protected_terms: set[str] | None = None,
        protected_phrases: set[str] | None = None,
    ) -> str:
        """
        Apply regex replacements sequentially.

        Formatting cleanup belongs to the Normalizer stage,
        so this method only fixes whitespace introduced
        directly by replacements.
        """

        protected_terms = protected_terms or set()
        protected_phrases = protected_phrases or set()

        for pattern, replacement in patterns.items():

            def replace(match: re.Match[str]) -> str:

                matched = match.group(0)
                lowered = matched.lower()
            
                for phrase in protected_phrases:
                    if phrase.lower() in lowered:
                        return matched
            
                for term in protected_terms:
                    if term.lower() in lowered:
                        return matched
            
                return replacement

            text = re.sub(
                pattern,
                replace,
                text,
                flags=self.REGEX_FLAGS,
            )

        # --------------------------------------------------
        # Cleanup only whitespace introduced by replacements
        # --------------------------------------------------

        text = re.sub(r" {2,}", " ", text)

        text = re.sub(r"\s+([,.;:!?])", r"\1", text)

        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text