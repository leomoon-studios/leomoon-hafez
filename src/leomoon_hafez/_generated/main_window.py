# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(850, 711)
        main.setMinimumSize(QSize(850, 711))
        icon = QIcon()
        icon.addFile(u":/res/icons/main.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main.setWindowIcon(icon)
        main.setLayoutDirection(Qt.RightToLeft)
        main.setStyleSheet(u"QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}\n"
"QLabel#titleLbl {color: rgb(68,68,68);}\n"
"QLabel#verLbl {color: rgb(68,68,68);}")
        self.centralwidget = QWidget(main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.banner = QFrame(self.centralwidget)
        self.banner.setObjectName(u"banner")
        self.banner.setMinimumSize(QSize(0, 119))
        self.banner.setMaximumSize(QSize(16777215, 119))
        self.banner.setSizeIncrement(QSize(0, 0))
        self.banner.setFrameShape(QFrame.NoFrame)
        self.banner.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.banner)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 9, 0, 9)
        self.horizontalSpacer_2 = QSpacerItem(24, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.logoLbl = QLabel(self.banner)
        self.logoLbl.setObjectName(u"logoLbl")
        self.logoLbl.setMinimumSize(QSize(101, 101))
        self.logoLbl.setMaximumSize(QSize(101, 101))
        self.logoLbl.setPixmap(QPixmap(u":/res/icons/main.svg"))
        self.logoLbl.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.logoLbl)

        self.horizontalSpacer = QSpacerItem(24, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.titleLbl = QLabel(self.banner)
        self.titleLbl.setObjectName(u"titleLbl")
        self.titleLbl.setMinimumSize(QSize(0, 40))
        self.titleLbl.setMaximumSize(QSize(16777215, 45))
        font = QFont()
        font.setFamilies([u"Vazir FD"])
        font.setPointSize(24)
        font.setBold(True)
        self.titleLbl.setFont(font)

        self.verticalLayout.addWidget(self.titleLbl)

        self.verLbl = QLabel(self.banner)
        self.verLbl.setObjectName(u"verLbl")
        font1 = QFont()
        font1.setFamilies([u"Vazir FD"])
        font1.setPointSize(12)
        self.verLbl.setFont(font1)

        self.verticalLayout.addWidget(self.verLbl)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addWidget(self.banner)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(141, 531))
        self.frame.setMaximumSize(QSize(141, 531))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(0)
        self.ghazalRdo = QRadioButton(self.frame)
        self.ghazalRdo.setObjectName(u"ghazalRdo")
        self.ghazalRdo.setGeometry(QRect(49, 0, 91, 31))
        font2 = QFont()
        font2.setFamilies([u"Vazir FD"])
        font2.setPointSize(14)
        self.ghazalRdo.setFont(font2)
        self.ghazalRdo.setChecked(True)
        self.masnaviRdo = QRadioButton(self.frame)
        self.masnaviRdo.setObjectName(u"masnaviRdo")
        self.masnaviRdo.setGeometry(QRect(49, 80, 91, 31))
        self.masnaviRdo.setFont(font2)
        self.gheteRdo = QRadioButton(self.frame)
        self.gheteRdo.setObjectName(u"gheteRdo")
        self.gheteRdo.setGeometry(QRect(49, 120, 91, 31))
        self.gheteRdo.setFont(font2)
        self.ghasideRdo = QRadioButton(self.frame)
        self.ghasideRdo.setObjectName(u"ghasideRdo")
        self.ghasideRdo.setGeometry(QRect(49, 40, 91, 31))
        self.ghasideRdo.setFont(font2)
        self.robayiRdo = QRadioButton(self.frame)
        self.robayiRdo.setObjectName(u"robayiRdo")
        self.robayiRdo.setGeometry(QRect(58, 160, 82, 31))
        self.robayiRdo.setFont(font2)
        self.nastalighBtn = QPushButton(self.frame)
        self.nastalighBtn.setObjectName(u"nastalighBtn")
        self.nastalighBtn.setGeometry(QRect(0, 390, 141, 41))
        self.nastalighBtn.setFont(font2)
        self.vazirBtn = QPushButton(self.frame)
        self.vazirBtn.setObjectName(u"vazirBtn")
        self.vazirBtn.setGeometry(QRect(0, 340, 141, 41))
        self.vazirBtn.setFont(font2)
        self.plusBtn = QPushButton(self.frame)
        self.plusBtn.setObjectName(u"plusBtn")
        self.plusBtn.setGeometry(QRect(100, 490, 41, 41))
        self.plusBtn.setFont(font2)
        icon1 = QIcon()
        icon1.addFile(u":/res/icons/plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plusBtn.setIcon(icon1)
        self.plusBtn.setIconSize(QSize(20, 20))
        self.minusBtn = QPushButton(self.frame)
        self.minusBtn.setObjectName(u"minusBtn")
        self.minusBtn.setGeometry(QRect(0, 490, 41, 41))
        self.minusBtn.setFont(font2)
        icon2 = QIcon()
        icon2.addFile(u":/res/icons/minus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minusBtn.setIcon(icon2)
        self.minusBtn.setIconSize(QSize(20, 20))
        self.searchRdo = QRadioButton(self.frame)
        self.searchRdo.setObjectName(u"searchRdo")
        self.searchRdo.setGeometry(QRect(58, 200, 82, 31))
        self.searchRdo.setFont(font2)
        self.searchInp = QLineEdit(self.frame)
        self.searchInp.setObjectName(u"searchInp")
        self.searchInp.setEnabled(False)
        self.searchInp.setGeometry(QRect(40, 241, 101, 31))
        self.searchInp.setFont(font2)
        self.searchBtn = QPushButton(self.frame)
        self.searchBtn.setObjectName(u"searchBtn")
        self.searchBtn.setEnabled(False)
        self.searchBtn.setGeometry(QRect(0, 240, 33, 33))
        self.searchBtn.setFont(font1)
        icon3 = QIcon()
        icon3.addFile(u":/res/icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.searchBtn.setIcon(icon3)
        self.searchBtn.setIconSize(QSize(20, 16))
        self.printBtn = QPushButton(self.frame)
        self.printBtn.setObjectName(u"printBtn")
        self.printBtn.setGeometry(QRect(50, 490, 41, 41))
        self.printBtn.setFont(font2)
        icon4 = QIcon()
        icon4.addFile(u":/res/icons/print.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.printBtn.setIcon(icon4)
        self.printBtn.setIconSize(QSize(25, 25))
        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 323, 141, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.randomBtn = QPushButton(self.frame)
        self.randomBtn.setObjectName(u"randomBtn")
        self.randomBtn.setGeometry(QRect(0, 280, 141, 41))
        self.randomBtn.setFont(font2)
        self.themeBtn = QPushButton(self.frame)
        self.themeBtn.setObjectName(u"themeBtn")
        self.themeBtn.setGeometry(QRect(0, 440, 141, 41))
        self.themeBtn.setFont(font2)

        self.verticalLayout_2.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.listLst = QListWidget(self.centralwidget)
        self.listLst.setObjectName(u"listLst")
        self.listLst.setMinimumSize(QSize(145, 0))
        self.listLst.setMaximumSize(QSize(145, 16777215))
        self.listLst.setFont(font1)

        self.horizontalLayout_3.addWidget(self.listLst)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"Vazir"])
        self.textEdit.setFont(font3)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)

        self.horizontalLayout_3.addWidget(self.textEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 9)
        self.copyLbl = QLabel(self.centralwidget)
        self.copyLbl.setObjectName(u"copyLbl")
        self.copyLbl.setMinimumSize(QSize(131, 31))
        self.copyLbl.setMaximumSize(QSize(131, 31))
        font4 = QFont()
        font4.setFamilies([u"Vazir FD"])
        font4.setPointSize(10)
        self.copyLbl.setFont(font4)
        self.copyLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.copyLbl)

        self.horizontalFrame_2 = QFrame(self.centralwidget)
        self.horizontalFrame_2.setObjectName(u"horizontalFrame_2")
        self.horizontalFrame_2.setMinimumSize(QSize(459, 0))
        self.horizontalFrame_2.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_4.setSpacing(9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.slider = QSlider(self.horizontalFrame_2)
        self.slider.setObjectName(u"slider")
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setInvertedAppearance(True)

        self.horizontalLayout_4.addWidget(self.slider)

        self.playBtn = QPushButton(self.horizontalFrame_2)
        self.playBtn.setObjectName(u"playBtn")
        self.playBtn.setMinimumSize(QSize(31, 31))
        self.playBtn.setMaximumSize(QSize(31, 31))
        icon5 = QIcon()
        icon5.addFile(u":/res/icons/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.playBtn.setIcon(icon5)
        self.playBtn.setIconSize(QSize(16, 16))
        self.playBtn.setFlat(False)

        self.horizontalLayout_4.addWidget(self.playBtn)


        self.horizontalLayout.addWidget(self.horizontalFrame_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        main.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.ghazalRdo, self.ghasideRdo)
        QWidget.setTabOrder(self.ghasideRdo, self.masnaviRdo)
        QWidget.setTabOrder(self.masnaviRdo, self.gheteRdo)
        QWidget.setTabOrder(self.gheteRdo, self.robayiRdo)
        QWidget.setTabOrder(self.robayiRdo, self.searchRdo)
        QWidget.setTabOrder(self.searchRdo, self.searchInp)
        QWidget.setTabOrder(self.searchInp, self.searchBtn)
        QWidget.setTabOrder(self.searchBtn, self.vazirBtn)
        QWidget.setTabOrder(self.vazirBtn, self.nastalighBtn)
        QWidget.setTabOrder(self.nastalighBtn, self.plusBtn)
        QWidget.setTabOrder(self.plusBtn, self.minusBtn)
        QWidget.setTabOrder(self.minusBtn, self.printBtn)
        QWidget.setTabOrder(self.printBtn, self.listLst)
        QWidget.setTabOrder(self.listLst, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.playBtn)
        QWidget.setTabOrder(self.playBtn, self.slider)

        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"MainWindow", None))
        self.logoLbl.setText("")
        self.titleLbl.setText(QCoreApplication.translate("main", u"\u062f\u06cc\u0648\u0627\u0646 \u062d\u0627\u0641\u0638", None))
        self.verLbl.setText(QCoreApplication.translate("main", u"\u0646\u0633\u062e\u0647", None))
        self.ghazalRdo.setText(QCoreApplication.translate("main", u"\u063a\u0632\u0644\u06cc\u0627\u062a", None))
        self.masnaviRdo.setText(QCoreApplication.translate("main", u"\u0645\u062b\u0646\u0648\u06cc\u0627\u062a", None))
        self.gheteRdo.setText(QCoreApplication.translate("main", u"\u0645\u0642\u0637\u0639\u0627\u062a", None))
        self.ghasideRdo.setText(QCoreApplication.translate("main", u"\u0642\u0635\u0627\u06cc\u062f", None))
        self.robayiRdo.setText(QCoreApplication.translate("main", u"\u0631\u0628\u0627\u0639\u06cc\u0627\u062a", None))
        self.nastalighBtn.setText(QCoreApplication.translate("main", u"\u0642\u0644\u0645 \u0646\u0633\u062a\u0639\u0644\u06cc\u0642", None))
        self.vazirBtn.setText(QCoreApplication.translate("main", u"\u0642\u0644\u0645 \u0648\u0632\u06cc\u0631", None))
        self.plusBtn.setText("")
        self.minusBtn.setText("")
        self.searchRdo.setText(QCoreApplication.translate("main", u"\u062c\u0633\u062a\u062c\u0648", None))
        self.searchBtn.setText("")
        self.printBtn.setText("")
        self.randomBtn.setText(QCoreApplication.translate("main", u"\u0641\u0627\u0644 \u062d\u0627\u0641\u0638", None))
        self.themeBtn.setText(QCoreApplication.translate("main", u"\u062a\u063a\u06cc\u06cc\u0631 \u067e\u0648\u0633\u062a\u0647", None))
        self.textEdit.setHtml(QCoreApplication.translate("main", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Vazir'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.copyLbl.setText(QCoreApplication.translate("main", u"\u00a9 LeoMoon Studios", None))
        self.playBtn.setText("")
    # retranslateUi

