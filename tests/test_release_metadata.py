from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "prepare_release_metadata.py"


def test_release_metadata_renders_all_expected_artifact_names(tmp_path: Path) -> None:
    output = tmp_path / "metadata.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--tag",
            "v2.1.0",
            "--release-date",
            "2026-10-25T12:00:00-07:00",
            "--commit-sha",
            "a" * 40,
            "--allow-unverified-tag",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout == ""
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "commit_sha": "a" * 40,
        "linux_aarch64_appimage_filename": "leomoon-hafez-2.1.0-linux-aarch64.AppImage",
        "linux_x86_64_appimage_filename": "leomoon-hafez-2.1.0-linux-x86_64.AppImage",
        "macos_arm64_dmg_filename": "leomoon-hafez-2.1.0-macos-arm64.dmg",
        "release_date": "2026-10-25T19:00:00Z",
        "release_manifest_filename": "leomoon-hafez-2.1.0-manifest.json",
        "tag": "v2.1.0",
        "version": "2.1.0",
        "windows_arm64_setup_filename": "leomoon-hafez-2.1.0-windows-arm64-setup.exe",
        "windows_file_version": "2.1.0.0",
        "windows_x64_setup_filename": "leomoon-hafez-2.1.0-windows-x64-setup.exe",
    }


def test_release_metadata_rejects_malformed_tags() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--tag",
            "2.1.0",
            "--release-date",
            "2026-10-25T00:00:00Z",
            "--commit-sha",
            "a" * 40,
            "--allow-unverified-tag",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "Release tags must match" in completed.stderr
