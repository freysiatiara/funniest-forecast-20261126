import os
import sys

LINE = "Wobbleford expects light drizzle from 9 to 5; after hours, the rain clocks out and the pavements stay dry."


def resolve_output_path():
    if os.environ.get("ENTRY_OUTPUT"):
        return os.environ["ENTRY_OUTPUT"]
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def main():
    line = LINE
    if not (1 <= len(line) <= 120):
        sys.exit("gate failed: length %d outside 1-120" % len(line))
    if not line.strip():
        sys.exit("gate failed: blank line")
    if "\n" in line or "\r" in line:
        sys.exit("gate failed: not a single line")
    if any(ord(c) < 32 for c in line):
        sys.exit("gate failed: control character present")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
