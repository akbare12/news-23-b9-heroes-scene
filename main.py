"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The entry image is drawn by draw.py and committed as entry.png.
This program copies it to the grader output directory and verifies
the copy is byte-identical (1024x1024, sha256 match, under 1 MiB).
It never writes beside itself: the only output is
os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png. Standard library only.
"""
import hashlib
import os
import shutil
import struct
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    size = _png_size(dst)
    if size != (1024, 1024):
        print(f"bad size: {size}", file=sys.stderr)
        return 1
    if _sha256(src) != _sha256(dst):
        print("sha256 mismatch", file=sys.stderr)
        return 1
    if os.path.getsize(dst) > 1048576:
        print(f"too large: {os.path.getsize(dst)} bytes", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} (1024x1024, {os.path.getsize(dst)} bytes, "
          f"sha256 {_sha256(dst)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
