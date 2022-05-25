import re
from typing import Union, Sequence

from PySide6 import QtCore, QtWidgets, QtGui

from views.autogen.code_item import Ui_CodeItem
from views.code_highlighter import CodeHighlighter


class CodeTextBox(QtWidgets.QTextEdit):
    font_changed = QtCore.Signal()

    spaces = ' ' * 4
    n_spaces = len(spaces)

    def __init__(self, parent: Union[QtWidgets.QWidget, None], code: str = ''):
        super().__init__(parent=parent)
        self.sizePolicy().setHorizontalStretch(1)
        self.setAcceptRichText(False)
        self.highlighter = CodeHighlighter(self)
        self.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.setPlainText(code)
        self.setTabStopDistance(35)
        self.startswith_add_indent = \
            re.compile(r'\b(async def|def|class|if|elif|else|try|except|finally|for|while|with|match|case)\b')
        self.startswith_del_indent = \
            re.compile(r'\b(break|continue|raise|return|pass)\b')
        self.setFont(self.font())

    def setFont(self, font: Union[QtGui.QFont, str, Sequence[str]]) -> None:
        super().setFont(font)
        self.font_changed.emit()

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        text_cursor = self.textCursor()
        has_selection = text_cursor.hasSelection()
        e_text = e.text()
        # Tab (Indent)
        if e.key() == QtGui.Qt.Key_Tab:
            text_cursor.beginEditBlock()

            if not has_selection:
                text_cursor.insertText(self.spaces[text_cursor.positionInBlock() % self.n_spaces:])
                text_cursor.endEditBlock()
                return

            start_block = self.document().findBlock(text_cursor.selectionStart())
            end_block = self.document().findBlock(text_cursor.selectionEnd())
            text_cursor.setPosition(start_block.position())
            text_cursor.setPosition(end_block.position() + end_block.length() - 1, QtGui.QTextCursor.KeepAnchor)

            text = text_cursor.selectedText()
            text_length = len(text)
            start = text_cursor.selectionStart()
            end = text_cursor.selectionEnd()
            lines = []
            for line in text.splitlines():
                not_space_pos = next((i for i, x in enumerate(start_block.text()) if not x.isspace()), 0)
                lines.append(self.spaces[not_space_pos % self.n_spaces:] + line)
            text = '\n'.join(lines)
            text_cursor.removeSelectedText()
            text_cursor.insertText(text)
            text_cursor.setPosition(start)
            text_cursor.setPosition(end + len(text) - text_length, QtGui.QTextCursor.KeepAnchor)
            text_cursor.endEditBlock()
            self.setTextCursor(text_cursor)
            return
        # BackTab (Dedent)
        if e.key() == QtGui.Qt.Key_Backtab:
            text_cursor.beginEditBlock()

            if not has_selection:
                block = text_cursor.block()
                block_position = block.position()
                text_cursor.setPosition(block_position)
                not_space_pos = next((i for i, x in enumerate(block.text()) if not x.isspace()), block.length() - 1)
                text_cursor.setPosition(block_position + not_space_pos, QtGui.QTextCursor.KeepAnchor)
                text_cursor.removeSelectedText()
                text_cursor.insertText(self.spaces * ((not_space_pos - 1) // self.n_spaces))
                text_cursor.endEditBlock()
                self.setTextCursor(text_cursor)
                return

            start_block = self.document().findBlock(text_cursor.selectionStart())
            end_block = self.document().findBlock(text_cursor.selectionEnd())
            text_cursor.setPosition(start_block.position())
            text_cursor.setPosition(end_block.position() + end_block.length() - 1, QtGui.QTextCursor.KeepAnchor)
            text = text_cursor.selectedText()
            text_length = len(text)
            start = text_cursor.selectionStart()
            end = text_cursor.selectionEnd()
            lines = []
            for line in text.splitlines():
                not_space_pos = next((i for i, x in enumerate(line) if not x.isspace()), len(line))
                lines.append(self.spaces * ((not_space_pos - 1) // self.n_spaces) + line[not_space_pos:])
            text = '\n'.join(lines)
            text_cursor.removeSelectedText()
            text_cursor.insertText(text)
            text_cursor.setPosition(start)
            text_cursor.setPosition(end + len(text) - text_length, QtGui.QTextCursor.KeepAnchor)
            text_cursor.endEditBlock()
            self.setTextCursor(text_cursor)
            return
        # Ctrl+C & Ctrl+X
        if e.key() in (QtGui.Qt.Key_C, QtGui.Qt.Key_X) and e.modifiers() == QtGui.Qt.ControlModifier \
                and not has_selection:
            block = text_cursor.block()
            text_cursor.setPosition(block.position())
            text_cursor.setPosition(block.position() + block.length() -
                                    (block.blockNumber() == self.document().blockCount() - 1),
                                    QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(text_cursor)
            super().keyPressEvent(e)
            return
        # Ctrl+D
        if e.key() == QtGui.Qt.Key_D and e.modifiers() == QtGui.Qt.ControlModifier:
            text_cursor.beginEditBlock()
            if not has_selection:
                block = text_cursor.block()
                text_cursor.setPosition(block.position())
                text_cursor.setPosition(block.position() + block.length() -
                                        (block.blockNumber() == self.document().blockCount() - 1),
                                        QtGui.QTextCursor.KeepAnchor)
            end = text_cursor.selectionEnd()
            text = text_cursor.selectedText()
            text_cursor.setPosition(end)
            text_cursor.insertText(text)
            start = end
            end = text_cursor.position()
            text_cursor.setPosition(start)
            text_cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            text_cursor.endEditBlock()
            self.setTextCursor(text_cursor)
            return
        # Backspace
        if e.key() == QtGui.Qt.Key_Backspace and not has_selection:
            block = text_cursor.block()
            position = text_cursor.position()
            text_cursor.setPosition(block.position())
            text_cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
            text = text_cursor.selectedText()[::-1]
            if text and text[0] == self.spaces[0]:
                text_cursor.beginEditBlock()
                m1 = next((i for i, x in enumerate(text) if not x.isspace()), len(text))
                m2 = len(text) % 4 or 4
                text_cursor.setPosition(position)
                for i in range(min(m1, m2)):
                    text_cursor.deletePreviousChar()
                text_cursor.endEditBlock()
                self.setTextCursor(text_cursor)
                return
        # Ctrl+/
        elif e.key() == QtGui.Qt.Key_Slash and e.modifiers() == QtGui.Qt.ControlModifier:
            text_cursor.beginEditBlock()

            if not has_selection:
                block = text_cursor.block()
                block_text = block.text()
                not_space_idx = next((i for i, x in enumerate(block_text) if not x.isspace()), None)
                if not_space_idx is not None and block_text[not_space_idx] == '#':  # uncomment
                    text_cursor.setPosition(block.position() + not_space_idx)
                    text_cursor.deleteChar()
                    if not_space_idx + 1 < len(block_text) and block_text[not_space_idx + 1] == ' ':
                        text_cursor.deleteChar()
                    text_cursor.endEditBlock()
                    self.setTextCursor(text_cursor)
                    return

                # comment
                block_position = block.position()
                text_cursor.setPosition(block_position)
                not_space_pos = next((i for i, x in enumerate(block.text()) if not x.isspace()), block.length() - 1)
                text_cursor.setPosition(block_position + not_space_pos)
                text_cursor.insertText('# ')
                text_cursor.endEditBlock()
                self.setTextCursor(text_cursor)
                return

            start_block_position = self.document().findBlock(text_cursor.selectionStart()).position()
            end_block = self.document().findBlock(text_cursor.selectionEnd())
            text_cursor.setPosition(start_block_position)
            text_cursor.setPosition(end_block.position() + end_block.length() - 1, QtGui.QTextCursor.KeepAnchor)
            text = text_cursor.selectedText()
            lines = text.splitlines()
            new_lines = []
            for line in lines:
                not_space_idx = next((i for i, x in enumerate(line) if not x.isspace()), None)
                if not_space_idx is not None and line[not_space_idx] == '#':  # uncomment
                    one_space = int(not_space_idx + 1 < len(line) and line[not_space_idx + 1] == ' ')
                    new_line = line[:not_space_idx] + line[not_space_idx + 1 + one_space:]
                else:  # comment
                    new_line = '# ' + line
                new_lines.append(new_line)
            new_text = '\n'.join(new_lines)
            text_cursor.removeSelectedText()
            text_cursor.insertText(new_text)
            position = text_cursor.position()
            text_cursor.setPosition(start_block_position)
            text_cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
            text_cursor.endEditBlock()
            self.setTextCursor(text_cursor)
            return
        # Enter
        if e.key() == QtGui.Qt.Key_Return:
            block = text_cursor.block()
            if text_cursor.positionInBlock() + 1 == block.length():
                text_cursor.beginEditBlock()
                line = block.text()
                not_space_pos = next((i for i, x in enumerate(line) if not x.isspace()), len(line))
                source_indent = ((not_space_pos + self.n_spaces - 1) // self.n_spaces)
                add_indent = bool(self.startswith_add_indent.match(line[not_space_pos:]))
                del_indent = bool(self.startswith_del_indent.match(line[not_space_pos:]))
                text_cursor.insertText('\n' + self.spaces * (source_indent + add_indent - del_indent))
                text_cursor.endEditBlock()
                self.setTextCursor(text_cursor)
                return
        e = QtGui.QKeyEvent(e.type(),
                            e.key(),
                            e.modifiers(),
                            e_text)
        super().keyPressEvent(e)

    def insertPlainText(self, text: str) -> None:  # Ctrl+V
        if not text:
            return
        if text.isspace():
            self.textCursor().insertText(text.replace('\t', self.spaces))
            return
        text_cursor = self.textCursor()
        line = text_cursor.block().text()
        not_space_pos = next((i for i, x in enumerate(line) if not x.isspace()), len(line))
        prefix_indent = ((not_space_pos + self.n_spaces - 1) // self.n_spaces)
        # remove prefix
        lines = text.replace('\t', self.spaces).splitlines()

        new_lines = []
        common_indent = None
        for i, line in enumerate(lines):
            line_indent = next((i for i, x in enumerate(line) if not x.isspace()), len(line))
            indent = (line_indent + self.n_spaces - 1) // self.n_spaces
            if common_indent is None:
                common_indent = indent
            else:
                common_indent = min(common_indent, indent)
            new_lines.append((indent, line[line_indent:]))

        r_lines = []
        for i, (indent, line) in enumerate(new_lines):
            new_indent = indent - common_indent + prefix_indent * (i != 0)
            r_lines.append(self.spaces * new_indent + line)
        # add prefix
        text = '\n'.join(line.rstrip(' ') if not line.isspace() else line
                         for i, line in enumerate(r_lines))
        super().insertPlainText(text)

    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:  # Ctrl+V
        self.insertPlainText(source.text())

    @QtCore.Slot(QtGui.QShowEvent)
    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        QtCore.QCoreApplication.processEvents()
        self.font_changed.emit()


class OutputTextBox(QtWidgets.QTextEdit):
    font_changed = QtCore.Signal()
    hide_show_signal = QtCore.Signal(bool)

    def __init__(self, parent: Union[QtWidgets.QWidget, None], init_text: str = ''):
        super().__init__(parent=parent)
        self.sizePolicy().setHorizontalStretch(1)
        self.setAcceptRichText(False)
        self.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.setPlainText(init_text)
        self.setTabStopDistance(35)
        self.setReadOnly(True)
        self.setFont(self.font())

    def setFont(self, font: Union[QtGui.QFont, str, Sequence[str]]) -> None:
        super().setFont(font)
        self.font_changed.emit()

    @QtCore.Slot(bool)
    def hide_show_slot(self, visible: bool = None):
        self.hide_show_signal.emit(visible)


class CodeItem(QtWidgets.QWidget):
    execute_signal = QtCore.Signal(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit)
    stop_signal = QtCore.Signal(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit, bool)
    del_signal = QtCore.Signal()
    change_height_signal = QtCore.Signal(QtCore.QSize)
    changed_signal = QtCore.Signal()

    def __init__(self, parent: Union[QtWidgets.QWidget, None],
                 caption: str = '',
                 code: str = '', *,
                 hint: str = '',
                 output: str = '',
                 show_output: bool = ...):
        super().__init__(parent=parent)
        self.ui = Ui_CodeItem()
        self.ui.setupUi(self)
        self.min_widget_height = 110
        self.setMinimumHeight(self.min_widget_height)

        # add code editor
        self.code_editor = CodeTextBox(self)
        self.code_editor.textChanged.connect(self.change_size_slot)
        self.code_editor.font_changed.connect(self.change_size_slot)
        self.code_editor.textChanged.connect(self.changed_signal)
        self.ui.code_frame_vertical_layout.addWidget(self.code_editor)

        # add output text box
        self.output_text_box = OutputTextBox(self)
        self.output_text_box_min_height = 50
        self.output_text_box_max_height = 200
        self.output_text_box.setHtml(output)
        self.output_text_box.setMinimumHeight(self.output_text_box_min_height)
        self.output_text_box.setMaximumHeight(self.output_text_box_max_height)
        self.output_text_box.textChanged.connect(self.change_size_slot)
        self.output_text_box.font_changed.connect(self.change_size_slot)
        self.output_text_box.textChanged.connect(self.changed_signal)
        self.output_text_box.hide_show_signal.connect(self.hide_show_output_slot)
        self.ui.output_frame_vertical_layout.addWidget(self.output_text_box)
        self.ui.output_frame_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)

        # caption and indicator labels
        self.ui.code_caption.setText(caption)
        self.code_caption = self.ui.code_caption
        self.code_caption.textChanged.connect(self.changed_signal)
        self.ui.indicator_label.setText(hint)
        self.ui.indicator_label.setFont(QtGui.QFont('Consolas', 11))
        self.indicator_label = self.ui.indicator_label

        # signals and slots
        self.ui.start_button.clicked.connect(self.execute_slot)
        self.ui.stop_button.clicked.connect(self.stop_slot)
        self.ui.del_button.clicked.connect(self.del_slot)
        self.ui.del_button.clicked.connect(self.changed_signal)
        self.ui.hide_show_output_button.clicked.connect(self.hide_show_output_slot)

        # update widget
        self.code_editor.setPlainText(code)
        output = len(self.output_text_box.toPlainText())
        if show_output is not ...:
            self.hide_show_output_slot(show_output)
        elif output:
            self.hide_show_output_slot(True)
        else:
            self.hide_show_output_slot(False)

    @QtCore.Slot()
    def execute_slot(self):
        self.execute_signal.emit(self.indicator_label, self.code_editor, self.output_text_box)

    @QtCore.Slot()
    def stop_slot(self, force: bool = False, del_reason: bool = False):
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить остановку блока кода?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.stop_signal.emit(self.indicator_label, self.code_editor, self.output_text_box, del_reason)

    @QtCore.Slot()
    def del_slot(self, force: bool = False):
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить остановку и удаление блока кода?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.stop_slot(force=True, del_reason=True)
            self.del_signal.emit()

    @QtCore.Slot(bool)
    def hide_show_output_slot(self, visible: bool = None):
        if not visible or visible is None and not self.output_text_box.isHidden():  # not use isVisible!
            self.output_text_box.hide()
            self.ui.hide_show_output_button.setChecked(False)
        elif visible or visible is None and self.output_text_box.isHidden():
            self.output_text_box.show()
            self.ui.hide_show_output_button.setChecked(True)
        self.change_size_slot()
        self.output_text_box.setTextColor(QtGui.QColor().black())

    @QtCore.Slot()
    def change_size_slot(self):
        height_1 = max(self.min_widget_height,
                       self.code_editor.document().size().height()) + \
                   self.code_editor.horizontalScrollBar().height() * 3 // 2
        height_2 = min(max(self.output_text_box_min_height,
                           self.output_text_box.document().size().height()),
                       self.output_text_box_max_height) + \
                   self.output_text_box.horizontalScrollBar().height() * 3 // 2
        self.code_editor.setFixedHeight(height_1)
        self.output_text_box.setFixedHeight(height_2)
        widget_height = self.code_editor.height() + \
                        self.code_caption.height() + \
                        self.ui.main_vertical_layout.contentsMargins().top() * 2 + \
                        self.ui.main_vertical_layout.contentsMargins().bottom() * 2 + \
                        int((not self.output_text_box.isHidden()) * self.output_text_box.height())
        self.setMinimumHeight(widget_height)
        self.change_height_signal.emit(QtCore.QSize(self.width(), widget_height))

    @QtCore.Slot(QtGui.QFont)
    def change_font(self, font: QtGui.QFont):
        self.code_editor.setFont(font)
        self.output_text_box.setFont(font)
