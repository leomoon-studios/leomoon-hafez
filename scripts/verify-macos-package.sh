#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 4 ]] || { echo "Usage: $0 APP_BUNDLE DMG VERSION arm64" >&2; exit 2; }
app="$1"; dmg="$2"; version="$3"; architecture="$4"
executable="$app/Contents/MacOS/LeoMoon Hafez"

[[ -d "$app" && -x "$executable" && -f "$app/Contents/Info.plist" ]] || { echo "Invalid macOS application bundle" >&2; exit 1; }
[[ -s "$dmg" && "$(basename "$dmg")" == "leomoon-hafez-$version-macos-$architecture.dmg" ]] || { echo "Unexpected DMG artifact" >&2; exit 1; }
[[ "$(plutil -extract CFBundleIdentifier raw "$app/Contents/Info.plist")" == "com.leomoon.Hafez" ]] || { echo "Unexpected bundle identifier" >&2; exit 1; }
[[ "$(plutil -extract CFBundleShortVersionString raw "$app/Contents/Info.plist")" == "$version" ]] || { echo "Unexpected bundle version" >&2; exit 1; }
[[ "$(plutil -extract LSMinimumSystemVersion raw "$app/Contents/Info.plist")" == "12.0" ]] || { echo "Unexpected minimum macOS version" >&2; exit 1; }
[[ "$(lipo -archs "$executable")" == arm64 ]] || { echo "Application is not ARM64-only" >&2; exit 1; }
find "$app/Contents" -type f -name 'libQt6Multimedia*.dylib' | grep -q . || { echo "Bundled Qt multimedia library is missing" >&2; exit 1; }
find "$app/Contents" -type f -name 'libQt6PrintSupport*.dylib' | grep -q . || { echo "Bundled Qt printing library is missing" >&2; exit 1; }
hdiutil imageinfo "$dmg" >/dev/null
if [[ -n "${HAFEZ_MACOS_CODESIGN_IDENTITY:-}" ]]; then codesign --verify --deep --strict --verbose=2 "$app"; fi
if [[ -n "${HAFEZ_MACOS_NOTARY_PROFILE:-}" ]]; then xcrun stapler validate "$dmg"; fi
