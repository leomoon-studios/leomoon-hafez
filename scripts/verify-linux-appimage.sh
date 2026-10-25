#!/usr/bin/env bash
set -euo pipefail

if (( $# != 3 )); then
    echo "Usage: $0 APPIMAGE VERSION x86_64|aarch64" >&2
    exit 2
fi

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
appimage="$(realpath "$1")"; version="$2"; architecture="$3"
[[ -x "$appimage" ]] || { echo "AppImage is not executable: $appimage" >&2; exit 1; }
[[ "$(basename "$appimage")" == "leomoon-hafez-$version-linux-$architecture.AppImage" ]] || { echo "Unexpected AppImage filename" >&2; exit 1; }
file_description="$(file -b "$appimage")"
case "$architecture" in
    x86_64) [[ "$file_description" == *"x86-64"* ]] ;;
    aarch64) [[ "$file_description" == *"aarch64"* || "$file_description" == *"ARM aarch64"* ]] ;;
esac || { echo "AppImage architecture does not match $architecture: $file_description" >&2; exit 1; }

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
(
    cd "$work_dir"
    APPIMAGE_EXTRACT_AND_RUN=1 "$appimage" --appimage-extract >/dev/null
)
root="$work_dir/squashfs-root"
desktop="$root/usr/share/applications/com.leomoon.Hafez.desktop"
[[ -x "$root/AppRun" && -x "$root/usr/bin/leomoon-hafez" && -x "$root/usr/lib/leomoon-hafez/LeoMoon Hafez" ]] || { echo "AppImage launch files are missing or not executable" >&2; exit 1; }
[[ -f "$desktop" && -f "$root/usr/share/icons/hicolor/256x256/apps/com.leomoon.Hafez.png" ]] || { echo "AppImage desktop metadata or icon is missing" >&2; exit 1; }
grep -Fx 'Exec=leomoon-hafez' "$desktop" >/dev/null
grep -Fx 'Icon=com.leomoon.Hafez' "$desktop" >/dev/null
grep -Fx 'Categories=Education;Utility;' "$desktop" >/dev/null
find "$root" -type f \( -name 'libqxcb.so' -o -name 'libqoffscreen.so' -o -name 'libffmpegmediaplugin.so' \) | grep -q . || { echo "Bundled Qt platform or multimedia plugins are missing" >&2; exit 1; }
for library in libQt6Core.so libQt6Gui.so libQt6Multimedia.so libQt6PrintSupport.so; do
    find "$root" -type f -name "$library*" | grep -q . || { echo "Bundled Qt library is missing: $library" >&2; exit 1; }
done
audio_count="$(find "$root" -type f -name '*.wav' | wc -l)"
[[ "$audio_count" -eq 495 ]] || { echo "Expected 495 bundled audio files, found $audio_count" >&2; exit 1; }
poem_archive="$(find "$root" -type f -name 'hafez-poems.zip' -print -quit)"
[[ -n "$poem_archive" && "$(unzip -Z1 "$poem_archive" | wc -l)" -eq 576 ]] || { echo "The bundled poem archive is incomplete" >&2; exit 1; }
if strings "$root/usr/lib/leomoon-hafez/LeoMoon Hafez" | grep -F "$repo_dir" >/dev/null; then
    echo "AppImage contains a repository-only path" >&2
    exit 1
fi
echo "Verified $appimage"
