from __future__ import annotations

import tiktoken

class TokenCounter:
    """
    Central token counting utility.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.encoder = tiktoken.encoding_for_model(model)

    def count(self, text: str) -> int:
        return len(self.encoder.encode(text))
    