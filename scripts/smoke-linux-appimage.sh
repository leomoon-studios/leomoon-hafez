#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
    echo "Usage: $0 APPIMAGE" >&2
    exit 2
fi

appimage="$(realpath "$1")"
[[ -x "$appimage" ]] || { echo "AppImage is not executable: $appimage" >&2; exit 1; }
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
set +e
timeout 10s xvfb-run -a env -i HOME="$work_dir/home" PATH=/usr/bin:/bin TMPDIR="$work_dir" APPIMAGE_EXTRACT_AND_RUN=1 QT_QPA_PLATFORM=xcb QT_QPA_PLATFORMTHEME='' QT_STYLE_OVERRIDE=Fusion QT_MULTIMEDIA_PREFERRED_PLUGINS=ffmpeg "$appimage" >"$work_dir/output.log" 2>&1
status=$?
set -e
[[ "$status" -eq 124 ]] || { cat "$work_dir/output.log" >&2; echo "AppImage exited before the smoke-test timeout" >&2; exit 1; }
echo "Linux AppImage startup smoke test passed"
