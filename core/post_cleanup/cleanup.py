from __future__ import annotations

import re


class PostCompressionCleanup:
    """
    Cleans artifacts introduced by LLMLingua.
    """

    def clean(
        self,
        text: str,
    ) -> str:
    
        import re
    
        # Duplicate words
        text = re.sub(
            r"\b([A-Za-z0-9_]+)\b(?:\s+\1\b)+",
            r"\1",
            text,
            flags=re.IGNORECASE,
        )
    
        # Remove duplicate non-empty lines
        seen: set[str] = set()
        result: list[str] = []
    
        for line in text.splitlines():
        
            stripped = line.strip()
    
            if not stripped:
                result.append("")
                continue
            
            key = stripped.casefold()
    
            if key in seen:
                continue
            
            seen.add(key)
            result.append(line)
    
        text = "\n".join(result)
    
        # Duplicate punctuation
        text = re.sub(
            r"([.,!?;:])(?:\s*\1)+",
            r"\1",
            text,
        )
    
        # Spaces before punctuation
        text = re.sub(
            r"\s+([,.;:!?])",
            r"\1",
            text,
        )
    
        # Multiple spaces
        text = re.sub(
            r" {2,}",
            " ",
            text,
        )
    
        # Collapse blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )
    
        return text.strip()