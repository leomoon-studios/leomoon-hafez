#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 4 ]] || { echo "Usage: $0 LINUX_DIRECTORY WINDOWS_DIRECTORY MACOS_DIRECTORY OUTPUT_DIRECTORY" >&2; exit 2; }
linux_dir="$(realpath "$1")"; windows_dir="$(realpath "$2")"; macos_dir="$(realpath "$3")"; output_dir="$4"
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tag="${GITHUB_REF_NAME:-}"
[[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "GITHUB_REF_NAME must be a vMAJOR.MINOR.PATCH release tag" >&2; exit 2; }
version="${tag#v}"
case "$output_dir" in ""|/|"$linux_dir"|"$windows_dir"|"$macos_dir"|"$repo_dir") echo "Refusing to replace unsafe release directory: $output_dir" >&2; exit 1 ;; esac
expected_assets=(
    "leomoon-hafez-$version-linux-x86_64.AppImage"
    "leomoon-hafez-$version-linux-aarch64.AppImage"
    "leomoon-hafez-$version-windows-x64-setup.exe"
    "leomoon-hafez-$version-windows-arm64-setup.exe"
    "leomoon-hafez-$version-macos-arm64.dmg"
)
artifacts=()
for asset_name in "${expected_assets[@]}"; do
    mapfile -t matches < <(find "$linux_dir" "$windows_dir" "$macos_dir" -type f -name "$asset_name" -print)
    (( ${#matches[@]} == 1 )) || { echo "Expected exactly one release asset named $asset_name, found ${#matches[@]}" >&2; exit 1; }
    artifacts+=("${matches[0]}")
done
rm -rf "$output_dir"
mkdir -p "$output_dir"
for artifact in "${artifacts[@]}"; do cp "$artifact" "$output_dir/$(basename "$artifact")"; done
( cd "$output_dir" && sha256sum ./* > SHA256SUMS )
echo "Collected $(find "$output_dir" -maxdepth 1 -type f | wc -l) individual release assets"
