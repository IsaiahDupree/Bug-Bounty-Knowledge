"""
analyze_book.py — extract bug-bounty / web-security TECHNIQUES & vulnerability classes from a book
using a cheap LLM, map-reduce over excerpts → a structured Markdown technique reference.

Defensive/educational framing: we capture vulnerability CLASSES, how to FIND/TEST them, minimal-impact
proof-of-concept approach, IMPACT (CWE/severity), and REMEDIATION — for authorized testing and
responsible disclosure. No target-specific exploits, no weaponized payloads.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract import book_text
import keyloader

PROVIDER = os.environ.get("PROVIDER", "openai").lower()
MODEL = os.environ.get("BOOK_MODEL",
                       "claude-haiku-4-5-20251001" if PROVIDER == "anthropic" else "gpt-4o-mini")

MAX_CHUNKS = int(os.environ.get("MAX_CHUNKS", "40"))
CHUNK = 12000


def _make_client():
    if PROVIDER == "anthropic":
        import anthropic
        return anthropic.Anthropic(api_key=keyloader.anthropic_key())
    import openai
    return openai.OpenAI(api_key=keyloader.openai_key())


MAP_PROMPT = (
    "You are mining a bug-bounty / web-security book for ACTIONABLE, TRANSFERABLE knowledge for an "
    "AUTHORIZED hunter who follows responsible disclosure. From the excerpt below extract only concrete "
    "content as terse bullets:\n"
    "• vulnerability classes / techniques (name + one-line idea + CWE if implied)\n"
    "• where it lives (attack surface / affected component)\n"
    "• how to FIND/TEST it (recon signals, indicators, what to look for)\n"
    "• proof-of-impact approach at a HIGH LEVEL (how you'd demonstrate it minimally — NOT a weaponized "
    "or target-specific payload)\n"
    "• impact / severity and remediation\n• tools, methodology, recon/automation tips\n"
    "Ignore prose, marketing, filler. Do NOT output working exploit code or live payloads against real "
    "targets. If the excerpt has no extractable security content, reply with exactly: NONE"
)

REDUCE_PROMPT = (
    "You are compiling a TECHNIQUE REFERENCE from extraction notes across the security book \"{title}\". "
    "Synthesise (dedupe, organise) into clean Markdown with these sections:\n\n"
    "## Overview  (2-3 sentences: scope and angle of the book)\n"
    "## Techniques & Vulnerability Classes  (one '### Name' subsection per concrete technique: "
    "**idea**; where it applies / attack surface; how to find & test; proof-of-impact approach "
    "(minimal, responsible — no weaponized payloads); impact & CWE; remediation)\n"
    "## Recon & Methodology  (workflow, enumeration, automation tips)\n"
    "## Tooling  (tools named, what each is for)\n"
    "## Reporting & Disclosure  (how the book frames writing the report / scope / ethics)\n"
    "## Transferable takeaways  (what's worth adding to our own hunting checklist; be honest about "
    "what is generic or dated)\n\n"
    "Be specific and concise. Do NOT reproduce long passages (original study notes, not the book's text). "
    "Do NOT include working exploits or live payloads. If notes are thin, say so rather than padding.\n\n"
    "NOTES:\n{notes}"
)


def _chunks(text: str):
    cks = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)]
    return (cks[:MAX_CHUNKS], len(cks) > MAX_CHUNKS)


def _call(client, prompt: str, max_tokens: int, retries: int = 4) -> str:
    for a in range(retries):
        try:
            if PROVIDER == "anthropic":
                m = client.messages.create(model=MODEL, max_tokens=max_tokens,
                                           messages=[{"role": "user", "content": prompt}])
                return m.content[0].text.strip()
            r = client.chat.completions.create(model=MODEL, max_tokens=max_tokens,
                                               messages=[{"role": "user", "content": prompt}])
            return (r.choices[0].message.content or "").strip()
        except Exception as e:
            if a == retries - 1:
                raise
            time.sleep(2 ** a)
    return ""


def clean_title(name: str) -> str:
    s = Path(name).stem
    parts = [p for p in s.split(" - ") if "libgen" not in p.lower()] or [s]
    cand = parts[1] if len(parts) >= 2 else parts[0]
    cand = re.split(r"[({\[]", cand)[0].replace("_", " ").strip(" -_")
    return re.sub(r"\s+", " ", cand) or s


def slugify(name: str) -> str:
    t = re.sub(r"[^A-Za-z0-9 ]", " ", clean_title(name))
    slug = re.sub(r"\s+", "-", t.strip()).lower()[:50].strip("-") or "book"
    return f"{slug}-{hashlib.md5(name.encode()).hexdigest()[:4]}"


def analyze(path: str, out_dir: str) -> str:
    client = _make_client()
    text = book_text(path)
    if not text or len(text) < 2000:
        raise RuntimeError(f"no usable text extracted ({0 if not text else len(text)} chars)")
    cks, truncated = _chunks(text)
    notes = []
    for idx, c in enumerate(cks):
        t = _call(client, MAP_PROMPT + "\n\nEXCERPT:\n" + c, 900)
        if t and t.upper() != "NONE":
            notes.append(t)
        print(f"    chunk {idx+1}/{len(cks)} {'·' if t.upper()=='NONE' else '+'}", end="\r", flush=True)
    combined = "\n".join(notes)[:140000]
    md_body = _call(client, REDUCE_PROMPT.format(title=clean_title(Path(path).name), notes=combined), 3500)

    slug = slugify(Path(path).name)
    src = Path(path).name
    header = (
        f"# {clean_title(src)}\n\n"
        f"> **AI-generated research summary** (model: `{MODEL}`, map-reduce over {len(cks)} excerpts"
        f"{', TRUNCATED at MAX_CHUNKS' if truncated else ''}). Original study notes — vulnerability "
        f"classes, techniques, and methodology extracted for AUTHORIZED testing + responsible "
        f"disclosure, **not** the book's verbatim text and **not** weaponized exploits.\n"
        f">\n> **Source book:** {src}\n\n---\n\n"
    )
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out = Path(out_dir) / f"{slug}.md"
    out.write_text(header + md_body + "\n")
    return str(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: analyze_book.py <book path> [out_dir]"); sys.exit(1)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).resolve().parents[1] / "books")
    print(f"\nwrote {analyze(sys.argv[1], out_dir)}")
