from __future__ import annotations

from models import NormalizationContext

from .normalizer import Normalizer


class CodeFenceNormalizer(Normalizer):
    """
    Remove unnecessary blank lines immediately inside Markdown code fences.
    """

    @property
    def priority(self) -> int:
        return 70

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        if not context.is_markdown:
            return text

        lines = text.splitlines()

        normalized: list[str] = []

        inside_code = False
        skip_leading_blank = False

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("```"):

                inside_code = not inside_code

                normalized.append(line)

                skip_leading_blank = inside_code

                continue

            if inside_code:

                if skip_leading_blank and not stripped:
                    continue

                skip_leading_blank = False

            normalized.append(line)

        while (
            len(normalized) >= 2
            and normalized[-1].strip() == ""
            and normalized[-2].strip().startswith("```")
        ):
            normalized.pop(-2)

        return "\n".join(normalized)