#!/usr/bin/env python3
"""Write the finished front-page image to /output/entry.png.

The image is rendered by gen.py (same repository) and shipped as
entry.png; this program only copies it to the output directory, so it
runs with no network and always writes the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
