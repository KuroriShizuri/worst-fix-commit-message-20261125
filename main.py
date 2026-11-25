#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message - make.fun entry.

Writes exactly one commit message (at most 100 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Stdlib only, deterministic, no network.
"""
import os
import sys

ENTRY = "fix(perf): halved load times by deleting the half users actually used"
MAX_CHARS = 100


def validate(text):
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d chars, over the %d-char gate" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def validate_written(path):
    """Read entry.txt back from disk and re-validate the artifact itself."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("entry.txt is not valid UTF-8: %s" % exc)
    validate(text.rstrip("\n"))
    if text.count("\n") > 1:
        raise ValueError("entry.txt must be a single line")
    return text


def write_entry():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    data = (validate(ENTRY) + "\n").encode("utf-8")
    with open(target, "wb") as f:
        f.write(data)
    with open(target, "rb") as f:
        if f.read() != data:
            raise ValueError("entry.txt round-trip mismatch")
    validate_written(target)
    return target


def main(argv):
    if "--self-test" in argv:
        validate(ENTRY)
        print("self-test ok: %d chars" % len(ENTRY))
        return 0
    if "--check" in argv:
        validate(ENTRY)
        print("check ok: %d chars, within %d" % (len(ENTRY), MAX_CHARS))
        return 0
    try:
        write_entry()
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
