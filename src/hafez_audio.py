"""Audio discovery and playback state for Hafez poems."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PlaybackState:
    """Track player state independently from the Qt multimedia object."""

    playing: bool = False
    position: int = 0
    duration: int = 0

    def start(self) -> None:
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def reset(self) -> None:
        self.playing = False
        self.position = 0
        self.duration = 0

    def update_position(self, position: int) -> None:
        self.position = max(0, position)

    def update_duration(self, duration: int) -> None:
        self.duration = max(0, duration)


@dataclass(frozen=True)
class AudioLibrary:
    """Map ghazal names to recordings stored beside the poem archive."""

    directory: Path

    def __init__(self, directory: str | Path) -> None:
        object.__setattr__(self, "directory", Path(directory))

    def path_for_poem(self, poem_name: str) -> Path | None:
        path = self.directory / f"{poem_name}.wav"
        return path if path.is_file() else None

    def has_audio(self, poem_name: str) -> bool:
        return self.path_for_poem(poem_name) is not None

    def names(self) -> set[str]:
        if not self.directory.is_dir():
            return set()
        return {path.stem for path in self.directory.glob("*.wav")}
