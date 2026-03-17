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

## Reference: BeeWare iOS Python toolchain (Python-Apple-support)

BeeWare’s [Python-Apple-support](https://github.com/beeware/Python-Apple-support) project builds Python for Apple platforms by producing **Xcode XCFrameworks**:

- `make iOS` downloads + patches CPython and prerequisites, then builds **multi-ABI** `Python.xcframework` slices (device + simulator) and packages them as `.tar.gz` artifacts under `dist/`.
- Each XCFramework slice is also a usable `PYTHONHOME` layout (`bin/`, `include/`, `lib/`).
- For cross-compiling third-party wheels, it provides “host Python looks like iOS” helpers:
  - `platform-config/.../sitecustomize.py` (activate via `PYTHONPATH`)
  - `make_cross_venv.py` (patch an existing venv so builds see iOS sysconfig/platform values)

Their ecosystem around this:

- [mobile-forge](https://github.com/beeware/mobile-forge) builds **binary wheels** for iOS using the Python-Apple-support runtimes.
- [mobile-wheels](https://github.com/beeware/mobile-wheels) tracks which popular packages ship Android/iOS wheels; it recommends using [`cibuildwheel`](https://cibuildwheel.pypa.io/en/stable/platforms/) for mobile wheel builds.

### What we can reuse here

Even if we keep using `kivy-ios` recipes for now, the BeeWare approach is useful as a reference for:

- **Required CPython 3.13 iOS configure flags** and constraints (e.g. framework builds).
- **Cross-build environment shims** (their `platform-config` / `make_cross_venv.py`) that may help build some packages that assume `sysconfig` matches the target.
- A “known-good” artifact format (`Python.xcframework`) for consumers that integrate via Xcode, not via `kivy-ios` dist layout.

### When switching to Python-Apple-support may be better

Consider switching this repo to *consume* BeeWare’s `Python.xcframework` artifacts (instead of building CPython via `kivy-ios`) if:

- CPython 3.13+ iOS build requirements keep diverging from `kivy-ios` expectations, or
- we want a distribution format that plugs directly into Xcode projects (XCFramework-first), or
- we want to build/publish iOS wheels using `mobile-forge`/`cibuildwheel` and only maintain **package** recipes, not the CPython toolchain itself.

