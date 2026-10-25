from __future__ import annotations

from pathlib import Path
from random import Random
from zipfile import ZipFile

import pytest

from hafez_corpus import CATEGORY_COUNTS, CorpusError, PoemArchive


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_POEMS = PROJECT_ROOT / "tests" / "fixtures" / "poems"


def build_fixture_archive(path: Path) -> PoemArchive:
    with ZipFile(path, "w") as archive:
        for poem in sorted(FIXTURE_POEMS.iterdir()):
            archive.write(poem, poem.name)
    return PoemArchive(path, password=None)


def test_legacy_archive_has_expected_encrypted_category_counts() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db")

    assert archive.is_encrypted()
    assert {category: len(archive.names(category)) for category in CATEGORY_COUNTS} == CATEGORY_COUNTS
    assert sum(CATEGORY_COUNTS.values()) == len(archive.names()) == 576


def test_legacy_archive_reads_public_domain_poem_text() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db")

    text = archive.read_text("غزل شماره 1")

    assert text
    assert "<br />" in archive.html("غزل شماره 1")


def test_legacy_archive_rejects_an_incorrect_password() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db", password=b"incorrect")

    with pytest.raises(CorpusError, match="Unable to read"):
        archive.read_text("غزل شماره 1")


def test_fixture_archive_sorts_searches_and_escapes_html(tmp_path: Path) -> None:
    archive = build_fixture_archive(tmp_path / "poems.zip")

    assert archive.names("غزل") == ["غزل شماره 2.txt", "غزل شماره 10.txt"]
    assert {category: len(archive.names(category)) for category in CATEGORY_COUNTS} == {
        "غزل": 2,
        "قصیده": 1,
        "مثنوی": 1,
        "قطعه": 1,
        "رباعی": 1,
    }
    assert set(archive.search("آزمایشی")) == {
        "رباعی شماره 1.txt",
        "غزل شماره 2.txt",
        "غزل شماره 10.txt",
        "قصیده شماره 1.txt",
        "مثنوی شماره 1.txt",
        "قطعه شماره 1.txt",
    }
    assert archive.search("") == []
    assert archive.search("ناپیدا") == []
    assert archive.html("غزل شماره 2.txt") == "دومین شعر آزمایشی<br />بهار آمد"


def test_random_name_is_deterministic_with_supplied_random_source(tmp_path: Path) -> None:
    archive = build_fixture_archive(tmp_path / "poems.zip")

    assert archive.random_name("غزل", Random(1)) == "غزل شماره 2.txt"


def test_legacy_random_selection_stays_within_the_495_ghazals() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db")
    ghazals = archive.names("غزل")

    assert len(ghazals) == 495
    assert archive.random_name("غزل", Random(1)) in ghazals


def test_archive_reports_missing_poems_and_archives(tmp_path: Path) -> None:
    archive = build_fixture_archive(tmp_path / "poems.zip")

    with pytest.raises(CorpusError, match="does not exist"):
        archive.read_text("غزل شماره 999.txt")
    with pytest.raises(CorpusError, match="missing"):
        PoemArchive(tmp_path / "missing.zip").names()
    invalid_archive = tmp_path / "invalid.zip"
    invalid_archive.write_text("not a ZIP", encoding="utf-8")
    with pytest.raises(CorpusError, match="invalid"):
        PoemArchive(invalid_archive).names()
