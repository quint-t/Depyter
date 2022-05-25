from copy import copy
from datetime import datetime
from typing import Set, List, Tuple, Union, Callable

from PySide6 import QtCore, QtWidgets, QtGui

from models.project import Project
from models.template import list_templates, get_template, create_template, edit_template, del_template, \
    DATASETS_TEMPLATES_DIR, ARCHITECTURE_TEMPLATES_DIR, TRAIN_VAL_TEST_TEMPLATES_DIR, \
    VISUALIZATION_TEMPLATES_DIR, EXPORT_TEMPLATES_DIR
from views.app_settings_window import AppSettingsWindow
from views.autogen.mainwindow import Ui_MainWindow
from views.autogen.tab_project import Ui_TabProject
from views.autogen.templates import Ui_Templates
from views.code_item import CodeItem
from views.text_item import TextItem


def log(obj: object, icon: str = None, standards_buttons: Set[str] = None, default_button: str = None):
    obj_x = str(obj)
    time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    if not (icon == 'None' or icon is None):
        title_x = 'Внимание'
        # icon
        icon_x = QtWidgets.QMessageBox.NoIcon
        if icon in {
            'Question', 'Information', 'Warning', 'Critical'
        }:
            icon_x = getattr(QtWidgets.QMessageBox, icon)
        # standards_buttons
        standards_buttons_x = QtWidgets.QMessageBox.NoButton
        standard_buttons = {
            'Ok', 'Open', 'Save', 'Cancel', 'Close',
            'Discard', 'Apply', 'Reset', 'RestoreDefaults',
            'Help', 'SaveAll', 'Yes', 'YesToAll', 'No',
            'NoToAll', 'Abort', 'Retry', 'Ignore'
        }
        if isinstance(standards_buttons, set):
            for button in standards_buttons:
                if button in standard_buttons:
                    standards_buttons_x |= getattr(QtWidgets.QMessageBox, button)
        # default_button
        default_button_x = QtWidgets.QMessageBox.NoButton
        if isinstance(default_button, str):
            default_button_x = getattr(QtWidgets.QMessageBox, default_button)
        # message box
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(icon_x)
        message_box.setWindowTitle(title_x)
        message_box.setText(obj_x)
        message_box.setStandardButtons(standards_buttons_x)
        message_box.setDefaultButton(default_button_x)
        message_box.exec()
    return f'{time}. {obj}'


class PushButtonEx(QtWidgets.QPushButton):
    clicked_obj_name_signal = QtCore.Signal(str)

    update_template_signal = QtCore.Signal(str)
    rename_template_signal = QtCore.Signal(str)
    del_template_signal = QtCore.Signal(str)

    add_template_signal = QtCore.Signal()
    del_section_signal = QtCore.Signal()

    add_section_signal = QtCore.Signal()
    update_sections_signal = QtCore.Signal()

    def __init__(self, text: str, parent: Union[QtWidgets.QWidget, None]):
        super().__init__(text=text, parent=parent)
        self.edit_template_action = QtGui.QAction("Обновить шаблон по выбранным блокам")
        self.edit_template_action.triggered.connect(self.edit_template_slot)
        self.rename_template_action = QtGui.QAction("Изменить название шаблона")
        self.rename_template_action.triggered.connect(self.rename_template_slot)
        self.del_template_action = QtGui.QAction("Удалить шаблон")
        self.del_template_action.triggered.connect(self.del_template_slot)

        self.add_template_action = QtGui.QAction("Добавить шаблон по выбранным блокам в раздел")
        self.add_template_action.triggered.connect(self.add_template_signal)
        self.del_section_action = QtGui.QAction("Удалить раздел со всеми шаблонами")
        self.del_section_action.triggered.connect(self.del_section_signal)

        self.add_section_action = QtGui.QAction("Добавить раздел")
        self.add_section_action.triggered.connect(self.add_section_signal)
        self.update_sections_action = QtGui.QAction("Обновить все разделы с шаблонами")
        self.update_sections_action.triggered.connect(self.update_sections_signal)

        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.edit_template_action)
        self.menu.addAction(self.rename_template_action)
        self.menu.addAction(self.del_template_action)
        self.menu.addSeparator()
        self.menu.addAction(self.add_template_action)
        self.menu.addAction(self.del_section_action)
        self.menu.addSeparator()
        self.menu.addAction(self.add_section_action)
        self.menu.addAction(self.update_sections_action)

    @QtCore.Slot()
    def edit_template_slot(self):
        self.update_template_signal.emit(self.objectName())

    @QtCore.Slot()
    def rename_template_slot(self):
        self.rename_template_signal.emit(self.objectName())

    @QtCore.Slot()
    def del_template_slot(self):
        self.del_template_signal.emit(self.objectName())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtGui.Qt.LeftButton:
            self.clicked_obj_name_signal.emit(self.objectName())
        elif event.button() == QtGui.Qt.RightButton:
            self.menu.exec(event.globalPos())
        else:
            super().mouseReleaseEvent(event)


class GroupBox(QtWidgets.QGroupBox):
    add_template_signal = QtCore.Signal(str)
    del_section_signal = QtCore.Signal(str)

    add_section_signal = QtCore.Signal()
    update_sections_signal = QtCore.Signal()

    def __init__(self, title: str, parent: Union[QtWidgets.QWidget, None]):
        super().__init__(title=title, parent=parent)
        self.add_template_action = QtGui.QAction("Добавить шаблон по выбранным блокам в раздел")
        self.add_template_action.triggered.connect(self.add_template_slot)
        self.del_section_action = QtGui.QAction("Удалить раздел со всеми шаблонами")
        self.del_section_action.triggered.connect(self.del_section_slot)

        self.add_section_action = QtGui.QAction("Добавить раздел")
        self.add_section_action.triggered.connect(self.add_section_signal)
        self.update_action = QtGui.QAction("Обновить все разделы с шаблонами")
        self.update_action.triggered.connect(self.update_sections_signal)

        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.add_template_action)
        self.menu.addAction(self.del_section_action)
        self.menu.addSeparator()
        self.menu.addAction(self.add_section_action)
        self.menu.addAction(self.update_action)

    @QtCore.Slot()
    def add_template_slot(self):
        self.add_template_signal.emit(self.objectName())

    @QtCore.Slot()
    def del_section_slot(self):
        self.del_section_signal.emit(self.objectName())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtGui.Qt.RightButton:
            self.menu.exec(event.globalPos())
        else:
            super().mouseReleaseEvent(event)


