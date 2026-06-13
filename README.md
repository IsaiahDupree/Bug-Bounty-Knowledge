# Bug Bounty Knowledge

AI-extracted **technique references** from a shelf of bug-bounty / web-security books — a structured,
searchable knowledge base of vulnerability classes, how to find and test them, minimal proof-of-impact
approaches, severity, and remediation. Companion to the trading [`Trading-Knowledge`] repo; same
pipeline, security corpus.

> **Authorized testing + responsible disclosure only.** These notes are for hunting on programs you are
> authorized to test, within scope and rules of engagement, with minimal-impact PoCs reported through
> the program channel. No target-specific exploits, no weaponized payloads, no mass-exploitation tooling.

## What's here
- `books/` — one Markdown technique reference per source security book: overview, named
  vulnerability classes (idea / attack surface / how to find & test / proof-of-impact / impact & CWE /
  remediation), recon methodology, tooling, and reporting/disclosure notes.
- `techniques/` — one doc **per vulnerability class** (not per book): aggregates how every book covers
  it, and links to the `bbkit` helper + tests where one exists. See `techniques/README.md`.
- `bbkit/` — the **defensive security toolkit as code**: CVSS v3.1 scoring, JWT structural analysis,
  severity/CWE mapping, encoding helpers for in-scope PoC, and a disclosure-report generator. Pure,
  dependency-free, fully tested.
- `tests/` — hand-computed unit tests for `bbkit` (CVSS conformance against FIRST.org vectors) and the
  book classifier.
- `tools/` — extraction + summarization pipeline, the shared book **classifier**, and the doc/MOC builders.

## The toolkit (bbkit)
```bash
pip install pytest          # only test-time dep; bbkit itself is stdlib-only
pytest tests/ -q
```
```python
from bbkit import cvss, jwt_tool, severity, report
cvss.score_vector("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N")   # -> 6.1 (reflected XSS)
severity.rating(6.1)                                                # -> "Medium"
jwt_tool.analyze(token)                                             # structural JWT findings (no cracking)
print(report.render(finding))                                      # a clean disclosure report
```

## Book discernment (shared with Trading-Knowledge)
`tools/classify.py` decides which knowledge base each `~/Downloads` book belongs to — finance/trading/
crypto vs bug-bounty/security — by weighted keyword scoring, so each repo's `run_all.py` processes
**only its own corpus**. Identical classifier lives in both repos.
```bash
python3 tools/classify.py        # list every Downloads book with its category
python3 tools/run_all.py         # analyze the bug-bounty books only (skips trading)
python3 tools/build_index.py && python3 tools/build_technique_docs.py && python3 tools/build_obsidian.py
```

## Honest disclaimers
- These are **original study notes synthesised by an LLM** — vulnerability *concepts*, methodology, and
  remediation extracted for research. They are **not** the books' verbatim text and **not** working
  exploits (no long passages, no weaponized payloads; fair-use summary with source attribution).
- An LLM summary can miss nuance or be dated. **Verify against the source and against current behavior**
  before relying on any technique, and only test systems you are authorized to test.
- **Source books are NOT included** in this repo (copyright; they stay local).
