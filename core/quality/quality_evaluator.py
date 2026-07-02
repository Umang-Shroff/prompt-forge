from __future__ import annotations

import re


from models import (
    IntentType,
    PromptData,
)

class QualityEvaluator:
    """
    Evaluates the quality of a prompt and updates PromptData.
    """

    def evaluate(
        self,
        prompt: PromptData,
    ) -> None:

        text = prompt.current_prompt

        quality = prompt.quality

        # ---------------------------------
        # Clarity
        # ---------------------------------

        quality.clarity = 100.0

        vague_words = (
            "something",
            "anything",
            "maybe",
            "etc",
            "somehow",
        )

        for word in vague_words:

            if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                quality.clarity -= 10

        # ---------------------------------
        # Structure
        # ---------------------------------

        quality.structure = 60.0

        if "\n" in text:
            quality.structure += 20

        if any(
            marker in text
            for marker in (
                "- ",
                "* ",
                "1.",
                "2.",
            )
        ):
            quality.structure += 20

        # ---------------------------------
        # Conciseness
        # ---------------------------------

        words = len(text.split())

        if words < 50:
            quality.conciseness = 100.0

        elif words < 100:
            quality.conciseness = 90.0

        elif words < 200:
            quality.conciseness = 75.0

        else:
            quality.conciseness = 60.0

        # ---------------------------------
        # Completeness
        # ---------------------------------

        quality.completeness = 50.0

        # ---------------------------------
        # Specificity
        # ---------------------------------
        
        quality.specificity = 70.0
        
        if prompt.intent.has(IntentType.ROLE):
            quality.specificity += 15
        
        if prompt.optimization_hints.preferred_keywords:
            quality.specificity += 15

        # ---------------------------------
        # Overall
        # ---------------------------------

        quality.overall = round(
            (
                quality.clarity
                + quality.structure
                + quality.conciseness
                + quality.completeness
                + quality.specificity
            )
            / 5,
            1,
        )