"""
jwt_tool.py — STRUCTURAL analysis of a JWT (no signature verification, no cracking). Decodes the
header/payload and flags the common misconfigurations a hunter checks first: `alg:none`, a weak/HMAC
where asymmetric is expected, missing expiry, and `kid` injection surface. Pure parsing only.
"""
from __future__ import annotations

import base64
import json
from typing import Dict, List, Tuple


def _b64url_decode(seg: str) -> bytes:
    pad = "=" * (-len(seg) % 4)
    return base64.urlsafe_b64decode(seg + pad)


def decode(token: str) -> Tuple[Dict, Dict]:
    """Return (header, payload) dicts from a JWT. Does NOT verify the signature. Raises on malformed."""
    parts = token.strip().split(".")
    if len(parts) not in (2, 3):
        raise ValueError("not a JWT (expected 2-3 dot-separated segments)")
    header = json.loads(_b64url_decode(parts[0]))
    payload = json.loads(_b64url_decode(parts[1]))
    return header, payload


def analyze(token: str) -> List[str]:
    """List of structural findings (strings). Empty list = nothing obvious from structure alone.
    Checks are advisory — confirm exploitability against the actual server in scope."""
    findings: List[str] = []
    header, payload = decode(token)
    alg = str(header.get("alg", "")).lower()
    if alg in ("none", ""):
        findings.append("alg:none — server may accept an unsigned token (CWE-347/CWE-287). Test in scope.")
    if alg.startswith("hs"):
        findings.append("HMAC (HS*) alg — if the server also accepts RS* with this key, test the "
                        "RS256->HS256 key-confusion class (use the public key as the HMAC secret).")
    if "kid" in header:
        findings.append("'kid' header present — check for path-traversal / SQLi in key lookup (kid injection).")
    if "exp" not in payload:
        findings.append("no 'exp' claim — token may not expire (CWE-613 insufficient session expiration).")
    if "alg" not in header:
        findings.append("no 'alg' in header — unusual; inspect how the server selects the verification alg.")
    return findings
