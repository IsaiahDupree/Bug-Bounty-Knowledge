"""Tests for the build pipeline (previously untested): the markdown parsers and the
canonicalization / filename / title helpers that turn extracted book notes into the
techniques/ docs and the Obsidian vault. A bug here silently misfiles a whole vuln
class across every generated doc, so these lock the behavior down.

xfail markers flag REAL bugs in canon() substring-precedence (generic families shadow
specific ones) — see test_canon_known_misclassification_bugs.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_obsidian as BO
import build_technique_docs as BT
import keyloader as KL


# --------------------------------------------------------------------------- canon()

@pytest.mark.parametrize("raw,expected", [
    ("Reflected XSS", "Cross-Site Scripting (XSS)"),
    ("Stored cross-site scripting", "Cross-Site Scripting (XSS)"),
    ("Blind SQLi", "SQL Injection"),
    ("UNION-based SQL injection", "SQL Injection"),
    ("SSRF via webhook", "Server-Side Request Forgery (SSRF)"),
    ("IDOR on /profile", "IDOR / Broken Access Control"),
    ("OAuth login bypass", "Authentication & Session"),
    ("Path traversal", "Path Traversal / LFI"),
    ("Local File Inclusion (LFI)", "Path Traversal / LFI"),
    ("Remote Code Execution", "Command Injection / RCE"),
    ("XML External Entity (XXE)", "XXE"),
    ("Server-Side Template Injection", "SSTI"),
    ("CORS misconfiguration", "CORS Misconfiguration"),
    ("Race condition in coupon redemption", "Race Conditions"),
    ("GraphQL mass assignment", "API Security"),
])
def test_canon_correct_classifications(raw, expected):
    assert BO.canon(raw) == expected


def test_canon_titlecase_fallback_for_unknown():
    assert BO.canon("some   novel   technique") == "Some Novel Technique"


def test_canon_subdomain_takeover_is_its_own_family():
    # fixed: Subdomain Takeover is listed before the broad Recon family ('subdomain')
    assert BO.canon("Subdomain Takeover") == "Subdomain Takeover"


def test_canon_csrf_token_is_csrf():
    # fixed: CSRF is listed before Authentication (whose generic 'token' used to shadow it)
    assert BO.canon("CSRF token theft") == "CSRF"


def test_canon_hardcoded_credentials_is_info_disclosure():
    # fixed: Information Disclosure ('hardcoded') is listed before Auth ('credential')
    assert BO.canon("Hardcoded credentials in JS") == "Information Disclosure"


# ----------------------------------------------------------------------- safe_name()

@pytest.mark.parametrize("raw,expected", [
    ("A/B:C#D|E", "A B C D E"),
    ("weird [name] {junk}", "weird name {junk}"),   # only []\/:#^| are stripped; {} kept
    ("trailing dots... ", "trailing dots"),
    ("Name^[1]", "Name 1"),
    ("plain title", "plain title"),
])
def test_safe_name(raw, expected):
    assert BO.safe_name(raw) == expected


def test_safe_name_truncates_to_90():
    out = BO.safe_name("x" * 200)
    assert len(out) <= 90 and out == "x" * 90


def test_safe_name_is_filesystem_safe():
    bad = 'a/b\\c:d#e^f[g]h|i'
    out = BO.safe_name(bad)
    assert not any(ch in out for ch in '/\\:#^[]|')


# ------------------------------------------------------------------------------ wl()

def test_wl_plain_name_no_alias():
    assert BO.wl("Clean Name") == "[[Clean Name]]"


def test_wl_unsafe_name_gets_alias():
    # safe_name changes "A/B" -> "A B", so the wikilink must keep the display alias
    assert BO.wl("A/B") == "[[A B|A/B]]"


# --------------------------------------------------------------- clean_book_title()

@pytest.mark.parametrize("raw,expected", [
    ("Some Author - Great Bug Bounty Book {libgen}.epub", "Great Bug Bounty Book"),
    ("Title with [12] junk.pdf", "Title with junk"),
    ("Web Hacking 101", "Web Hacking 101"),
])
def test_clean_book_title(raw, expected):
    assert BT.clean_book_title(raw) == expected


def test_clean_book_title_caps_length():
    assert len(BT.clean_book_title("z" * 200)) <= 70


def test_clean_book_title_current_entity_behavior():
    # Regression lock of CURRENT behavior: the apostrophe-entity regex strips "&039"
    # but leaves the trailing ";" (see xfail below for the intended clean result).
    assert BT.clean_book_title("Peter &039;s Handbook") == "Peter ';s Handbook"


@pytest.mark.xfail(reason="clean_book_title regex '&_?0?39_?s?' strips '&039' but leaves the "
                          "HTML-entity terminator ';' (and does not match the '&#039;' form at all).",
                   strict=True)
def test_clean_book_title_should_fully_clean_apostrophe_entity():
    assert BT.clean_book_title("Peter &039;s Handbook") == "Peter 's Handbook"


# ---------------------------------------------------------------- parse_blocks() / parse_book()

FIXTURE = """# Jane Doe - The Web Hacker's Field Guide {libgen}.epub

