"""
Locate an Anthropic (or OpenAI) API key from existing local .env files — same
"live off the land" pattern as HFT/harness/openai_key.py. Returns the key
STRING for runtime use; this file contains only candidate PATHS, never a key,
so it is safe to commit. Keys are never printed or logged.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_CANDIDATES = [
    "/Users/isaiahdupree/Documents/Software/GTMEngineering/.env",
    "/Users/isaiahdupree/.openclaw/.env",
    "/Users/isaiahdupree/Documents/Software/TradingBot/.env",
    str(Path.home() / ".env"),
]


def _read_key(path: str, name: str) -> Optional[str]:
    p = Path(path)
    if not p.exists():
        return None
    for line in p.read_text(errors="ignore").splitlines():
        line = line.strip()
        if line.startswith(name + "="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    return None


def get_key(name: str = "ANTHROPIC_API_KEY") -> str:
    if os.environ.get(name):
        return os.environ[name]
    for c in _CANDIDATES:
        v = _read_key(c, name)
        if v:
            return v
    raise RuntimeError(f"no {name} found in env or {_CANDIDATES}")


def anthropic_key() -> str:
    return get_key("ANTHROPIC_API_KEY")


def openai_key() -> str:
    return get_key("OPENAI_API_KEY")
