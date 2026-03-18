#!/usr/bin/env python3

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        import ssl  # noqa: F401
        import sqlite3  # noqa: F401
    except ModuleNotFoundError as e:
        print(f"smoke_test: missing expected stdlib module: {e}", file=sys.stderr)
        return 1

    payload = {
        "python": sys.version.split()[0],
        "openssl": getattr(ssl, "OPENSSL_VERSION", None),
        "sqlite": getattr(sqlite3, "sqlite_version", None),
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

