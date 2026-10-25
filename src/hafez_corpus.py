"""Archive-backed access to the bundled Hafez poem corpus."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from random import Random
from zipfile import BadZipFile, ZipFile

from natsort import natsorted


LEGACY_ARCHIVE_PASSWORD = b"z!WbsdCkm#"
CATEGORY_COUNTS = {
    "غزل": 495,
    "قصیده": 3,
    "مثنوی": 2,
    "قطعه": 34,
    "رباعی": 42,
}


class CorpusError(RuntimeError):
    """Raised when the bundled poem archive cannot provide requested content."""


@dataclass(frozen=True)
class PoemArchive:
    """Read Persian poem files from the legacy password-protected ZIP archive."""

    path: Path
    password: bytes | None = LEGACY_ARCHIVE_PASSWORD

    def __init__(self, path: str | Path, password: bytes | None = LEGACY_ARCHIVE_PASSWORD) -> None:
        object.__setattr__(self, "path", Path(path))
        object.__setattr__(self, "password", password)

    @property
    def exists(self) -> bool:
        return self.path.is_file()

    def _open(self) -> ZipFile:
        if not self.exists:
            raise CorpusError(f"Poem archive is missing: {self.path}")
        try:
            return ZipFile(self.path)
        except BadZipFile as error:
            raise CorpusError(f"Poem archive is invalid: {self.path}") from error

    def names(self, category: str | None = None) -> list[str]:
        with self._open() as archive:
            names = archive.namelist()
        if category is not None:
            names = [name for name in names if name.startswith(category)]
        return list(natsorted(names))

    def is_encrypted(self) -> bool:
        with self._open() as archive:
            return any(info.flag_bits & 0x1 for info in archive.infolist())

    def read_text(self, name: str) -> str:
        with self._open() as archive:
            if name not in archive.namelist():
                raise CorpusError(f"Poem does not exist in the archive: {name}")
            try:
                content = archive.read(name, pwd=self.password)
            except (RuntimeError, BadZipFile) as error:
                raise CorpusError(f"Unable to read poem from the archive: {name}") from error
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise CorpusError(f"Poem is not UTF-8 text: {name}") from error

    def search(self, query: str) -> list[str]:
        if not query:
            return []
        return [name for name in self.names() if query in self.read_text(name)]

    def random_name(self, category: str, random_source: Random | None = None) -> str:
        names = self.names(category)
        if not names:
            raise CorpusError(f"No poems exist for category: {category}")
        return (random_source or Random()).choice(names)

    def html(self, name: str) -> str:
        return "<br />".join(escape(line) for line in self.read_text(name).splitlines())
