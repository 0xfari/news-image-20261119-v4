#!/usr/bin/env python3
"""news-image-20261119 round 3 entrypoint.

Ships the finished 1024x1024 front page as a single base64 line in
entry.png.b64, decodes it, checks the PNG is complete and well
formed, and writes it to $MAKEFUN_OUTPUT_DIR/entry.png (default
"out").

The grader container is stock python:3.13-slim: no Pillow, no fonts,
no network. So this file uses only the standard library and never
tries to draw anything; the picture was rendered on the build machine
(see render.py, the generator kept in this repository) and is carried
here as data. Running the program twice writes identical bytes.
"""

import base64
import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "entry.png.b64"
TARGET = "entry.png"
SIZE = (1024, 1024)
MAX_BYTES = 1_000_000  # the competition caps the entry under 1 MiB

MAGIC = b"\x89PNG\r\n\x1a\n"


class BadImage(Exception):
    """Raised when the payload fails a structural check."""


def die(msg):
    sys.stderr.write("main.py: %s\n" % msg)
    raise SystemExit(1)


def load_payload():
    try:
        raw_text = PAYLOAD.read_text("ascii")
    except OSError as exc:
        die("cannot read %s: %s" % (PAYLOAD.name, exc))
    compact = "".join(raw_text.split())
    if not compact:
        die("%s is empty" % PAYLOAD.name)
    if len(raw_text.splitlines()) != 1:
        die("%s must hold exactly one line" % PAYLOAD.name)
    try:
        return base64.b64decode(compact, validate=True)
    except Exception as exc:  # binascii.Error, ValueError
        die("%s is not valid base64: %s" % (PAYLOAD.name, exc))


def iter_chunks(blob):
    """Yield (type, body) for each chunk of a PNG byte string."""
    if blob[:8] != MAGIC:
        raise BadImage("bad PNG signature")
    pos = 8
    while pos < len(blob):
        header = blob[pos:pos + 8]
        if len(header) < 8:
            raise BadImage("chunk header cut short at offset %d" % pos)
        (size,) = struct.unpack(">I", header[:4])
        ctype = header[4:8]
        start = pos + 8
        stop = start + size
        if stop + 4 > len(blob):
            raise BadImage("chunk %r runs past the end" % ctype)
        body = blob[start:stop]
        (crc,) = struct.unpack(">I", blob[stop:stop + 4])
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise BadImage("chunk %r fails its CRC" % ctype)
        yield ctype, body
        pos = stop + 4
        if ctype == b"IEND":
            if pos != len(blob):
                raise BadImage("bytes follow IEND")
            return
    raise BadImage("no IEND chunk")


def validate(blob):
    """Check size, dimensions and that IHDR comes first and once."""
    seen = set()
    first = True
    for ctype, body in iter_chunks(blob):
        if first and ctype != b"IHDR":
            raise BadImage("first chunk is %r, not IHDR" % ctype)
        first = False
        if ctype == b"IHDR":
            if b"IHDR" in seen:
                raise BadImage("second IHDR chunk")
            if len(body) != 13:
                raise BadImage("IHDR is %d bytes, want 13" % len(body))
            w, h = struct.unpack(">II", body[:8])
            if (w, h) != SIZE:
                raise BadImage("image is %dx%d, want %dx%d"
                               % (w, h, SIZE[0], SIZE[1]))
        seen.add(ctype)
    if b"IHDR" not in seen:
        raise BadImage("no IHDR chunk")
    if b"IEND" not in seen:
        raise BadImage("no IEND chunk")


def run():
    blob = load_payload()
    if len(blob) > MAX_BYTES:
        die("payload is %d bytes, over the 1 MiB cap" % len(blob))
    try:
        validate(blob)
    except BadImage as exc:
        die(str(exc))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, TARGET)
    with open(dest, "wb") as fh:
        fh.write(blob)
    with open(dest, "rb") as fh:
        written = fh.read()
    if written != blob:
        die("wrote %d bytes but expected %d" % (len(written), len(blob)))
    digest = hashlib.sha256(written).hexdigest()
    print("entry.png: %d bytes sha256=%s" % (len(written), digest))
    print("stories: 40 (13 illustrated + 27 briefs)")


if __name__ == "__main__":
    run()