class Stage(QtWidgets.QWidget):
    loaded_template = QtCore.Signal(list)  # List[Tuple[str, str, str]]

    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent)
        self.ui = Ui_Templates()
        self.ui.setupUi(self)
        self.dir = None
        self.templates_types = dict()
        self.buttons_to_templates = dict()
        self.group_boxes_to_template_types = dict()
        self.get_selected_blocks = get_selected_blocks_func

        self.add_section_action = QtGui.QAction("Добавить раздел")
        self.add_section_action.triggered.connect(self.add_section_slot)
        self.update_action = QtGui.QAction("Обновить все разделы с шаблонами")
        self.update_action.triggered.connect(self._load_templates)

        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.add_section_action)
        self.menu.addAction(self.update_action)

    @QtCore.Slot()
    def add_section_slot(self, force: bool = False, template_type: str = ''):
        status = False
        if not force:
            template_type, status = QtWidgets.QInputDialog().getText(self,
                                                                     'Введите название раздела (тип шаблона)',
                                                                     'Название раздела (тип шаблона)',
                                                                     QtWidgets.QLineEdit.Normal,
                                                                     'Раздел-1')
        if force or status:
            group_box = GroupBox(title=template_type, parent=self)
            group_box_layout = QtWidgets.QVBoxLayout()
            group_box.setLayout(group_box_layout)
            group_box.add_template_signal.connect(self.add_template_slot)
            group_box.del_section_signal.connect(self.del_section_slot)
            group_box.add_section_signal.connect(self.add_section_slot)
            group_box.update_sections_signal.connect(self._load_templates)
            group_box_name = 'group_box_' + str(len(self.group_boxes_to_template_types) + 1)
            group_box.setObjectName(group_box_name)
            self.ui.main_widget_vertical_layout.addWidget(group_box)
            self.templates_types[template_type] = [group_box, group_box_layout]
            group_box_layout.findChildren(PushButtonEx)
            self.group_boxes_to_template_types[group_box_name] = template_type
            group_box.repaint()

    @QtCore.Slot(str)
    def del_section_slot(self, group_box_obj_name: str):
        if group_box_obj_name in self.group_boxes_to_template_types:
            template_type = self.group_boxes_to_template_types[group_box_obj_name]
            if QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                     'Вопрос',
                                     f'Вы уверены, что хотите удалить раздел {template_type} со всеми шаблонами?',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                     self).exec() == QtWidgets.QMessageBox.Yes:
                group_box, group_box_layout = self.templates_types[template_type]
                for i in reversed(range(group_box_layout.count())):
                    widget_item = group_box_layout.takeAt(i)
                    if widget_item and isinstance(widget_item.widget(), PushButtonEx):
                        button = widget_item.widget()
                        button_obj_name = button.objectName()
                        if button_obj_name in self.buttons_to_templates:
                            filename, *_ = self.buttons_to_templates[button.objectName()]
                            del_template(filename)
                self._load_templates()

    @QtCore.Slot(str)
    def add_template_slot(self, group_box_obj_name: str):
        if group_box_obj_name in self.group_boxes_to_template_types:
            template_name, status = QtWidgets.QInputDialog.getMultiLineText(self,
                                                                            'Введите название шаблона',
                                                                            'Название шаблона',
                                                                            'Шаблон-1')
            if status:
                template_code_blocks = self.get_selected_blocks()
                create_template(self.dir, self.group_boxes_to_template_types[group_box_obj_name],
                                template_name, template_code_blocks)
                self._load_templates()

    @QtCore.Slot(str)
    def update_template_slot(self, button_obj_name: str):
        if button_obj_name in self.buttons_to_templates:
            filename, template_type, template_name, template_code_blocks, *_ = self.buttons_to_templates[
                button_obj_name]
            if QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                     'Вопрос',
                                     f'Вы уверены, что хотите обновить шаблон {template_type}/{template_name}?',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                     self).exec() == QtWidgets.QMessageBox.Yes:
                template_code_blocks = self.get_selected_blocks()
                edit_template(filename, template_type, template_name, template_code_blocks)
                self._load_templates()

    @QtCore.Slot(str)
    def rename_template_slot(self, button_obj_name: str):
        if button_obj_name in self.buttons_to_templates:
            filename, template_type, template_name, template_code_blocks, *_ = self.buttons_to_templates[
                button_obj_name]
            template_name, status = QtWidgets.QInputDialog.getMultiLineText(self,
                                                                            'Введите новое название шаблона',
                                                                            'Название шаблона',
                                                                            template_name)
            if status:
                edit_template(filename, template_type, template_name, template_code_blocks, rename=True)
                self._load_templates()

    @QtCore.Slot(str)
    def del_template_slot(self, button_obj_name: str):
        if button_obj_name in self.buttons_to_templates:
            filename, template_type, template_name, template_code_blocks, button, *_ = self.buttons_to_templates[
                button_obj_name]
            if QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                     'Вопрос',
                                     f'Вы уверены, что хотите удалить шаблон {template_type}/{template_name}?',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                     self).exec() == QtWidgets.QMessageBox.Yes:
                del_template(filename)
                self._load_templates()

    @QtCore.Slot()
    def _load_templates(self):
        if self.dir is None:
            return
        if self.templates_types:
            self.buttons_to_templates.clear()
            self.group_boxes_to_template_types.clear()
            for group_box, group_box_layout in self.templates_types.values():
                group_box.deleteLater()
                group_box_layout.deleteLater()
            self.templates_types.clear()
        for filename, template_type, template_name in list_templates(self.dir):
            template_code_blocks = get_template(self.dir, filename)
            if template_type not in self.templates_types:
                self.add_section_slot(force=True, template_type=template_type)
            button_name = 'button_' + str(len(self.buttons_to_templates) + 1)
            button = PushButtonEx(text=template_name, parent=self)
            button.setObjectName(button_name)
            button.update_template_signal.connect(self.update_template_slot)
            button.rename_template_signal.connect(self.rename_template_slot)
            button.del_template_signal.connect(self.del_template_slot)
            button.add_template_signal.connect(self.templates_types[template_type][0].add_template_slot)
            button.del_section_signal.connect(self.templates_types[template_type][0].del_section_slot)
            button.add_section_signal.connect(self.add_section_slot)
            button.update_sections_signal.connect(self._load_templates)
            button.clicked_obj_name_signal.connect(self._load_template_slot)
            self.templates_types[template_type][1].addWidget(button)
            self.buttons_to_templates[button_name] = (filename, template_type,
                                                      template_name, template_code_blocks,
                                                      button)
        self.repaint()

    @QtCore.Slot(str)
    def _load_template_slot(self, obj_name: str):
        if self.dir is None:
            return
        filename, template_type, template_name, template_code_blocks, button, *_ = self.buttons_to_templates[obj_name]
        self.loaded_template.emit(template_code_blocks)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtGui.Qt.RightButton:
            self.menu.exec(event.globalPos())
        else:
            super().mouseReleaseEvent(event)


