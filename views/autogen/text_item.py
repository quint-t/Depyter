# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_item.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from  . import resources_rc

class Ui_TextItem(object):
    def setupUi(self, TextItem):
        if not TextItem.objectName():
            TextItem.setObjectName(u"TextItem")
        TextItem.resize(500, 200)
        self.main_vertical_layout = QVBoxLayout(TextItem)
        self.main_vertical_layout.setSpacing(0)
        self.main_vertical_layout.setObjectName(u"main_vertical_layout")
        self.main_vertical_layout.setContentsMargins(3, 3, 3, 3)
        self.text_caption = QLineEdit(TextItem)
        self.text_caption.setObjectName(u"text_caption")
        font = QFont()
        font.setPointSize(12)
        self.text_caption.setFont(font)
        self.text_caption.setStyleSheet(u"background-color: rgba(255, 255, 255, 10);")
        self.text_caption.setFrame(False)
        self.text_caption.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.main_vertical_layout.addWidget(self.text_caption)

        self.main_frame = QFrame(TextItem)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame_horizontal_layout = QHBoxLayout(self.main_frame)
        self.main_frame_horizontal_layout.setSpacing(0)
        self.main_frame_horizontal_layout.setObjectName(u"main_frame_horizontal_layout")
        self.main_frame_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.left_bar_frame = QFrame(self.main_frame)
        self.left_bar_frame.setObjectName(u"left_bar_frame")
        self.left_bar_frame.setMinimumSize(QSize(40, 0))
        self.left_bar_frame.setMaximumSize(QSize(40, 16777215))
        self.left_bar_frame.setFrameShape(QFrame.StyledPanel)
        self.left_bar_frame.setFrameShadow(QFrame.Raised)
        self.left_bar_frame_vertical_layout = QVBoxLayout(self.left_bar_frame)
        self.left_bar_frame_vertical_layout.setSpacing(0)
        self.left_bar_frame_vertical_layout.setObjectName(u"left_bar_frame_vertical_layout")
        self.left_bar_frame_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.edit_button = QPushButton(self.left_bar_frame)
        self.edit_button.setObjectName(u"edit_button")
        icon = QIcon()
        icon.addFile(u":/icons/icons/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.edit_button.setIcon(icon)
        self.edit_button.setIconSize(QSize(17, 17))

        self.left_bar_frame_vertical_layout.addWidget(self.edit_button)

        self.update_button = QPushButton(self.left_bar_frame)
        self.update_button.setObjectName(u"update_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/update.png", QSize(), QIcon.Normal, QIcon.Off)
        self.update_button.setIcon(icon1)
        self.update_button.setIconSize(QSize(17, 17))

        self.left_bar_frame_vertical_layout.addWidget(self.update_button)

        self.del_button = QPushButton(self.left_bar_frame)
        self.del_button.setObjectName(u"del_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.del_button.setIcon(icon2)
        self.del_button.setIconSize(QSize(15, 15))

        self.left_bar_frame_vertical_layout.addWidget(self.del_button)

        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.left_bar_frame_vertical_layout.addItem(self.vertical_spacer)


        self.main_frame_horizontal_layout.addWidget(self.left_bar_frame)

        self.text_frame = QFrame(self.main_frame)
        self.text_frame.setObjectName(u"text_frame")
        self.text_frame.setFrameShape(QFrame.StyledPanel)
        self.text_frame.setFrameShadow(QFrame.Raised)
        self.text_frame_vertical_layout = QVBoxLayout(self.text_frame)
        self.text_frame_vertical_layout.setSpacing(0)
        self.text_frame_vertical_layout.setObjectName(u"text_frame_vertical_layout")
        self.text_frame_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.main_frame_horizontal_layout.addWidget(self.text_frame)


        self.main_vertical_layout.addWidget(self.main_frame)


        self.retranslateUi(TextItem)

        QMetaObject.connectSlotsByName(TextItem)
    # setupUi

    def retranslateUi(self, TextItem):
        TextItem.setWindowTitle(QCoreApplication.translate("TextItem", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0431\u043b\u043e\u043a\u0430 \u0442\u0435\u043a\u0441\u0442\u0430", None))
        self.text_caption.setText(QCoreApplication.translate("TextItem", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a", None))
#if QT_CONFIG(tooltip)
        self.edit_button.setToolTip(QCoreApplication.translate("TextItem", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043a\u0430\u043a HTML", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.update_button.setToolTip(QCoreApplication.translate("TextItem", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0432\u0438\u0434", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.del_button.setToolTip(QCoreApplication.translate("TextItem", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

