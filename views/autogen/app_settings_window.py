# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_settings_window.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFontComboBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)
from  . import resources_rc

class Ui_AppSettings(object):
    def setupUi(self, AppSettings):
        if not AppSettings.objectName():
            AppSettings.setObjectName(u"AppSettings")
        AppSettings.resize(450, 152)
        icon = QIcon()
        icon.addFile(u":/icons/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        AppSettings.setWindowIcon(icon)
        self.centralwidget = QWidget(AppSettings)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption_font_widget = QWidget(self.centralwidget)
        self.caption_font_widget.setObjectName(u"caption_font_widget")
        self.caption_font_widget_horizontal_layout = QHBoxLayout(self.caption_font_widget)
        self.caption_font_widget_horizontal_layout.setSpacing(5)
        self.caption_font_widget_horizontal_layout.setObjectName(u"caption_font_widget_horizontal_layout")
        self.caption_font_widget_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.caption_font_label = QLabel(self.caption_font_widget)
        self.caption_font_label.setObjectName(u"caption_font_label")
        self.caption_font_label.setMinimumSize(QSize(140, 0))

        self.caption_font_widget_horizontal_layout.addWidget(self.caption_font_label)

        self.caption_font_combo_box = QFontComboBox(self.caption_font_widget)
        self.caption_font_combo_box.setObjectName(u"caption_font_combo_box")
        font = QFont()
        self.caption_font_combo_box.setCurrentFont(font)

        self.caption_font_widget_horizontal_layout.addWidget(self.caption_font_combo_box)

        self.caption_font_spin_box = QSpinBox(self.caption_font_widget)
        self.caption_font_spin_box.setObjectName(u"caption_font_spin_box")
        self.caption_font_spin_box.setMinimumSize(QSize(50, 0))
        self.caption_font_spin_box.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.caption_font_spin_box.setMinimum(6)
        self.caption_font_spin_box.setMaximum(28)
        self.caption_font_spin_box.setValue(14)

        self.caption_font_widget_horizontal_layout.addWidget(self.caption_font_spin_box)

        self.caption_font_widget_horizontal_layout.setStretch(1, 1)

        self.verticalLayout.addWidget(self.caption_font_widget)

        self.text_font_widget = QWidget(self.centralwidget)
        self.text_font_widget.setObjectName(u"text_font_widget")
        self.text_font_widget_horizontal_layout = QHBoxLayout(self.text_font_widget)
        self.text_font_widget_horizontal_layout.setSpacing(5)
        self.text_font_widget_horizontal_layout.setObjectName(u"text_font_widget_horizontal_layout")
        self.text_font_widget_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.text_font_label = QLabel(self.text_font_widget)
        self.text_font_label.setObjectName(u"text_font_label")
        self.text_font_label.setMinimumSize(QSize(140, 0))

        self.text_font_widget_horizontal_layout.addWidget(self.text_font_label)

        self.text_font_combo_box = QFontComboBox(self.text_font_widget)
        self.text_font_combo_box.setObjectName(u"text_font_combo_box")
        self.text_font_combo_box.setCurrentFont(font)

        self.text_font_widget_horizontal_layout.addWidget(self.text_font_combo_box)

        self.text_font_spin_box = QSpinBox(self.text_font_widget)
        self.text_font_spin_box.setObjectName(u"text_font_spin_box")
        self.text_font_spin_box.setMinimumSize(QSize(50, 0))
        self.text_font_spin_box.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.text_font_spin_box.setMinimum(6)
        self.text_font_spin_box.setMaximum(28)
        self.text_font_spin_box.setValue(12)

        self.text_font_widget_horizontal_layout.addWidget(self.text_font_spin_box)

        self.text_font_widget_horizontal_layout.setStretch(1, 1)

        self.verticalLayout.addWidget(self.text_font_widget)

        self.code_font_widget = QWidget(self.centralwidget)
        self.code_font_widget.setObjectName(u"code_font_widget")
        self.code_font_widget_horizontal_layout = QHBoxLayout(self.code_font_widget)
        self.code_font_widget_horizontal_layout.setSpacing(5)
        self.code_font_widget_horizontal_layout.setObjectName(u"code_font_widget_horizontal_layout")
        self.code_font_widget_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.code_font_label = QLabel(self.code_font_widget)
        self.code_font_label.setObjectName(u"code_font_label")
        self.code_font_label.setMinimumSize(QSize(140, 0))

        self.code_font_widget_horizontal_layout.addWidget(self.code_font_label)

        self.code_font_combo_box = QFontComboBox(self.code_font_widget)
        self.code_font_combo_box.setObjectName(u"code_font_combo_box")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(12)
        self.code_font_combo_box.setCurrentFont(font1)

        self.code_font_widget_horizontal_layout.addWidget(self.code_font_combo_box)

        self.code_font_spin_box = QSpinBox(self.code_font_widget)
        self.code_font_spin_box.setObjectName(u"code_font_spin_box")
        self.code_font_spin_box.setMinimumSize(QSize(50, 0))
        self.code_font_spin_box.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.code_font_spin_box.setMinimum(6)
        self.code_font_spin_box.setMaximum(28)
        self.code_font_spin_box.setValue(12)

        self.code_font_widget_horizontal_layout.addWidget(self.code_font_spin_box)

        self.code_font_widget_horizontal_layout.setStretch(1, 1)

        self.verticalLayout.addWidget(self.code_font_widget)

        self.reload_settings_button = QPushButton(self.centralwidget)
        self.reload_settings_button.setObjectName(u"reload_settings_button")

        self.verticalLayout.addWidget(self.reload_settings_button)

        self.gc_collect_button = QPushButton(self.centralwidget)
        self.gc_collect_button.setObjectName(u"gc_collect_button")

        self.verticalLayout.addWidget(self.gc_collect_button)

        self.main_buttons_widget = QWidget(self.centralwidget)
        self.main_buttons_widget.setObjectName(u"main_buttons_widget")
        self.main_buttons_widget_horizontal_layout = QHBoxLayout(self.main_buttons_widget)
        self.main_buttons_widget_horizontal_layout.setSpacing(5)
        self.main_buttons_widget_horizontal_layout.setObjectName(u"main_buttons_widget_horizontal_layout")
        self.main_buttons_widget_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.apply_button = QPushButton(self.main_buttons_widget)
        self.apply_button.setObjectName(u"apply_button")

        self.main_buttons_widget_horizontal_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton(self.main_buttons_widget)
        self.cancel_button.setObjectName(u"cancel_button")

        self.main_buttons_widget_horizontal_layout.addWidget(self.cancel_button)

        self.main_buttons_widget_horizontal_layout.setStretch(0, 1)

        self.verticalLayout.addWidget(self.main_buttons_widget)

        AppSettings.setCentralWidget(self.centralwidget)

        self.retranslateUi(AppSettings)

        self.apply_button.setDefault(True)


        QMetaObject.connectSlotsByName(AppSettings)
    # setupUi

    def retranslateUi(self, AppSettings):
        AppSettings.setWindowTitle(QCoreApplication.translate("AppSettings", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f", None))
        self.caption_font_label.setText(QCoreApplication.translate("AppSettings", u"\u0428\u0440\u0438\u0444\u0442 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u043e\u0432:", None))
        self.caption_font_combo_box.setCurrentText(QCoreApplication.translate("AppSettings", u"Segoe UI", None))
        self.text_font_label.setText(QCoreApplication.translate("AppSettings", u"\u0428\u0440\u0438\u0444\u0442 \u0431\u043b\u043e\u043a\u043e\u0432 \u0442\u0435\u043a\u0441\u0442\u0430:", None))
        self.text_font_combo_box.setCurrentText(QCoreApplication.translate("AppSettings", u"Segoe UI", None))
        self.code_font_label.setText(QCoreApplication.translate("AppSettings", u"\u0428\u0440\u0438\u0444\u0442 \u0431\u043b\u043e\u043a\u043e\u0432 \u043a\u043e\u0434\u0430:", None))
        self.code_font_combo_box.setCurrentText(QCoreApplication.translate("AppSettings", u"Arial", None))
        self.reload_settings_button.setText(QCoreApplication.translate("AppSettings", u"\u041f\u0435\u0440\u0435\u0447\u0438\u0442\u0430\u0442\u044c \u0444\u0430\u0439\u043b \u043d\u0430\u0441\u0442\u0440\u043e\u0435\u043a settings.ini", None))
        self.gc_collect_button.setText(QCoreApplication.translate("AppSettings", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u043d\u0435\u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c\u0443\u044e \u043f\u0430\u043c\u044f\u0442\u044c", None))
        self.apply_button.setText(QCoreApplication.translate("AppSettings", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.cancel_button.setText(QCoreApplication.translate("AppSettings", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

