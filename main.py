#!/usr/bin/env python3
"""Write one sentence of everyday wonder to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only, no network. The sentence is validated (blank / multi-line /
over 200 chars) before anything is written, then read back to verify.
"""

import os
import sys

MAX_CHARS = 200

ENTRY = (
    "The bus window fogs with my breath, and for one stop the whole city "
    "outside becomes a drawing I can erase with a fingertip."
)


def main() -> int:
    text = ENTRY.strip()
    if not text:
        print("error: entry is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    # One sentence only: no sentence-ending punctuation before the final char.
    if any(ch in text[:-1] for ch in ".!?"):
        print("error: entry must be a single sentence", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: entry is {len(text)} chars, over the {MAX_CHARS}-char limit",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = text + "\n"
    if len(payload) > MAX_CHARS + 1:
        print("error: entry file would exceed the 200-char gate",
              file=sys.stderr)
        return 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(payload)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != payload:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
