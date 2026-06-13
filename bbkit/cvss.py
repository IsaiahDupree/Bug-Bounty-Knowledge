"""
cvss.py — CVSS v3.1 Base Score calculator (pure, spec-exact). Turn a finding's metrics into the
number triage teams expect on a report. Implements the official FIRST.org v3.1 formula including the
exact `roundup` and the scope-dependent Privileges-Required weights.

    from bbkit.cvss import base_score, parse_vector
    base_score(parse_vector("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"))  # -> 9.8
"""
from __future__ import annotations

import math
from typing import Dict

AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
AC = {"L": 0.77, "H": 0.44}
UI = {"N": 0.85, "R": 0.62}
CIA = {"H": 0.56, "L": 0.22, "N": 0.00}
PR_UNCHANGED = {"N": 0.85, "L": 0.62, "H": 0.27}
PR_CHANGED = {"N": 0.85, "L": 0.68, "H": 0.50}   # Scope:Changed raises the value of having privileges

REQUIRED = ("AV", "AC", "PR", "UI", "S", "C", "I", "A")


def parse_vector(vector: str) -> Dict[str, str]:
    """Parse a 'CVSS:3.1/AV:N/.../A:H' string into {metric: value}. Raises on missing base metrics."""
    parts = [p for p in vector.strip().split("/") if p and not p.upper().startswith("CVSS:")]
    m = {}
    for p in parts:
        if ":" in p:
            k, v = p.split(":", 1)
            m[k.upper()] = v.upper()
    missing = [k for k in REQUIRED if k not in m]
    if missing:
        raise ValueError(f"missing base metrics: {missing}")
    return m


def _roundup(x: float) -> float:
    """CVSS v3.1 roundup: smallest 1-decimal number >= x (avoids float drift via integer math)."""
    i = round(x * 100000)
    if i % 10000 == 0:
        return i / 100000.0
    return (math.floor(i / 10000) + 1) / 10.0


def base_score(m: Dict[str, str]) -> float:
    """CVSS v3.1 Base Score (0.0–10.0) from a parsed metric dict."""
    scope_changed = m["S"].upper() == "C"
    pr_table = PR_CHANGED if scope_changed else PR_UNCHANGED
    iss = 1 - (1 - CIA[m["C"]]) * (1 - CIA[m["I"]]) * (1 - CIA[m["A"]])
    if scope_changed:
        impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    else:
        impact = 6.42 * iss
    exploitability = 8.22 * AV[m["AV"]] * AC[m["AC"]] * pr_table[m["PR"]] * UI[m["UI"]]
    if impact <= 0:
        return 0.0
    raw = (1.08 if scope_changed else 1.0) * (impact + exploitability)
    return _roundup(min(raw, 10.0))


def score_vector(vector: str) -> float:
    return base_score(parse_vector(vector))
