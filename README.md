# LeoMoon Hafez

## Introduction

LeoMoon Hafez is a desktop reader for Hafez poetry. It provides Persian poem browsing and search, light and dark themes, Vazir and IranNastaliq display fonts, printing, and bundled audio recitations.

The application is being modernized as a cross-platform Python and Qt 6 project. It supports Windows, macOS, and Linux with a shared codebase and native release packages for each platform.

## Features

- Browse 576 Hafez poems by form.
- Search Persian poem text with Unicode support.
- Listen to 495 bundled audio recitations.
- Switch between Vazir and IranNastaliq display fonts.
- Print a poem from the application.
- Light and dark themes that follow the operating system preference.

## Usage

1. Download the package for your computer from the [GitHub releases page](https://github.com/leomoon-studios/leomoon-hafez/releases). Windows provides x64 and ARM64 installers, Linux provides x86_64 and ARM64 AppImages, and macOS provides an ARM64 DMG.
2. Open LeoMoon Hafez.
3. Select a poem category, browse the list, or use the search mode to find poem text.
4. Choose Vazir or IranNastaliq, adjust text size, print the selected poem, or play its recitation.

## Build

Requirements:

- Python 3.12 or newer
- A project-local `.venv`
- `uv` installed only inside that `.venv`

```sh
python -m venv .venv
.venv/bin/python -m pip install "uv==0.13.5"
.venv/bin/uv sync --all-extras --locked
.venv/bin/python scripts/generate_qt.py
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q
```

Run the application with `.venv/bin/python -m leomoon_hafez`. On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

## Packaging

Release packages are platform-specific: Windows uses x64 and ARM64 Inno Setup installers, Linux uses x86_64 and ARM64 AppImages, and macOS uses one native ARM64 DMG. Each package is built from the same PyInstaller one-directory application and includes release metadata and SHA-256 checksums.

The platform workflows install locked dependencies in a project-local `.venv`, regenerate Qt sources, run Ruff and pytest, build the native bundle, then package and smoke-test the final artifact. Windows and macOS support optional protected signing credentials. Linux AppImage tooling is downloaded with pinned SHA-256 checksums.

## Release builds

Use the **Manual platform builds** GitHub Actions workflow for a non-publishing platform test. The final release workflow builds Windows x64 and ARM64 installers, Linux x86_64 and ARM64 AppImages, and the macOS ARM64 DMG after tag validation.

The application executable is named `LeoMoon Hafez`. Release asset filenames use the stable `leomoon-hafez` slug. Do not commit certificates, private keys, Apple passwords, tokens, package outputs, virtual environments, or signing keychains. Protected GitHub Actions secrets hold optional signing credentials.

## Runtime assets

The release includes the 576-poem `hafez-poems.zip` corpus, 495 WAV-container recordings, Vazir and IranNastaliq fonts, and application icons under `src/leomoon_hafez/assets/`. The audio payload intentionally dominates final package size. Editable artwork remains in `gfx/` as maintenance source material and is not used directly by release builds.

Git LFS is not used because every checkout and CI build needs the complete fixed corpus and recording set. Old poem-download experiments are not retained.

## Settings and privacy

Theme and font choices are controlled locally in the application. LeoMoon Hafez does not require an account or send poem, search, or playback data to a network service.

## Remove

Use the normal uninstall method for the installed package. On Windows, use Apps and Features or the installer’s uninstaller. On macOS, remove the copied application from Applications. On Linux, remove the AppImage file.

## Third-party notices

The application includes Qt for Python, DarkDetect, natsort, Vazir, IranNastaliq, corpus material, audio recordings, and icon assets. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for notices, sources, licenses, checksums, and runtime purposes.
