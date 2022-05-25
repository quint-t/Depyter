import gc

from PySide6 import QtWidgets, QtCore, QtGui

from models.app_settings import AppSettings
from views.autogen.app_settings_window import Ui_AppSettings


class AppSettingsWindow(QtWidgets.QMainWindow):
    code_block_font_changed_signal = QtCore.Signal(QtGui.QFont)
    text_block_font_changed_signal = QtCore.Signal(QtGui.QFont)
    caption_font_changed_signal = QtCore.Signal(QtGui.QFont)

    def __init__(self, config_file: str = None):
        super().__init__()
        self.ui = Ui_AppSettings()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.app_settings = AppSettings(config_file=config_file)
        self.ui.apply_button.clicked.connect(self.apply)
        self.ui.cancel_button.clicked.connect(self.cancel)
        self.ui.reload_settings_button.clicked.connect(self.reload_settings)
        self.ui.gc_collect_button.clicked.connect(self._gc_collect)
        self._from_model_to_ui()
        self._last_settings = self.app_settings.get_settings()

    def show(self):
        self._last_settings = self.app_settings.get_settings()
        super().show()

    def apply(self):
        self._from_ui_to_model()
        self.close()

    def cancel(self):
        self.app_settings.set_settings(self._last_settings, ignore_main_window_settings=True)
        self._from_model_to_ui()
        self.close()

    def _from_model_to_ui(self):
        # combo box
        self.ui.code_font_combo_box.setCurrentFont(self.app_settings.code_font)
        self.ui.text_font_combo_box.setCurrentFont(self.app_settings.text_font)
        self.ui.caption_font_combo_box.setCurrentFont(self.app_settings.caption_font)
        # spin box
        self.ui.code_font_spin_box.setValue(self.app_settings.code_font.pointSize())
        self.ui.text_font_spin_box.setValue(self.app_settings.text_font.pointSize())
        self.ui.caption_font_spin_box.setValue(self.app_settings.caption_font.pointSize())
        self._emit_ui_signals_for_updating()

    def _from_ui_to_model(self):
        self.app_settings.code_font = QtGui.QFont(self.ui.code_font_combo_box.currentFont().family(),
                                                  self.ui.code_font_spin_box.value())
        self.app_settings.text_font = QtGui.QFont(self.ui.text_font_combo_box.currentFont().family(),
                                                  self.ui.text_font_spin_box.value())
        self.app_settings.caption_font = QtGui.QFont(self.ui.caption_font_combo_box.currentFont().family(),
                                                     self.ui.caption_font_spin_box.value())
        self._emit_ui_signals_for_updating()

    def _emit_ui_signals_for_updating(self):
        self.code_block_font_changed_signal.emit(self.app_settings.code_font)
        self.text_block_font_changed_signal.emit(self.app_settings.text_font)
        self.caption_font_changed_signal.emit(self.app_settings.caption_font)

    def load_settings_from_config_file(self, config_file: str):
        self.app_settings.load_settings_from_config_file(filename=config_file)
        self._from_model_to_ui()
        self._last_settings = self.app_settings.get_settings()

    def save_settings_to_config_file(self, config_file: str):
        self.app_settings.save_settings_to_config_file(filename=config_file)

    @QtCore.Slot()
    def reload_settings(self):
        self.app_settings.load_settings_from_config_file(filename=self.app_settings.config_file)
        self._from_model_to_ui()

    @staticmethod
    def _gc_collect():
        gc.disable()
        n = gc.collect()
        gc.enable()
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                              'Очистка неиспользуемой памяти',
                              f'Удалено объектов: {n}',
                              QtWidgets.QMessageBox.Ok).exec()
