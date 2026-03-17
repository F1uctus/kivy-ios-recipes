#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    default_upstream = repo_root / "ios-python-pins.json"

    upstream_path = Path(argv[1]).resolve() if len(argv) > 1 else default_upstream
    local_path = repo_root / "pins.json"

    if not upstream_path.exists():
        raise FileNotFoundError(
            f"Upstream pins not found at {upstream_path}. "
            "Pass explicit path: python scripts/pins_check.py /path/to/ios-python-pins.json"
        )

    upstream = _read_json(upstream_path)
    local = _read_json(local_path)

    if upstream == local:
        print("OK: pins.json matches upstream pins.")
        return 0

    # Produce a minimal, stable diff summary without extra deps.
    def get_versions(doc: dict) -> dict[str, str]:
        out: dict[str, str] = {}
        py = doc.get("python", {}).get("recipes", {})
        for name, meta in py.items():
            out[f"python:{name}"] = str(meta.get("version"))
        pkgs = doc.get("packages", {})
        for name, meta in pkgs.items():
            out[f"pkg:{name}"] = str(meta.get("version"))
        return out

    up_v = get_versions(upstream)
    lo_v = get_versions(local)

    keys = sorted(set(up_v) | set(lo_v))
    changed = [k for k in keys if up_v.get(k) != lo_v.get(k)]

    print("ERROR: pins.json differs from upstream pins.")
    if changed:
        print("Version mismatches:")
        for k in changed:
            print(f"- {k}: local={lo_v.get(k)!r} upstream={up_v.get(k)!r}")
    else:
        print("No version-key differences detected; structure/content differs elsewhere.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

