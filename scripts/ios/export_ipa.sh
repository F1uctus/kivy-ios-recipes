#!/usr/bin/env bash
# Archive and export a signed .ipa for device installation (macOS + Xcode).
#
# Prerequisites:
# - Development team set on the SpacySmoke target (Signing & Capabilities)
# - Edit ios/SpacySmoke/ExportOptions-ios_development.plist teamID if not using automatic
#
# Usage:
#   ./scripts/ios/export_ipa.sh [path/to/SpacySmoke.xcodeproj]

set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PROJ="${1:-$REPO/ios/SpacySmoke/SpacySmoke.xcodeproj}"
SCHEME="SpacySmoke"
ARCHIVE="$REPO/ios/SpacySmoke/build/${SCHEME}.xcarchive"
EXPORT="$REPO/ios/SpacySmoke/build/ipa"
PLIST="$REPO/ios/SpacySmoke/ExportOptions-ios_development.plist"

mkdir -p "$(dirname "$ARCHIVE")" "$EXPORT"

xcodebuild \
  -project "$PROJ" \
  -scheme "$SCHEME" \
  -configuration Release \
  -destination "generic/platform=iOS" \
  -archivePath "$ARCHIVE" \
  archive

xcodebuild \
  -exportArchive \
  -archivePath "$ARCHIVE" \
  -exportPath "$EXPORT" \
  -exportOptionsPlist "$PLIST"

echo "IPA(s) under: $EXPORT"
