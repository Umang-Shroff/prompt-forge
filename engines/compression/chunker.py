from __future__ import annotations

import re
from typing import List


class PromptChunker:
    """
    Splits text into semantically useful chunks.
    """

    def chunk(self, text: str) -> List[str]:

        # split by double newline first (paragraph structure)
        paragraphs = re.split(r"\n\s*\n", text)

        chunks: List[str] = []

        for p in paragraphs:

            p = p.strip()

            if not p:
                continue

            # further split large paragraphs
            if len(p) > 800:
                sentences = re.split(r"(?<=[.!?])\s+", p)
                chunks.extend(sentences)
            else:
                chunks.append(p)

        return chunks