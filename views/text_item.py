import re
from copy import copy
from html.parser import HTMLParser
from typing import Union, Sequence

from PySide6 import QtWidgets, QtCore, QtGui, QtNetwork

from views.autogen.text_item import Ui_TextItem


class HTMLFormatter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__result = []
        self.__indent = 0
        self.__spaces = ' ' * 4

    def reset(self):
        super().reset()
        self.__result = []

    def get_formatted_html(self):
        return '\n'.join('\n'.join(indent + subpart.strip(' \t\v')
                                   for subpart in part.splitlines() if subpart and not subpart.isspace())
                         for indent, part in self.__result if part and not part.isspace())

    def get_dedented_html(self):
        return '\n'.join('\n'.join(subpart.strip(' \t\v')
                                   for subpart in part.splitlines() if subpart and not subpart.isspace())
                         for _, part in self.__result if part and not part.isspace())

    def handle_charref(self, name):
        super().handle_charref(name)
        charref = f"&#{name};"
        if self.__result:
            self.__result[-1][1] += charref
        else:
            indent = self.__indent * self.__spaces
            self.__result.append((indent, charref))

    def handle_entityref(self, name):
        super().handle_entityref(name)
        entityref = f"&{name};"
        if self.__result:
            self.__result[-1][1] += entityref
        else:
            indent = self.__indent * self.__spaces
            self.__result.append((indent, entityref))

    def handle_comment(self, data):
        super().handle_comment(data)
        indent = self.__indent * self.__spaces
        self.__result.append((indent, f"<!--{data}-->"))

    def handle_decl(self, decl):
        super().handle_decl(decl)
        indent = self.__indent * self.__spaces
        self.__result.append((indent, f"<!{decl}>"))

    def handle_pi(self, data):
        super().handle_pi(data)
        indent = self.__indent * self.__spaces
        self.__result.append((indent, f"<?{data}>"))

    def handle_startendtag(self, tag, attrs):
        super().handle_startendtag(tag, attrs)
        indent = self.__indent * self.__spaces
        s_attrs = ''
        for attr in attrs:
            q = '"'
            if '"' in attr[1]:
                q = "'"
            s_attrs += f" {attr[0]}={q}{attr[1]}{q}"
        self.__result.append((indent, f"<{tag}{s_attrs} />"))

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        indent = self.__indent * self.__spaces
        self.__indent += 1
        s_attrs = ''
        for attr in attrs:
            q = '"'
            if '"' in attr[1]:
                q = "'"
            s_attrs += f" {attr[0]}={q}{attr[1]}{q}"
        self.__result.append((indent, f"<{tag}{s_attrs}>"))

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        self.__indent -= 1
        indent = self.__indent * self.__spaces
        self.__result.append((indent, f"</{tag}>"))

    def handle_data(self, data):
        super().handle_data(data)
        indent = self.__indent * self.__spaces
        self.__result.append((indent, data))

    def unknown_decl(self, data) -> None:
        super().unknown_decl(data)
        indent = self.__indent * self.__spaces
        self.__result.append((indent, f"<![{data}]>"))


