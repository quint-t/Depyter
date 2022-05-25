# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templates.ui'
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
from PySide6.QtWidgets import (QApplication, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Templates(object):
    def setupUi(self, Templates):
        if not Templates.objectName():
            Templates.setObjectName(u"Templates")
        Templates.resize(200, 300)
        self.main_vertical_layout = QVBoxLayout(Templates)
        self.main_vertical_layout.setSpacing(0)
        self.main_vertical_layout.setObjectName(u"main_vertical_layout")
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(Templates)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName(u"scroll_area_widget_contents")
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 198, 298))
        self.scroll_area_vertical_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area_vertical_layout.setSpacing(0)
        self.scroll_area_vertical_layout.setObjectName(u"scroll_area_vertical_layout")
        self.scroll_area_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(self.scroll_area_widget_contents)
        self.main_widget.setObjectName(u"main_widget")
        self.main_widget_vertical_layout = QVBoxLayout(self.main_widget)
        self.main_widget_vertical_layout.setSpacing(0)
        self.main_widget_vertical_layout.setObjectName(u"main_widget_vertical_layout")
        self.main_widget_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area_vertical_layout.addWidget(self.main_widget)

        self.vertical_spacer = QSpacerItem(20, 281, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scroll_area_vertical_layout.addItem(self.vertical_spacer)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.main_vertical_layout.addWidget(self.scroll_area)


        self.retranslateUi(Templates)

        QMetaObject.connectSlotsByName(Templates)
    # setupUi

    def retranslateUi(self, Templates):
        Templates.setWindowTitle(QCoreApplication.translate("Templates", u"\u0428\u0430\u0431\u043b\u043e\u043d\u044b", None))
    # retranslateUi

