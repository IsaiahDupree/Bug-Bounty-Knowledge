"""
build_technique_docs.py — per-technique reference docs in the repo's `techniques/` folder. For each
canonical vulnerability-class it aggregates the `### <technique>` detail blocks from EVERY book that
covers it, and links to the bbkit code that helps with it (scoring, JWT analysis, encoding, reporting).

    python3 tools/build_technique_docs.py

Idempotent. Reuses canon()/FAMILIES from build_obsidian.
"""
from __future__ import annotations

import re
import sys
import glob
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_obsidian import canon, safe_name

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
OUT = REPO / "techniques"
GITHUB = "https://github.com/IsaiahDupree/Bug-Bounty-Knowledge"

# canonical technique -> (module, function/area, test node) implemented in bbkit/
TECHNIQUE_CODE = {
    "Authentication & Session": ("bbkit.jwt_tool", "decode / analyze",
                                 "tests/test_bbkit.py::test_jwt_decode_and_alg_none"),
    "Path Traversal / LFI": ("bbkit.encoders", "path_traversal / double_url_encode",
                             "tests/test_bbkit.py::test_encoders"),
    "Cross-Site Scripting (XSS)": ("bbkit.encoders", "html_entities / case_permute (filter-evasion analysis)",
                                   "tests/test_bbkit.py::test_encoders"),
    "Reporting & Disclosure": ("bbkit.report", "Finding / render",
                               "tests/test_bbkit.py::test_report_render_has_required_sections"),
}
# every finding also uses bbkit.cvss + bbkit.severity (cross-cutting) — noted in the doc footer.


def clean_book_title(md_title: str) -> str:
    t = re.sub(r"\{.*?\}|\[\d+\]|libgen.*|\.epub|\.pdf", "", md_title)
    t = re.sub(r"&_?0?39_?s?", "'", t)
    if " - " in t[:40]:
        t = t.split(" - ")[-1]
    return re.sub(r"\s+", " ", t).strip()[:70]


def parse_blocks(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = "Untitled"
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = clean_book_title(m.group(1))
    blocks, name, buf, in_sec = [], None, [], False
    for line in text.splitlines():
        if re.match(r"^##\s+Techniques", line, re.I):
            in_sec = True
            continue
        if in_sec and re.match(r"^##\s+\w", line):
            break
        if not in_sec:
            continue
        h = re.match(r"^###\s+(.+)$", line)
        if h:
            if name:
                blocks.append((name, "\n".join(buf).strip()))
            name, buf = h.group(1).strip().rstrip("."), []
        elif name:
            buf.append(line)
    if name:
        blocks.append((name, "\n".join(buf).strip()))
    return title, blocks


def main() -> int:
    notes = sorted(glob.glob(str(BOOKS / "*.md")))
    if not notes:
        print("no books/*.md — run run_all.py first")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    # Preserve hand-authored docs (e.g. curated playbooks): only generator-produced docs carry the
    # GEN_MARK. We remove stale generated docs at the end, never the authored ones.

    agg = {}
    for p in notes:
        title, blocks = parse_blocks(Path(p))
        for name, body in blocks:
            agg.setdefault(canon(name), []).append((title, name, body))

    rows = []
    for tech in sorted(agg):
        entries = agg[tech]
        books = sorted({e[0] for e in entries})
        code = TECHNIQUE_CODE.get(tech)
        lines = [f"# {tech}", "",
                 f"_Aggregated from **{len(books)}** book(s) on the [Bug-Bounty-Knowledge]({GITHUB}) "
                 f"shelf. For AUTHORIZED testing + responsible disclosure._", ""]
        if code:
            mod, fn, test = code
            lines += [f"**Helper code:** `{mod}.{fn}`  ·  **Test:** `{test}`",
                      f"```bash\npytest {test.split('::')[0]} -k {test.split('::')[-1].replace('test_','')}\n```", ""]
        lines += ["**Books:** " + ", ".join(books), "", "---", "", "## How the shelf describes it", ""]
        for book, orig, body in entries:
            label = f'{book} — as "{orig}"' if orig.lower() != tech.lower() else book
            lines += [f"### {label}", "", body or "_(no detail extracted)_", ""]
        lines += ["---", "_Score every confirmed finding with `bbkit.cvss` + `bbkit.severity`, "
                  "write it up with `bbkit.report`._"]
        (OUT / (safe_name(tech) + ".md")).write_text("\n".join(lines), encoding="utf-8")
        rows.append((tech, len(books), bool(code), safe_name(tech) + ".md"))

    # remove STALE generated docs (carry the GEN_MARK but no longer produced); keep authored docs
    GEN_MARK = "## How the shelf describes it"
    produced = {fname for _, _, _, fname in rows} | {"README.md"}
    preserved = []
    for existing in OUT.glob("*.md"):
        if existing.name in produced:
            continue
        if GEN_MARK in existing.read_text(errors="ignore"):
            existing.unlink()                       # stale generated doc
        else:
            preserved.append(existing.name)         # hand-authored — keep

    rows.sort(key=lambda r: -r[1])
    idx = ["# Techniques", "",
           f"Per-technique references aggregated across the {len(notes)}-book shelf. Each links every "
           "book that describes the vulnerability class and, where built, its bbkit helper + tests.", "",
           "| Technique / Vuln class | Books | Code | Doc |", "|---|---|---|---|"]
    for tech, nb, has_code, fname in rows:
        idx.append(f"| {tech} | {nb} | {'✅' if has_code else '—'} | [{fname}](./{fname.replace(' ', '%20')}) |")
    (OUT / "README.md").write_text("\n".join(idx), encoding="utf-8")

    coded = sum(1 for r in rows if r[2])
    extra = f" + {len(preserved)} authored preserved" if preserved else ""
    print(f"techniques/ → {len(rows)} technique docs ({coded} linked to code), 1 README{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
