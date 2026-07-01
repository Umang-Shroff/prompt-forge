from __future__ import annotations

import re

from models import (
    NormalizationContext,
    PromptType,
)

from .config import (
    COLLAPSE_MULTIPLE_SPACES,
    REPLACE_TABS,
    TAB_SIZE,
)
from .normalizer import Normalizer


class WhitespaceNormalizer(Normalizer):
    """
    Normalize horizontal whitespace while preserving
    formatting required for structured content.
    """

    @property
    def priority(self) -> int:
        return 40

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        if REPLACE_TABS:
            text = text.replace(
                "\t",
                " " * TAB_SIZE,
            )


        # --------------------------------------------------
        # Structured formats are handled later
        # --------------------------------------------------

        if context.is_structured:
            return text

        # --------------------------------------------------
        # Source Code
        # --------------------------------------------------

        if context.is_code:

            normalized = []

            for line in text.splitlines():

                content = line.lstrip()

                indentation = line[: len(line) - len(content)]

                if COLLAPSE_MULTIPLE_SPACES:

                    content = re.sub(
                        r"[ ]{2,}",
                        " ",
                        content,
                    )

                normalized.append(
                    indentation + content
                )

            return "\n".join(normalized)

        # --------------------------------------------------
        # Markdown
        # --------------------------------------------------

        if context.is_markdown:

            inside_code_block = False

            normalized = []

            for line in text.splitlines():

                if line.strip().startswith("```"):

                    inside_code_block = not inside_code_block

                    normalized.append(line)

                    continue

                if inside_code_block:

                    normalized.append(line)

                    continue

                if COLLAPSE_MULTIPLE_SPACES:

                    line = re.sub(
                        r"[ ]{2,}",
                        " ",
                        line,
                    )

                normalized.append(line)

            return "\n".join(normalized)

        # --------------------------------------------------
        # Plain text / mixed
        # --------------------------------------------------

        if COLLAPSE_MULTIPLE_SPACES:

            text = re.sub(
                r"[ ]{2,}",
                " ",
                text,
            )

        return text