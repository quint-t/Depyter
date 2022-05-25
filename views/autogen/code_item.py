# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'code_item.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
from  . import resources_rc

class Ui_CodeItem(object):
    def setupUi(self, CodeItem):
        if not CodeItem.objectName():
            CodeItem.setObjectName(u"CodeItem")
        CodeItem.resize(500, 200)
        icon = QIcon()
        icon.addFile(u":/icons/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        CodeItem.setWindowIcon(icon)
        self.main_vertical_layout = QVBoxLayout(CodeItem)
        self.main_vertical_layout.setSpacing(0)
        self.main_vertical_layout.setObjectName(u"main_vertical_layout")
        self.main_vertical_layout.setContentsMargins(3, 3, 3, 3)
        self.code_caption = QLineEdit(CodeItem)
        self.code_caption.setObjectName(u"code_caption")
        font = QFont()
        font.setPointSize(12)
        self.code_caption.setFont(font)
        self.code_caption.setStyleSheet(u"background-color: rgba(255, 255, 255, 10);")
        self.code_caption.setFrame(False)
        self.code_caption.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.main_vertical_layout.addWidget(self.code_caption)

        self.main_frame = QFrame(CodeItem)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame_horizontal_layout = QHBoxLayout(self.main_frame)
        self.main_frame_horizontal_layout.setSpacing(0)
        self.main_frame_horizontal_layout.setObjectName(u"main_frame_horizontal_layout")
        self.main_frame_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.left_bar_frame = QFrame(self.main_frame)
        self.left_bar_frame.setObjectName(u"left_bar_frame")
        self.left_bar_frame.setMinimumSize(QSize(50, 0))
        self.left_bar_frame.setMaximumSize(QSize(50, 16777215))
        self.left_bar_frame.setFrameShape(QFrame.StyledPanel)
        self.left_bar_frame.setFrameShadow(QFrame.Raised)
        self.left_bar_frame_vertical_layout = QVBoxLayout(self.left_bar_frame)
        self.left_bar_frame_vertical_layout.setSpacing(0)
        self.left_bar_frame_vertical_layout.setObjectName(u"left_bar_frame_vertical_layout")
        self.left_bar_frame_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.indicator_label = QLabel(self.left_bar_frame)
        self.indicator_label.setObjectName(u"indicator_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.indicator_label.sizePolicy().hasHeightForWidth())
        self.indicator_label.setSizePolicy(sizePolicy)
        self.indicator_label.setMinimumSize(QSize(0, 20))
        self.indicator_label.setFont(font)
        self.indicator_label.setAlignment(Qt.AlignCenter)

        self.left_bar_frame_vertical_layout.addWidget(self.indicator_label)

        self.start_button = QPushButton(self.left_bar_frame)
        self.start_button.setObjectName(u"start_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/run.png", QSize(), QIcon.Normal, QIcon.Off)
        self.start_button.setIcon(icon1)
        self.start_button.setIconSize(QSize(17, 17))

        self.left_bar_frame_vertical_layout.addWidget(self.start_button)

        self.stop_button = QPushButton(self.left_bar_frame)
        self.stop_button.setObjectName(u"stop_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/stop_execution.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_button.setIcon(icon2)
        self.stop_button.setIconSize(QSize(15, 15))

        self.left_bar_frame_vertical_layout.addWidget(self.stop_button)

        self.del_button = QPushButton(self.left_bar_frame)
        self.del_button.setObjectName(u"del_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.del_button.setIcon(icon3)
        self.del_button.setIconSize(QSize(15, 15))

        self.left_bar_frame_vertical_layout.addWidget(self.del_button)

        self.hide_show_output_button = QPushButton(self.left_bar_frame)
        self.hide_show_output_button.setObjectName(u"hide_show_output_button")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/output.png", QSize(), QIcon.Normal, QIcon.Off)
        self.hide_show_output_button.setIcon(icon4)
        self.hide_show_output_button.setIconSize(QSize(15, 15))
        self.hide_show_output_button.setCheckable(True)

        self.left_bar_frame_vertical_layout.addWidget(self.hide_show_output_button)

        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.left_bar_frame_vertical_layout.addItem(self.vertical_spacer)


        self.main_frame_horizontal_layout.addWidget(self.left_bar_frame)

        self.code_frame = QFrame(self.main_frame)
        self.code_frame.setObjectName(u"code_frame")
        self.code_frame.setFrameShape(QFrame.StyledPanel)
        self.code_frame.setFrameShadow(QFrame.Raised)
        self.code_frame_vertical_layout = QVBoxLayout(self.code_frame)
        self.code_frame_vertical_layout.setSpacing(0)
        self.code_frame_vertical_layout.setObjectName(u"code_frame_vertical_layout")
        self.code_frame_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.main_frame_horizontal_layout.addWidget(self.code_frame)


        self.main_vertical_layout.addWidget(self.main_frame)

        self.output_frame = QFrame(CodeItem)
        self.output_frame.setObjectName(u"output_frame")
        self.output_frame.setFrameShape(QFrame.StyledPanel)
        self.output_frame.setFrameShadow(QFrame.Raised)
        self.output_frame_vertical_layout = QVBoxLayout(self.output_frame)
        self.output_frame_vertical_layout.setSpacing(0)
        self.output_frame_vertical_layout.setObjectName(u"output_frame_vertical_layout")
        self.output_frame_vertical_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.output_frame_vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.main_vertical_layout.addWidget(self.output_frame)

        self.main_vertical_layout.setStretch(2, 1)

        self.retranslateUi(CodeItem)

        QMetaObject.connectSlotsByName(CodeItem)
    # setupUi

    def retranslateUi(self, CodeItem):
        CodeItem.setWindowTitle(QCoreApplication.translate("CodeItem", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0431\u043b\u043e\u043a\u0430 \u043a\u043e\u0434\u0430", None))
        self.code_caption.setText(QCoreApplication.translate("CodeItem", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a", None))
        self.indicator_label.setText(QCoreApplication.translate("CodeItem", u"[]", None))
#if QT_CONFIG(tooltip)
        self.start_button.setToolTip(QCoreApplication.translate("CodeItem", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.stop_button.setToolTip(QCoreApplication.translate("CodeItem", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.del_button.setToolTip(QCoreApplication.translate("CodeItem", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.hide_show_output_button.setToolTip(QCoreApplication.translate("CodeItem", u"\u0421\u043a\u0440\u044b\u0442\u044c/\u043f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0432\u044b\u0432\u043e\u0434", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