## Overview
A practical guide to finding web vulnerabilities.

## Techniques & Vulnerability Classes

### Cross-Site Scripting (XSS)
Reflected and stored XSS.
Use HTML-entity encoding to test filters.

### SQL Injection.
Union-based and blind extraction.

## Tools
Burp Suite, sqlmap.

### This Heading Is Outside The Section
should be ignored
"""


def _write(tmp_path, text):
    p = tmp_path / "book.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_parse_blocks_extracts_named_blocks(tmp_path):
    title, blocks = BT.parse_blocks(_write(tmp_path, FIXTURE))
    assert title == "The Web Hacker's Field Guide"
    names = [n for n, _ in blocks]
    assert names == ["Cross-Site Scripting (XSS)", "SQL Injection"]  # trailing '.' stripped
    body0 = dict(blocks)["Cross-Site Scripting (XSS)"]
    assert "Reflected and stored XSS." in body0
    assert "HTML-entity encoding" in body0
    # the "### outside" heading after '## Tools' must NOT be captured
    assert all("Outside The Section" not in n for n in names)


def test_parse_blocks_stops_at_next_h2(tmp_path):
    title, blocks = BT.parse_blocks(_write(tmp_path, FIXTURE))
    bodies = "\n".join(b for _, b in blocks)
    assert "Burp Suite" not in bodies  # '## Tools' content excluded


def test_parse_blocks_no_section_returns_empty(tmp_path):
    title, blocks = BT.parse_blocks(_write(tmp_path, "# Only A Title\n\nNo techniques here.\n"))
    assert blocks == []


def test_parse_book_matches_block_names(tmp_path):
    # build_obsidian.parse_book returns just the raw technique names from the same section
    title, names = BO.parse_book(_write(tmp_path, FIXTURE))
    assert title == "Jane Doe - The Web Hacker's Field Guide {libgen}.epub"  # raw title, not cleaned
    assert names == ["Cross-Site Scripting (XSS)", "SQL Injection"]


def test_parse_book_and_parse_blocks_agree_on_names(tmp_path):
    p = _write(tmp_path, FIXTURE)
    _, names = BO.parse_book(p)
    _, blocks = BT.parse_blocks(p)
    assert names == [n for n, _ in blocks]


# ------------------------------------------------------------------- keyloader._read_key

def test_read_key_basic(tmp_path):
    env = tmp_path / ".env"
    env.write_text('ANTHROPIC_API_KEY="fake-anthropic-value"\nOTHER=foo\n')
    assert KL._read_key(str(env), "ANTHROPIC_API_KEY") == "fake-anthropic-value"


def test_read_key_strips_single_quotes(tmp_path):
    env = tmp_path / ".env"
    env.write_text("OPENAI_API_KEY='fake-openai-value'\n")
    assert KL._read_key(str(env), "OPENAI_API_KEY") == "fake-openai-value"


def test_read_key_missing_file_returns_none():
    assert KL._read_key("/nonexistent/path/.env", "ANTHROPIC_API_KEY") is None


def test_read_key_absent_name_returns_none(tmp_path):
    env = tmp_path / ".env"
    env.write_text("SOMETHING_ELSE=x\n")
    assert KL._read_key(str(env), "ANTHROPIC_API_KEY") is None


def test_read_key_prefix_not_confused(tmp_path):
    # "ANTHROPIC_API_KEY_OLD" must not satisfy a request for "ANTHROPIC_API_KEY"
    env = tmp_path / ".env"
    env.write_text("ANTHROPIC_API_KEY_OLD=stale\n")
    assert KL._read_key(str(env), "ANTHROPIC_API_KEY") is None


@pytest.mark.xfail(reason="_read_key uses startswith(name + '='), so 'KEY = value' with "
                          "spaces around '=' (valid in some .env styles) is not matched.",
                   strict=True)
def test_read_key_tolerates_spaces_around_equals(tmp_path):
    env = tmp_path / ".env"
    env.write_text("ANTHROPIC_API_KEY = spaced-value\n")
    assert KL._read_key(str(env), "ANTHROPIC_API_KEY") == "spaced-value"


def test_get_key_prefers_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "env-value")
    assert KL.get_key("ANTHROPIC_API_KEY") == "env-value"


def test_get_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("DEFINITELY_NOT_A_KEY", raising=False)
    with pytest.raises(RuntimeError):
        KL.get_key("DEFINITELY_NOT_A_KEY")
