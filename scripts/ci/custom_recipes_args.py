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
    emitted: set[Path] = set()
    for name in recipe_names:
        p = repo_root / "recipes" / name
        if p.is_dir():
            print(f"--add-custom-recipe {p}")
            emitted.add(p.resolve())

    # Include any extra local recipes not listed in pins.json (for transitive
    # runtime dependencies we add in custom recipes, e.g. typing_extensions).
    for p in sorted((repo_root / "recipes").iterdir()):
        if not p.is_dir():
            continue
        resolved = p.resolve()
        if resolved in emitted:
            continue
        print(f"--add-custom-recipe {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

