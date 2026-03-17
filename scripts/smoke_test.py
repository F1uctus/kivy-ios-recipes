#!/usr/bin/env python3

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        import numpy  # noqa: F401
        import pydantic_core  # noqa: F401
        import thinc  # noqa: F401
        import spacy  # noqa: F401
    except ModuleNotFoundError as e:
        # On CI we can only execute the hostpython; iOS-built extension modules
        # cannot be imported on the macOS host interpreter.
        print(f"smoke_test: skipping package imports: {e}", file=sys.stderr)
        return 0

    payload = {
        "numpy": getattr(numpy, "__version__", None),
        "pydantic_core": getattr(pydantic_core, "__version__", None),
        "thinc": getattr(thinc, "__version__", None),
        "spacy": getattr(spacy, "__version__", None),
    }
    print(json.dumps(payload, ensure_ascii=False))

    nlp = spacy.blank("en")
    doc = nlp("hello world")
    assert [t.text for t in doc] == ["hello", "world"]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

