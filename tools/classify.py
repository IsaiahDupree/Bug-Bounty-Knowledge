"""
classify.py — discern which knowledge-base a downloaded book belongs to, so each repo's pipeline
processes ONLY its own corpus (Trading-Knowledge takes finance/trading/crypto; Bug-Bounty-Knowledge
takes security/hacking). Shared, identical logic in both repos.

Weighted keyword scoring over the filename: strong domain phrases ("bug bounty", "algorithmic trading")
outweigh weak/ambiguous single words ("crypto", "python"). Returns the dominant category, or "other"
when neither domain clears a minimum, or "ambiguous" when the two are close.

    python3 tools/classify.py [dir]      # list every book in ~/Downloads (or dir) with its category

`crypto` is deliberately weak + dual-counted: crypto-CURRENCY (trading) vs crypto-GRAPHY (security) is
decided by the surrounding strong terms, never by "crypto" alone.
"""
from __future__ import annotations

import os
import re
import sys
import glob
from pathlib import Path

# (keyword, weight). Multi-word domain phrases are strong; single ambiguous words are weak.
TRADING = [
    ("algorithmic trading", 10), ("day trading", 10), ("mean reversion", 9), ("market making", 9),
    ("technical analysis", 8), ("black scholes", 8), ("short-selling", 8), ("short selling", 8),
    ("trading", 6), ("forex", 7), ("algo", 5), ("scalping", 7), ("candlestick", 7),
    ("stock", 5), ("market", 4), ("invest", 5), ("portfolio", 5), ("options", 4), ("quant", 5),
    ("hft", 7), ("high-frequency", 8), ("momentum", 4), ("backtest", 5), ("smart money", 5),
    ("contrarian", 5), ("reinforcement learning", 3), ("neural network", 2),
]
BUGBOUNTY = [
    ("bug bounty", 12), ("bug hunting", 11), ("bug hunting", 11), ("ethical hacking", 10),
    ("penetration test", 10), ("pentest", 9), ("red team", 9), ("attack surface", 9),
    ("web security", 9), ("vulnerabilit", 8), ("exploit", 7), ("owasp", 9), ("recon", 6),
    ("osint", 7), ("hacking", 8), ("hacker", 6), ("cybersecurity", 8), ("cyber security", 8),
    ("malware", 7), ("reverse engineering", 7), ("burp", 8), ("ctf", 7), ("offensive security", 9),
    ("responsible disclosure", 9), ("application security", 8), ("appsec", 8), ("xss", 7),
    ("sql injection", 8), ("ssrf", 8),
]
# weak ambiguous terms counted for BOTH (decided by company they keep)
AMBIGUOUS = {"crypto": ("trading", "bugbounty"), "python": (None, None), "ai": (None, None)}

MIN_SCORE = 5       # below this for the top domain -> "other"
MARGIN = 3          # winner must beat runner-up by this much, else "ambiguous"


def score(name: str):
    s = name.lower()
    t = sum(w for kw, w in TRADING if kw in s)
    b = sum(w for kw, w in BUGBOUNTY if kw in s)
    # "crypto" nudges whichever domain already has signal (currency vs graphy); never decides alone
    if "crypto" in s:
        if t > b:
            t += 2
        elif b > t:
            b += 2
    return t, b


def classify(name: str) -> str:
    t, b = score(name)
    top, lo = (max(t, b), min(t, b))
    if top < MIN_SCORE:
        return "other"
    if top - lo < MARGIN:
        return "ambiguous"
    return "trading" if t > b else "bugbounty"


def category_of(path: str) -> str:
    return classify(os.path.basename(path))


def books_in(directory: str):
    return sorted(glob.glob(os.path.join(directory, "*.epub")) +
                  glob.glob(os.path.join(directory, "*.pdf")))


def main() -> int:
    d = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads")
    rows = [(category_of(p), os.path.basename(p)) for p in books_in(d)]
    from collections import Counter
    counts = Counter(c for c, _ in rows)
    print(f"{d}  —  {len(rows)} books: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for cat in ("trading", "bugbounty", "ambiguous", "other"):
        items = [n for c, n in rows if c == cat]
        if items:
            print(f"\n[{cat}] ({len(items)})")
            for n in items:
                t, b = score(n)
                print(f"  t{t:>2} b{b:>2}  {n[:78]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
