from __future__ import annotations

import re

from core.regions import (
    Region,
    RegionType,
)
from ..regions.inline_code_splitter import InlineCodeSplitter

class RegionClassifier:

    _FENCE = re.compile(
        r"```.*?```",
        re.DOTALL,
    )

    def __init__(self) -> None:

        self._splitter = InlineCodeSplitter()

    def classify(
        self,
        text: str,
    ) -> list[Region]:

        regions: list[Region] = []

        last = 0

        for match in self._FENCE.finditer(text):

            if match.start() > last:

                regions.extend(
                    self._classify_plain(
                        text[last:match.start()]
                    )
                )

            regions.append(
                Region(
                    type=RegionType.CODE,
                    text=match.group(),
                    compressible=False,
                    is_code=True,
                )
            )

            last = match.end()

        if last < len(text):

            regions.extend(
                self._classify_plain(
                    text[last:]
                )
            )

        return regions

    def _classify_plain(
        self,
        text: str,
    ) -> list[Region]:
    
        text = text.strip()
    
        if not text:
            return []
    
        split_regions = self._splitter.split(text)
    
        regions: list[Region] = []
    
        for is_code, block in split_regions:
        
            block = block.strip()
    
            if not block:
                continue
            
            lower = block.lower()
    
            if self._looks_like_json(block):
            
                regions.append(
                    Region(
                        type=RegionType.JSON,
                        text=block,
                        compressible=False,
                    )
                )
    
                continue
            
            if self._looks_like_xml(block):
            
                regions.append(
                    Region(
                        type=RegionType.XML,
                        text=block,
                        compressible=False,
                    )
                )
    
                continue
            
            if self._looks_like_sql(lower):
            
                regions.append(
                    Region(
                        type=RegionType.SQL,
                        text=block,
                        compressible=False,
                    )
                )
    
                continue
            
            if self._looks_like_log(block):
            
                regions.append(
                    Region(
                        type=RegionType.LOG,
                        text=block,
                        compressible=False,
                    )
                )
    
                continue
            
            if is_code or self._looks_like_code(block):
            
                regions.append(
                    Region(
                        type=RegionType.CODE,
                        text=block,
                        compressible=False,
                        is_code=True,
                    )
                )
    
                continue
            
            regions.append(
                Region(
                    type=RegionType.TEXT,
                    text=block,
                    compressible=True,
                )
            )
    
        return regions

    def _looks_like_json(self, text: str) -> bool:

        return (
            text.startswith("{")
            or text.startswith("[")
        )

    def _looks_like_xml(self, text: str) -> bool:

        return (
            text.startswith("<")
            and "</" in text
        )

    def _looks_like_sql(self, text: str) -> bool:

        keywords = (
            "select ",
            "insert ",
            "update ",
            "delete ",
            "create table",
            "alter table",
            "drop table",
        )

        return any(
            k in text
            for k in keywords
        )

    def _looks_like_log(self, text: str) -> bool:

        return bool(
            re.search(
                r"\d{4}-\d\d-\d\d.*?(ERROR|WARN|INFO)",
                text,
            )
        )

    def _looks_like_code(
        self,
        text: str,
    ) -> bool:

        score = 0

        # ---------------------------------
        # Language keywords
        # ---------------------------------

        keyword_patterns = (
            r"\bclass\b",
            r"\bdef\b",
            r"\bimport\b",
            r"\bfrom\b",
            r"\breturn\b",
            r"\bfunction\b",
            r"\bconst\b",
            r"\blet\b",
            r"\bvar\b",
            r"\basync\b",
            r"\bawait\b",
            r"\bpublic\b",
            r"\bprivate\b",
            r"\bprotected\b",
            r"\bstatic\b",
            r"\bvoid\b",
            r"\bnew\b",
            r"\binterface\b",
            r"\bextends\b",
            r"\bimplements\b",
            r"\bpackage\b",
            r"\bnamespace\b",
            r"\busing\b",
            r"\bSELECT\b",
            r"\bINSERT\b",
            r"\bUPDATE\b",
            r"\bDELETE\b",
            r"\bFROM\b",
            r"\bWHERE\b",
            r"\bJOIN\b",
        )

        for pattern in keyword_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE | re.MULTILINE,
            ):
                score += 2

        # ---------------------------------
        # Function / method calls
        # ---------------------------------

        score += len(
            re.findall(
                r"[A-Za-z_][A-Za-z0-9_]*\s*\(",
                text,
            )
        )

        # ---------------------------------
        # Member access
        # ---------------------------------

        score += len(
            re.findall(
                r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_]",
                text,
            )
        )

        # ---------------------------------
        # Operators
        # ---------------------------------

        operators = (
            "=>",
            "::",
            "==",
            "!=",
            "<=",
            ">=",
            "+=",
            "-=",
            "*=",
            "/=",
            "=",
            "{",
            "}",
            ";",
        )

        for op in operators:
            score += text.count(op)

        # ---------------------------------
        # JSX / HTML
        # ---------------------------------

        score += len(
            re.findall(
                r"</?[A-Za-z][^>]*>",
                text,
            )
        )

        # ---------------------------------
        # Python indentation
        # ---------------------------------

        if re.search(
            r"^\s{4,}\S",
            text,
            re.MULTILINE,
        ):
            score += 3

        # ---------------------------------
        # CamelCase identifiers
        # ---------------------------------

        score += len(
            re.findall(
                r"\b[a-z]+[A-Z][A-Za-z0-9]*\b",
                text,
            )
        )

        return score >= 8