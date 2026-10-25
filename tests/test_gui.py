from __future__ import annotations

from pathlib import Path

from PySide6 import QtGui

from leomoon_hafez import app as main
from leomoon_hafez.audio import AudioLibrary
from leomoon_hafez.version import __version__


PROJECT_ROOT = Path(__file__).resolve().parents[1]
class _Signal:
    def __init__(self) -> None:
        self.callback = None

    def connect(self, callback) -> None:
        self.callback = callback


class _PreviewDialog:
    instance = None

    def __init__(self) -> None:
        self.paintRequested = _Signal()
        self.icon = None
        self.executed = False
        _PreviewDialog.instance = self

    def setWindowIcon(self, icon) -> None:
        self.icon = icon

    def exec(self) -> None:
        self.executed = True


def test_main_window_starts_and_exercises_primary_controls(qtbot, monkeypatch) -> None:
    monkeypatch.setattr(main, "isDark", lambda: False)
    QtGui.QFontDatabase.addApplicationFont(":/res/fonts/Vazir-FD.ttf")
    QtGui.QFontDatabase.addApplicationFont(":/res/fonts/IranNastaliq.ttf")

    window = main.mainUi()
    qtbot.addWidget(window)
    window.show()

    assert window.windowTitle() == f"LeoMoon Hafez {__version__}"
    assert window.ui.verLbl.text() == f"نسخه {__version__}"
    assert window.ui.listLst.count() == 495
    assert window.ui.playBtn.isVisible()
    assert window.ui.slider.isVisible()
    assert window.player.audioOutput() is window.audio_output

    previous_theme = window.themeFlg
    window._theme()
    assert window.themeFlg is not previous_theme
    window._nastaliq()
    assert window.ui.textEdit.font().family() == "IranNastaliq"
    window._vazir()
    assert window.ui.textEdit.font().family() == "Vazir FD"
    original_size = window.ui.textEdit.font().pointSize()
    window._plus()
    assert window.ui.textEdit.font().pointSize() == original_size + 3
    window._minus()
    assert window.ui.textEdit.font().pointSize() == original_size

    window._hRandom()
    assert window.ui.listLst.currentItem() is not None
    assert window.ui.listLst.currentItem().text().startswith("غزل")
    assert window.player.source().isLocalFile()

    window.durationChanged(100)
    window.positionChanged(20)
    assert (window.playback.position, window.playback.duration) == (20, 100)
    assert window.ui.slider.value() == 20
    window._play()
    assert window.playback.playing
    window._play()
    assert not window.playback.playing
    window._media_error(None, "fixture error")
    assert not window.playback.playing
    assert window.ui.slider.value() == 0

    monkeypatch.setattr(main.QtPrintSupport, "QPrintPreviewDialog", _PreviewDialog)
    window._preview()
    assert _PreviewDialog.instance.executed
    assert _PreviewDialog.instance.paintRequested.callback is not None

    window.ui.ghasideRdo.setChecked(True)
    assert not window.ui.playBtn.isVisible()
    assert not window.ui.slider.isVisible()
    assert window.ui.textEdit.toPlainText()

    window.ui.ghazalRdo.setChecked(True)
    window.audio_library = AudioLibrary(PROJECT_ROOT / "tests" / "fixtures" / "no-audio")
    window.ui.listLst.setCurrentRow(0)
    window._listChange()
    assert not window.ui.playBtn.isVisible()
    assert not window.ui.slider.isVisible()

    window._hSearch()
    assert window.ui.searchInp.isEnabled()
    assert window.ui.searchBtn.isEnabled()
    window.ui.searchInp.setText("الا")
    window._searchList()
    assert window.ui.listLst.count() > 0


def test_main_window_handles_missing_poem_and_audio_assets(qtbot, monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(main, "isDark", lambda: False)
    monkeypatch.setattr(main, "ASSETS_DIR", tmp_path)

    window = main.mainUi()
    qtbot.addWidget(window)
    window.show()

    assert window.ui.listLst.count() == 0
    assert not window.audio_library.names()
