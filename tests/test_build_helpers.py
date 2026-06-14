"""
Unit/property coverage for the build helpers: canon() over many security technique names (idempotency
+ known families), safe_name/wl, and the build_llms title/summary extractor.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_obsidian as BO
import build_llms as BL


# ----------------------------- canon known mappings -----------------------------

KNOWN = [
    ("Reflected XSS", "Cross-Site Scripting (XSS)"),
    ("Stored Cross-Site Scripting", "Cross-Site Scripting (XSS)"),
    ("DOM-based XSS", "Cross-Site Scripting (XSS)"),
    ("Blind SQL Injection", "SQL Injection"),
    ("Error-based SQLi", "SQL Injection"),
    ("SSRF via image proxy", "Server-Side Request Forgery (SSRF)"),
    ("CSRF on password change", "CSRF"),
    ("XML External Entity (XXE)", "XXE"),
    ("Server-Side Template Injection", "SSTI"),
    ("Open Redirect in return_url", "Open Redirect"),
    ("CORS misconfiguration", "CORS Misconfiguration"),
    ("Path Traversal", "Path Traversal / LFI"),
    ("Local File Inclusion", "Path Traversal / LFI"),
    ("OS Command Injection", "Command Injection / RCE"),
    ("Remote Code Execution", "Command Injection / RCE"),
    ("Unrestricted File Upload", "File Upload"),
    ("Insecure Deserialization", "Insecure Deserialization"),
    ("Race condition on coupons", "Race Conditions"),
    ("Subdomain Takeover", "Subdomain Takeover"),
    ("IDOR on invoice id", "IDOR / Broken Access Control"),
    ("Broken Access Control", "IDOR / Broken Access Control"),
    ("GraphQL introspection / API security", "API Security"),
    ("Hardcoded credentials", "Information Disclosure"),
    ("Sensitive data exposure", "Information Disclosure"),
    ("OAuth misconfiguration", "Authentication & Session"),
    ("JWT none-alg bypass", "Authentication & Session"),
    ("Business logic flaw", "Business Logic"),
    ("Subdomain enumeration", "Recon & Enumeration"),
    ("Google dorking / OSINT", "OSINT"),
    ("Automated fuzzing with Burp", "Automation & Tooling"),
]


@pytest.mark.parametrize("raw,expected", KNOWN)
def test_canon_known(raw, expected):
    assert BO.canon(raw) == expected


@pytest.mark.parametrize("raw", [r for r, _ in KNOWN] + [
    "Some Brand New Technique", "HTTP Request Smuggling", "Cache Poisoning",
    "Prototype Pollution", "Mass Assignment", "Clickjacking", "Session Fixation",
    "NoSQL Injection", "LDAP Injection", "XPath Injection", "Host Header Injection",
    "Web Cache Deception", "Account Takeover", "2FA Bypass", "Rate Limit Bypass",
])
def test_canon_idempotent(raw):
    once = BO.canon(raw)
    assert BO.canon(once) == once               # canonical form is a fixed point


def test_canon_titlecase_fallback():
    assert BO.canon("totally unheard of thing") == "Totally Unheard Of Thing"


# ----------------------------- safe_name / wl -----------------------------

@pytest.mark.parametrize("raw,expected", [
    ("Cross-Site Scripting (XSS)", "Cross-Site Scripting (XSS)"),
    ("Path Traversal / LFI", "Path Traversal LFI"),
    ("IDOR / Broken Access Control", "IDOR Broken Access Control"),
    ("A#B|C", "A B C"),
    ("Name^[1]", "Name 1"),
    ("trailing...  ", "trailing"),
    ("plain", "plain"),
])
def test_safe_name(raw, expected):
    assert BO.safe_name(raw) == expected


@pytest.mark.parametrize("raw", ["Path Traversal / LFI", "IDOR / Broken Access Control", "A/B", "X:Y"])
def test_wl_aliases_unsafe(raw):
    assert BO.wl(raw) == f"[[{BO.safe_name(raw)}|{raw}]]"


@pytest.mark.parametrize("raw", ["CSRF", "XXE", "SSTI", "Open Redirect", "Market"])
def test_wl_no_alias_when_safe(raw):
    assert BO.wl(raw) == f"[[{raw}]]"


@pytest.mark.parametrize("raw", ["x" * 200, "y" * 91, "z" * 90, "Cross-Site Scripting (XSS)"])
def test_safe_name_caps_90(raw):
    assert len(BO.safe_name(raw)) <= 90


# ----------------------------- build_llms._title_and_summary -----------------------------

@pytest.mark.parametrize("text,title,summary", [
    ("# Title\n\nA summary.", "Title", "A summary."),
    ("# Only\n", "Only", ""),
    ("# T\n\n## Sub\nbody", "T", "body"),
    ("no h1\nsecond", "", "second"),
    ("# A\n> quote\nreal", "A", "real"),
    ("# A\n---\n| t |\nreal", "A", "real"),
    ("", "", ""),
    ("# Trim  \n\n   padded   ", "Trim", "padded"),
])
def test_llms_title_and_summary(text, title, summary):
    t, s = BL._title_and_summary(text)
    assert t == title and s == summary


@pytest.mark.parametrize("text", ["# x\n" + "y" * 400, "# h\n\n" + "z " * 200, "# a\n\nshort"])
def test_llms_summary_capped(text):
    _, s = BL._title_and_summary(text)
    assert len(s) <= 160


def test_llms_raw_base_is_github_or_empty():
    rb = BL._raw_base()
    assert rb == "" or rb.startswith("https://raw.githubusercontent.com/")
    if rb:
        assert rb.rstrip("/").endswith(("main", "master")) or "/Bug-Bounty-Knowledge/" in rb
