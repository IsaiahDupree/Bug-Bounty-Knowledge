"""
Book → plain text. EPUB via zip + BeautifulSoup (always available); PDF via
pypdf if installed. Returns concatenated readable text; strips scripts/styles.
"""
from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup


def epub_text(path: str) -> str:
    z = zipfile.ZipFile(path)
    # opf spine gives true reading order; fall back to sorted html names.
    docs = [n for n in z.namelist() if n.lower().endswith((".xhtml", ".html", ".htm"))]
    docs.sort()
    parts = []
    for n in docs:
        try:
            soup = BeautifulSoup(z.read(n), "html.parser")
        except Exception:
            continue
        for tag in soup(["script", "style"]):
            tag.decompose()
        t = soup.get_text(" ", strip=True)
        if t:
            parts.append(t)
    return "\n\n".join(parts)


def pdf_text(path: str) -> Optional[str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        r = PdfReader(path)
        return "\n\n".join((pg.extract_text() or "") for pg in r.pages)
    except Exception:
        return None


def book_text(path: str) -> Optional[str]:
    pl = str(path).lower()
    if pl.endswith(".epub"):
        return epub_text(path)
    if pl.endswith(".pdf"):
        return pdf_text(path)
    return None
