"""
encoders.py — standard encoding/transform helpers for crafting MINIMAL, in-scope proof-of-impact and
for WAF/filter-evasion analysis during authorized testing. These are generic transforms (the same ones
Burp's encoder offers), not target-specific payloads. Pure.
"""
from __future__ import annotations

import base64
from typing import List
from urllib.parse import quote


def url_encode(s: str, safe: str = "") -> str:
    return quote(s, safe=safe)


def double_url_encode(s: str) -> str:
    """Percent-encode twice — the classic filter-bypass check (server decodes once, validator saw raw)."""
    return quote(quote(s, safe=""), safe="")


def base64url(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")


def html_entities(s: str) -> str:
    """Encode every char as a decimal HTML entity (XSS filter-evasion analysis)."""
    return "".join(f"&#{ord(c)};" for c in s)


def path_traversal(depth: int, target: str = "etc/passwd") -> str:
    """Build a `../`*depth + target sequence for testing path-traversal reach in an AUTHORIZED target.
    Educational generator — does not access the filesystem."""
    if depth < 0:
        raise ValueError("depth must be >= 0")
    return "../" * depth + target.lstrip("/")


def case_permute(s: str) -> List[str]:
    """A few case variants (e.g. ScRiPt) for case-insensitive-filter checks. Bounded, not exhaustive."""
    return list({s.lower(), s.upper(), s.title(),
                 "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(s))})
