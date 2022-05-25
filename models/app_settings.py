import configparser
import sys
from copy import copy

from PySide6 import QtGui, QtCore, QtWidgets


class AppSettings(QtCore.QObject):
    width_signal = QtCore.Signal(int)
    height_signal = QtCore.Signal(int)
    style_signal = QtCore.Signal(str)
    maximized_signal = QtCore.Signal(bool)
    code_block_font_signal = QtCore.Signal(QtGui.QFont)
    text_block_font_signal = QtCore.Signal(QtGui.QFont)
    caption_font_signal = QtCore.Signal(QtGui.QFont)

    c_main_settings = 'MainWindow-Settings'
    c_width = 'width'
    c_height = 'height'
    c_style = 'style'
    c_maximized = 'maximized'

    c_font_settings = 'Font-Settings'
    c_caption_font_family = 'caption-font-family'
    c_caption_font_size = 'caption-font-size'
    c_text_block_font_family = 'text-block-font-family'
    c_text_block_font_size = 'text-block-font-size'
    c_code_block_font_family = 'code-block-font-family'
    c_code_block_font_size = 'code-block-font-size'

    def __init__(self, config_file: str = None):
        super().__init__(parent=None)
        # default main settings
        self._width = 800
        self._height = 600
        self._style = ''
        self._maximized = False

        # default font settings
        self._code_font = QtGui.QFont('Consolas', 12)
        self._text_font = QtGui.QFont('Segoe UI', 12)
        self._caption_font = QtGui.QFont('Segoe UI', 14)

        # load settings from config file
        self.config_file = config_file
        self.load_settings_from_config_file(filename=self.config_file)

    def load_settings_from_config_file(self, filename: str,
                                       ignore_main_window_settings: bool = False):
        if filename is None:
            return
        self.config_file = filename
        try:
            config = configparser.ConfigParser()
            config.read(filename)
            # main_settings
            if self.c_main_settings in config:
                if self.c_width in config[self.c_main_settings] \
                        and config[self.c_main_settings][self.c_width].isdigit() and not ignore_main_window_settings:
                    self._width = int(config[self.c_main_settings][self.c_width])
                self.width_signal.emit(self._width)
                if self.c_height in config[self.c_main_settings] \
                        and config[self.c_main_settings][self.c_width].isdigit() and not ignore_main_window_settings:
                    self._height = int(config[self.c_main_settings][self.c_height])
                self.height_signal.emit(self._height)
                if self.c_style in config[self.c_main_settings]:
                    style = config[self.c_main_settings][self.c_style].lower()
                    all_styles = QtWidgets.QStyleFactory.keys()
                    print('All windows styles:', list(all_styles), file=sys.stderr)
                    founded_style = next((x for x in all_styles if style == x.lower()), None)
                    if founded_style is not None:
                        self._style = founded_style
                        self.style_signal.emit(founded_style)
                self.style_signal.emit(self._style)
                if self.c_maximized in config[self.c_main_settings] and not ignore_main_window_settings:
                    self._maximized = (config[self.c_main_settings][self.c_maximized].lower() == 'true')
                self.maximized_signal.emit(self._maximized)
            # font_settings
            if self.c_font_settings in config:
                # self._caption_font
                if self.c_caption_font_family in config[self.c_font_settings]:
                    self._caption_font.setFamily(config[self.c_font_settings][self.c_caption_font_family])
                if self.c_caption_font_size in config[self.c_font_settings] \
                        and config[self.c_font_settings][self.c_caption_font_size].isdigit():
                    point_size = max(6, min(28, int(config[self.c_font_settings][self.c_caption_font_size])))
                    self._caption_font.setPointSize(point_size)
                self.caption_font_signal.emit(self._caption_font)
                # self._text_font
                if self.c_text_block_font_family in config[self.c_font_settings]:
                    self._text_font.setFamily(config[self.c_font_settings][self.c_text_block_font_family])
                if self.c_text_block_font_size in config[self.c_font_settings] \
                        and config[self.c_font_settings][self.c_text_block_font_size].isdigit():
                    point_size = max(6, min(28, int(config[self.c_font_settings][self.c_text_block_font_size])))
                    self._text_font.setPointSize(point_size)
                self.text_block_font_signal.emit(self._text_font)
                # self._code_font
                if self.c_code_block_font_family in config[self.c_font_settings]:
                    self._code_font.setFamily(config[self.c_font_settings][self.c_code_block_font_family])
                if self.c_code_block_font_size in config[self.c_font_settings] \
                        and config[self.c_font_settings][self.c_code_block_font_size].isdigit():
                    point_size = max(6, min(28, int(config[self.c_font_settings][self.c_code_block_font_size])))
                    self._code_font.setPointSize(point_size)
                self.code_block_font_signal.emit(self._code_font)
        except:
            __import__('traceback').print_exc()

    def save_settings_to_config_file(self, filename):
        if filename is None:
            return
        self.config_file = filename
        try:
            config = configparser.ConfigParser()
            # main_settings
            config.add_section(self.c_main_settings)
            config.set(self.c_main_settings, self.c_width, str(self._width))
            config.set(self.c_main_settings, self.c_height, str(self._height))
            config.set(self.c_main_settings, self.c_style, self._style)
            config.set(self.c_main_settings, self.c_maximized, str(self._maximized))
            # font_settings
            config.add_section(self.c_font_settings)
            config.set(self.c_font_settings, self.c_caption_font_family, self._caption_font.family())
            config.set(self.c_font_settings, self.c_caption_font_size, str(self._caption_font.pointSize()))
            config.set(self.c_font_settings, self.c_text_block_font_family, self._text_font.family())
            config.set(self.c_font_settings, self.c_text_block_font_size, str(self._text_font.pointSize()))
            config.set(self.c_font_settings, self.c_code_block_font_family, self._code_font.family())
            config.set(self.c_font_settings, self.c_code_block_font_size, str(self._code_font.pointSize()))
            with open(filename, mode='w', encoding='utf-8') as fp:
                config.write(fp)
        except:
            __import__('traceback').print_exc()

    @property
    def width(self) -> int:
        return self._width  # int is non-mutable type

    @property
    def height(self) -> int:
        return self._height  # int is non-mutable type

    @property
    def style(self) -> str:
        return self._style  # string is non-mutable type

    @property
    def maximized(self) -> bool:
        return self._maximized  # bool is non-mutable type

    @property
    def code_font(self) -> QtGui.QFont:
        return copy(self._code_font)

    @property
    def text_font(self) -> QtGui.QFont:
        return copy(self._text_font)

    @property
    def caption_font(self) -> QtGui.QFont:
        return copy(self._caption_font)

    @width.setter
    def width(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'AppSettings.width.arg: {value}')
        self._width = max(100, min(2000, value))
        self.width_signal.emit(self._width)

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'AppSettings.height.arg: {value}')
        self._height = max(100, min(2000, value))
        self.height_signal.emit(self._height)

    @style.setter
    def style(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'AppSettings.style.arg: {value}')
        self._style = value
        self.style_signal.emit(self._style)

    @maximized.setter
    def maximized(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f'AppSettings.value.arg: {value}')
        self._maximized = value
        self.maximized_signal.emit(self._maximized)

    @code_font.setter
    def code_font(self, font: QtGui.QFont):
        if not isinstance(font, QtGui.QFont):
            raise TypeError(f'AppSettings.code_font.arg: {font}')
        self._code_font = font
        self.code_block_font_signal.emit(self._code_font)

    @text_font.setter
    def text_font(self, font: QtGui.QFont):
        if not isinstance(font, QtGui.QFont):
            raise TypeError(f'AppSettings.text_font.arg: {font}')
        self._text_font = font
        self.text_block_font_signal.emit(self._text_font)

    @caption_font.setter
    def caption_font(self, font: QtGui.QFont):
        if not isinstance(font, QtGui.QFont):
            raise TypeError(f'AppSettings.caption_font.arg: {font}')
        self._caption_font = font
        self.caption_font_signal.emit(self._caption_font)

    def get_settings(self):
        return {
            'width': copy(self.width),
            'height': copy(self.height),
            'style': copy(self.style),
            'maximized': copy(self.maximized),
            'code_font': copy(self.code_font),
            'text_font': copy(self.text_font),
            'caption_font': copy(self.caption_font)
        }

    def set_settings(self, d: dict, ignore_main_window_settings: bool):
        if not ignore_main_window_settings:
            self.width = copy(d.get('width', self.width))
            self.height = copy(d.get('height', self.height))
            self.maximized = copy(d.get('maximized', self.maximized))
        self.style = copy(d.get('style', self.style))
        self.code_font = copy(d.get('code_font', self.code_font))
        self.text_font = copy(d.get('text_font', self.text_font))
        self.caption_font = copy(d.get('caption_font', self.caption_font))
        if not ignore_main_window_settings:
            self.width_signal.emit(self._width)
            self.height_signal.emit(self._height)
            self.maximized_signal.emit(self._maximized)
        self.style_signal.emit(self._style)
        self.code_block_font_signal.emit(self._code_font)
        self.text_block_font_signal.emit(self._text_font)
        self.caption_font_signal.emit(self._caption_font)