class StageDatasets(Stage):
    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent, get_selected_blocks_func=get_selected_blocks_func)
        self.dir = DATASETS_TEMPLATES_DIR
        self._load_templates()


class StageArchitecture(Stage):
    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent, get_selected_blocks_func=get_selected_blocks_func)
        self.dir = ARCHITECTURE_TEMPLATES_DIR
        self._load_templates()


class StageTrainValTest(Stage):
    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent, get_selected_blocks_func=get_selected_blocks_func)
        self.dir = TRAIN_VAL_TEST_TEMPLATES_DIR
        self._load_templates()


class StageVisualization(Stage):
    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent, get_selected_blocks_func=get_selected_blocks_func)
        self.dir = VISUALIZATION_TEMPLATES_DIR
        self._load_templates()


class StageExport(Stage):
    def __init__(self, parent: Union[QtWidgets.QWidget, None], get_selected_blocks_func: Callable):
        super().__init__(parent=parent, get_selected_blocks_func=get_selected_blocks_func)
        self.dir = EXPORT_TEMPLATES_DIR
        self._load_templates()


class BlocksWidgetItem(QtWidgets.QListWidgetItem, QtCore.QObject):
    delete_item_signal = QtCore.Signal(QtWidgets.QListWidgetItem)

    def __init__(self, listview: QtWidgets.QListWidget = None):
        super().__init__(listview=listview)
        self.listview = listview

    def set_list_view(self, listview: QtWidgets.QListWidget) -> None:
        self.listview = listview

    @QtCore.Slot(QtCore.QSize)
    def setSizeHint(self, size: QtCore.QSize) -> None:
        super().setSizeHint(QtCore.QSize(10, size.height()))  # not replace 10 to another
        if self.listview is not None:
            self.listview.viewport().update()

    @QtCore.Slot()
    def delete_item_slot(self) -> None:
        if self.listview is not None:
            self.listview.takeItem(self.listview.indexFromItem(self).row())
            self.deleteLater()


class ListWidget(QtWidgets.QListWidget):
    changed_signal = QtCore.Signal()

    def __init__(self, parent: Union[QtWidgets.QWidget, None] = None):
        super().__init__(parent=parent)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:  # fixes one issue with item being removed after move
        item_widgets = []
        for i in range(self.count()):
            item = self.item(i)
            item_widgets.append((item, self.itemWidget(item)))
        super().dropEvent(event)
        i = 0
        while i < self.count():
            item = self.item(i)
            if item is not None and not isinstance(item, BlocksWidgetItem):
                self.takeItem(i)
                last_item, last_widget = item_widgets[i - 1]
                if isinstance(last_widget, CodeItem):
                    item = BlocksWidgetItem()
                    item.setSizeHint(last_widget.sizeHint())
                    last_widget.change_height_signal.connect(item.setSizeHint)
                    last_widget.del_signal.connect(item.delete_item_slot)
                    last_widget.changed_signal.connect(self.changed_slot)
                    item.delete_item_signal.connect(self.removeItemWidget)
                    self.insertItem(i, item)
                    self.setItemWidget(item, last_widget)
                    item.set_list_view(self)
                    last_widget.change_size_slot()
                elif isinstance(last_widget, TextItem):
                    item = BlocksWidgetItem()
                    item.setSizeHint(last_widget.sizeHint())
                    last_widget.change_height_signal.connect(item.setSizeHint)
                    last_widget.del_signal.connect(item.delete_item_slot)
                    last_widget.changed_signal.connect(self.changed_slot)
                    item.delete_item_signal.connect(self.removeItemWidget)
                    self.insertItem(i, item)
                    self.setItemWidget(item, last_widget)
                    item.set_list_view(self)
                    last_widget.change_size_slot()
                else:
                    i -= 1
                continue
            i += 1
        self.changed_signal.emit()

    @QtCore.Slot()
    def changed_slot(self):
        self.changed_signal.emit()


