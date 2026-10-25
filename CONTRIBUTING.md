# Contributing to LeoMoon Hafez

Use Python 3.12 and create dependencies only inside `.venv`: `python3.12 -m venv .venv`, `.venv/bin/python -m pip install "uv==0.13.5"`, then `.venv/bin/uv sync --all-extras --locked`.

Run `scripts/generate_qt.py` whenever Qt Designer `.ui` or `.qrc` sources change. Commit the deterministic `src/leomoon_hafez/_generated/main_window.py` output when it changes. `resources_rc.py` is generated locally and ignored.

Before opening a change, run Ruff and the headless test suite from the README. Preserve Persian Unicode. Corpus, audio, and font changes must preserve the supported formats and document source, license, checksum, and runtime purpose in `THIRD_PARTY_NOTICES.md`.

Use GitHub Actions **Manual platform builds** for native Windows x64 and ARM64 installers, Linux x86_64 and ARM64 AppImages, and the macOS ARM64 DMG. Do not add Intel macOS, universal, PKG, or legacy installer projects.

Signing and notarization use protected GitHub repository secrets. Do not commit certificates, private keys, provisioning profiles, Apple passwords, tokens, virtual environments, local signing keychains, or package outputs.
