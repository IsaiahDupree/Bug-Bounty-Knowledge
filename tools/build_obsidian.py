"""
build_obsidian.py — sync the extracted technique notes into the Obsidian vault as a categorized
knowledge base: one note per book + a Map-of-Content (MOC) per vulnerability-class/technique that
wikilinks every book covering it + a top-level index.

    python3 tools/build_obsidian.py            # -> ~/.memory/vault/Bug Bounty Books
    VAULT=/path/to/vault python3 tools/build_obsidian.py

Idempotent: rewrites the "Bug Bounty Books" subtree each run. Source of truth = books/*.md in this repo.
"""
from __future__ import annotations

import os
import re
import glob
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = REPO / "books"
VAULT = Path(os.environ.get("VAULT", str(Path.home() / ".memory" / "vault")))
ROOT = VAULT / "Bug Bounty Books"
GITHUB = "https://github.com/IsaiahDupree/Bug-Bounty-Knowledge"

# canonical technique/vuln-class -> substrings that map to it.
# ORDER MATTERS: canon() returns the FIRST family with a matching substring, so SPECIFIC named vuln
# classes are listed BEFORE broad attribute families (e.g. CSRF before Authentication so CSRF's "csrf"
# is matched before Auth's generic "token"; Subdomain Takeover before Recon's generic "subdomain";
# Information Disclosure before Auth so "hardcoded credentials" -> Info Disclosure not "credential").
FAMILIES = {
    # --- specific, named vulnerability classes (most precise first) ---
    "Cross-Site Scripting (XSS)": ["xss", "cross-site scripting", "cross site scripting"],
    "SQL Injection": ["sql injection", "sqli", "blind sql", "union-based"],
    "Server-Side Request Forgery (SSRF)": ["ssrf", "server-side request", "server side request"],
    "CSRF": ["csrf", "cross-site request forgery", "cross site request"],
    "XXE": ["xxe", "xml external entity", "external entity"],
    "SSTI": ["ssti", "template injection", "server-side template"],
    "Open Redirect": ["open redirect", "unvalidated redirect"],
    "CORS Misconfiguration": ["cors", "cross-origin"],
    "Path Traversal / LFI": ["path traversal", "directory traversal", "lfi", "local file inclusion",
                             "file inclusion"],
    "Command Injection / RCE": ["command injection", "rce", "remote code execution", "code execution",
                                "os command"],
    "File Upload": ["file upload", "unrestricted upload", "upload bypass"],
    "Insecure Deserialization": ["deserialization", "deserialisation", "pickle", "object injection"],
    "Race Conditions": ["race condition", "toctou", "concurrency"],
    "Subdomain Takeover": ["subdomain takeover", "dangling dns"],
    "IDOR / Broken Access Control": ["idor", "insecure direct object", "broken access", "bola",
                                     "authorization bypass", "privilege escalation", "access control"],
    "API Security": ["api security", "rest api", "graphql", "api endpoint", "mass assignment"],
    # --- broad attribute families (after the specific ones above) ---
    "Information Disclosure": ["information disclosure", "info leak", "sensitive data", "exposure",
                               "secret", "hardcoded"],
    "Authentication & Session": ["authentication", "session", "jwt", "oauth", "login", "credential",
                                 "password reset", "mfa", "2fa", "token"],
    "Business Logic": ["business logic", "logic flaw", "logic bug", "workflow"],
    "Recon & Enumeration": ["recon", "reconnaissance", "enumeration", "subdomain", "asset discovery",
                            "fingerprint", "content discovery", "directory brute"],
    "OSINT": ["osint", "open source intelligence", "google dork", "dorking"],
    "Automation & Tooling": ["automation", "scripting", "burp", "scanner", "fuzzing", "fuzz"],
    "Reporting & Disclosure": ["report", "disclosure", "triage", "writing the report", "bounty program"],
}


def safe_name(title: str) -> str:
    t = re.sub(r"[\\/:#\^\[\]|]+", " ", title)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:90].rstrip(" .")


def wl(name: str) -> str:
    s = safe_name(name)
    return f"[[{s}]]" if s == name else f"[[{s}|{name}]]"


