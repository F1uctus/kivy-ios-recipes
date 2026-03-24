#!/usr/bin/env bash
# Download the latest successful "ios python dist build" artifact and unzip it.
# Requires: gh CLI, jq, unzip.
#
# Layout after run:
#   <out>/ios-python-dist-iphoneos-arm64.zip   (raw artifact file)
#   <out>/extracted/dist/                      (kivy-ios dist tree)
#   <out>/extracted/pins.json
#
# IMPORTANT: GitHub Actions runs triggered by push set BUILD_SPACY=0, so those
# artifacts usually contain CPython only (no spaCy). For a spaCy-enabled tree,
# run manually:
#   gh workflow run 'ios python dist build' -f platform=iphoneos-arm64 -f build_spacy=true
# then re-run this script after that run succeeds.

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-F1uctus/kivy-ios-recipes}"
OUT="${1:-.artifacts/latest-dist}"
WORKFLOW="${WORKFLOW_NAME:-ios python dist build}"

mkdir -p "$OUT"

RUN_ID="$(gh run list --repo "$REPO" --workflow "$WORKFLOW" --status success --limit 1 --json databaseId --jq '.[0].databaseId')"
if [[ -z "$RUN_ID" || "$RUN_ID" == "null" ]]; then
  echo "No successful runs found for $WORKFLOW in $REPO" >&2
  exit 1
fi

echo "Downloading artifact from run $RUN_ID ($REPO)"
gh run download "$RUN_ID" --repo "$REPO" -D "$OUT" --name "ios-python-dist-iphoneos-arm64"

ZIP="$OUT/ios-python-dist-iphoneos-arm64.zip"
if [[ ! -f "$ZIP" ]]; then
  echo "Expected $ZIP missing after download" >&2
  exit 1
fi

EXT="$OUT/extracted"
rm -rf "$EXT"
mkdir -p "$EXT"
unzip -q -o "$ZIP" -d "$EXT"

DIST_DIR="$EXT/dist"
if [[ ! -d "$DIST_DIR" ]]; then
  echo "Unzip did not contain dist/ at $DIST_DIR" >&2
  exit 1
fi

SPACY_DIR="$DIST_DIR/root/python3/lib/python3.13/site-packages/spacy"
if [[ ! -d "$SPACY_DIR" ]]; then
  echo ""
  echo "WARNING: This artifact does not include spaCy (typical for push-triggered CI)."
  echo "  To build and fetch a spaCy dist, run on the repo:"
  echo "    gh workflow run 'ios python dist build' -f platform=iphoneos-arm64 -f build_spacy=true"
  echo "  Then download the artifact from that run (or rerun this script once it is green)."
  echo ""
fi

echo "OK: dist at $DIST_DIR"
echo "Set DIST_PATH for Xcode build:"
echo "  export DIST_PATH=\"$(realpath "$DIST_DIR")\""
echo "  # or copy ios/SpacySmoke/Generated/Dist.xcconfig.sample -> Generated/Dist.xcconfig and edit DIST_PATH"
