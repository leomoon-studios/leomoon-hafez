#!/usr/bin/env python3
"""Validate a PyInstaller bundle manifest produced by scripts/build.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EXPECTED_ASSET_DETAILS = {
    "poem_count": 576,
    "audio_count": 495,
    "audio_format": "RIFF/WAVE container with MPEG Layer 3 audio",
    "artifact_format": "pyinstaller-onedir",
    "application": "LeoMoon Hafez",
    "application_directory": "leomoon-hafez",
}
ARCHITECTURES = {
    "x64": {"x86_64", "amd64"},
    "arm64": {"arm64", "aarch64"},
    "aarch64": {"aarch64", "arm64"},
}


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("version")
    parser.add_argument("architecture", choices=ARCHITECTURES)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: cannot read manifest: {error}", file=sys.stderr)
        return 2

    expected = {**EXPECTED_ASSET_DETAILS, "version": args.version}
    errors = [
        f"{key} is {manifest.get(key)!r}, expected {value!r}"
        for key, value in expected.items()
        if manifest.get(key) != value
    ]
    reported_architecture = str(manifest.get("architecture", "")).lower()
    if reported_architecture not in ARCHITECTURES[args.architecture]:
        errors.append(
            f"architecture is {reported_architecture!r}, expected one of {sorted(ARCHITECTURES[args.architecture])!r}"
        )
    if not isinstance(manifest.get("canonical_asset_size"), int) or manifest["canonical_asset_size"] <= 0:
        errors.append("canonical_asset_size must be a positive integer")
    if errors:
        print("error: invalid bundle manifest:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 2
    print(args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
