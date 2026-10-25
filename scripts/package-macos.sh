#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
stage_dir=""; dist_dir=""; version=""; release_date=""; commit=""; architecture=""
usage() { echo "Usage: $0 --stage-dir DIR --dist-dir DIR --version VERSION --release-date DATE --commit SHA --architecture arm64" >&2; }
while (( $# )); do
    case "$1" in
        --stage-dir) stage_dir="$2"; shift 2 ;;
        --dist-dir) dist_dir="$2"; shift 2 ;;
        --version) version="$2"; shift 2 ;;
        --release-date) release_date="$2"; shift 2 ;;
        --commit) commit="$2"; shift 2 ;;
        --architecture) architecture="$2"; shift 2 ;;
        *) usage; exit 2 ;;
    esac
done
[[ -n "$stage_dir" && -n "$dist_dir" && -n "$version" && -n "$release_date" && -n "$commit" && "$architecture" == arm64 ]] || { usage; exit 2; }
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ && "$release_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T && "$commit" =~ ^[0-9a-fA-F]{7,64}$ ]] || { echo "Invalid release metadata" >&2; exit 2; }
stage_dir="$(realpath "$stage_dir")"
dist_parent="$(cd "$(dirname "$dist_dir")" && pwd -P)"; dist_dir="$dist_parent/$(basename "$dist_dir")"
app="$stage_dir/LeoMoon Hafez.app"
[[ -d "$app" && -x "$app/Contents/MacOS/LeoMoon Hafez" ]] || { echo "Stage directory must contain LeoMoon Hafez.app" >&2; exit 1; }
[[ "$dist_dir" != / && "$dist_dir" != "$repo_dir" ]] || { echo "Refusing to replace unsafe artifact directory: $dist_dir" >&2; exit 1; }

if [[ -n "${HAFEZ_MACOS_CODESIGN_IDENTITY:-}" ]]; then
    while IFS= read -r -d '' binary; do
        codesign --force --options runtime --timestamp --sign "$HAFEZ_MACOS_CODESIGN_IDENTITY" "$binary"
    done < <(find "$app/Contents" -type f -print0 | while IFS= read -r -d '' candidate; do file "$candidate" | grep -q 'Mach-O' && printf '%s\0' "$candidate"; done)
    codesign --force --options runtime --timestamp --sign "$HAFEZ_MACOS_CODESIGN_IDENTITY" "$app"
else
    echo "Producing an unsigned ARM64 macOS application bundle."
fi

package_dir="$repo_dir/build/package/macos"; dmg_root="$package_dir/dmg-root"
rm -rf "$package_dir" "$dist_dir"
mkdir -p "$dmg_root" "$dist_dir"
cp -a "$app" "$dmg_root/"
install -m 0644 "$repo_dir/packaging/windows/EULA.txt" "$dmg_root/EULA.txt"
install -m 0644 "$repo_dir/THIRD_PARTY_NOTICES.md" "$dmg_root/THIRD_PARTY_NOTICES.md"
dmg="$dist_dir/leomoon-hafez-$version-macos-arm64.dmg"
# Use the normal Finder layout and icon. No custom installer artwork is required.
hdiutil create -quiet -volname "LeoMoon Hafez" -srcfolder "$dmg_root" -ov -format UDZO "$dmg"
if [[ -n "${HAFEZ_MACOS_NOTARY_PROFILE:-}" ]]; then
    arguments=(notarytool submit "$dmg" --keychain-profile "$HAFEZ_MACOS_NOTARY_PROFILE" --wait)
    if [[ -n "${HAFEZ_MACOS_NOTARY_KEYCHAIN:-}" ]]; then arguments+=(--keychain "$HAFEZ_MACOS_NOTARY_KEYCHAIN"); fi
    xcrun "${arguments[@]}"
    xcrun stapler staple "$dmg"
fi
bash "$repo_dir/scripts/verify-macos-package.sh" "$app" "$dmg" "$version" arm64
cat > "$dist_dir/release-manifest.json" <<EOF
{
  "application": "LeoMoon Hafez",
  "version": "$version",
  "release_date": "$release_date",
  "commit": "$commit",
  "platform": "macos",
  "architectures": "arm64",
  "artifact_format": "DMG",
  "signed": $([ -n "${HAFEZ_MACOS_CODESIGN_IDENTITY:-}" ] && printf true || printf false),
  "notarized": $([ -n "${HAFEZ_MACOS_NOTARY_PROFILE:-}" ] && printf true || printf false)
}
EOF
( cd "$dist_dir" && shasum -a 256 ./* > SHA256SUMS && shasum -a 256 -c SHA256SUMS )
echo "macOS release artifacts are ready in $dist_dir"
