#!/usr/bin/env python3
"""Ensure spaCy stack packages are present in the built iOS dist site-packages.

Import-based checks (e.g. scripts/smoke_test_spacy.py) must run inside a process
that matches the kivy-ios target: native extensions are built for iOS (or
iOS Simulator) and generally cannot be loaded with macOS hostpython, even when
PYTHONPATH points at the same site-packages tree.

To exercise imports, run Python embedded in an app on the iOS Simulator or a
device (see workflow comments / future ios-simulator-smoke job).
"""

from __future__ import annotations

import sys
from pathlib import Path


def _must_exist(site: Path, name: str) -> bool:
    p = site / name
    if p.exists():
        return True
    return (site / f"{name}.py").is_file()


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    site = repo / "dist" / "root" / "python3" / "lib" / "python3.13" / "site-packages"
    if not site.is_dir():
        print(f"verify_spacy_dist_layout: missing {site}", file=sys.stderr)
        return 1

    required = (
        "blis",
        "catalogue",
        "confection",
        "cymem",
        "murmurhash",
        "preshed",
        "pydantic",
        "pydantic_core",
        "spacy",
        "srsly",
        "thinc",
        "typing_extensions",
    )
    missing = [n for n in required if not _must_exist(site, n)]
    if missing:
        print(
            "verify_spacy_dist_layout: missing packages/modules: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    ujson_dir = site / "srsly" / "ujson"
    if not ujson_dir.is_dir():
        print(f"verify_spacy_dist_layout: missing {ujson_dir}", file=sys.stderr)
        return 1
    so = list(ujson_dir.glob("ujson*.so"))
    if not so:
        print(
            "verify_spacy_dist_layout: no srsly ujson extension (*.so) under "
            f"{ujson_dir}",
            file=sys.stderr,
        )
        return 1

    pc = list((site / "pydantic_core").glob("_pydantic_core*.so"))
    if not pc:
        print(
            "verify_spacy_dist_layout: no pydantic_core native lib under "
            f"{site / 'pydantic_core'}",
            file=sys.stderr,
        )
        return 1

    print("verify_spacy_dist_layout: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
