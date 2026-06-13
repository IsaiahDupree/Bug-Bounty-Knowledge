"""
build_index.py — INDEX.md: a file listing of every book reference + ONE cheap
cross-book synthesis (which vulnerability classes recur across the shelf, which
book to read for what). Run after run_all.py.
"""
from __future__ import annotations

import glob
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_book import _make_client, _call, MODEL

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "books"


def main() -> int:
    mds = sorted(BOOKS.glob("*.md"))
    digest, listing = [], []
    for m in mds:
        txt = m.read_text(errors="ignore")
        title = txt.splitlines()[0].lstrip("# ").strip()
        strats = re.findall(r"^###\s+(.+)$", txt, re.M)
        ov = ""
        mo = re.search(r"## Overview\s*\n+(.+)", txt)
        if mo:
            ov = mo.group(1).strip()[:300]
        listing.append(f"- **[{title}](books/{m.name})** — "
                       f"{len(strats)} techniques: {', '.join(s.strip() for s in strats[:8])}"
                       + (" …" if len(strats) > 8 else ""))
        digest.append(f"BOOK: {title}\nOVERVIEW: {ov}\nTECHNIQUES: {', '.join(strats)}\n")

    prompt = (
        "Below are technique digests from " + str(len(mds)) + " bug-bounty / web-security books. Write "
        "a concise Markdown cross-book synthesis with:\n"
        "## Vulnerability classes that RECUR across the shelf  (the consensus checklist — name + which "
        "books agree, e.g. XSS, SQLi, SSRF, IDOR/access-control, CSRF, XXE, SSTI, auth/session, recon)\n"
        "## Distinctive or advanced techniques  (things only one or two books cover)\n"
        "## Which book to read for what  (1 line each, by strength — recon vs web vulns vs reporting)\n"
        "## Responsible-use note  (for AUTHORIZED testing in scope + responsible disclosure only; these "
        "are study notes, not weaponized exploits — verify against current behavior).\nKeep it tight.\n\n"
        "DIGESTS:\n" + "\n".join(digest)
    )
    synth = _call(_make_client(), prompt, 2200)

    header = (
        "# Bug Bounty Knowledge — Index\n\n"
        f"AI-extracted technique references from **{len(mds)} bug-bounty / web-security books** "
        f"(model `{MODEL}`). For AUTHORIZED testing + responsible disclosure. Each links to its full "
        f"notes in `books/`.\n\n"
        "## Books\n" + "\n".join(listing) + "\n\n---\n\n" + synth + "\n"
    )
    (ROOT / "INDEX.md").write_text(header)
    print(f"wrote {ROOT/'INDEX.md'} ({len(mds)} books indexed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