class TextBox(QtWidgets.QTextEdit):
    font_changed = QtCore.Signal()

    def __init__(self, parent: Union[QtWidgets.QWidget, None]):
        super().__init__(parent=parent)
        super().setFont(QtGui.QFont(self.font().family(), 1))
        self.setReadOnly(False)
        self.setAcceptRichText(False)
        self.sizePolicy().setHorizontalStretch(1)
        self.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.WidgetWidth)
        self.setContextMenuPolicy(QtGui.Qt.NoContextMenu)
        self.setTabStopDistance(35)
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextEditorInteraction)
        self._font_size_regexp = re.compile(r'(<.*?font-size:)\s*?(\d+)\s*?pt')
        self._resources = dict()
        self._insert_plain_text_action = QtGui.QAction('Paste Plain Text')
        self._insert_html_action = QtGui.QAction('Paste HTML')
        self._insert_markdown_action = QtGui.QAction('Paste Markdown')
        self._insert_plain_text_action.triggered.connect(self.insert_plain_text_slot)
        self._insert_html_action.triggered.connect(self.insert_html_slot)
        self._insert_markdown_action.triggered.connect(self.insert_markdown_slot)
        self._last_anchor = ''
        self._network_access_manager = QtNetwork.QNetworkAccessManager(self)
        self._network_access_manager.finished.connect(self._after_download)

    @QtCore.Slot(int, QtCore.QUrl)
    def loadResource(self, resource_type: int, url: Union[QtCore.QUrl, str]):
        if isinstance(url, QtCore.QUrl):
            r = self._resources.get(url.url())
            if r is None:
                self._network_access_manager.get(QtNetwork.QNetworkRequest(url))
                return QtGui.QImage()
            return r
        else:
            return super(TextBox, self).loadResource(resource_type, url)

    @QtCore.Slot(QtNetwork.QNetworkReply)
    def _after_download(self, network_reply: QtNetwork.QNetworkReply):
        try:
            url = network_reply.url().url()
            byte_array = network_reply.readAll()
            try:
                self._resources[url] = QtGui.QImage.fromData(byte_array)
            except:
                self._resources[url] = QtGui.QImage()
            self.edit_document_images()
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot(QtGui.QFont, int)
    def setFont(self, font: Union[QtGui.QFont, str, Sequence[str]], original_point_size: int) -> None:
        if font.pointSize() < 6:
            super().setFont(font)
            self.font_changed.emit()
            return
        previous_font_size = self.font().pointSize() if self.font().pointSize() != 1 else original_point_size
        super().setFont(QtGui.QFont(self.font().family(), 1))
        original_html = self.toHtml()
        super().setFont(font)
        current_font_size = self.font().pointSize()
        difference = current_font_size - (previous_font_size if previous_font_size >= 6 else current_font_size)
        pos = self._font_size_regexp.search(original_html)
        while pos is not None:
            font_size_pre = pos.group(1)
            font_point_size = pos.group(2)
            if font_point_size.isdigit():
                font_point_size = int(font_point_size)
                new_font_point_size = max(6, min(28, difference + font_point_size))
                original_html = original_html[:pos.start(0)] + \
                                f"{font_size_pre}{new_font_point_size}pt" + original_html[pos.end(0) + 1:]
            pos = self._font_size_regexp.search(original_html, pos.end(0) + 1)
        self.setHtml(original_html)
        self.font_changed.emit()

    @QtCore.Slot(QtGui.QMouseEvent)
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        anchor = self.anchorAt(event.pos())
        if event.button() == QtGui.Qt.RightButton and anchor:
            self._last_anchor = anchor
            menu = QtWidgets.QMenu()
            copy_link_action = QtGui.QAction('Copy Link Location')
            copy_link_action.triggered.connect(self.copy_link)
            menu.addAction(copy_link_action)
            menu.exec(event.globalPos())
        elif event.button() == QtGui.Qt.RightButton:
            menu = self.createStandardContextMenu()
            if menu is not None:
                menu.addSeparator()
                menu.addAction(self._insert_html_action)
                menu.addAction(self._insert_markdown_action)
                menu.addAction(self._insert_plain_text_action)
                menu.exec(event.globalPos())
        else:
            super().mouseReleaseEvent(event)

    def _update_line_height(self):
        text_cursor = self.textCursor()
        document = self.document()
        for i in range(document.blockCount()):
            block = document.findBlockByNumber(i)
            block_format = block.blockFormat()
            block_format.setLineHeight(100, QtGui.QTextBlockFormat.ProportionalHeight)
            text_cursor.setPosition(block.position())
            text_cursor.setBlockFormat(block_format)

    @QtCore.Slot(str)
    def insertHtml(self, html: str) -> None:
        super().insertHtml(html)
        self._update_line_height()

    @QtCore.Slot(str)
    def insertPlainText(self, text: str) -> None:
        super().insertPlainText(text)
        self._update_line_height()

    @QtCore.Slot(str)
    def setHtml(self, html: str) -> None:
        super().setHtml(html)
        self._update_line_height()

    @QtCore.Slot(str)
    def setMarkdown(self, markdown: str) -> None:
        super().setMarkdown(markdown)
        self._update_line_height()

    @QtCore.Slot()
    def copy_link(self):
        if self._last_anchor:
            QtGui.QClipboard().setText(self._last_anchor)

    @QtCore.Slot()
    def insert_plain_text_slot(self):
        try:
            text = QtGui.QClipboard().text()
            if text:
                self.insertPlainText(text)
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot()
    def insert_html_slot(self):
        try:
            text = QtGui.QClipboard().text()
            if text:
                self.insertHtml(text)
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot()
    def insert_markdown_slot(self):
        try:
            markdown = QtGui.QClipboard().text()
            if markdown:
                text_edit = QtWidgets.QTextEdit()
                text_edit.setStyle(self.style())
                text_edit.setStyleSheet(self.styleSheet())
                text_edit.setFont(self.font())
                text_edit.setMarkdown(markdown)
                html = text_edit.toHtml()
                if html:
                    self.insertHtml(html)
                text_edit.deleteLater()
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot(QtCore.QMimeData)
    def canInsertFromMimeData(self, source: QtCore.QMimeData) -> bool:
        return source.hasImage() or source.hasUrls() or super().canInsertFromMimeData(source)

    @QtCore.Slot(QtCore.QMimeData)
    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:
        if source.hasImage():
            self.drop_image(QtCore.QUrl(), source.imageData())
        elif source.hasUrls():
            for url in source.urls():
                info = QtCore.QFileInfo(url.url())
                if info.suffix().lower() in QtGui.QImageReader.supportedImageFormats():
                    self.drop_image(url, None)
                else:
                    self.drop_text_file(url)
        else:
            super().insertFromMimeData(source)

    @QtCore.Slot()
    def edit_document_images(self):
        for resource_name, resource_data in self._resources.items():
            if isinstance(resource_data, QtGui.QImage):
                if resource_data is None or isinstance(resource_data, QtGui.QImage) and resource_data.isNull():
                    continue
                resource_data = self.edit_image(resource_name, resource_data)
                if resource_data is None or isinstance(resource_data, QtGui.QImage) and resource_data.isNull():
                    continue
                self.document().addResource(QtGui.QTextDocument.ImageResource, resource_name, resource_data)
        last_w, last_h = self.size().width(), self.size().height()
        self.resize(2000, self.height())
        self.viewport().update()
        self.resize(last_w, last_h)
        self.viewport().update()
        self.font_changed.emit()

    def edit_image(self, image_name: str, image: Union[QtGui.QImage, QtGui.QPixmap]):
        if image is None:
            return QtGui.QImage()
        if isinstance(image, QtGui.QPixmap):
            image = image.toImage()
        if image_name:
            if image_name not in self._resources:
                self._resources[image_name] = image.copy()
            else:
                image = self._resources[image_name].copy()
        if image.width() <= 0 or image.height() <= 0:
            return image
        # white background
        new_image = QtGui.QImage(image.size(), QtGui.QImage.Format_RGB32)
        new_image.fill(QtGui.QColor('#ffffff'))
        painter = QtGui.QPainter(new_image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceAtop)
        painter.drawImage(0, 0, image)
        painter.end()
        # resizing, compressing
        image = new_image.copy()
        image = image.convertToFormat(QtGui.QImage.Format_RGB666)
        max_pixels = min(500 * 500, image.width() * image.height())
        width = min(self.width() * 9 // 10, int((max_pixels / (image.height() / image.width())) ** 0.5))
        height = int((max_pixels / (image.width() / image.height())) ** 0.5)
        image = image.scaled(width, height, QtGui.Qt.KeepAspectRatio, QtGui.Qt.SmoothTransformation)
        return image

    @QtCore.Slot(QtCore.QUrl, QtGui.QImage)
    def drop_image(self, url: QtCore.QUrl, image: Union[QtGui.QImage, None]):
        if image is not None and not image.isNull():
            if not url.isEmpty():
                src = url.toLocalFile()
            else:
                src = ''
            image = self.edit_image(src, image)
            if src:
                self.document().addResource(QtGui.QTextDocument.ImageResource, src, image)
                self.textCursor().insertImage(src)
            else:
                byte_array = QtCore.QByteArray()
                buffer = QtCore.QBuffer(byte_array)
                image.save(buffer, "jpg")
                data = byte_array.toBase64().toStdString()
                src = f'data:image/jpg;base64,{data}'
                self.textCursor().insertImage(src)
        elif image is None:
            self.document().addResource(QtGui.QTextDocument.ImageResource, url.url(), image)
            self.textCursor().insertImage(url.url())

    @QtCore.Slot(QtCore.QUrl)
    def drop_text_file(self, url: QtCore.QUrl):
        file = QtCore.QFile(url.toLocalFile())
        if file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
            self.textCursor().insertText(file.readAll())

    @QtCore.Slot(QtGui.QShowEvent)
    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        QtCore.QCoreApplication.processEvents()
        self.font_changed.emit()


class TextItem(QtWidgets.QWidget):
    del_signal = QtCore.Signal()
    change_height_signal = QtCore.Signal(QtCore.QSize)
    changed_signal = QtCore.Signal()

    def __init__(self, parent: Union[QtWidgets.QWidget, None], caption: str = '', text: str = ''):
        super().__init__(parent=parent)
        self.ui = Ui_TextItem()
        self.ui.setupUi(self)
        self._code_font = copy(self.font())
        self.min_widget_height = 70
        self.setMinimumHeight(self.min_widget_height)

        # add text editor
        self.text_editor = TextBox(self)
        self.text_editor.font_changed.connect(self.change_size_slot)
        self.text_editor.textChanged.connect(self.change_size_slot)
        self.text_editor.textChanged.connect(self.changed_signal)
        self.ui.text_frame_vertical_layout.addWidget(self.text_editor)

        # caption label
        self.ui.text_caption.setText(caption)
        self.text_caption = self.ui.text_caption
        self.text_caption.textChanged.connect(self.changed_signal)

        # signals and slots
        self.ui.edit_button.clicked.connect(self.edit_slot)
        self.ui.del_button.clicked.connect(self.del_slot)
        self.ui.del_button.clicked.connect(self.changed_signal)
        self.ui.update_button.clicked.connect(self.text_editor.edit_document_images)

        # update widget
        self.text_editor.setHtml(text)

    @QtCore.Slot()
    def edit_slot(self):
        menu = QtWidgets.QMenu()
        edit_as_html_action = QtGui.QAction('Edit as HTML')
        edit_as_markdown_action = QtGui.QAction('Edit as Markdown')
        edit_as_html_action.triggered.connect(self.edit_as_html_slot)
        edit_as_markdown_action.triggered.connect(self.edit_as_markdown_slot)
        menu.addSeparator()
        menu.addAction(edit_as_html_action)
        menu.addAction(edit_as_markdown_action)
        menu.exec(QtGui.QCursor.pos())

    @QtCore.Slot()
    def update_code_font(self, font: QtGui.QFont):
        self._code_font = copy(font)

    @QtCore.Slot()
    def edit_as_html_slot(self):
        try:
            formatter = HTMLFormatter()
            formatter.feed(self.text_editor.toHtml())
            input_dialog = QtWidgets.QInputDialog()
            input_dialog.setWindowTitle('Режим редактирования HTML')
            input_dialog.setLabelText('HTML:')
            input_dialog.setTextValue(formatter.get_formatted_html())
            input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            input_dialog.setOption(QtWidgets.QInputDialog.UsePlainTextEditForTextInput)
            input_dialog.setStyleSheet(
                "QPlainTextEdit{"
                f"    font-size:{self._code_font.pointSize()}pt;"
                f"    font-family:{repr(self._code_font.family())};"
                "}"
            )
            input_dialog.resize(800, 600)
            if input_dialog.exec():
                html = input_dialog.textValue()
                formatter.reset()
                formatter.feed(html)
                self.text_editor.setHtml(formatter.get_dedented_html())
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot()
    def edit_as_markdown_slot(self):
        try:
            html = self.text_editor.toHtml()
            text_edit = QtWidgets.QTextEdit()
            text_edit.setStyle(self.text_editor.style())
            text_edit.setStyleSheet(self.text_editor.styleSheet())
            text_edit.setFont(self.text_editor.font())
            text_edit.setHtml(html)
            markdown = text_edit.toMarkdown()

            input_dialog = QtWidgets.QInputDialog()
            input_dialog.setWindowTitle('Режим редактирования Markdown')
            input_dialog.setLabelText('Markdown:')
            input_dialog.setTextValue(markdown)
            input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            input_dialog.setOption(QtWidgets.QInputDialog.UsePlainTextEditForTextInput)
            input_dialog.setStyleSheet(
                "QPlainTextEdit{"
                f"    font-size:{self._code_font.pointSize()}pt;"
                f"    font-family:{repr(self._code_font.family())};"
                "}"
            )
            input_dialog.resize(800, 600)
            if input_dialog.exec():
                markdown = input_dialog.textValue()
                self.text_editor.setMarkdown(markdown)
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot(bool)
    def del_slot(self, force: bool = False):
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить удаление текстового блока?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.del_signal.emit()

    @QtCore.Slot()
    def change_size_slot(self):
        heights = (self.min_widget_height,
                   self.text_editor.document().size().height())
        widget_height = max(*heights) + \
                        self.text_caption.height() + \
                        self.ui.main_vertical_layout.contentsMargins().top() + \
                        self.ui.main_vertical_layout.contentsMargins().bottom() + \
                        self.text_editor.horizontalScrollBar().height() * 2 // 5
        self.setMinimumHeight(widget_height)
        self.change_height_signal.emit(QtCore.QSize(self.width(), widget_height))
