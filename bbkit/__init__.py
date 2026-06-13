"""
bbkit — executable, dependency-free helpers for AUTHORIZED bug-bounty work and responsible disclosure.
The analog of Trading-Knowledge's strategy_lib, built from the security book shelf. Everything here is
DEFENSIVE / analytical: severity scoring, JWT structural analysis, report generation, and standard
encoding helpers for crafting minimal proof-of-impact in scope. No target-specific exploits, no
mass-exploitation tooling. Every function is pure and unit-tested in tests/test_bbkit.py.
"""
from . import cvss, jwt_tool, severity, report, encoders  # noqa: F401

__all__ = ["cvss", "jwt_tool", "severity", "report", "encoders"]
