"""
report.py — turn a confirmed finding into a clean disclosure report (the deliverable that gets paid
and triaged fast). Renders the standard structure: title, severity+CVSS, CWE, scope, repro steps,
minimal PoC, impact, remediation, references. Pure string-building.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .cvss import score_vector
from .severity import rating, cwe_name


@dataclass
class Finding:
    title: str
    target: str                       # in-scope asset/endpoint
    cwe: str                          # e.g. "CWE-79"
    cvss_vector: str                  # e.g. "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"
    summary: str
    steps: List[str]                  # numbered reproduction steps
    impact: str
    remediation: str
    poc: Optional[str] = None         # minimal proof-of-impact (no destructive actions)
    references: List[str] = field(default_factory=list)

    def score(self) -> float:
        return score_vector(self.cvss_vector)

    def severity(self) -> str:
        return rating(self.score())


def render(f: Finding) -> str:
    """Markdown report for one finding."""
    cwe_label = cwe_name(f.cwe)
    cwe_line = f"{f.cwe}" + (f" — {cwe_label}" if cwe_label else "")
    out = [
        f"# {f.title}",
        "",
        f"- **Severity:** {f.severity()} (CVSS {f.score():.1f})",
        f"- **CVSS vector:** `{f.cvss_vector}`",
        f"- **CWE:** {cwe_line}",
        f"- **Affected target (in scope):** {f.target}",
        "",
        "## Summary",
        f.summary,
        "",
        "## Steps to Reproduce",
    ]
    out += [f"{i}. {s}" for i, s in enumerate(f.steps, 1)]
    if f.poc:
        out += ["", "## Proof of Concept (minimal, non-destructive)", "", "```", f.poc, "```"]
    out += [
        "",
        "## Impact",
        f.impact,
        "",
        "## Remediation",
        f.remediation,
    ]
    if f.references:
        out += ["", "## References"] + [f"- {r}" for r in f.references]
    out += ["", "---", "_Tested under program scope and rules of engagement; reported via the program "
            "channel (responsible disclosure). No data exfiltrated beyond proving impact._"]
    return "\n".join(out)
