#-*- coding: utf-8 -*-

import sys
import os.path #file check
# import platform #detect os platform
# import re #sorting files
import random #faal
# from pathlib import Path #home directory
from natsort import natsorted #sort numbers properly
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport #pyqt stuff
from PyQt5 import QtMultimedia as M
import zipfile
# import io
from ext.darkdetect import isDark #darkdetect 0.5.0 [ https://github.com/albertosottile/darkdetect ] 20210912
#local imports
from gui.guiMain import Ui_main

#version: 1.1.4

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

title = 'دیوان حافظ'
ver = '1.0.0'

class mainUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)
        self.themeFlg = False
        self.setAcceptDrops(True) #accept file drops
        self.ui = Ui_main()
        self.ui.setupUi(self)
        ###############################################################################
        ####### Theme startup #########################################################
        ###############################################################################
        if isDark():
            self.themeFlg = False
            self._theme()
        ###############################################################################
        ####### Variables #############################################################
        ###############################################################################
        self.play = False
        self.setWindowTitle('LeoMoon Hafez '+ver)
        self.ui.titleLbl.setText(title)
        self.ui.verLbl.setText('نسخه '+ver)
        self.datapath = os.path.dirname(os.path.realpath(sys.argv[0]))+'/data.db'
        self.audiopath = os.path.dirname(os.path.realpath(sys.argv[0]))+'/audio/'
        self.data = zipfile.ZipFile(self.datapath, 'r')
        self.data.setpassword(b'z!WbsdCkm#')
        self.ui.copyLbl.setText('© LeoMoon Studios')
        #hotkeys
        self.hotSearch = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
        self.hotSearch.activated.connect(self._hSearch)
        self.hotZoomIn = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+="), self)
        self.hotZoomIn.activated.connect(self._plus)
        self.hotPrint = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+P"), self)
        self.hotPrint.activated.connect(self._preview)
        self.hotZoomOut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+-"), self)
        self.hotZoomOut.activated.connect(self._minus)
        self.hotZoomOut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+0"), self)
        self.hotZoomOut.activated.connect(self._vazir)
        self.hotPlay = QtWidgets.QShortcut(QtGui.QKeySequence("Space"), self)
        self.hotPlay.activated.connect(self._hPlay)
        self.hotRandom = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.hotRandom.activated.connect(self._hRandom)
        #ui functions
        self.ui.ghazalRdo.toggled.connect(self._path)
        self.ui.ghasideRdo.toggled.connect(self._path)
        self.ui.masnaviRdo.toggled.connect(self._path)
        self.ui.gheteRdo.toggled.connect(self._path)
        self.ui.robayiRdo.toggled.connect(self._path)
        self.ui.searchRdo.toggled.connect(self._search)
        self.ui.searchBtn.clicked.connect(self._searchList)
        self.ui.searchBtn.setAutoDefault(True) #set the default button
        self.ui.searchInp.returnPressed.connect(self._searchList) #set what enter does
        self.ui.randomBtn.clicked.connect(self._hRandom)
        self.ui.vazirBtn.clicked.connect(self._vazir)
        self.ui.nastalighBtn.clicked.connect(self._nastaliq)
        self.ui.plusBtn.clicked.connect(self._plus)
        self.ui.printBtn.clicked.connect(self._preview)
        self.ui.minusBtn.clicked.connect(self._minus)
        self.ui.listLst.itemSelectionChanged.connect(self._listChange)
        self.ui.playBtn.clicked.connect(self._play)
        self.ui.slider.sliderMoved.connect(self._setPosition)
        self.ui.slider.valueChanged.connect(self._mediaCheck)
        self.ui.ghazalRdo.setChecked(True)
        self.ui.listLst.clear()
        font = QtGui.QFont()
        font.setFamily('Vazir FD')
        font.setPointSize(15)
        self.ui.textEdit.setFont(font)
        self._path()
        self.ui.listLst.setCurrentRow(0)
        self.ui.listLst.setFocus()
        #platform changes
        # if sys.platform.startswith('darwin'): #macos
        #     #move +5x
        #     #resize +11y
        #     self.ui.vazirBtn.hide()
        #     self.ui.nastalighBtn.hide()
        #     self.ui.ghazalRdo.move(self.ui.ghazalRdo.pos().x()+2, self.ui.ghazalRdo.pos().y())
        #     self.ui.ghasideRdo.move(self.ui.ghasideRdo.pos().x()+2, self.ui.ghasideRdo.pos().y())
        #     self.ui.masnaviRdo.move(self.ui.masnaviRdo.pos().x()+2, self.ui.masnaviRdo.pos().y())
        #     self.ui.gheteRdo.move(self.ui.gheteRdo.pos().x()+2, self.ui.gheteRdo.pos().y())
        #     self.ui.robayiRdo.move(self.ui.robayiRdo.pos().x()+2, self.ui.robayiRdo.pos().y())
        #     self.ui.searchRdo.move(self.ui.searchRdo.pos().x()+2, self.ui.searchRdo.pos().y())
        #     self.ui.randomBtn.move(self.ui.randomBtn.pos().x()-6, self.ui.randomBtn.pos().y()-2)
        #     self.ui.randomBtn.resize(self.ui.randomBtn.width()+12, self.ui.randomBtn.height()+6)
        #     self.ui.titleLbl.setFont(QtGui.QFont("Vazir", 29, QtGui.QFont.Black))
        #     self.ui.verLbl.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.ghazalRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.ghasideRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.masnaviRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.gheteRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.robayiRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.searchRdo.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.listLst.setFont(QtGui.QFont('Vazir FD', 17))
        #     self.ui.textEdit.setFont(QtGui.QFont('Vazir FD', 18))
        #     self.ui.copyLbl.setFont(QtGui.QFont('Vazir FD', 14))
        #     #pyqt 5.14.1 fixes
        #     self.ui.searchBtn.resize(self.ui.searchBtn.width()+11, self.ui.searchBtn.height()+6)
        #     self.ui.plusBtn.resize(self.ui.plusBtn.width()+11, self.ui.plusBtn.height()+6)
        #     self.ui.printBtn.resize(self.ui.printBtn.width()+11, self.ui.printBtn.height()+6)
        #     self.ui.minusBtn.resize(self.ui.minusBtn.width()+11, self.ui.minusBtn.height()+6)
        #     self.ui.searchBtn.move(self.ui.searchBtn.pos().x()-6, self.ui.searchBtn.pos().y()-2)
        #     self.ui.plusBtn.move(self.ui.plusBtn.pos().x()-6, self.ui.vazirBtn.pos().y()-2)
        #     self.ui.printBtn.move(self.ui.printBtn.pos().x()-6, self.ui.vazirBtn.pos().y()-2)
        #     self.ui.minusBtn.move(self.ui.minusBtn.pos().x()-6, self.ui.vazirBtn.pos().y()-2)
        #     self.ui.playBtn.setFlat(True)
            #pyqt 5.10.1 fixes
            #self.ui.plusBtn.resize(self.ui.plusBtn.width()+2, self.ui.plusBtn.height()+3)
            #self.ui.printBtn.resize(self.ui.printBtn.width()+2, self.ui.printBtn.height()+3)
            #self.ui.minusBtn.resize(self.ui.minusBtn.width()+2, self.ui.minusBtn.height()+3)
            #self.ui.plusBtn.move(self.ui.plusBtn.pos().x()-2, self.ui.vazirBtn.pos().y())
            #self.ui.printBtn.move(self.ui.printBtn.pos().x()-1, self.ui.vazirBtn.pos().y())
            #self.ui.minusBtn.move(self.ui.minusBtn.pos().x(), self.ui.vazirBtn.pos().y())

    ###############################################################################
    ####### Functions #############################################################
    ###############################################################################
    def svgColorChange(self, svg_filepath, color='red'):
        img = QtGui.QPixmap(svg_filepath)
        qp = QtGui.QPainter(img)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        qp.fillRect( img.rect(), QtGui.QColor(color) )
        qp.end()
        return QtGui.QIcon(img)

    def _theme(self):
        if not self.themeFlg:
            self.ui.searchBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/search.svg', 'lightGray')))
            self.ui.plusBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/plus.svg', 'lightGray')))
            self.ui.printBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/print.svg', 'lightGray')))
            self.ui.minusBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/minus.svg', 'lightGray')))
            self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'lightGray')))
            dark_theme = QtGui.QPalette()
            dark_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(55,53,53))
            dark_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(30,30,30))
            dark_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(55,55,55))
            dark_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Link, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
            dark_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53))
            QtGui.QGuiApplication.setPalette(dark_theme)
            self.setStyleSheet("""
                                    QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #5e5b5b, stop:1 #373535); border-radius: 0px;}
                                    QLabel#titleLbl {color: rgb(227,227,227);}
                                    QLabel#verLbl {color: rgb(227,227,227);}
                                        """)
            # self.ui.actionDarkMode.setChecked(True)
        else:
            self.ui.searchBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/search.svg', 'black')))
            self.ui.plusBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/plus.svg', 'black')))
            self.ui.printBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/print.svg', 'black')))
            self.ui.minusBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/minus.svg', 'black')))
            self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'black')))
            light_theme = QtGui.QPalette()
            light_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Link, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(128,128,128))
            light_theme.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(243,243,243))
            QtGui.QGuiApplication.setPalette(light_theme)
            self.setStyleSheet("""
                                    QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}
                                    QLabel#titleLbl {color: rgb(68,68,68);}
                                    QLabel#verLbl {color: rgb(68,68,68);}
                                        """)
            # self.ui.actionDarkMode.setChecked(False)
        self.themeFlg = not self.themeFlg

    def _preview(self):
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.setWindowIcon(QtGui.QIcon(':/res/icons/main.svg'))
        preview.paintRequested.connect(lambda p: self.ui.textEdit.print_(p))
        preview.exec_()

    def _path(self):
        self.ui.listLst.clear()
        if self.ui.ghazalRdo.isChecked():
            self.pre = 'غزل'
        elif self.ui.ghasideRdo.isChecked():
            self.pre = 'قصیده'
        elif self.ui.masnaviRdo.isChecked():
            self.pre = 'مثنوی'
        elif self.ui.gheteRdo.isChecked():
            self.pre = 'قطعه'
        elif self.ui.robayiRdo.isChecked():
            self.pre = 'رباعی'
        if self.ui.ghazalRdo.isChecked():
            self.ui.playBtn.show()
            self.ui.slider.show()
        else:
            self.ui.playBtn.hide()
            self.ui.slider.hide()
        if os.path.exists(self.datapath):
            alist = natsorted([f for f in self.data.namelist() if f.startswith(self.pre)][0:])
            self.ui.searchInp.setDisabled(True)
            self.ui.searchBtn.setDisabled(True)
            self.ui.searchBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/search.svg', 'blue')))
            self.ui.listLst.addItems(alist)
            self.ui.listLst.setCurrentRow(0)
            self.ui.listLst.setFocus()

    def _search(self):
        self.ui.playBtn.hide()
        self.ui.slider.hide()
        self.ui.listLst.clear()
        self.ui.textEdit.clear()
        self.ui.searchInp.setDisabled(False)
        self.ui.searchBtn.setDisabled(False)
        if self.themeFlg:
            self.ui.searchBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/search.svg', 'lightGray')))
        else:
            self.ui.searchBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/search.svg', 'black')))
        self.ui.searchInp.setFocus()

    def _hSearch(self):
        self.ui.searchRdo.setChecked(True)

    def _hPlay(self):
        if self.ui.playBtn.isVisible():
            self._play()

    def _hRandom(self):
        self.ui.ghazalRdo.setChecked(True)
        self.ui.listLst.setCurrentRow(random.randrange(0,496,1))

    def _searchList(self):
        self.ui.listLst.clear()
        slist = natsorted(self.data.namelist())
        if self.ui.searchInp.text() != '':
            for s in slist:
                if bytes(self.ui.searchInp.text(), 'utf-8') in self.data.read(s):
                    self.ui.listLst.addItem(s)

    def _vazir(self):
        font = QtGui.QFont()
        font.setFamily('Vazir FD')
        font.setPointSize(15)
        self.ui.textEdit.setFont(font)
        self.ui.listLst.setFocus()

    def _nastaliq(self):
        font = QtGui.QFont()
        font.setFamily('IranNastaliq-Web')
        font.setPointSize(20)
        self.ui.textEdit.setFont(font)
        self.ui.listLst.setFocus()

    def _plus(self):
        font = QtGui.QFont()
        font.setFamily(self.ui.textEdit.font().family())
        font.setPointSize(self.ui.textEdit.font().pointSize()+3)
        self.ui.textEdit.setFont(font)
        self.ui.listLst.setFocus()

    def _minus(self):
        font = QtGui.QFont()
        font.setFamily(self.ui.textEdit.font().family())
        font.setPointSize(self.ui.textEdit.font().pointSize()-3)
        self.ui.textEdit.setFont(font)
        self.ui.listLst.setFocus()

    def _listChange(self):
        self.player = M.QMediaPlayer()
        if 'غزل' in self.ui.listLst.currentItem().text() and os.path.exists(self.audiopath+self.ui.listLst.currentItem().text()+'.wav'):
            self.ui.playBtn.show()
            self.ui.slider.show()
            self.audio = QtCore.QUrl.fromLocalFile(self.audiopath+self.ui.listLst.currentItem().text()+'.wav')
            self.content = M.QMediaContent(self.audio)
            self.player.setMedia(self.content)
            if self.themeFlg:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'lightGray')))
            else:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'black')))
            self.play = False
            self.player.stop()
            self.ui.slider.setValue(0)
            self.player.positionChanged.connect(self.positionChanged)
            self.player.durationChanged.connect(self.durationChanged)
        else:
            self.ui.playBtn.hide()
            self.ui.slider.hide()
            self.play = False
            self.player.stop()
        if self.ui.listLst.currentItem().text() in self.data.namelist():
            self.ui.textEdit.setHtml('<p style=\"text-align: center;\">'+self.data.read(self.ui.listLst.currentItem().text()).decode("utf-8").replace('\n', '<br \>')+'</p>')
        # if self.ui.autoCbox.isChecked() and os.path.exists(self.audiopath+self.ui.listLst.currentItem().text()+'.wav'):
        #     self._play()

    def _play(self):
        if self.play:
            self.player.pause()
            if self.themeFlg:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'lightGray')))
            else:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/play.svg', 'black')))
            self.play = False
        else:
            self.player.play()
            if self.themeFlg:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/pause.svg', 'lightGray')))
            else:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/pause.svg', 'black')))
            self.play = True
        self.ui.listLst.setFocus()

    def positionChanged(self, position):
        self.ui.slider.setValue(position)

    def durationChanged(self, duration):
        self.ui.slider.setRange(0, duration)

    def _setPosition(self, position):
        self.player.setPosition(position)

    def _next(self):
        if self.ui.autoCbox.isChecked() and self.ui.listLst.currentRow() + 1 < self.ui.listLst.count():
            self.player = ''
            self.content = ''
            self.ui.listLst.setCurrentRow(self.ui.listLst.currentRow() + 1)
            current = self.ui.listLst.currentRow() + 1
            if current < self.ui.listLst.count():
                self.ui.listLst.setCurrentRow(current)

    def _mediaCheck(self): #reset playback when it reaches the end
        if self.player.duration() == self.ui.slider.value():
            self.play = False
            self.player.stop()
            if self.themeFlg:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/pause.svg', 'lightGray')))
            else:
                self.ui.playBtn.setIcon(QtGui.QIcon(self.svgColorChange(':/res/icons/pause.svg', 'black')))
            self.ui.slider.setValue(0)
            # self._next()

    def _exit(self):
        self.close()

    def closeEvent(self, event):
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/IranNastaliq-Web.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Black.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-FD.ttf') #add custom font no install
    main = mainUi()
    if not os.path.exists(main.datapath):
        popup = QtWidgets.QMessageBox()
        popup.setWindowIcon(QtGui.QIcon(':/res/icons/main.svg'))
        popup.setIcon(QtWidgets.QMessageBox.Critical)
        popup.setWindowTitle('خطا')
        popup.setText('پوشه data موجود نمی‌باشد!')
        font = QtGui.QFont()
        font.setFamily('Vazir FD')
        font.setPointSize(10)
        popup.setFont(font)
        popup.setMinimumSize(200,423)
        popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
        popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
        popup.exec_()
        main.close()
    else:
        main.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
