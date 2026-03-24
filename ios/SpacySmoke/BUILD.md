# SpacySmoke — minimal iOS app (embedded kivy-ios Python + spaCy)

All **build, archive, and `.ipa` export** steps require **macOS with Xcode**
(GitHub Codespaces / Linux cannot drive the iOS toolchain).

## What you get

- UIKit app with **Run smoke.py**, **Copy all**, **Share log file**
- Logs go to **Documents / `spacy_smoke_log.txt`** plus on-screen text (including full tracebacks)
- **Share** uses the standard iOS sheet (AirDrop, Mail, “Save to Files”, etc.) so you can send logs easily

## 1) Obtain a `dist/` tree (with spaCy)

Push-triggered CI artifacts are usually **CPython only** (no spaCy). For spaCy:

```bash
gh workflow run 'ios python dist build' \
  -R F1uctus/kivy-ios-recipes \
  -f platform=iphoneos-arm64 \
  -f build_spacy=true
# wait for green run, then:
./scripts/download_latest_dist.sh .artifacts/my-dist
export DIST_PATH="$(realpath .artifacts/my-dist/extracted/dist)"
```

If `./scripts/download_latest_dist.sh` warns that `site-packages/spacy` is missing, the artifact is not a spaCy build — trigger the workflow command above and download again.

## 2) Generate Xcode project (XcodeGen + link flags)

```bash
brew install xcodegen   # once
chmod +x scripts/download_latest_dist.sh scripts/ios/*.sh

./scripts/ios/bootstrap_spacy_smoke_xcode.sh "$DIST_PATH"
open ios/SpacySmoke/SpacySmoke.xcodeproj
```

In Xcode: select your **Team** for signing, pick your **iPhone/iPad** (USB or Wi‑Fi), **Run**.

### iPad / iPhone over USB (interactive debugging)

1. Unlock the device, connect USB (or USB‑C hub on iPad).
2. **Trust** this computer when prompted.
3. On device: **Settings → Privacy & Security → Developer Mode** → On (iOS 16+).
4. Xcode: **Window → Devices and Simulators** — device should appear; enable **Connect via network** for Wi‑Fi debugging after first USB pairing.

### iOS Simulator (arm64, closest hosted CPU to Apple Silicon devices)

1. Choose an **iPhone / iPad simulator** as run destination in Xcode.  
2. You must use a dist built for the **simulator** slice:

   ```bash
   gh workflow run 'ios python dist build' … -f platform=iphonesimulator-arm64 -f build_spacy=true
   ```

   Unzip that artifact and point `DIST_PATH` at it, then re-run `bootstrap_spacy_smoke_xcode.sh`.

A **device** `.ipa` (iphoneos-arm64) will **not** run on the simulator and vice versa.

## 3) Export `.ipa` (side load / dev install)

After the app runs from Xcode at least once with valid signing:

```bash
./scripts/ios/export_ipa.sh
```

Edit `ExportOptions-ios_development.plist` (`teamID`, `method`) to match your signing setup.

## 4) Linking / static library issues

`gen_ldflags_xcconfig.sh` uses `-force_load` on every `dist/lib/iphoneos/*.a` in sorted order. If you hit duplicate symbols or missing symbols:

- Prefer regenerating the Xcode project from the same machine that built `dist/` using **kivy-ios** `toolchain update` (reads `dist/state.db` and recipe metadata), **or**
- Manually trim/reorder libraries (advanced).

## 5) Why not validate spaCy on macOS hostpython?

iOS-target extension modules (`.so`) are built for **iOS**, not macOS. Running `python` on the Mac with `PYTHONPATH` pointed at the iOS tree will fail on native imports (e.g. `srsly.ujson`). This app runs **embedded Python on the device/simulator** instead.
