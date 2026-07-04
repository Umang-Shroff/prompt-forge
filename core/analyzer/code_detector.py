from __future__ import annotations

import re

from .config import CODE_MATCH_WEIGHT, MAX_CONFIDENCE, MIN_CODE_CONFIDENCE
from models import PromptData

from .detector import Detector
from .patterns import CODE_PATTERNS


class CodeDetector(Detector):
    """
    Detects whether the prompt contains source code.
    """

    @property
    def priority(self) -> int:
        return 10

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt
    
        score = 0.0
    
        # ----------------------------------
        # Existing language patterns
        # ----------------------------------
    
        for language, regexes in CODE_PATTERNS.items():
        
            matches = sum(
                bool(re.search(regex, text, re.MULTILINE))
                for regex in regexes
            )
    
            if matches:
            
                prompt.analysis.add_language(language)
    
                score += matches * CODE_MATCH_WEIGHT
    
        # ----------------------------------
        # Generic code signals
        # ----------------------------------
    
        generic_patterns = [
            r"\b(def|class|return|import|from|if|elif|else|for|while|try|except|finally)\b",
            r"\b(function|const|let|var|export|default|async|await)\b",
            r"\b(public|private|protected|static|void|new|package|namespace)\b",
            r"\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|JOIN)\b",
            r"[A-Za-z_][A-Za-z0-9_]*\s*\(",
            r"=>",
            r"\{|\}",
            r";",
            r"^\s{4,}\S",
            r"\t+\S",
            r"<[A-Za-z][^>]*>",
        ]
    
        for pattern in generic_patterns:
        
            if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
                score += CODE_MATCH_WEIGHT
    
        if score >= MIN_CODE_CONFIDENCE:
        
            prompt.analysis.mark_detected(
                "code",
                min(score, MAX_CONFIDENCE),
            )