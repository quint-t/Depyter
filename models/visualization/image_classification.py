# template-name: Загрузка изображения из Интернета
# template-name: и его классификация
# template-type: Классификация изображений
# <code-block> Image Classification Visualization Instrument
import os
import sys

import numpy as np
import tensorflow as tf
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow,
                               QPushButton, QWidget)


class Ui_ExampleWindow(object):
    def setupUi(self, ExampleWindow):
        if not ExampleWindow.objectName():
            ExampleWindow.setObjectName(u"ExampleWindow")
        ExampleWindow.resize(410, 240)
        self.centralwidget = QWidget(ExampleWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphics_label = QLabel(self.centralwidget)
        self.graphics_label.setObjectName(u"graphics_label")
        self.graphics_label.setGeometry(QRect(10, 40, 251, 192))
        self.url_line_edit = QLineEdit(self.centralwidget)
        self.url_line_edit.setObjectName(u"url_line_edit")
        self.url_line_edit.setGeometry(QRect(10, 10, 251, 20))
        self.load_button = QPushButton(self.centralwidget)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setGeometry(QRect(270, 10, 131, 21))
        self.classify_button = QPushButton(self.centralwidget)
        self.classify_button.setObjectName(u"classify_button")
        self.classify_button.setGeometry(QRect(270, 40, 131, 21))
        self.result_line_edit = QLineEdit(self.centralwidget)
        self.result_line_edit.setObjectName(u"result_line_edit")
        self.result_line_edit.setGeometry(QRect(270, 70, 131, 21))
        self.score_line_edit = QLineEdit(self.centralwidget)
        self.score_line_edit.setObjectName(u"score_line_edit")
        self.score_line_edit.setGeometry(QRect(270, 100, 131, 21))
        ExampleWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ExampleWindow)

        QMetaObject.connectSlotsByName(ExampleWindow)

    # setupUi

    def retranslateUi(self, ExampleWindow):
        self.load_button.setText(QCoreApplication.translate("ExampleWindow", "Загрузить", None))
        self.classify_button.setText(QCoreApplication.translate("ExampleWindow", "Классифицировать", None))
        pass
    # retranslateUi


class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ExampleWindow()
        self.ui.setupUi(self)
        self.ui.load_button.clicked.connect(self.load_slot)
        self.ui.classify_button.clicked.connect(self.classify_slot)
        self.ui.url_line_edit.setText(
            "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg")
        self._image_array = None

    @QtCore.Slot()
    def load_slot(self):
        global img_height, img_width
        image_url = self.ui.url_line_edit.text()
        image_path = tf.keras.utils.get_file('example_file', origin=image_url)
        os.remove(image_path)
        image_path = tf.keras.utils.get_file('example_file', origin=image_url)
        img = QtGui.QImage(image_path)
        img = img.scaled(self.ui.graphics_label.width(), self.ui.graphics_label.height(), QtCore.Qt.KeepAspectRatio)
        self.ui.graphics_label.clear()
        self.ui.graphics_label.setPixmap(QtGui.QPixmap.fromImage(img))
        img = tf.keras.utils.load_img(
            image_path, target_size=(img_height, img_width)
        )
        self._image_array = tf.keras.utils.img_to_array(img)
        self._image_array = tf.expand_dims(self._image_array, 0)  # Create a batch

    @QtCore.Slot()
    def classify_slot(self):
        global class_names
        if self._image_array is None:
            return
        predictions = model.predict(self._image_array)
        score = tf.nn.softmax(predictions[0])
        self.ui.result_line_edit.setText(class_names[np.argmax(score)])
        self.ui.score_line_edit.setText(str(100 * np.max(score)))


if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()
window = ExampleWindow()
window.show()
app.exec()
