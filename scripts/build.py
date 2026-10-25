#!/usr/bin/env python3
"""Build a versioned, one-directory LeoMoon Hafez application with PyInstaller."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


VERSION_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = PROJECT_ROOT / "build"
SPECIFICATION = PROJECT_ROOT / "packaging" / "pyinstaller" / "hafez.spec"
MACOS_INFO_TEMPLATE = PROJECT_ROOT / "packaging" / "macos" / "Info.plist.in"
ASSETS_DIRECTORY = PROJECT_ROOT / "src" / "leomoon_hafez" / "assets"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-date", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output-dir", type=Path, default=BUILD_ROOT / "pyinstaller")
    parser.add_argument("--clean", action="store_true")
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Path:
    if VERSION_PATTERN.fullmatch(args.version) is None:
        raise ValueError("--version must use MAJOR.MINOR.PATCH form.")
    if datetime.fromisoformat(args.release_date.replace("Z", "+00:00")).tzinfo is None:
        raise ValueError("--release-date must include a UTC or numeric offset.")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", args.commit):
        raise ValueError("--commit must be a hexadecimal Git commit SHA.")
    output_directory = args.output_dir.resolve()
    build_root = BUILD_ROOT.resolve()
    if output_directory == build_root or build_root not in output_directory.parents:
        raise ValueError("--output-dir must be a dedicated directory below build/.")
    return output_directory


def asset_inventory() -> dict[str, object]:
    poem_archive = ASSETS_DIRECTORY / "data" / "hafez-poems.zip"
    audio_files = tuple((ASSETS_DIRECTORY / "audio").glob("*.wav"))
    with ZipFile(poem_archive) as archive:
        poem_count = len(archive.infolist())
    return {
        "poem_count": poem_count,
        "audio_count": len(audio_files),
        "canonical_asset_size": poem_archive.stat().st_size + sum(item.stat().st_size for item in audio_files),
        "audio_format": "RIFF/WAVE container with MPEG Layer 3 audio",
    }


def installed_versions() -> tuple[str, str, str]:
    from PyInstaller import __version__ as pyinstaller_version
    from PySide6 import QtCore, __version__ as pyside6_version

    return pyside6_version, QtCore.qVersion(), pyinstaller_version


def build(args: argparse.Namespace, output_directory: Path) -> Path:
    if output_directory.exists():
        if not args.clean:
            raise FileExistsError(f"{output_directory} exists. Pass --clean to replace it.")
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True)
    work_directory = output_directory / ".work"
    work_directory.mkdir()
    runtime_hook = work_directory / "set_build_version.py"
    runtime_hook.write_text(
        "import os\n" f"os.environ.setdefault('LEOMOON_HAFEZ_VERSION', {args.version!r})\n",
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment["LEOMOON_HAFEZ_VERSION"] = args.version
    environment["LEOMOON_HAFEZ_RUNTIME_HOOK"] = str(runtime_hook)
    if sys.platform == "darwin":
        info_plist = work_directory / "Info.plist"
        info_plist.write_text(
            MACOS_INFO_TEMPLATE.read_text(encoding="utf-8").replace("@VERSION@", args.version),
            encoding="utf-8",
        )
        environment["LEOMOON_HAFEZ_MACOS_INFO_PLIST"] = str(info_plist)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--distpath",
            str(output_directory),
            "--workpath",
            str(work_directory / "pyinstaller"),
            str(SPECIFICATION),
        ],
        check=True,
        cwd=PROJECT_ROOT,
        env=environment,
    )
    application_directory = output_directory / "leomoon-hafez"
    if sys.platform == "darwin":
        bundle = output_directory / "LeoMoon Hafez.app"
        executable = bundle / "Contents" / "MacOS" / "LeoMoon Hafez"
    else:
        executable_name = "LeoMoon Hafez.exe" if sys.platform == "win32" else "LeoMoon Hafez"
        executable = application_directory / executable_name
    if not executable.is_file():
        raise FileNotFoundError("PyInstaller did not produce the expected application executable.")
    if sys.platform == "darwin":
        shutil.move(str(bundle), application_directory)
    return application_directory


def write_manifest(args: argparse.Namespace, output_directory: Path, application_directory: Path) -> Path:
    pyside6_version, qt_version, pyinstaller_version = installed_versions()
    manifest = {
        "application": "LeoMoon Hafez",
        "version": args.version,
        "release_date": args.release_date,
        "commit": args.commit,
        "platform": sys.platform,
        "architecture": platform.machine(),
        "artifact_format": "pyinstaller-onedir",
        "application_directory": application_directory.name,
        "python_version": platform.python_version(),
        "pyside6_version": pyside6_version,
        "qt_version": qt_version,
        "pyinstaller_version": pyinstaller_version,
        **asset_inventory(),
    }
    manifest_path = output_directory / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def main() -> int:
    try:
        args = arguments()
        output_directory = validate_arguments(args)
        application_directory = build(args, output_directory)
        manifest_path = write_manifest(args, output_directory, application_directory)
    except (FileExistsError, FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
