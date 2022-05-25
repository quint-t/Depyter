import html as html_module
import json
import os
import pickle
from copy import deepcopy
from typing import Union, Tuple, List, Any

from PySide6 import QtCore, QtWidgets

from models.code_execution import ExecutionEnvironment


class Project(QtCore.QObject):  # добавить сигнал "все запущенные блоки завершили свое выполнение"
    kernel_stopped = QtCore.Signal()
    error_occurred = QtCore.Signal()
    ready_for_execution = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self._name = ''
        self._path = ''
        self._project_filename = ''
        self._blocks = []
        self._other_settings = dict()
        self._environment = None
        self._process = None

    def _process_start(self):
        self._environment = ExecutionEnvironment(self.path[0])
        self._environment.create(clear_all_before_creating=False)
        self._process = self._environment.create_execution_process()
        self._process.kernel_stopped.connect(self.kernel_stopped)
        self._process.error_occurred.connect(self.error_occurred)
        self._process.ready_for_execution.connect(self.ready_for_execution)

    @staticmethod
    def new_project(full_project_path: str):
        project = Project()
        name = os.path.basename(os.path.dirname(full_project_path)) + '/' + os.path.basename(full_project_path)
        project.name = name[:name.rfind('.')]
        project.path = os.path.split(full_project_path)
        return project

    @staticmethod
    def open_project(full_project_path: str, full_ipynb_path: str):
        if full_ipynb_path is not None:
            with open(full_ipynb_path, 'rb') as fin:
                json_data = json.load(fin)
                blocks = []
                if isinstance(json_data, dict) and isinstance(json_data.get('cells'), list):
                    for cell in json_data['cells']:
                        if isinstance(cell, dict) and cell.get('cell_type') == 'code':
                            source = ''
                            output = ''
                            if isinstance(cell.get('source'), (str, list)):
                                source = ''.join(map(str, cell['source']))
                            if isinstance(cell.get('outputs'), list):
                                for cell_output in cell['outputs']:
                                    if isinstance(cell_output, dict) and isinstance(cell_output.get('data'), dict):
                                        for data_type, data in cell_output.get('data').items():
                                            if isinstance(data, list):
                                                if data_type == 'text/html':
                                                    s = ''.join(map(str, data))
                                                    output += '\n' * bool(output) + s
                                                    break
                                                elif data_type == 'text/plain':
                                                    s = ''.join(map(str, data))
                                                    output += '\n' * bool(output) + html_module.escape(s)
                                                    break
                                                elif data_type == 'text/markdown':
                                                    s = ''.join(map(str, data))
                                                    text_edit = QtWidgets.QTextEdit()
                                                    text_edit.setMarkdown(s)
                                                    s = text_edit.toHtml()
                                                    text_edit.deleteLater()
                                                    output += '\n' * bool(output) + s
                                                    break
                                    elif isinstance(cell_output, dict) and isinstance(cell_output.get('text'), list):
                                        s = ''.join(map(str, cell_output.get('text')))
                                        if cell_output.get('name') == 'stderr':
                                            output += '\n' * bool(
                                                output) + f'<font color="red">{html_module.escape(s)}</font>'
                                        else:
                                            output += '\n' * bool(output) + f'{html_module.escape(s)}'
                            blocks.append(('Блок кода', source, output.replace('\n', '<br>')))
                        elif cell.get('cell_type') == 'markdown':
                            html = ''
                            if isinstance(cell.get('source'), (str, list)):
                                markdown = ''.join(map(str, cell['source']))
                                text_edit = QtWidgets.QTextEdit()
                                text_edit.setMarkdown(markdown)
                                html = text_edit.toHtml()
                                text_edit.deleteLater()
                            blocks.append(('Блок текста', html))
                        elif cell.get('cell_type') == 'html':
                            html = ''
                            if isinstance(cell.get('source'), (str, list)):
                                html = ''.join(map(str, cell['source']))
                            blocks.append(('Блок текста', html))
            project = Project.new_project(full_project_path)
            project.blocks = blocks
            project.save_project()
        else:
            project = Project()
            with open(full_project_path, 'rb') as fp:
                name, path, blocks, *other = pickle.load(fp)
                project.name = name
                project.path = os.path.split(full_project_path)
                project.blocks = blocks
                if other and isinstance(other[0], dict):
                    project.other_settings = other[0]
        return project

    @QtCore.Slot(str)
    def duplicate_project(self, full_dup_project_path: str):
        project = Project.new_project(full_dup_project_path)
        project.blocks = self._blocks
        project.other_settings = self._other_settings
        return project

    @QtCore.Slot()
    def save_project(self):
        if self._project_filename:
            with open(os.path.join(*self.path), 'wb') as fp:
                pickle.dump((self._name, self.path, self._blocks, self._other_settings), fp)

    @QtCore.Slot()
    def close_project(self):
        if self._process is not None:
            self._process.kill()

    @QtCore.Slot(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit)
    def run_code_block(self, indicator_label: QtWidgets.QLabel,
                       code_editor: QtWidgets.QTextEdit,
                       output_box: QtWidgets.QTextEdit):
        if self._process is None:
            self._process_start()
        self._process.add_to_execution_queue(indicator_label, code_editor, output_box)

    @QtCore.Slot(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit, bool)
    def stop_code_block(self, indicator_label: QtWidgets.QLabel,
                        code_editor: QtWidgets.QTextEdit,
                        output_box: QtWidgets.QTextEdit,
                        del_reason: bool):
        if self._process is not None:
            self._process.stop_block_execution(indicator_label, code_editor, output_box, del_reason)

    @QtCore.Slot()
    def interrupt_execution(self) -> Union[None, type(...)]:
        if self._process is None:
            return ...
        return self._process.interrupt_execution()

    @QtCore.Slot()
    def restart_kernel(self) -> Union[None, type(...)]:
        if self._process is not None:
            self._process.restart()
        return ...

    @QtCore.Slot()
    def is_kernel_started(self):
        return self._process is not None

    # properties

    @property
    def name(self) -> str:
        return self._name  # string is non-mutable type

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'Project.name.arg: {name}')
        name = ''.join(x for x in name if x.isprintable())
        if not name:
            raise ValueError(f'Invalid name for project: {name}')
        self._name = name

    @property
    def path(self) -> Tuple[str, str]:
        return self._path, self._project_filename  # string is non-mutable type

    @path.setter
    def path(self, path_and_project_filename: Tuple[str, str]):
        if not isinstance(path_and_project_filename, tuple):
            raise TypeError(f'Project.path.arg: {path_and_project_filename}')
        new_path, project_filename = path_and_project_filename
        if not (isinstance(new_path, str) and isinstance(project_filename, str)):
            d = {'new_path': new_path, 'project_filename': project_filename}
            raise TypeError(f'Project.path.arg: {d}')
        if not os.path.exists(new_path) or not os.path.isdir(new_path):
            raise NotADirectoryError(f'Project.path. Path to dir must be exists, got: {new_path}')
        if not os.access(new_path, os.R_OK | os.W_OK | os.X_OK):
            raise PermissionError('Project.path. Project directory must have all access permissions')
        self._path = new_path
        self._project_filename = project_filename

    @property
    def full_path(self):
        return os.path.join(self._path, self._project_filename)  # string is non-mutable type

    @property
    def blocks(self) -> List[Union[Tuple[str, str, str], Tuple[str, str]]]:
        return deepcopy(self._blocks)

    @blocks.setter
    def blocks(self, blocks: List[Union[Tuple[str, str, str], Tuple[str, str]]]):
        if not isinstance(blocks, list):
            raise TypeError(f'Project.blocks.arg: {blocks}')
        if not all(isinstance(block, tuple) and (len(block) >= 2 and
                                                 isinstance(block[0], str) and
                                                 isinstance(block[1], str) and
                                                 (len(block) == 2 or len(block) == 3 and
                                                  isinstance(block[2], str)))
                   for block in blocks):
            raise TypeError(f'Project.blocks.args: {blocks}')
        self._blocks = deepcopy(blocks)

    @property
    def other_settings(self) -> dict:
        return deepcopy(self._other_settings)

    def get_other_setting(self, setting_name: str):
        return deepcopy(self._other_settings.get(setting_name))

    def set_other_setting(self, setting_name: str, setting_value: Any):
        pickle.dumps(setting_value)  # may throw
        self._other_settings[setting_name] = setting_value

    @other_settings.setter
    def other_settings(self, other_settings: dict):
        if not isinstance(other_settings, dict):
            raise TypeError(f'Project.other_settings.arg: {other_settings}')
        self._other_settings = deepcopy(other_settings)
