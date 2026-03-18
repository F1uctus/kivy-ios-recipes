#!/usr/bin/env python3

from __future__ import annotations

import json

import numpy
import pydantic_core
import spacy
import thinc


def main() -> int:
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
