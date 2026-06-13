"""
Broad coverage for the rest of bbkit: severity bands + CWE table, JWT structural analysis across many
token shapes, encoder transforms, and report rendering invariants. Parametrized, real assertions.
"""
import base64
import json
import itertools
import pytest

from bbkit import severity, jwt_tool, encoders, report


# ----------------------------- severity bands -----------------------------

BAND_POINTS = {
    0.0: "None",
    0.1: "Low", 1.0: "Low", 2.5: "Low", 3.8: "Low", 3.9: "Low",
    4.0: "Medium", 5.0: "Medium", 6.0: "Medium", 6.8: "Medium", 6.9: "Medium",
    7.0: "High", 7.5: "High", 8.0: "High", 8.8: "High", 8.9: "High",
    9.0: "Critical", 9.5: "Critical", 9.8: "Critical", 10.0: "Critical",
}


@pytest.mark.parametrize("score,label", list(BAND_POINTS.items()))
def test_rating_bands(score, label):
    assert severity.rating(score) == label


@pytest.mark.parametrize("score", [round(x * 0.5, 1) for x in range(0, 21)])   # every 0.5, 0.0–10.0
def test_rating_consistent_with_numeric_bands(score):
    r = severity.rating(score)
    assert r in ("None", "Low", "Medium", "High", "Critical")
    if score == 0.0:
        assert r == "None"
    elif score < 4.0:
        assert r == "Low"
    elif score < 7.0:
        assert r == "Medium"
    elif score < 9.0:
        assert r == "High"
    else:
        assert r == "Critical"


@pytest.mark.parametrize("bad", [-0.1, 10.1, 11, -5])
def test_rating_rejects_out_of_range(bad):
    with pytest.raises(ValueError):
        severity.rating(bad)


@pytest.mark.parametrize("cwe_id,name", list(severity.CWE.items()))
def test_cwe_table_complete(cwe_id, name):
    assert severity.cwe_name(cwe_id) == name
    assert severity.cwe_name(cwe_id.replace("CWE-", "")) == name      # numeric form
    assert severity.cwe_name(cwe_id.lower()) == name                  # case-insensitive


@pytest.mark.parametrize("unknown", ["CWE-999999", "0", "CWE-abc", "not-a-cwe"])
def test_cwe_unknown_returns_none(unknown):
    assert severity.cwe_name(unknown) is None


# ----------------------------- JWT structural analysis -----------------------------

def _b64(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")


def _tok(header, payload):
    return f"{_b64(header)}.{_b64(payload)}.sig"


@pytest.mark.parametrize("alg", ["none", "None", "NONE", "nOnE"])
def test_jwt_alg_none_variants_flagged(alg):
    findings = jwt_tool.analyze(_tok({"alg": alg}, {"sub": "1", "exp": 9999999999}))
    assert any("alg:none" in f for f in findings)


@pytest.mark.parametrize("alg", ["HS256", "HS384", "HS512", "hs256"])
def test_jwt_hmac_keyconfusion_flagged(alg):
    findings = jwt_tool.analyze(_tok({"alg": alg}, {"sub": "1", "exp": 9999999999}))
    assert any("key-confusion" in f for f in findings)


@pytest.mark.parametrize("alg", ["RS256", "ES256", "PS256"])
def test_jwt_asymmetric_not_flagged_for_hmac(alg):
    findings = jwt_tool.analyze(_tok({"alg": alg}, {"sub": "1", "exp": 9999999999}))
    assert not any("key-confusion" in f for f in findings)


def test_jwt_missing_exp_flagged():
    assert any("exp" in f for f in jwt_tool.analyze(_tok({"alg": "RS256"}, {"sub": "1"})))


def test_jwt_kid_present_flagged():
    findings = jwt_tool.analyze(_tok({"alg": "RS256", "kid": "../../x"}, {"exp": 1}))
    assert any("kid" in f for f in findings)


def test_jwt_decode_roundtrip():
    h, p = jwt_tool.decode(_tok({"alg": "HS256", "typ": "JWT"}, {"user": "admin", "exp": 1}))
    assert h["typ"] == "JWT" and p["user"] == "admin"


@pytest.mark.parametrize("bad", ["", "onlyone", "a.b.c.d.e", "not-base64-@@@.x.y"])
def test_jwt_malformed_raises(bad):
    with pytest.raises(Exception):
        jwt_tool.decode(bad)


# ----------------------------- encoders -----------------------------

@pytest.mark.parametrize("raw,enc", [
    ("a b", "a%20b"), ("/", "%2F"), ("<", "%3C"), (">", "%3E"),
    ("&", "%26"), ("#", "%23"), ("a/b c", "a%2Fb%20c"),
])
def test_url_encode(raw, enc):
    assert encoders.url_encode(raw) == enc


@pytest.mark.parametrize("raw", ["<", "/", " ", "../", "a b/c"])
def test_double_url_encode_is_encode_of_encode(raw):
    assert encoders.double_url_encode(raw) == encoders.url_encode(encoders.url_encode(raw, safe=""), safe="")


@pytest.mark.parametrize("s", ["a", "ab", "abc", "<script>", "x" * 20])
def test_html_entities_roundtrips_to_codepoints(s):
    out = encoders.html_entities(s)
    assert out == "".join(f"&#{ord(c)};" for c in s)


@pytest.mark.parametrize("depth,target,expected", [
    (0, "etc/passwd", "etc/passwd"),
    (1, "etc/passwd", "../etc/passwd"),
    (3, "etc/passwd", "../../../etc/passwd"),
    (5, "/win.ini", "../../../../../win.ini"),
])
def test_path_traversal(depth, target, expected):
    assert encoders.path_traversal(depth, target) == expected


@pytest.mark.parametrize("depth", range(0, 12))
def test_path_traversal_depth_count(depth):
    assert encoders.path_traversal(depth, "x").count("../") == depth


def test_path_traversal_negative_raises():
    with pytest.raises(ValueError):
        encoders.path_traversal(-1)


@pytest.mark.parametrize("s", ["script", "alert", "AbC"])
def test_case_permute_contains_upper_lower(s):
    variants = encoders.case_permute(s)
    assert s.upper() in variants and s.lower() in variants


@pytest.mark.parametrize("raw", ["payload", "../../x", "<svg>", "a=b&c=d"])
def test_base64url_decodes_back(raw):
    enc = encoders.base64url(raw)
    pad = "=" * (-len(enc) % 4)
    assert base64.urlsafe_b64decode(enc + pad).decode() == raw


# ----------------------------- report rendering -----------------------------

CWES = ["CWE-79", "CWE-89", "CWE-918", "CWE-639", "CWE-352"]
VECTORS = [
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
]


@pytest.mark.parametrize("cwe,vector", list(itertools.product(CWES, VECTORS)))
def test_report_render_invariants(cwe, vector):
    f = report.Finding(
        title="Finding", target="https://scope.test/x", cwe=cwe, cvss_vector=vector,
        summary="s", steps=["one", "two"], impact="i", remediation="r",
        poc="marker", references=["https://ref"],
    )
    md = report.render(f)
    for section in ("# Finding", "## Summary", "## Steps to Reproduce", "## Impact", "## Remediation"):
        assert section in md
    assert f"CVSS {f.score():.1f}" in md
    assert f.severity() in md
    assert cwe in md
    assert "1. one" in md and "2. two" in md
    assert "responsible disclosure" in md.lower()


def test_report_without_optional_fields():
    f = report.Finding("T", "scope", "CWE-79", "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
                       "s", ["x"], "i", "r")
    md = report.render(f)
    assert "## References" not in md and "Proof of Concept" not in md
