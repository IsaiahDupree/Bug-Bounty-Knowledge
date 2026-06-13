"""
build_llms.py — make the whole knowledge base trivially LLM-ingestable.

Emits, at the repo root:
  • llms.txt        — navigation index (llmstxt.org style): every doc with its title + 1-line summary
                       + relative path, grouped by folder. Small; for an agent to pick what to read.
  • llms-full.txt   — the ENTIRE corpus concatenated into one file (clear `# === FILE: path ===`
                       separators) for single-shot ingestion / RAG chunking.
  • llms.txt.gz, llms-full.txt.gz — gzip counterparts (≈3-5x smaller; same content).

Repo-agnostic: walks whichever doc folders exist (books/, strategies/, techniques/, code-strategies/)
plus README.md + INDEX.md. Run after the other build_* tools.

    python3 tools/build_llms.py
"""
from __future__ import annotations

import glob
import gzip
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# doc folders in preferred reading order; only those that exist are used
FOLDERS = ["", "books", "strategies", "techniques", "code-strategies"]
TOP_FILES = ["README.md", "INDEX.md"]


def _title_and_summary(text: str):
    lines = text.splitlines()
    title = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), "")
    # first non-empty, non-heading, non-blockquote line as the summary
    summary = ""
    for l in lines[1:]:
        s = l.strip()
        if s and not s.startswith(("#", ">", "---", "|", "```")):
            summary = re.sub(r"\s+", " ", s)[:160]
            break
    return title, summary


def _docs():
    """Ordered list of (relpath, text), deduped."""
    seen, out = set(), []
    for name in TOP_FILES:
        p = ROOT / name
        if p.exists():
            seen.add(p.resolve()); out.append((name, p.read_text(errors="ignore")))
    for folder in FOLDERS:
        base = ROOT / folder if folder else ROOT
        if not base.is_dir():
            continue
        for fp in sorted(glob.glob(str(base / "*.md"))):
            rp = Path(fp).resolve()
            if rp in seen:
                continue
            seen.add(rp)
            rel = os.path.relpath(fp, ROOT)
            out.append((rel, Path(fp).read_text(errors="ignore")))
    return out


def main() -> int:
    docs = _docs()
    repo_title, repo_summary = _title_and_summary((ROOT / "README.md").read_text(errors="ignore")) \
        if (ROOT / "README.md").exists() else (ROOT.name, "")

    # --- llms.txt (navigation index) ---
    idx = [f"# {repo_title}", "", f"> {repo_summary}" if repo_summary else "",
           "", "Machine-readable index of this knowledge base. Each entry: title — summary (path).", ""]
    by_folder = {}
    for rel, text in docs:
        folder = os.path.dirname(rel) or "(root)"
        t, s = _title_and_summary(text)
        by_folder.setdefault(folder, []).append((t or rel, s, rel))
    for folder in sorted(by_folder, key=lambda f: (f != "(root)", f)):
        idx.append(f"## {folder}")
        for t, s, rel in by_folder[folder]:
            idx.append(f"- [{t}]({rel})" + (f" — {s}" if s else ""))
        idx.append("")
    llms = "\n".join(idx).rstrip() + "\n"
    (ROOT / "llms.txt").write_text(llms)

    # --- llms-full.txt (whole corpus, one file) ---
    parts = [f"# {repo_title} — full corpus",
             f"# {len(docs)} documents concatenated for LLM ingestion. Separator: '# === FILE: <path> ==='",
             ""]
    for rel, text in docs:
        parts.append(f"\n# === FILE: {rel} ===\n")
        parts.append(text.rstrip())
    full = "\n".join(parts).rstrip() + "\n"
    (ROOT / "llms-full.txt").write_text(full)

    # --- gzip counterparts ---
    for fname in ("llms.txt", "llms-full.txt"):
        data = (ROOT / fname).read_bytes()
        with gzip.open(ROOT / (fname + ".gz"), "wb") as fh:
            fh.write(data)

    full_kb = len(full.encode()) / 1024
    gz_kb = (ROOT / "llms-full.txt.gz").stat().st_size / 1024
    print(f"llms.txt ({len(docs)} docs indexed) + llms-full.txt ({full_kb:.0f}KB → "
          f"{gz_kb:.0f}KB gz, {full_kb/gz_kb:.1f}x) + .gz counterparts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
