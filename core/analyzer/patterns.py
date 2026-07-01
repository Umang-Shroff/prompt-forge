"""
Common detection patterns used by analyzer detectors.

Keeping all regular expressions in one place makes them
easy to maintain and extend.
"""

from __future__ import annotations


# ==========================================================
# Programming Languages
# ==========================================================

CODE_PATTERNS: dict[str, list[str]] = {
    "python": [
        r"\bdef\s+\w+\(",
        r"\bclass\s+\w+",
        r"\bimport\s+\w+",
        r"\bfrom\s+\w+\s+import\b",
        r"\bif\s+__name__\s*==\s*['\"]__main__['\"]",
    ],
    "java": [
        r"\bpublic\s+class\b",
        r"\bprivate\b",
        r"\bprotected\b",
        r"\bSystem\.out\.println",
        r"\bimplements\b",
        r"\bextends\b",
    ],
    "javascript": [
        r"\bfunction\b",
        r"\bconst\b",
        r"\blet\b",
        r"\bvar\b",
        r"=>",
    ],
    "typescript": [
        r"\binterface\b",
        r"\btype\b",
        r":\s*(string|number|boolean|any)",
        r"\bimplements\b",
    ],
    "cpp": [
        r"#include\s*<",
        r"\bstd::",
        r"\busing\s+namespace\b",
        r"\bcout\s*<<",
    ],
    "c": [
        r"#include\s*<stdio\.h>",
        r"\bprintf\s*\(",
        r"\bscanf\s*\(",
    ],
    "go": [
        r"\bpackage\s+main\b",
        r"\bfunc\b",
        r'fmt\.Print',
    ],
    "rust": [
        r"\bfn\s+main\b",
        r"\blet\s+mut\b",
        r"println!",
    ],
}


# ==========================================================
# Markdown
# ==========================================================

MARKDOWN_PATTERNS = [
    r"^#{1,6}\s",
    r"\*\*.+\*\*",
    r"\*.+\*",
    r"`{3}",
    r"\[.+\]\(.+\)",
    r"^\-\s",
    r"^\d+\.",
]


# ==========================================================
# SQL
# ==========================================================

SQL_PATTERNS = [
    r"\bSELECT\b",
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bCREATE\s+TABLE\b",
    r"\bALTER\s+TABLE\b",
    r"\bDROP\s+TABLE\b",
    r"\bWHERE\b",
    r"\bFROM\b",
]


# ==========================================================
# Logs
# ==========================================================

LOG_PATTERNS = [
    r"\bERROR\b",
    r"\bWARN\b",
    r"\bINFO\b",
    r"\bDEBUG\b",
    r"\d{4}-\d{2}-\d{2}",
    r"\d{2}:\d{2}:\d{2}",
    r"Traceback \(most recent call last\)",
    r"Exception:",
    r"at .+\(.+\)",
]