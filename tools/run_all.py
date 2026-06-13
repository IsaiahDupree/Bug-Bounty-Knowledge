"""
run_all.py — analyze every BUG-BOUNTY / SECURITY book in ~/Downloads into a technique .md in
../books/. Resumable: skips books already done.

Uses the shared classifier (classify.py) so it processes ONLY books that discern as `bugbounty` —
trading/finance/crypto books are left for the Trading-Knowledge repo. Run `python3 tools/classify.py`
to see how every Downloads book is categorized.

    python3 tools/run_all.py
"""
from __future__ import annotations

import glob
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_book import analyze, slugify, clean_title, MODEL, PROVIDER
from classify import category_of

DOWNLOADS = str(Path.home() / "Downloads")
OUT = str(Path(__file__).resolve().parents[1] / "books")
CATEGORY = "bugbounty"      # this repo's corpus


def main() -> int:
    all_books = sorted(glob.glob(os.path.join(DOWNLOADS, "*.epub")) +
                       glob.glob(os.path.join(DOWNLOADS, "*.pdf")))
    books = [b for b in all_books if category_of(b) == CATEGORY]
    skipped_other = len(all_books) - len(books)
    Path(OUT).mkdir(parents=True, exist_ok=True)
    print(f"provider={PROVIDER} model={MODEL} · {len(books)} {CATEGORY} books "
          f"({skipped_other} non-{CATEGORY} skipped) · → {OUT}\n")
    done = skip = err = 0
    t0 = time.time()
    for b in books:
        slug = slugify(os.path.basename(b))
        out = os.path.join(OUT, f"{slug}.md")
        title = clean_title(os.path.basename(b))[:60]
        if os.path.exists(out):
            print(f"  skip   {title}")
            skip += 1
            continue
        print(f"  ▶ {title}")
        try:
            analyze(b, OUT)
            print(f"    ✓ {slug}.md")
            done += 1
        except Exception as e:
            print(f"    ✗ {e}")
            err += 1
    print(f"\ndone={done} skip={skip} err={err}  ({int(time.time()-t0)}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
