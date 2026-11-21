#!/usr/bin/env python3
"""ORVENNA - The Sundial's Shadow.

Entrypoint for the-poster-for-a-place-that-i-2-20261121-0539.
Copies the pinned entry image (entry.png, shipped in this repository)
to the grader output directory. Standard library only, no network,
fully deterministic: the same bytes are written on every run.

The image is verified before it is placed: PNG magic, pinned byte
size, pinned sha256, and 1024x1024 dimensions read from the IHDR
chunk. After placement the output file is re-measured (size + sha256)
and must match the pinned values exactly.

The poster artwork is a bright painterly travel-poster painting
(sunny Mediterranean plaza, one golden sundial landmark, the place
name set huge across the sunlit pavement). It is checked by eye at
full size, then pinned here so the graded runs reproduce it byte
for byte.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

# Pinned by the build that produced entry.png (see VERIFICATION.md).
PINNED_SIZE = 423801
PINNED_SHA256 = (
    "8b96a30a8501e79f71db9e8232a4bfb8b7fa12338e37d461406a0bcbc2ca9fcd"
)
PINNED_WIDTH = 1024
PINNED_HEIGHT = 1024


def png_dimensions(path):
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png: not a PNG file")
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png: missing IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    size = os.path.getsize(SOURCE)
    if size != PINNED_SIZE:
        raise SystemExit(
            "entry.png size %d != pinned %d" % (size, PINNED_SIZE))
    digest = sha256_file(SOURCE)
    if digest != PINNED_SHA256:
        raise SystemExit("entry.png sha256 mismatch")
    width, height = png_dimensions(SOURCE)
    if (width, height) != (PINNED_WIDTH, PINNED_HEIGHT):
        raise SystemExit(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, PINNED_WIDTH, PINNED_HEIGHT))
    if size > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB cap")

    outdir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, "entry.png")
    shutil.copyfile(SOURCE, dest)

    if os.path.getsize(dest) != PINNED_SIZE:
        raise SystemExit("output size mismatch after copy")
    if sha256_file(dest) != PINNED_SHA256:
        raise SystemExit("output sha256 mismatch after copy")
    print("wrote %s (%d bytes, sha256 %s)" % (dest, PINNED_SIZE,
                                              PINNED_SHA256[:16]))


if __name__ == "__main__":
    main()
