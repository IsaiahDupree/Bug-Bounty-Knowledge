"""
Extensive CVSS v3.1 conformance + invariant tests. Two kinds, both non-circular:
  1. curated reference vectors with hand-verified published base scores;
  2. property/invariant tests over a deterministic sample of the metric space (range, 0.1 granularity,
     no-impact==0, and monotonicity in every metric) — these catch formula regressions without
     needing a known score for each case.
"""
import itertools
import pytest

from bbkit import cvss

# --- 1. curated reference vectors (hand-verified) ---
REFERENCE = {
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H": 9.8,
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H": 10.0,
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N": 6.1,
    "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H": 7.8,
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N": 0.0,
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N": 7.5,
    "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H": 8.1,
    "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H": 8.8,
    "CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H": 8.8,
    "CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H": 6.8,
    "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H": 7.2,
    "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N": 5.3,
}


@pytest.mark.parametrize("vector,expected", list(REFERENCE.items()))
def test_cvss_reference_scores(vector, expected):
    assert cvss.score_vector(vector) == pytest.approx(expected)


# --- 2a. deterministic sample of the metric space ---
AVv, ACv, PRv, UIv, Sv, CIAv = ["N", "A", "L", "P"], ["L", "H"], ["N", "L", "H"], ["N", "R"], ["U", "C"], ["N", "L", "H"]
ALL = list(itertools.product(AVv, ACv, PRv, UIv, Sv, CIAv, CIAv, CIAv))   # 5184 combos


def _vec(c):
    return "CVSS:3.1/AV:%s/AC:%s/PR:%s/UI:%s/S:%s/C:%s/I:%s/A:%s" % c


SAMPLE = [_vec(c) for c in ALL[::34]]            # ~152 evenly-spaced cases


@pytest.mark.parametrize("vector", SAMPLE)
def test_cvss_in_range_and_tenth_granularity(vector):
    s = cvss.score_vector(vector)
    assert 0.0 <= s <= 10.0
    assert abs(s * 10 - round(s * 10)) < 1e-9          # always a multiple of 0.1


@pytest.mark.parametrize("c", ALL[::40])             # ~130 cases
def test_cvss_no_impact_is_zero(c):
    # any vector with C=I=A=N must score exactly 0.0, regardless of exploitability metrics
    av, ac, pr, ui, s, *_ = c
    v = _vec((av, ac, pr, ui, s, "N", "N", "N"))
    assert cvss.score_vector(v) == 0.0


# --- 2b. monotonicity: easing any exploitability metric must not DECREASE the score ---
ORDER = {"AV": ["P", "L", "A", "N"], "AC": ["H", "L"], "PR": ["H", "L", "N"], "UI": ["R", "N"]}
BASES = [
    {"AV": "P", "AC": "H", "PR": "H", "UI": "R", "S": "U", "C": "L", "I": "L", "A": "L"},
    {"AV": "P", "AC": "H", "PR": "H", "UI": "R", "S": "C", "C": "H", "I": "H", "A": "H"},
    {"AV": "L", "AC": "H", "PR": "L", "UI": "R", "S": "U", "C": "H", "I": "N", "A": "L"},
]
MONO_CASES = [(metric, base) for metric in ORDER for base in BASES]


@pytest.mark.parametrize("metric,base", MONO_CASES)
def test_cvss_monotonic_in_exploitability(metric, base):
    scores = []
    for val in ORDER[metric]:
        m = dict(base, **{metric: val})
        scores.append(cvss.base_score(m))
    assert scores == sorted(scores), f"{metric} not monotonic: {scores}"


# --- 2c. monotonicity in impact metrics (N <= L <= H) ---
IMPACT_BASES = [
    {"AV": "N", "AC": "L", "PR": "N", "UI": "N", "S": "U"},
    {"AV": "N", "AC": "L", "PR": "N", "UI": "N", "S": "C"},
    {"AV": "L", "AC": "H", "PR": "L", "UI": "R", "S": "U"},
]
IMPACT_CASES = [(dim, base) for dim in ("C", "I", "A") for base in IMPACT_BASES]


@pytest.mark.parametrize("dim,base", IMPACT_CASES)
def test_cvss_monotonic_in_impact(dim, base):
    scores = []
    for val in ("N", "L", "H"):
        m = dict(base)
        m["C"], m["I"], m["A"] = "N", "N", "N"
        m[dim] = val                                  # vary one impact dim, others None
        scores.append(cvss.base_score(m))
    assert scores == sorted(scores)


# --- 2d. scope:changed never scores below scope:unchanged for identical other metrics ---
@pytest.mark.parametrize("c", ALL[::60])             # ~87 cases
def test_cvss_scope_changed_not_lower(c):
    av, ac, pr, ui, _s, cc, ii, aa = c
    if (cc, ii, aa) == ("N", "N", "N"):
        return                                       # both 0; nothing to compare
    u = cvss.score_vector(_vec((av, ac, pr, ui, "U", cc, ii, aa)))
    ch = cvss.score_vector(_vec((av, ac, pr, ui, "C", cc, ii, aa)))
    assert ch >= u - 1e-9


# --- parsing robustness ---
@pytest.mark.parametrize("vector", SAMPLE[:40])
def test_cvss_parse_roundtrips(vector):
    m = cvss.parse_vector(vector)
    assert set(("AV", "AC", "PR", "UI", "S", "C", "I", "A")).issubset(m)
    assert cvss.base_score(m) == cvss.score_vector(vector)


@pytest.mark.parametrize("bad", [
    "CVSS:3.1/AV:N", "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H", "", "garbage", "CVSS:3.1/",
])
def test_cvss_parse_rejects_incomplete(bad):
    with pytest.raises(ValueError):
        cvss.parse_vector(bad)
