# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_project.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSplitter,
    QTabWidget, QWidget)

class Ui_TabProject(object):
    def setupUi(self, TabProject):
        if not TabProject.objectName():
            TabProject.setObjectName(u"TabProject")
        TabProject.resize(436, 300)
        self.main_horizontal_layout = QHBoxLayout(TabProject)
        self.main_horizontal_layout.setSpacing(0)
        self.main_horizontal_layout.setObjectName(u"main_horizontal_layout")
        self.main_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(TabProject)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.tab_widget = QTabWidget(self.splitter)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setTabsClosable(False)
        self.splitter.addWidget(self.tab_widget)

        self.main_horizontal_layout.addWidget(self.splitter)


        self.retranslateUi(TabProject)

        self.tab_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(TabProject)
    # setupUi

    def retranslateUi(self, TabProject):
        TabProject.setWindowTitle(QCoreApplication.translate("TabProject", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
    # retranslateUi

