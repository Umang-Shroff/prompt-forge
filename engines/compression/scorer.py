from __future__ import annotations


class ImportanceScorer:
    """
    Lightweight heuristic scorer for chunk importance.
    Used before passing to LongLLMLingua.
    """

    KEYWORDS = [
        "important",
        "must",
        "critical",
        "note",
        "warning",
        "error",
        "step",
        "goal",
        "requirements",
    ]

    def score(self, text: str) -> float:

        score = 0.0
        lower = text.lower()

        # keyword boost
        for kw in self.KEYWORDS:
            if kw in lower:
                score += 1.0

        # length penalty (very long chunks less important)
        if len(text) > 1000:
            score -= 0.5

        # code boost
        if "{" in text or "def " in text or "class " in text:
            score += 0.5

        return score