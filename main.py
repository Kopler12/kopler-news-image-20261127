# The World Today - Friday 27 November 2026 (Python 3.13, standard library only).
#
# Entry for make.fun news-image-20261127: "Sum up 27 November's world news
# in one image". The image itself lives in this repository as entry.png -
# a newspaper front page drawn by render.py (Python + Pillow) - and this
# program writes those exact bytes to /output/entry.png. The copy is exact:
# shutil.copyfile preserves the file's bytes, so the graded image is the
# image in this repository, nothing more and nothing less.
#
# Deterministic: no network, no clock, no randomness. Running it twice
# writes the same bytes both times.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUT_DIR / "entry.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", TARGET)
print(f"wrote {TARGET} ({TARGET.stat().st_size} bytes)")
