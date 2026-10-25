# Changelog

## 2.0.0 (2026-10-25)

- Native release packages for Windows x64 and ARM64, Linux x86_64 and ARM64 AppImages, and a macOS ARM64 DMG.
- GitHub Actions platform builds, package smoke tests, checksums, and release metadata.
- Regression tests for the poem corpus, audio library, Qt UI, and release metadata.
- The unencrypted 576-poem archive and 495 bundled audio recordings in the standard package layout.
- Updated IranNastaliq font files and license material.
- Repository documentation for development, packaging, asset maintenance, contribution, and third-party notices.
- Migrated the application from PyQt5 to PySide6 and Qt 6.
- Moved the application to a standard `src/` package layout with generated Qt sources and modern project metadata.
- Locked maintained Python dependencies in `uv.lock` and updated DarkDetect, PyInstaller, and development tooling.
- Replaced legacy build scripts, compatibility DLLs, and installer callbacks with deterministic PyInstaller packaging and native platform installers.
- Updated supported systems to current Windows, Linux, and macOS releases.

## 1.1.5 (2021-10-05)

- Added cross-platform auto dark mode.
- Added "تغییر پوسته" button with Ctrl + M hotkey.
- Fixed multiple issues with audio playback.
- Updated all dependencies.

## 1.1.4 (2020-12-19)

- Fixed compatibility issue with macOS Big Sur.
- Minimum supported macOS changed to 10.14 Mojave.
- Fixed uninstall icon for Windows setup.
- Updated all dependencies.

## 1.1.3 (2020-05-20)

- Fixed crash on Windows 10 update 1909.
- Updated all dependencies.

## 1.1.2

- Updated core to the latest version.
- Updated all dependencies.
- Embedded main font into the application.
- Main logo is now in SVG.
- Fixed DPI scaling not working sometimes.
- Minimum supported macOS changed to 10.13.

## 1.1.1

- Minor improvements.
- Added “فال حافظ” button with Ctrl + R hotkey.
- Windows binary is now digitally signed.

## 1.1.0

- Added search.
- Added print.
- Added Ctrl + F hotkey to search.
- Added Ctrl + P hotkey to print.
- Added Ctrl + 0 hotkey to reset zoom to default.
- Added Spacebar hotkey to play.

## 1.0.1

- Fixed one typo.

## 1.0.0

- Initial release.