class TabProject(QtWidgets.QWidget):
    code_block_font_change_signal = QtCore.Signal(QtGui.QFont)
    text_block_font_change_signal = QtCore.Signal(QtGui.QFont, int)
    caption_font_change_signal = QtCore.Signal(QtGui.QFont)
    changed_signal = QtCore.Signal(QtWidgets.QWidget, bool)

    kernel_stopped = QtCore.Signal(str)
    error_occurred = QtCore.Signal(str)
    ready_for_execution = QtCore.Signal(str)

    def __init__(self, project: Project, parent: Union[QtWidgets.QWidget, None]):
        super().__init__(parent=parent)
        self.ui = Ui_TabProject()
        self.ui.setupUi(self)
        self.blocks_widget = ListWidget(self)
        self.blocks_widget.setObjectName(u"blocks_widget")
        self.blocks_widget.setGeometry(QtCore.QRect(120, 0, 132, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blocks_widget.sizePolicy().hasHeightForWidth())
        self.blocks_widget.setSizePolicy(sizePolicy)
        self.blocks_widget.setFrameShape(QtWidgets.QFrame.Box)
        self.blocks_widget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.blocks_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.blocks_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.blocks_widget.setDragEnabled(True)
        self.blocks_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.blocks_widget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.blocks_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.blocks_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.blocks_widget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.blocks_widget.setResizeMode(QtWidgets.QListView.Adjust)
        self.blocks_widget.changed_signal.connect(self.changed_slot)
        self.ui.splitter.addWidget(self.blocks_widget)

        self.stage_datasets = StageDatasets(self, self.get_selected_blocks)
        self.stage_architecture = StageArchitecture(self, self.get_selected_blocks)
        self.stage_train_val_test = StageTrainValTest(self, self.get_selected_blocks)
        self.stage_visualization = StageVisualization(self, self.get_selected_blocks)
        self.stage_export = StageExport(self, self.get_selected_blocks)
        self._code_block_font = QtGui.QFont('Segoe UI', pointSize=1)
        self._text_block_font = QtGui.QFont('Segoe UI', pointSize=1)
        self._caption_font = QtGui.QFont('Segoe UI', pointSize=1)
        self.ui.tab_widget.addTab(self.stage_datasets, 'Наборы данных')
        self.ui.tab_widget.addTab(self.stage_architecture, 'Архитектуры')
        self.ui.tab_widget.addTab(self.stage_train_val_test, 'Обучение, валидация, тестирование')
        self.ui.tab_widget.addTab(self.stage_visualization, 'Визуализация')
        self.ui.tab_widget.addTab(self.stage_export, 'Экспорт')
        self.ui.tab_widget.setCurrentWidget(self.stage_datasets)

        self.stage_datasets.loaded_template.connect(self._add_blocks)
        self.stage_architecture.loaded_template.connect(self._add_blocks)
        self.stage_train_val_test.loaded_template.connect(self._add_blocks)
        self.stage_visualization.loaded_template.connect(self._add_blocks)
        self.stage_export.loaded_template.connect(self._add_blocks)

        self._run_status = False

        self.blocks_widget.verticalScrollBar().setSingleStep(15)
        self._project = project
        self._project.kernel_stopped.connect(self.kernel_stopped_slot)
        self._project.error_occurred.connect(self.error_occurred_slot)
        self._project.ready_for_execution.connect(self.ready_for_execution_slot)
        self._init_project()
        self._last_text_font_size = self._project.get_other_setting('text-block-font-size')

        stage = self.stage_datasets
        size = stage.ui.main_widget.sizeHint()
        w = size.width() + stage.ui.scroll_area.verticalScrollBar().height()
        h = size.height() + stage.ui.scroll_area.horizontalScrollBar().height()
        self.ui.tab_widget.resize(QtCore.QSize(w, h))

    @QtCore.Slot()
    def kernel_stopped_slot(self):
        self._run_status = False
        self.kernel_stopped.emit(self.project_name())

    @QtCore.Slot()
    def error_occurred_slot(self):
        self._run_status = False
        self.error_occurred.emit(self.project_name())

    @QtCore.Slot()
    def ready_for_execution_slot(self):
        if self._run_status:
            self.ready_for_execution.emit(self.project_name())
        self._run_status = False

    def is_code_block_chosen(self):
        for item in self.blocks_widget.selectedItems():
            block_item = self.blocks_widget.itemWidget(item)
            if isinstance(block_item, CodeItem):
                return True
        return False

    def is_any_block_chosen(self):
        for item in self.blocks_widget.selectedItems():
            block_item = self.blocks_widget.itemWidget(item)
            if isinstance(block_item, CodeItem):
                return True
            elif isinstance(block_item, TextItem):
                return True
        return False

    def is_kernel_started(self):
        return self._project.is_kernel_started()

    def _init_project(self):
        for block in self._project.blocks:
            if len(block) == 3:  # CodeItem
                caption, code, output = block
                self._add_code_block(caption=caption, code=code, output=output)
            elif len(block) == 2:  # TextItem
                caption, text = block
                self._add_text_block(caption=caption, text=text)

    @QtCore.Slot(str, str, str, bool)
    def _add_code_block(self, caption: str = '', code: str = '', *,
                        output: str = '', show_output: bool = ..., to_visible: Union[bool, QtCore.QModelIndex] = False):
        code_item = CodeItem(parent=self, caption=caption, code=code, output=output, show_output=show_output)
        self.code_block_font_change_signal.connect(code_item.code_editor.setFont)
        self.code_block_font_change_signal.connect(code_item.output_text_box.setFont)
        self.caption_font_change_signal.connect(code_item.code_caption.setFont)
        code_item.execute_signal.connect(self._project.run_code_block)
        code_item.stop_signal.connect(self._project.stop_code_block)
        item = BlocksWidgetItem()
        item.set_list_view(self.blocks_widget)
        item.setSizeHint(code_item.sizeHint())
        code_item.change_height_signal.connect(item.setSizeHint)
        code_item.del_signal.connect(item.delete_item_slot)
        code_item.changed_signal.connect(self.changed_slot)
        item.delete_item_signal.connect(self.blocks_widget.removeItemWidget)
        rect = self.blocks_widget.viewport().contentsRect()
        pos = QtCore.QPoint((rect.topLeft().x() + rect.bottomLeft().x()) // 2,
                            (rect.topLeft().y() + rect.bottomLeft().y()) // 2)
        center = self.blocks_widget.indexAt(pos)
        if isinstance(to_visible, bool) and to_visible and center.isValid():
            self.blocks_widget.insertItem(center.row(), item)
        elif isinstance(to_visible, QtCore.QModelIndex) and to_visible.isValid():
            self.blocks_widget.insertItem(to_visible.row(), item)
        else:
            self.blocks_widget.addItem(item)
        self.blocks_widget.setItemWidget(item, code_item)
        self.caption_font_change_signal.emit(self._caption_font)
        self.code_block_font_change_signal.emit(self._code_block_font)
        item.setSelected(True)

    def _add_text_block(self, caption: str = '', text: str = '', to_visible: Union[bool, QtCore.QModelIndex] = False):
        text_item = TextItem(parent=self, caption=caption, text=text)
        self.text_block_font_change_signal.connect(text_item.text_editor.setFont)
        self.code_block_font_change_signal.connect(text_item.update_code_font)
        self.caption_font_change_signal.connect(text_item.text_caption.setFont)
        item = BlocksWidgetItem()
        item.set_list_view(self.blocks_widget)
        item.setSizeHint(text_item.sizeHint())
        text_item.change_height_signal.connect(item.setSizeHint)
        text_item.del_signal.connect(item.delete_item_slot)
        text_item.changed_signal.connect(self.changed_slot)
        item.delete_item_signal.connect(self.blocks_widget.removeItemWidget)
        rect = self.blocks_widget.viewport().contentsRect()
        pos = QtCore.QPoint((rect.topLeft().x() + rect.bottomLeft().x()) // 2,
                            (rect.topLeft().y() + rect.bottomLeft().y()) // 2)
        center = self.blocks_widget.indexAt(pos)
        if isinstance(to_visible, bool) and to_visible and center.isValid():
            self.blocks_widget.insertItem(center.row(), item)
        elif isinstance(to_visible, QtCore.QModelIndex) and to_visible.isValid():
            self.blocks_widget.insertItem(to_visible.row(), item)
        else:
            self.blocks_widget.addItem(item)
        self.blocks_widget.setItemWidget(item, text_item)
        self.caption_font_change_signal.emit(self._caption_font)
        self.code_block_font_change_signal.emit(self._code_block_font)
        self.text_block_font_change_signal.emit(self._text_block_font,
                                                self._project.get_other_setting('text-block-font-size'))
        item.setSelected(True)

    @QtCore.Slot(list)
    def _add_blocks(self, code_blocks: List[Tuple[str, str, str]]):  # Type, Caption, Code
        self.blocks_widget.clearSelection()
        rect = self.blocks_widget.viewport().contentsRect()
        pos = QtCore.QPoint((rect.topLeft().x() + rect.bottomLeft().x()) // 2,
                            (rect.topLeft().y() + rect.bottomLeft().y()) // 2)
        center = self.blocks_widget.indexAt(pos)
        if center.isValid():
            for block_type, caption, code_or_text in reversed(code_blocks):
                if block_type == 'code':
                    self._add_code_block(caption=caption, code=code_or_text, to_visible=center)
                elif block_type == 'text':
                    self._add_text_block(caption=caption, text=code_or_text, to_visible=center)
        else:
            for block_type, caption, code_or_text in code_blocks:
                if block_type == 'code':
                    self._add_code_block(caption=caption, code=code_or_text, to_visible=False)
                elif block_type == 'text':
                    self._add_text_block(caption=caption, text=code_or_text, to_visible=False)

    def get_selected_blocks(self) -> List[Union[Tuple[str, str, str], Tuple[str, str]]]:
        blocks = []
        for item in self.blocks_widget.selectedItems():
            block_item = self.blocks_widget.itemWidget(item)
            if isinstance(block_item, CodeItem):
                blocks.append(('code',
                               block_item.code_caption.text(),
                               block_item.code_editor.toPlainText()))
            elif isinstance(block_item, TextItem):
                blocks.append(('text', block_item.text_caption.text(), block_item.text_editor.toHtml()))
        return blocks

    def project_name(self) -> str:
        return self._project.name

    def project_path(self) -> str:
        return self._project.full_path

    @staticmethod
    def open_project(full_project_path: str, full_ipynb_path: str) -> Project:
        return Project.open_project(full_project_path, full_ipynb_path)

    def save_project(self):
        blocks = []
        for i in range(self.blocks_widget.count()):
            block_item = self.blocks_widget.itemWidget(self.blocks_widget.item(i))
            if isinstance(block_item, CodeItem):
                blocks.append((block_item.code_caption.text(),
                               block_item.code_editor.toPlainText(),
                               block_item.output_text_box.toHtml()))
            elif isinstance(block_item, TextItem):
                blocks.append((block_item.text_caption.text(), block_item.text_editor.toHtml(),))
        self._project.blocks = blocks
        self._project.set_other_setting('text-block-font-size', self._last_text_font_size)
        self._project.save_project()
        self.changed_signal.emit(self, False)

    def close_project(self):
        self._project.close_project()
        self.layout().removeWidget(self)
        self.deleteLater()

    def duplicate_project(self, full_dup_project_path: str) -> Project:
        return self._project.duplicate_project(full_dup_project_path)

    def add_code_block(self):
        self._add_code_block(caption='Блок кода', code='# code', to_visible=True)
        self.changed_signal.emit(self, True)

    def add_text_block(self):
        self._add_text_block(caption='Блок текста', text='Текст', to_visible=True)
        self.changed_signal.emit(self, True)

    def run_selected_blocks(self):
        b = False
        for item in self.blocks_widget.selectedItems():
            code_item = self.blocks_widget.itemWidget(item)
            if isinstance(code_item, CodeItem):
                self._run_status = True
                b = True
                code_item.execute_slot()
        if not b:
            raise Exception('Ни один блок кода не выбран для выполнения')

    def interrupt_execution(self) -> Union[None, type(...)]:
        return self._project.interrupt_execution()

    def restart_kernel(self) -> Union[None, type(...)]:
        r = self._project.restart_kernel()
        for i in range(self.blocks_widget.count()):
            block_item = self.blocks_widget.itemWidget(self.blocks_widget.item(i))
            if isinstance(block_item, CodeItem):
                block_item.indicator_label.setText('')
        return r

    def clear_outputs(self):
        b = False
        for item in self.blocks_widget.selectedItems():
            block_item = self.blocks_widget.itemWidget(item)
            if isinstance(block_item, CodeItem):
                block_item.output_text_box.setPlainText('')
                block_item.output_text_box.hide_show_signal.emit(False)
                b = True
        if b:
            self.changed_signal.emit(self, True)
        else:
            raise Exception('Ни один блок кода не выбран для очистки вывода')

    def delete_selected_blocks(self):
        b = False
        for item in self.blocks_widget.selectedItems():
            block_item = self.blocks_widget.itemWidget(item)
            if isinstance(block_item, CodeItem):
                block_item.del_slot(force=True)
                b = True
            elif isinstance(block_item, TextItem):
                block_item.del_slot(force=True)
                b = True
        if b:
            self.changed_signal.emit(self, True)
        else:
            raise Exception('Ни один блок не выбран для удаления')

    @QtCore.Slot(QtGui.QFont)
    def code_block_font_change_slot(self, font: QtGui.QFont):
        self._code_block_font = copy(font)
        self.code_block_font_change_signal.emit(font)

    @QtCore.Slot(QtGui.QFont)
    def text_block_font_change_slot(self, font: QtGui.QFont):
        self._text_block_font = copy(font)
        self._last_text_font_size = font.pointSize()
        self.text_block_font_change_signal.emit(font, self._project.get_other_setting('text-block-font-size'))

    @QtCore.Slot(QtGui.QFont)
    def caption_font_change_slot(self, font: QtGui.QFont):
        self._caption_font = copy(font)
        self.caption_font_change_signal.emit(font)

    @QtCore.Slot()
    def changed_slot(self):
        self.changed_signal.emit(self, True)


class MainWindow(QtWidgets.QMainWindow):
    main_close_signal = QtCore.Signal()
    update_style = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # app settings window
        self.app_settings_window = AppSettingsWindow()
        # project
        self.ui.a_new_project.triggered.connect(self.new_project_slot)
        self.ui.a_duplicate_project.triggered.connect(self.duplicate_project_slot)
        self.ui.a_open_project.triggered.connect(self.open_project_slot)
        self.ui.a_save_project.triggered.connect(self.save_project_slot)
        self.ui.a_close_project.triggered.connect(self.close_project)
        self.ui.a_app_settings.triggered.connect(self.app_settings_slot)
        self.ui.a_exit_program.triggered.connect(self.exit_program_slot)
        # operations
        self.ui.a_add_code_block.triggered.connect(self.add_code_block_slot)
        self.ui.a_add_text_block.triggered.connect(self.add_text_block_slot)
        self.ui.a_run_selected_blocks.triggered.connect(self.run_selected_blocks_slot)
        self.ui.a_stop_execution.triggered.connect(self.stop_execution_slot)
        self.ui.a_restart_kernel.triggered.connect(self.restart_kernel_slot)
        self.ui.a_clear_outputs.triggered.connect(self.clear_outputs_slot)
        self.ui.a_delete_selected_blocks.triggered.connect(self.delete_selected_blocks)
        # instruments
        self.ui.a_color_picker.triggered.connect(self.color_picker_slot)
        self.ui.a_file_selector.triggered.connect(self.file_selector_slot)
        # help
        self.ui.a_about.triggered.connect(self.about_slot)
        # other
        self.app_settings_window.app_settings.width_signal.connect(self._update_width)
        self.app_settings_window.app_settings.height_signal.connect(self._update_height)
        self.app_settings_window.app_settings.style_signal.connect(self._update_style)
        self.app_settings_window.app_settings.maximized_signal.connect(self._update_maximized)

    # project

    @QtCore.Slot()
    def new_project_slot(self):
        project_file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             caption='Сохранить файл проекта...',
                                                             dir='',
                                                             filter='NNC (*.nnc)')
        if not project_file or not project_file[0]:
            self.ui.status_label.setText('Отмена создания проекта.')
            return
        project_file = project_file[0]
        if not project_file.endswith('.nnc'):
            project_file += '.nnc'
        project_file = QtCore.QDir.toNativeSeparators(project_file)
        s = set()
        for tab_project in self.ui.tab_widget.findChildren(TabProject):
            s.add(tab_project.project_path())
        if project_file in s:
            self.log(f'Проект по пути {project_file} уже открыт.', icon='Warning', standard_buttons={'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока проект создается...')
        self.ui.status_label.repaint()
        try:
            project = Project.new_project(project_file)
            project.save_project()
            tab_project = TabProject(project, self)
            tab_project.changed_signal.connect(self.change_project_status_slot)
            tab_project.kernel_stopped.connect(self.kernel_stopped_slot)
            tab_project.error_occurred.connect(self.error_occurred_slot)
            tab_project.ready_for_execution.connect(self.ready_for_execution_slot)
            self.app_settings_window.code_block_font_changed_signal.connect(tab_project.code_block_font_change_slot)
            self.app_settings_window.text_block_font_changed_signal.connect(tab_project.text_block_font_change_slot)
            self.app_settings_window.caption_font_changed_signal.connect(tab_project.caption_font_change_slot)
            self.app_settings_window.apply()
            self.ui.tab_widget.addTab(tab_project, project.name)
            self.ui.tab_widget.setCurrentWidget(tab_project)
            self.change_project_status_slot(tab_project, False)
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось создать проект: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'Проект {tab_project.project_name()} создан.')

    @QtCore.Slot()
    def duplicate_project_slot(self):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        project_file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             caption='Продублировать файл проекта...',
                                                             dir='',
                                                             filter='NNC (*.nnc)')
        if not project_file or not project_file[0]:
            self.ui.status_label.setText('Отмена дублирования проекта.')
            return
        project_file = project_file[0]
        if not project_file.endswith('.nnc'):
            project_file += '.nnc'
        project_file = QtCore.QDir.toNativeSeparators(project_file)
        s = set()
        for tab_project in self.ui.tab_widget.findChildren(TabProject):
            s.add(tab_project.project_path())
        if project_file in s:
            self.log(f'Проект по пути {project_file} уже открыт.', icon='Warning', standard_buttons={'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока проект дублируется...')
        self.ui.status_label.repaint()
        try:
            project = current_tab.duplicate_project(project_file)
            project.save_project()
            tab_project = TabProject(project, self)
            tab_project.changed_signal.connect(self.change_project_status_slot)
            tab_project.kernel_stopped.connect(self.kernel_stopped_slot)
            tab_project.error_occurred.connect(self.error_occurred_slot)
            tab_project.ready_for_execution.connect(self.ready_for_execution_slot)
            self.app_settings_window.code_block_font_changed_signal.connect(tab_project.code_block_font_change_slot)
            self.app_settings_window.text_block_font_changed_signal.connect(tab_project.text_block_font_change_slot)
            self.app_settings_window.caption_font_changed_signal.connect(tab_project.caption_font_change_slot)
            self.app_settings_window.apply()
            self.ui.tab_widget.addTab(tab_project, project.name)
            self.ui.tab_widget.setCurrentWidget(tab_project)
            self.change_project_status_slot(tab_project, False)
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось дублировать проект: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'Проект {project.name} создан как дубликат {current_tab.project_name()}.')

    @QtCore.Slot()
    def open_project_slot(self):
        jupyter_notebook = None
        project_file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             caption='Выберите файл проекта для открытия...',
                                                             dir='',
                                                             filter='NNC (*.nnc);;IPython-Notebook (*.ipynb)')
        if not project_file or not project_file[0]:
            self.ui.status_label.setText('Отмена открытия проекта.')
            return
        project_file = project_file[0]
        if project_file.endswith('.ipynb'):
            jupyter_notebook = QtCore.QDir.toNativeSeparators(project_file)
            project_file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                 caption='Сохранить файл проекта в формат NNC...',
                                                                 dir='',
                                                                 filter='NNC (*.nnc)')
            if not project_file or not project_file[0]:
                self.ui.status_label.setText('Отмена открытия проекта.')
                return
            project_file = project_file[0]
            if not project_file.endswith('.nnc'):
                project_file += '.nnc'
        elif not project_file.endswith('.nnc'):
            project_file += '.nnc'
        project_file = QtCore.QDir.toNativeSeparators(project_file)
        s = set()
        for tab_project in self.ui.tab_widget.findChildren(TabProject):
            s.add(tab_project.project_path())
        if project_file in s:
            self.log(f'Проект по пути {project_file} уже открыт.', icon='Warning', standard_buttons={'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока проект открывается...')
        self.ui.status_label.repaint()
        try:
            project = TabProject.open_project(project_file, jupyter_notebook)
            tab_project = TabProject(project, self)
            tab_project.changed_signal.connect(self.change_project_status_slot)
            tab_project.kernel_stopped.connect(self.kernel_stopped_slot)
            tab_project.error_occurred.connect(self.error_occurred_slot)
            tab_project.ready_for_execution.connect(self.ready_for_execution_slot)
            self.app_settings_window.code_block_font_changed_signal.connect(tab_project.code_block_font_change_slot)
            self.app_settings_window.text_block_font_changed_signal.connect(tab_project.text_block_font_change_slot)
            self.app_settings_window.caption_font_changed_signal.connect(tab_project.caption_font_change_slot)
            self.app_settings_window.apply()
            self.ui.tab_widget.addTab(tab_project, project.name)
            self.ui.tab_widget.setCurrentWidget(tab_project)
            self.change_project_status_slot(tab_project, False)
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось открыть проект: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'Проект {tab_project.project_name()} открыт.')

    @QtCore.Slot()
    def save_project_slot(self):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока проект сохраняется...')
        self.ui.status_label.repaint()
        try:
            current_tab.save_project()
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось сохранить проект: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'Проект {current_tab.project_name()} сохранен.')

    @QtCore.Slot(bool)
    def close_project(self, force: bool = False):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Вы уверены, что хотите закрыть проект?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.ui.status_label.setText('Подождите, пока проект закрывается...')
            self.ui.status_label.repaint()
            tab_text = self.ui.tab_widget.tabText(self.ui.tab_widget.currentIndex())
            must_save = force or tab_text[-1] == '*' and QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                                                               'Вопрос',
                                                                               'Сохранить проект перед закрытием?',
                                                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                                               self).exec() == QtWidgets.QMessageBox.Yes
            try:
                if must_save:
                    current_tab.save_project()
                current_tab.close_project()
            except:
                e = __import__('traceback').format_exc()
                self.log(f'Не удалось закрыть проект: {e}.', 'Critical', {'Ok'})
                return
            self.log(f'Проект {current_tab.project_name()} закрыт.')
        else:
            self.ui.status_label.setText('Отмена закрытия проекта.')

    @QtCore.Slot()
    def app_settings_slot(self):
        self.app_settings_window.show()

    @QtCore.Slot()
    def exit_program_slot(self):
        self.close()

    # operations

    @QtCore.Slot()
    def add_code_block_slot(self):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока блок кода добавляется...')
        self.ui.status_label.repaint()
        try:
            current_tab.add_code_block()
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось добавить блок кода: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'В проект {current_tab.project_name()} добавлен блок кода.')

    @QtCore.Slot()
    def add_text_block_slot(self):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока блок текста добавляется...')
        self.ui.status_label.repaint()
        try:
            current_tab.add_text_block()
        except:
            e = __import__('traceback').format_exc()
            self.log(f'Не удалось добавить блок текста: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'В проект {current_tab.project_name()} добавлен блок текста.')

    @QtCore.Slot()
    def run_selected_blocks_slot(self):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if not current_tab.is_code_block_chosen():
            self.log('Ни один блок кода не выбран для выполнения.', 'Information', {'Ok'})
            return
        self.ui.status_label.setText('Подождите, пока выбранные блоки отправляются на выполнение...')
        self.ui.status_label.repaint()
        try:
            current_tab.run_selected_blocks()
        except BaseException as e:
            __import__('traceback').print_exc()
            self.log(f'Не удалось отправить выбранные блоки на выполнение: {e}.', 'Critical', {'Ok'})
            return
        self.log(f'В проекте {current_tab.project_name()} началось выполнение выбранных блоков.')

    @QtCore.Slot(bool)
    def stop_execution_slot(self, force: bool = False):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if not current_tab.is_kernel_started():
            if not force:
                self.log('Ядро не запущено.', 'Information', {'Ok'})
            return
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить остановку всех блоков кода выбранного проекта?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.ui.status_label.setText('Подождите, пока останавливается выполнение блоков...')
            self.ui.status_label.repaint()
            try:
                current_tab.interrupt_execution()
            except:
                e = __import__('traceback').format_exc()
                self.log(f'Не удалось остановить выполнение блоков: {e}.', 'Critical', {'Ok'})
                return
            self.log(f'В проекте {current_tab.project_name()} остановлено выполнение блоков.')

    @QtCore.Slot(bool)
    def restart_kernel_slot(self, force: bool = False):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if not current_tab.is_kernel_started():
            if not force:
                self.log('Ядро не запущено.', 'Information', {'Ok'})
            return
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить перезапуск ядра выбранного проекта?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.ui.status_label.setText('Подождите, пока ядро перезапускается...')
            self.ui.status_label.repaint()
            try:
                current_tab.restart_kernel()
            except:
                e = __import__('traceback').format_exc()
                self.log(f'Не удалось перезапустить ядро: {e}.', 'Critical', {'Ok'})
                return
            self.log(f'В проекте {current_tab.project_name()} перезапущено ядро.')

    @QtCore.Slot(bool)
    def clear_outputs_slot(self, force: bool = False):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if not current_tab.is_code_block_chosen():
            if not force:
                self.log('Ни один блок кода не выбран для очистки вывода.', 'Information', {'Ok'})
            return
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить очистку вывода выбранных блоков кода?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.ui.status_label.setText('Подождите, пока очистка вывода блоков не будет завершена...')
            self.ui.status_label.repaint()
            try:
                current_tab.clear_outputs()
            except BaseException as e:
                __import__('traceback').print_exc()
                self.log(f'Не удалось очистить вывод: {e}.', 'Critical', {'Ok'})
                return
            self.log(f'В проекте {current_tab.project_name()} очистка вывода выбранных блоков завершена.')

    @QtCore.Slot(bool)
    def delete_selected_blocks(self, force: bool = False):
        current_tab = self.ui.tab_widget.currentWidget()
        if not isinstance(current_tab, TabProject):
            self.log(f'Список проектов пуст.', 'Warning', {'Ok'})
            return
        if not current_tab.is_any_block_chosen():
            if not force:
                self.log('Ни один блок не выбран для удаления.', 'Information', {'Ok'})
            return
        if force or QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Подтвердить остановку и удаление выбранных блоков?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          self).exec() == QtWidgets.QMessageBox.Yes:
            self.ui.status_label.setText('Подождите, пока остановка и удаление блоков не будет завершено...')
            self.ui.status_label.repaint()
            try:
                current_tab.delete_selected_blocks()
            except BaseException as e:
                __import__('traceback').print_exc()
                self.log(f'Не удалось удалить выбранные блоки: {e}.', 'Critical', {'Ok'})
                return
            self.log(f'В проекте {current_tab.project_name()} удаление выбранных блоков завершено.')

    # instruments

    @QtCore.Slot()
    def color_picker_slot(self):
        color = QtWidgets.QColorDialog.getColor(parent=self, title='Выбрать цвет...')
        if color.isValid():
            cmyk = tuple(round(x, 3) for x in color.getCmyk())[:4]
            rgb = tuple(round(x, 3) for x in color.getRgb())[:3]
            hsl = tuple(round(x, 3) for x in color.getHsl())[:3]
            hsv = tuple(round(x, 3) for x in color.getHsv())[:3]
            s = '\n'.join([f'# CMYK: {cmyk}', f'# RGB: {rgb}', f'# HSL: {hsl}', f'# HSV: {hsv}'])
            QtGui.QClipboard().setText(s)
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information,
                                  'Информация',
                                  'Параметры цвета скопированы в буфер обмена.',
                                  QtWidgets.QMessageBox.Ok,
                                  self).exec()

    @QtCore.Slot()
    def file_selector_slot(self):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Выбрать файлы...', dir='')
        if filenames and filenames[0]:
            filenames = filenames[0]
            native_sep_filenames = []
            for filename in filenames:
                native_sep_filenames.append(QtCore.QDir.toNativeSeparators(filename))
            filenames = native_sep_filenames
            filenames_str = '[\n' + ',\n'.join(f'    r"{filename}"' for filename in filenames) + '\n]\n'
            QtGui.QClipboard().setText(filenames_str)
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information,
                                  'Информация',
                                  'Список выбранных файлов скопирован в буфер обмена.',
                                  QtWidgets.QMessageBox.Ok,
                                  self).exec()

    # help

    @QtCore.Slot()
    def about_slot(self):
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information,
                              f'О программе',
                              f'Приложение для ВКР (СПбГУТ)\n'
                              f'Разработал студент группы ИКПИ-84\n'
                              f'Коваленко Леонид\n'
                              f'Санкт-Петербург\n'
                              f'2022 год',
                              QtWidgets.QMessageBox.Ok, self).exec()

    # other

    def log(self, obj: object, icon: str = None, standard_buttons: Set[str] = None):
        text = log(obj, icon, standard_buttons)
        self.ui.log.appendPlainText(text)
        self.ui.status_label.setText(text.replace('\r\n', '; ').replace('\r', '; ').replace('\n', '; ')[:128])
        self.ui.log.viewport().update()
        self.ui.status_label.repaint()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                 'Вопрос',
                                 'Вы уверены, что хотите выйти?',
                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                 self).exec() == QtWidgets.QMessageBox.No:
            event.ignore()
            return
        for i in range(self.ui.tab_widget.count()):
            tab_text = self.ui.tab_widget.tabText(i)
            if tab_text[-1] == '*':
                r = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                          'Вопрос',
                                          'Сохранить все проекты перед выходом?',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                                          | QtWidgets.QMessageBox.Cancel,
                                          self).exec()
                if r == QtWidgets.QMessageBox.Yes:
                    for tab_project in self.ui.tab_widget.findChildren(TabProject):
                        try:
                            tab_project.save_project()
                            tab_project.close_project()
                        except:
                            e = __import__('traceback').format_exc()
                            r = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                                      'Вопрос',
                                                      f'Проигнорировать ошибку?\n{e}',
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                      self).exec()
                            if r == QtWidgets.QMessageBox.No:
                                event.ignore()
                                return
                elif r == QtWidgets.QMessageBox.Cancel:
                    event.ignore()
                    return
                break
        for tab_project in self.ui.tab_widget.findChildren(TabProject):
            tab_project.close_project()
        self.app_settings_window.app_settings.maximized = self.isMaximized()
        self.app_settings_window.app_settings.style = self.style().name()
        if not self.isMaximized():
            self.app_settings_window.app_settings.width = self.width()
            self.app_settings_window.app_settings.height = self.height()
        self.main_close_signal.emit()
        event.accept()

    @QtCore.Slot(QtWidgets.QWidget, bool)
    def change_project_status_slot(self, tab_project: QtWidgets.QWidget, changed: bool = True):
        try:
            idx = self.ui.tab_widget.indexOf(tab_project)
            tab_text = self.ui.tab_widget.tabText(idx)
            if changed and tab_text and tab_text[-1] != '*':
                self.ui.tab_widget.setTabText(idx, tab_text + '*')
            elif not changed and tab_text and tab_text[-1] == '*':
                self.ui.tab_widget.setTabText(idx, tab_text[:tab_text.rfind('*')])
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot(str)
    def load_settings_from_config_file_slot(self, config_file: str):
        self.app_settings_window.load_settings_from_config_file(config_file=config_file)

    @QtCore.Slot(str)
    def save_settings_to_config_file_slot(self, config_file: str):
        self.app_settings_window.save_settings_to_config_file(config_file=config_file)

    @QtCore.Slot(int)
    def _update_width(self, width: int):
        self.resize(width, self.height())

    @QtCore.Slot(int)
    def _update_height(self, height: int):
        self.resize(self.width(), height)

    @QtCore.Slot(str)
    def _update_style(self, style: str):
        self.update_style.emit(style)
        self.app_settings_window.repaint()
        self.repaint()

    @QtCore.Slot(bool)
    def _update_maximized(self, maximized: bool):
        if maximized:
            self.showMaximized()
        else:
            self.show()

    # for logging
    @QtCore.Slot(str)
    def kernel_stopped_slot(self, project_name: str):
        self.log(f'В проекте {project_name} ядро неожиданно завершилось. Необходимо перезапустить.')

    @QtCore.Slot(str)
    def error_occurred_slot(self, project_name: str):
        self.log(f'В проекте {project_name} при выполнении произошло исключение.')

    @QtCore.Slot(str)
    def ready_for_execution_slot(self, project_name: str):
        self.log(f'В проекте {project_name} завершилось выполнение выбранных ранее блоков.')
