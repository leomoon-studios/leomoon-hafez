from __future__ import annotations

from pathlib import Path

from hafez_audio import AudioLibrary, PlaybackState
from hafez_corpus import PoemArchive


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_audio_library_maps_existing_recordings(tmp_path: Path) -> None:
    recording = tmp_path / "غزل شماره 1.wav"
    recording.write_bytes(b"fixture audio")
    library = AudioLibrary(tmp_path)

    assert library.path_for_poem("غزل شماره 1") == recording
    assert library.has_audio("غزل شماره 1")
    assert not library.has_audio("غزل شماره 2")
    assert library.names() == {"غزل شماره 1"}


def test_playback_state_tracks_start_pause_position_duration_and_reset() -> None:
    state = PlaybackState()

    state.start()
    state.update_position(12)
    state.update_duration(60)
    assert state.playing and state.position == 12 and state.duration == 60
    state.pause()
    assert not state.playing
    state.reset()
    assert (state.playing, state.position, state.duration) == (False, 0, 0)


def test_bundled_audio_index_maps_one_to_one_to_ghazals() -> None:
    library = AudioLibrary(PROJECT_ROOT / "src" / "audio")
    corpus = PoemArchive(PROJECT_ROOT / "src" / "data.db")
    recording = library.path_for_poem("غزل شماره 1")

    assert library.names() == {name.removesuffix(".txt") for name in corpus.names("غزل")}
    with recording.open("rb") as stream:
        assert stream.read(4) == b"RIFF"
        stream.seek(8)
        assert stream.read(4) == b"WAVE"
