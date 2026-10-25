from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from random import Random
from types import SimpleNamespace
from zipfile import ZipFile

import pytest

import hafez_corpus
from hafez_corpus import CATEGORY_COUNTS, CorpusError, PoemArchive


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_POEMS = PROJECT_ROOT / "tests" / "fixtures" / "poems"
CANONICAL_CORPUS_DIGEST = "c8fd2f29f1bb190029147699585dfb99220fc541fddeb7f1762c3a52111e882f"


def build_fixture_archive(path: Path) -> PoemArchive:
    with ZipFile(path, "w") as archive:
        for poem in sorted(FIXTURE_POEMS.iterdir()):
            archive.write(poem, poem.name)
    return PoemArchive(path)


def test_unencrypted_archive_has_expected_category_counts() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db")

    assert not archive.is_encrypted()
    assert {category: len(archive.names(category)) for category in CATEGORY_COUNTS} == CATEGORY_COUNTS
    assert sum(CATEGORY_COUNTS.values()) == len(archive.names()) == 576


def test_unencrypted_archive_reads_public_domain_poem_text() -> None:
    archive = PoemArchive(PROJECT_ROOT / "src" / "data.db")

    text = archive.read_text("غزل شماره 1")

    assert text
    assert "<br />" in archive.html("غزل شماره 1")


def test_archive_rejects_encrypted_replacement(tmp_path: Path, monkeypatch) -> None:
    class EncryptedArchive:
        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

        def infolist(self):
            return [SimpleNamespace(flag_bits=0x1)]

    archive_path = tmp_path / "encrypted.zip"
    archive_path.touch()
    monkeypatch.setattr(hafez_corpus, "ZipFile", lambda _: EncryptedArchive())

    with pytest.raises(CorpusError, match="must not be encrypted"):
        PoemArchive(archive_path).names()


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


def test_random_selection_stays_within_the_495_ghazals() -> None:
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


def test_standard_zip_reader_opens_every_poem_without_a_password() -> None:
    archive_path = PROJECT_ROOT / "src" / "data.db"

    with ZipFile(archive_path) as archive:
        assert len(archive.infolist()) == 576
        assert all(not info.flag_bits & 0x1 for info in archive.infolist())
        digest = sha256()
        for name in archive.namelist():
            digest.update(name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(archive.read(name))
            digest.update(b"\0")
        assert digest.hexdigest() == CANONICAL_CORPUS_DIGEST
