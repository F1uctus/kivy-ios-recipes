#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    pins_path = repo_root / "pins.json"
    pins = json.loads(pins_path.read_text(encoding="utf-8"))

    recipe_names: list[str] = []
    recipe_names.extend(sorted((pins.get("python", {}).get("recipes") or {}).keys()))
    recipe_names.extend(sorted((pins.get("packages") or {}).keys()))

    # Toolchain expects each custom recipe path to end with the recipe folder name.
    # We output one argument per line for safe re-use in bash.
    for name in recipe_names:
        p = repo_root / "recipes" / name
        print(f'--add-custom-recipe {p}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

