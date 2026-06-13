"""
severity.py — map a CVSS base score to the qualitative rating triage uses, and a small lookup of the
CWE ids that recur across the bug-bounty shelf. Pure.
"""
from __future__ import annotations

from typing import Optional

# CVSS v3.1 qualitative severity bands
BANDS = [(0.0, 0.0, "None"), (0.1, 3.9, "Low"), (4.0, 6.9, "Medium"),
         (7.0, 8.9, "High"), (9.0, 10.0, "Critical")]

# the CWE ids that come up most on web bug-bounty programs (id -> name)
CWE = {
    "CWE-79": "Cross-site Scripting (XSS)",
    "CWE-89": "SQL Injection",
    "CWE-78": "OS Command Injection",
    "CWE-918": "Server-Side Request Forgery (SSRF)",
    "CWE-639": "Insecure Direct Object Reference (IDOR) / Authorization Bypass",
    "CWE-352": "Cross-Site Request Forgery (CSRF)",
    "CWE-22": "Path Traversal",
    "CWE-611": "XML External Entity (XXE)",
    "CWE-502": "Deserialization of Untrusted Data",
    "CWE-287": "Improper Authentication",
    "CWE-862": "Missing Authorization",
    "CWE-269": "Improper Privilege Management",
    "CWE-601": "Open Redirect",
    "CWE-94": "Code Injection",
    "CWE-200": "Exposure of Sensitive Information",
    "CWE-434": "Unrestricted File Upload",
    "CWE-1336": "Server-Side Template Injection (SSTI)",
    "CWE-384": "Session Fixation",
    "CWE-798": "Use of Hard-coded Credentials",
}


def rating(score: float) -> str:
    """CVSS v3.1 qualitative rating for a base score in [0,10]."""
    if not 0.0 <= score <= 10.0:
        raise ValueError("score must be in [0, 10]")
    if score == 0.0:
        return "None"
    for lo, hi, label in BANDS:
        if lo <= score <= hi:
            return label
    return "Critical"


def cwe_name(cwe_id: str) -> Optional[str]:
    """Human name for a CWE id ('CWE-79' or '79'); None if not in the local table."""
    cid = cwe_id.upper().strip()
    if cid.isdigit():
        cid = "CWE-" + cid
    if not cid.startswith("CWE-"):
        cid = "CWE-" + cid.replace("CWE", "").strip("-")
    return CWE.get(cid)
