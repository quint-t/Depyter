import os
import sys
from typing import List

from PySide6 import QtWidgets, QtCore, QtGui

from views.mainwindow import MainWindow


class Application(QtWidgets.QApplication):
    def __init__(self, sys_argv: List[str], config_file: str):
        super().__init__(sys_argv)
        self.setFont(QtGui.QFont('Segoe UI', 10))
        self.setQuitOnLastWindowClosed(False)
        self.config_file = config_file
        self.main_window = MainWindow()
        self.main_window.update_style.connect(self._update_style)
        self.main_window.load_settings_from_config_file_slot(config_file=self.config_file)
        self.main_window.main_close_signal.connect(self.exit_program)
        self.main_window.show()

    @QtCore.Slot(str)
    def _update_style(self, style: str):
        self.setStyle(style)

    @QtCore.Slot()
    def exit_program(self):
        self.main_window.save_settings_to_config_file_slot(config_file=self.config_file)
        self.quit()


def main():
    config_file = os.path.join(os.path.curdir, 'settings.ini')
    app = Application(sys_argv=sys.argv, config_file=config_file)
    exit(app.exec())


if __name__ == "__main__":
    main()
