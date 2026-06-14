"""
Integration tests over the ACTUAL generated docs (books/ + techniques/) and the index/llms/manifest
artifacts — every doc must be well-formed and parseable by the build pipeline. No mocks; real files.
One consolidated test per doc (multiple asserts) keeps coverage high without test-count bloat.
"""
import glob
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_obsidian as BO
import build_technique_docs as BT

BOOKS = sorted(glob.glob(str(ROOT / "books" / "*.md")))
TECHS = [p for p in sorted(glob.glob(str(ROOT / "techniques" / "*.md")))
         if Path(p).name != "README.md"]
GEN_MARK = "## How the shelf describes it"
GEN_TECHS = [p for p in TECHS if GEN_MARK in Path(p).read_text(errors="ignore")]
AUTHORED_TECHS = [p for p in TECHS if GEN_MARK not in Path(p).read_text(errors="ignore")]
MANIFEST = json.loads((ROOT / "manifest.json").read_text())


def test_corpus_present():
    assert len(BOOKS) >= 12 and len(GEN_TECHS) >= 30


@pytest.mark.parametrize("path", BOOKS, ids=lambda p: Path(p).stem[:28])
def test_book_doc(path):
    text = Path(path).read_text(errors="ignore")
    assert re.search(r"^#\s+\S", text, re.M), "no H1"
    assert "Source book:" in text or "AI-generated research summary" in text
    assert re.search(r"^##\s+Techniques", text, re.M | re.I), "no Techniques section"
    title, names = BO.parse_book(Path(path))
    assert title and len(names) >= 1, "no techniques parsed"
    _, blocks = BT.parse_blocks(Path(path))
    assert [n for n, _ in blocks] == names
    for n in names:
        c = BO.canon(n)
        assert c and BO.canon(c) == c                 # stable canonical family


@pytest.mark.parametrize("path", GEN_TECHS, ids=lambda p: Path(p).stem[:28])
def test_generated_technique_doc(path):
    text = Path(path).read_text(errors="ignore")
    assert re.search(r"^#\s+\S", text, re.M)
    assert "**Books:**" in text and GEN_MARK in text   # attributes its source books
    assert not any(ch in Path(path).stem for ch in '\\/:#^[]|')   # safe filename


@pytest.mark.parametrize("path", AUTHORED_TECHS or [None], ids=lambda p: Path(p).stem[:28] if p else "none")
def test_authored_technique_is_substantial(path):
    if path is None:
        pytest.skip("no hand-authored technique docs")
    text = Path(path).read_text(errors="ignore")
    assert len(text) > 500 and re.search(r"^#\s+\S", text, re.M)


# ----------------------------- index / llms / manifest -----------------------------

def test_index_lists_books():
    idx = (ROOT / "INDEX.md").read_text(errors="ignore")
    assert "Bug Bounty Knowledge" in idx and idx.count("](books/") >= 12


def test_llms_files_exist():
    for f in ("llms.txt", "llms-full.txt", "llms.txt.gz", "llms-full.txt.gz", "manifest.json"):
        assert (ROOT / f).exists(), f"missing {f}"


def test_manifest_well_formed():
    assert MANIFEST["name"] and MANIFEST["document_count"] == len(MANIFEST["documents"])
    assert MANIFEST["entrypoints"]["full_corpus"] == "llms-full.txt"


@pytest.mark.parametrize("doc", MANIFEST["documents"], ids=lambda d: d["path"][:30])
def test_manifest_entry_points_to_real_file(doc):
    assert (ROOT / doc["path"]).exists(), f"manifest references missing {doc['path']}"
    assert doc["title"]
    assert doc["raw_url"] is None or doc["raw_url"].startswith("https://raw.githubusercontent.com/")
    # every catalogued doc is also in the single-file corpus
    full = (ROOT / "llms-full.txt").read_text(errors="ignore")
    assert f"# === FILE: {doc['path']} ===" in full
