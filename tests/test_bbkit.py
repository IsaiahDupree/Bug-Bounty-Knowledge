"""
Unit tests for bbkit. CVSS expectations are the official FIRST.org v3.1 reference scores, so these
double as a conformance check. Pure, deterministic, no network, no live targets.
"""
import pytest

from bbkit import cvss, jwt_tool, severity, report, encoders


# ----------------------------- CVSS v3.1 (reference vectors) -----------------------------

def test_cvss_known_vectors():
    cases = {
        "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H": 9.8,   # unauth RCE-ish, scope unchanged
        "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H": 10.0,  # scope changed -> 10.0
        "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N": 6.1,   # canonical reflected XSS
        "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H": 7.8,   # local privilege escalation
        "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N": 0.0,   # no impact
    }
    for vec, expected in cases.items():
        assert cvss.score_vector(vec) == pytest.approx(expected), vec


def test_cvss_parse_rejects_missing_metrics():
    with pytest.raises(ValueError):
        cvss.parse_vector("CVSS:3.1/AV:N/AC:L")          # missing PR/UI/S/C/I/A


def test_cvss_roundup_is_ceiling_to_one_decimal():
    # IDOR read of others' data, network, no auth, no UI, scope unchanged -> 7.5
    assert cvss.score_vector("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N") == pytest.approx(7.5)


# ----------------------------- severity / CWE -----------------------------

def test_rating_bands():
    assert severity.rating(0.0) == "None"
    assert severity.rating(3.9) == "Low"
    assert severity.rating(6.1) == "Medium"
    assert severity.rating(7.8) == "High"
    assert severity.rating(9.8) == "Critical"
    with pytest.raises(ValueError):
        severity.rating(11.0)


def test_cwe_name_lookup_normalizes():
    assert severity.cwe_name("CWE-79") == "Cross-site Scripting (XSS)"
    assert severity.cwe_name("89") == "SQL Injection"
    assert severity.cwe_name("CWE-99999") is None


# ----------------------------- JWT structural analysis -----------------------------

def _jwt(header_b64, payload_b64):
    return f"{header_b64}.{payload_b64}.sig"


def test_jwt_decode_and_alg_none():
    # header {"alg":"none","typ":"JWT"}, payload {"user":"admin"} (no exp) — base64url, no padding
    import base64, json
    def b64(d): return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    tok = _jwt(b64({"alg": "none", "typ": "JWT"}), b64({"user": "admin"}))
    header, payload = jwt_tool.decode(tok)
    assert header["alg"] == "none" and payload["user"] == "admin"
    findings = jwt_tool.analyze(tok)
    assert any("alg:none" in f for f in findings)
    assert any("exp" in f for f in findings)            # missing-expiry flagged too


def test_jwt_hmac_keyconfusion_flagged():
    import base64, json
    def b64(d): return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    tok = _jwt(b64({"alg": "HS256"}), b64({"sub": "1", "exp": 9999999999}))
    findings = jwt_tool.analyze(tok)
    assert any("HS" in f and "key-confusion" in f for f in findings)


def test_jwt_rejects_malformed():
    with pytest.raises(ValueError):
        jwt_tool.decode("not-a-jwt")


# ----------------------------- encoders -----------------------------

def test_encoders():
    assert encoders.url_encode("a b/c") == "a%20b%2Fc"
    assert encoders.double_url_encode("<") == "%253C"           # %3C -> %253C
    assert encoders.html_entities("ab") == "&#97;&#98;"
    assert encoders.path_traversal(3) == "../../../etc/passwd"
    assert encoders.path_traversal(0, "/win.ini") == "win.ini"
    assert "AB" in encoders.case_permute("ab")
    with pytest.raises(ValueError):
        encoders.path_traversal(-1)


# ----------------------------- report rendering -----------------------------

def test_report_render_has_required_sections():
    f = report.Finding(
        title="Reflected XSS in search parameter",
        target="https://example-program-scope.test/search?q=",
        cwe="CWE-79",
        cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        summary="The q parameter is reflected without output encoding.",
        steps=["Browse to the search endpoint", "Submit a benign marker payload in q", "Observe it reflected unencoded"],
        impact="Script execution in a victim's session within the app origin.",
        remediation="Context-aware output encoding; CSP as defense in depth.",
        poc="q=<marker-proves-reflection>",
        references=["https://owasp.org/www-community/attacks/xss/"],
    )
    md = report.render(f)
    assert "Reflected XSS" in md
    assert "CVSS 6.1" in md and "Medium" in md
    assert "CWE-79 — Cross-site Scripting (XSS)" in md
    for section in ("## Summary", "## Steps to Reproduce", "## Impact", "## Remediation", "## References"):
        assert section in md
    assert "responsible disclosure" in md.lower()
    assert f.severity() == "Medium" and f.score() == pytest.approx(6.1)