def canon(technique: str) -> str:
    s = technique.lower()
    for fam, subs in FAMILIES.items():
        if any(sub in s for sub in subs):
            return fam
    return re.sub(r"\s+", " ", technique).strip().title()


def parse_book(path: Path):
    """(title, [raw technique names]) from a books/*.md note's '## Techniques' section."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = "Untitled"
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    techniques = []
    in_sec = False
    for line in text.splitlines():
        if re.match(r"^##\s+Techniques", line, re.I):
            in_sec = True
            continue
        if in_sec and re.match(r"^##\s+\w", line):
            break
        if in_sec:
            h = re.match(r"^###\s+(.+)$", line)
            if h:
                name = h.group(1).strip().rstrip(".")
                if name:
                    techniques.append(name)
    return title, techniques


def main() -> int:
    notes = sorted(glob.glob(str(BOOKS / "*.md")))
    if not notes:
        print("no books/*.md found — run run_all.py first")
        return 1
    if ROOT.exists():
        shutil.rmtree(ROOT)
    (ROOT / "books").mkdir(parents=True, exist_ok=True)
    (ROOT / "MOCs").mkdir(parents=True, exist_ok=True)

    books = []
    tech_to_books = {}
    for p in notes:
        title, raw = parse_book(Path(p))
        note_name = safe_name(title)
        cs = []
        for r in raw:
            c = canon(r)
            if c not in cs:
                cs.append(c)
            tech_to_books.setdefault(c, set()).add(note_name)
        books.append((note_name, title, cs, Path(p)))

    for note_name, title, cs, srcpath in books:
        body = srcpath.read_text(encoding="utf-8", errors="ignore")
        tags = ["bug-bounty-book"] + [
            "technique/" + re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-") for c in cs
        ]
        fm = ["---", f'title: "{title}"', "tags:"] + [f"  - {t}" for t in tags] + ["---", ""]
        links = "**Techniques covered:** " + ", ".join(wl(c) for c in cs) if cs else ""
        gh = f"**Repo note:** [{srcpath.name}]({GITHUB}/blob/main/books/{srcpath.name})"
        (ROOT / "books" / f"{note_name}.md").write_text(
            "\n".join(fm) + f"{links}\n\n{gh}\n\n---\n\n" + body, encoding="utf-8")

    recurring = []
    for tech in sorted(tech_to_books):
        bks = sorted(tech_to_books[tech])
        if len(bks) >= 2:
            recurring.append((tech, len(bks)))
        fm = ["---", f'title: "{tech}"', "tags:", "  - bug-bounty-technique-moc", "---", ""]
        lines = fm + [f"# {tech}", "", f"_Books on this shelf that cover **{tech}** ({len(bks)}):_", ""]
        lines += [f"- [[{b}]]" for b in bks]
        lines += ["", "---", "[[Bug Bounty Books MOC|← all bug bounty books]]"]
        (ROOT / "MOCs" / f"{safe_name(tech)}.md").write_text("\n".join(lines), encoding="utf-8")

    recurring.sort(key=lambda x: -x[1])
    idx = ["---", 'title: "Bug Bounty Books MOC"', "tags:", "  - moc", "---", "",
           "# Bug Bounty Books — Map of Content", "",
           f"AI-extracted technique notes from **{len(books)} bug-bounty / security books**. "
           f"Source of truth: [GitHub]({GITHUB}). For AUTHORIZED testing + responsible disclosure.", "",
           "## Techniques that recur across the shelf", ""]
    idx += [f"- {wl(t)} — {n} books" for t, n in recurring]
    idx += ["", "## All technique MOCs", ""]
    idx += [f"- {wl(t)}" for t in sorted(tech_to_books)]
    idx += ["", "## Books", ""]
    for note_name, title, cs, _ in sorted(books, key=lambda b: b[1].lower()):
        idx.append(f"- [[{note_name}]] — {', '.join(cs) if cs else 'no techniques parsed'}")
    (ROOT / "Bug Bounty Books MOC.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"vault → {ROOT}")
    print(f"  {len(books)} book notes · {len(tech_to_books)} technique MOCs "
          f"({len(recurring)} recurring) · 1 index")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
