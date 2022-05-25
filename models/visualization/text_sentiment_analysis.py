# template-name: Анализ тональности текста
# template-type: Классификация текста
# <code-block> Text Sentiment Analysis Visualization Instrument
import sys

import numpy as np
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow,
                               QPlainTextEdit, QPushButton, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 250)
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.analyze_button = QPushButton(self.centralwidget)
        self.analyze_button.setObjectName(u"analyze_button")
        self.analyze_button.setGeometry(QRect(10, 150, 381, 31))
        self.input_text_edit = QPlainTextEdit(self.centralwidget)
        self.input_text_edit.setObjectName(u"input_text_edit")
        self.input_text_edit.setGeometry(QRect(10, 10, 381, 131))
        self.result_label = QLabel(self.centralwidget)
        self.result_label.setObjectName(u"result_label")
        self.result_label.setGeometry(QRect(70, 190, 141, 20))
        self.score_label = QLabel(self.centralwidget)
        self.score_label.setObjectName(u"score_label")
        self.score_label.setGeometry(QRect(70, 220, 141, 20))
        self.result_line_edit = QLineEdit(self.centralwidget)
        self.result_line_edit.setObjectName(u"result_line_edit")
        self.result_line_edit.setGeometry(QRect(210, 190, 141, 20))
        self.score_line_edit = QLineEdit(self.centralwidget)
        self.score_line_edit.setObjectName(u"score_line_edit")
        self.score_line_edit.setGeometry(QRect(210, 220, 141, 20))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Анализ тональности текста", None))
        self.analyze_button.setText(QCoreApplication.translate("MainWindow", "Анализ тональности", None))
        self.result_label.setText(QCoreApplication.translate("MainWindow", "Результат:", None))
        self.score_label.setText(QCoreApplication.translate("MainWindow", "Значение:", None))
    # retranslateUi


class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.analyze_button.clicked.connect(self.analyze_slot)

    @QtCore.Slot()
    def analyze_slot(self):
        global model
        text = self.ui.input_text_edit.toPlainText()
        prediction = model.predict(np.array([text]))[0][0]
        self.ui.result_line_edit.setText('POSITIVE' if prediction >= 0 else 'NEGATIVE')
        self.ui.score_line_edit.setText(str(prediction))


if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()
window1, window2 = ExampleWindow(), ExampleWindow()
window1.show()
window2.show()
app.exec()
