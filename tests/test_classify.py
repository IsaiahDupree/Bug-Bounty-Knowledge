"""Tests for the shared book classifier — the discernment between the trading corpus and the
bug-bounty corpus must stay clean. Real filenames from ~/Downloads are used as fixtures."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import classify as C


TRADING_TITLES = [
    "Algorithmic Trading Systems and Strategies_ A New Approach.epub",
    "Laurent Bernut - Algorithmic Short-Selling with Python.pdf",
    "Contrarian Trading For Forex_Stock_Crypto_ Leave the Herd.pdf",
    "Haim Bodek - The Problem of HFT - High Frequency Trading.epub",
    "Van Der Post - Coding Black Scholes_ Algorithmic Options Trading.epub",
    "High Probability Scalping Strategy Playbook.epub",
]
BUGBOUNTY_TITLES = [
    "Alex Thomas, Ghostlulz - Bug Bounty Playbook v1 (2019).pdf",
    "Sanjib Sinha - Bug Bounty Hunting For Web Security.pdf",
    "Jann Moon - Enumerating Esoteric Attack Surfaces_ Recon for Bug Bounty.pdf",
    "Redefining Hacking_ A Guide to Red Teaming and Bug Bounty Hunting.epub",
    "Syed Abuthahir - The secret of bug hunting. Bug bounty automation with python.pdf",
    "John Jackson - Corporate Cybersecurity_ Bug Bounty Program.pdf",
]


def test_trading_titles_classify_trading():
    for t in TRADING_TITLES:
        assert C.classify(t) == "trading", t


def test_bugbounty_titles_classify_bugbounty():
    for t in BUGBOUNTY_TITLES:
        assert C.classify(t) == "bugbounty", t


def test_no_cross_contamination():
    # the single most important property: a trading book never reads as bugbounty and vice-versa
    assert all(C.classify(t) != "bugbounty" for t in TRADING_TITLES)
    assert all(C.classify(t) != "trading" for t in BUGBOUNTY_TITLES)


def test_crypto_is_disambiguated_by_context():
    # "crypto" alone must not decide; the strong neighbour wins
    assert C.classify("Crypto Trading Mastery_ Forex and Day Trading.pdf") == "trading"
    assert C.classify("Attacking Modern Crypto_ Web Security and Exploitation.pdf") == "bugbounty"


def test_unrelated_book_is_other():
    assert C.classify("Gardening for Beginners_ A Seasonal Guide.epub") == "other"
    assert C.classify("French Cooking Made Simple.pdf") == "other"
