# F1uctus's recipes for kivy-ios

This folder is intended to be deployed as the repository `F1uctus/kivy-ios-recipes`.

## Goals

- Build an embeddable Python distribution for iOS (device + simulator) that includes **spaCy 3.8.11**.
- Keep the **authoritative pins** in sync with the Android recipe set (`p4a-recipes`) used in this workspace.
- Publish CI artifacts as GitHub Releases (similar to how `p4a-recipes` publishes `p4a-dist.zip`).

## Pins

The authoritative pins for this workspace are captured in:

- `../ios-python-pins.json` (generated from `p4a-recipes`)

This repo keeps a copy at:

- `./pins.json`

CI validates these stay in sync.

## Local development (macOS)

Prerequisites (kivy-ios expectations):

- Xcode + Command Line Tools
- Homebrew packages: `autoconf`, `automake`, `libtool`, `pkg-config`, `ccache`

Install toolchain:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install kivy-ios
```

List recipes:

```bash
toolchain recipes
```

Build with custom recipes (example):

```bash
toolchain build python3 --add-custom-recipe "$(pwd)/recipes/python3"
```

