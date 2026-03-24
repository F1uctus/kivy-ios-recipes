"""
spaCy smoke test for embedded iOS Python (kivy-ios dist).
Writes a full trace log for copy/share from the app UI.
"""

from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path


def log_path() -> Path:
    base = os.environ.get("IOS_APP_DOCUMENTS")
    if base:
        return Path(base) / "spacy_smoke_log.txt"
    return Path(os.environ.get("TMPDIR", "/tmp")) / "spacy_smoke_log.txt"


def main() -> None:
    lines: list[str] = []

    def tee(msg: str) -> None:
        text = msg.rstrip("\n")
        lines.append(text)
        print(text, flush=True)

    tee(f"=== SpacySmoke {sys.version.split()[0]} ===")
    tee(f"PYTHONHOME={os.environ.get('PYTHONHOME')}")
    tee(f"PYTHONPATH={os.environ.get('PYTHONPATH')}")
    tee(f"CWD={os.getcwd()}")

    try:
        import spacy  # noqa: F401

        tee(f"import spacy -> {spacy.__version__}")
        import thinc

        tee(f"import thinc -> {thinc.__version__}")

        nlp = spacy.blank("en")
        doc = nlp("Hello from iOS smoke. Numbers: 42.")
        toks = [t.text for t in doc]
        tee(f"tokens: {toks}")
        tee(f"assert tokenization: {toks[:2] == ['Hello', 'from']}")
        n = doc[4]
        tee(f"token[4] shape via lex: text={n.text!r} is_alpha={n.is_alpha}")

        tee("=== OK: spaCy smoke finished ===")
    except BaseException:
        tee("=== EXCEPTION ===")
        tee(traceback.format_exc())
    finally:
        out = log_path()
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            body = "\n".join(lines) + "\n"
            out.write_text(body, encoding="utf-8")
            tee(f"=== Log file: {out} ===")
        except OSError as e:
            tee(f"!!! could not write log file: {e}")


if __name__ == "__main__":
    main()
