import ast
import html as html_module
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import venv
from collections import deque
from multiprocessing.connection import Listener
from sys import platform
from threading import Lock, Event
from typing import Union

from PySide6 import QtCore, QtWidgets, QtGui

CLIENT_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), 'client.py')


class Worker(QtCore.QObject):
    update_ui = QtCore.Signal(int, str, str)
    clear_execution_queue = QtCore.Signal()
    kernel_stopped = QtCore.Signal()
    error_occurred = QtCore.Signal()
    read_input_signal = QtCore.Signal(str)
    get_block_signal = QtCore.Signal()

    _execute_regex = re.compile(r'^([ \t]*?)(!!@|!!|!@|!)((?:.+?\\\n|.*?)+[^\n]*)', flags=re.MULTILINE | re.DOTALL)

    def __init__(self, path, address: str, port: int, password: bytes):
        super(Worker, self).__init__()
        self._path = path
        self._input = None
        self._code_block = None
        self._n = 0
        self._listener = Listener(address=(address, port), family='AF_INET', authkey=password)
        self.address = self._listener.address[0]
        self.port = self._listener.address[1]
        self.password = password
        self._code_block_event = Event()
        self._code_block_lock = Lock()
        self._manual_stop = False
        self._replace_string = '\n'.join(x.strip(' \t\r\n') for x in r"""{0}import subprocess, sys, codecs
                                    {0}__p = subprocess.Popen({1}, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True)
                                    {0}__stdout, __return_code = '', -1
                                    {0}for __l in iter(__p.stdout.readline, None):
                                    {0}    if 'would remove' in __l.lower():
                                    {0}        __p.stdin.write('\n')
                                    {0}    if __l:
                                    {0}        if {2}:
                                    {0}            print(__l.strip('\n'))
                                    {0}        __stdout += __l.strip('\n') + '\n'
                                    {0}    __return_code = __p.poll()
                                    {0}    if __return_code is not None:
                                    {0}        break
                                    {0}del __l, __p""".strip(' \t\r\n').split('\n')).format

    def set_input(self, input_arg: Union[str, None]):
        self._input = input_arg

    def set_code_block(self, code_block: Union[str, None]):
        with self._code_block_lock:
            self._code_block = code_block
            self._code_block_event.set()

    @QtCore.Slot()
    def run(self) -> None:
        read_commands = {'<read>', '<readline>', '<readlines>'}
        while True:
            try:
                with self._listener.accept() as self._conn_for_execution, \
                        self._listener.accept() as self._conn_for_interrupting:
                    try:
                        self._manual_stop = False
                        self._n = 0
                        b = False
                        while True:
                            std, received_output = self._conn_for_execution.recv()
                            if std == '<block>':
                                if b:
                                    self._n += 1
                                else:  # first
                                    b = True
                            self.update_ui.emit(self._n, std, received_output)
                            if std == '<error>':
                                self.clear_execution_queue.emit()
                                self.error_occurred.emit()
                            elif std == '<block>':
                                if self._code_block is None:
                                    self._code_block_event.clear()
                                while not self._code_block_event.is_set():
                                    self.get_block_signal.emit()
                                    self._code_block_event.wait(timeout=0.05)
                                with self._code_block_lock:
                                    code = self._code_block
                                    search = self._execute_regex.search(code)
                                    while search:
                                        groups = search.groups()
                                        if len(groups) != 3:
                                            search = self._execute_regex.search(code, search.end() + 1)
                                            continue
                                        indent, exec_type, shell = search.groups()
                                        shell = ' '.join(part.strip(' \\\t\r\n') for part in shell.splitlines())
                                        if exec_type[:2] == '!!':
                                            splitted = []
                                            temp = ''
                                            state = 0
                                            for part in re.split(r'\s+', shell):
                                                if state == 0:
                                                    if part[:2] == '{!':
                                                        if len(part) > 3 and part[-2:] == '!}':
                                                            splitted.append(('exec', part[2:-2]))
                                                        else:
                                                            temp = part[2:]
                                                            state = 1
                                                    elif part and part[0] == '\"':
                                                        if len(part) > 1 and part[-1] == '\"':
                                                            splitted.append(part)
                                                        else:
                                                            temp = part
                                                            state = 2
                                                    elif part and part[0] == '\'':
                                                        if len(part) > 1 and part[-1] == '\'':
                                                            splitted.append(part)
                                                        else:
                                                            temp = part
                                                            state = 3
                                                    elif part:
                                                        splitted.append(part)
                                                elif state == 1:
                                                    if part[-2:] == '!}':
                                                        temp += ' ' + part[:-2]
                                                        splitted.append(('exec', temp))
                                                        state = 0
                                                        temp = ''
                                                    else:
                                                        temp += ' ' + part
                                                elif state == 2:
                                                    if part and part[-1] == '\"':
                                                        temp += ' ' + part
                                                        splitted.append(temp)
                                                        state = 0
                                                        temp = ''
                                                    else:
                                                        temp += ' ' + part
                                                elif state == 3:
                                                    if part and part[-1] == '\'':
                                                        temp += ' ' + part
                                                        splitted.append(temp)
                                                        state = 0
                                                        temp = ''
                                                    else:
                                                        temp += ' ' + part
                                                else:
                                                    state = 0
                                            if state == 1 and temp:
                                                splitted.append(('exec', temp))
                                            elif state == 2 and temp:
                                                splitted.append(temp)
                                            elif state == 3 and temp:
                                                splitted.append(temp)
                                        else:
                                            splitted = shlex.split(shell)
                                        first = splitted[0]
                                        if not os.path.isabs(first):
                                            dir_path, dir_names, filenames = next(os.walk(self._path,
                                                                                          topdown=True,
                                                                                          onerror=None,
                                                                                          followlinks=False),
                                                                                  ('', [], []))
                                            for filename in filenames:
                                                if filename == first or filename.startswith(first + '.'):
                                                    first = os.path.join(self._path, filename)
                                                    break
                                        splitted[0] = first
                                        win32_type = ('[', ']') if 'win32' in platform else ('" ".join([', '])')
                                        result = win32_type[0]
                                        for part in splitted:
                                            if isinstance(part, tuple) and len(part) == 2 and part[0] == 'exec':
                                                result += f"str({part[1]}),"
                                            elif isinstance(part, str):
                                                result += f'{repr(part)},'
                                        result += win32_type[1]
                                        ins_s = self._replace_string(indent, result, '@' not in exec_type)
                                        code = code[:search.start()] + ins_s + code[search.end():]
                                        search = self._execute_regex.search(code, search.start() + len(ins_s) + 1)
                                        print('command: ', result, file=sys.stderr)
                                    self._conn_for_execution.send(code)
                                    self._code_block = None
                            elif std in read_commands:
                                if self._input is None:
                                    self.read_input_signal.emit(std)
                                self._conn_for_execution.send(self._input)
                                self._input = None
                    except (OSError, EOFError):
                        pass
                    except:
                        __import__('traceback').print_exc()
                if not self._manual_stop:
                    self.kernel_stopped.emit()
            except:
                __import__('traceback').print_exc()

    @QtCore.Slot()
    def interrupt(self):
        try:
            self._conn_for_interrupting.send('interrupt')
        except:
            pass

    @QtCore.Slot()
    def exit(self):
        try:
            self._conn_for_interrupting.close()
        except:
            pass
        try:
            self._conn_for_execution.close()
        except:
            pass
        self._manual_stop = True


class ExecutionProcess(QtCore.QObject):
    kernel_stopped = QtCore.Signal()
    error_occurred = QtCore.Signal()
    ready_for_execution = QtCore.Signal()

    _set_input = QtCore.Signal(str)
    _set_code_block = QtCore.Signal(str)

    _read_input_signal = QtCore.Signal(str)

    def __init__(self,
                 env_path: str,
                 *,
                 address: str = 'localhost',
                 port: Union[int, None] = None,
                 password: bytes = b'secret'):
        super().__init__()
        self._env_path = env_path
        if 'win32' in platform:
            scripts_dir = 'Scripts'
        else:
            scripts_dir = 'bin'
        self._path = os.path.join(self._env_path, scripts_dir)
        self._path_to_activate = os.path.join(self._env_path, scripts_dir, 'activate')
        self._path_to_python = os.path.join(self._env_path, scripts_dir, 'python')
        if port is None or port < 49152 or port > 65535:
            port = 0
        self._current_indicator_label = None
        self._current_output_box = None
        self._exec_process = None
        self._dialog = QtWidgets.QInputDialog()
        self._exec_deque = deque()

        # locks
        self._ui_lock = Lock()
        self._deque_lock = Lock()

        # thread
        self._thread = QtCore.QThread()
        # qobject
        self._worker = Worker(self._path, address, port, password)
        # connect signals to slots
        self._worker.moveToThread(self._thread)
        self._worker.update_ui.connect(self._update_ui, QtCore.Qt.BlockingQueuedConnection)
        self._worker.kernel_stopped.connect(self.kernel_stopped, QtCore.Qt.BlockingQueuedConnection)
        self._worker.clear_execution_queue.connect(self.clear_execution_queue_slot, QtCore.Qt.BlockingQueuedConnection)
        self._worker.error_occurred.connect(self.error_occurred, QtCore.Qt.BlockingQueuedConnection)
        self._worker.read_input_signal.connect(self.read_input_slot, QtCore.Qt.BlockingQueuedConnection)
        self._worker.get_block_signal.connect(self._get_next_block, QtCore.Qt.BlockingQueuedConnection)
        self._set_input.connect(self._worker.set_input)
        self._set_code_block.connect(self._worker.set_code_block)
        self._thread.started.connect(self._worker.run)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()
        self.restart()

    @QtCore.Slot(int, str, str)
    def _update_ui(self, n: int, std: str, received_output: str):
        with self._ui_lock:
            if self._current_output_box is not None:
                if received_output and '\r' in received_output:
                    text_cursor = self._current_output_box.textCursor()
                    text_cursor.movePosition(QtGui.QTextCursor.End)
                    block = text_cursor.block()
                    position = text_cursor.position()
                    text_cursor.setPosition(block.position())
                    text_cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
                    text_cursor.removeSelectedText()
                    self._current_output_box.setTextCursor(text_cursor)
                    received_output = received_output[received_output.rfind('\r') + 1:]
                if received_output and '\b' in received_output:
                    backspace = 0
                    s = ''
                    for x in reversed(received_output):
                        if x == '\b':
                            backspace += 1
                        elif backspace > 0:
                            backspace -= 1
                        else:
                            s += x
                    received_output = s[::-1]
                if std == '<stderr>' or std == '<error>':
                    received_output = html_module.escape(received_output).replace(' ', '&nbsp;').replace('\n', '<br>')
                    self._current_output_box.insertHtml(f'<font color="red">{received_output}</font>')
                    if self._current_output_box.isHidden():
                        self._current_output_box.hide_show_slot(True)
                elif std == '<stdout>':
                    received_output = html_module.escape(received_output).replace(' ', '&nbsp;').replace('\n', '<br>')
                    self._current_output_box.insertHtml(f'<font color="black">{received_output}</font>')
                    if self._current_output_box.isHidden():
                        self._current_output_box.hide_show_slot(True)
                return_code = self.return_code()
                if isinstance(return_code, int):
                    out = f'Process finished with exit code {return_code}'
                    self._current_output_box.insertHtml(f'<font color="red">{out}</font>')
                    if self._current_output_box.isHidden():
                        self._current_output_box.hide_show_slot(True)
            if self._current_indicator_label is not None:
                if std == '<error>':
                    self._current_indicator_label.setText('[ERR]')
                elif std == '<block>':
                    if n != 0:
                        self._current_indicator_label.setText(f'[{n}]')

    @QtCore.Slot(str)
    def read_input_slot(self, std):
        multi_string = (std == '<read>' or std == '<readlines>')
        q_caption = 'многострочного' if multi_string else 'однострочного'
        q_quotes = '"""' if multi_string else '"'
        items = [
            f'{q_quotes}без экранирования{q_quotes}',
            f'r{q_quotes}обычный, с экранированием{q_quotes}',
            f'b{q_quotes}байтовая строка, без экранирования{q_quotes}',
            f'rb{q_quotes}байтовая строка, с экранированием{q_quotes}'
        ]
        text = ''
        status = False
        while not status:
            input_type, status = self._dialog.getItem(None, f'Запрос {q_caption} ввода',
                                                      'Выберите режим ввода', items, 1, False)
            if status:
                if std == '<read>' or std == '<readlines>':
                    text, status = self._dialog.getMultiLineText(None,
                                                                 'Запрос многострочного ввода',
                                                                 'Введите запрашиваемый текст',
                                                                 text)
                else:
                    text, status = self._dialog.getText(None,
                                                        'Запрос однострочного ввода',
                                                        'Введите запрашиваемый текст',
                                                        QtWidgets.QLineEdit.Normal,
                                                        text)
                if status:
                    try:
                        if input_type == items[0]:
                            text = text.replace('\\\"', '"').replace('"', '\\\"')
                            text = ast.literal_eval(f'{q_quotes}{text}{q_quotes}')
                        elif input_type == items[2]:
                            text = text.replace('\\\"', '"').replace('"', '\\\"')
                            text = ast.literal_eval(f'b{q_quotes}{text}{q_quotes}')
                        elif input_type == items[3]:
                            text = text.replace('\\\"', '"').replace('"', '\\\"')
                            text = ast.literal_eval(f'rb{q_quotes}{text}{q_quotes}')
                    except BaseException as e:
                        e = e.args
                        if isinstance(e, tuple) and e:
                            e = e[0]
                        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question,
                                              'Ошибка',
                                              f'Ошибка ввода: {e}',
                                              QtWidgets.QMessageBox.Ok,
                                              None).exec()
                        status = False
                        continue
                    break
        self._worker.set_input(text)

    def __del__(self):
        self.kill()

    def kill(self):
        self.interrupt_execution()
        if self._exec_process is not None:
            self._worker.exit()
            self._exec_process.terminate()
            self._exec_process = None
        with self._ui_lock:
            self._current_indicator_label = None
            self._current_output_box = None

    def restart(self):
        if self._exec_process is not None:
            self.kill()
        with open(CLIENT_PATH, mode='r', encoding='utf-8') as fp, \
                tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py',
                                            dir=self._env_path, delete=False) as tmp:
            tmp.write(fp.read())
            tmp.flush()
            filename = tmp.name
        self._exec_process = subprocess.Popen([self._path_to_python, '-uBq', filename,
                                               f'--address={self._worker.address}',
                                               f'--port={self._worker.port}',
                                               f'--password={self._worker.password.decode("utf-8")}'],
                                              stdin=subprocess.DEVNULL,
                                              stderr=subprocess.STDOUT,
                                              cwd=self._env_path)

    @QtCore.Slot()
    def _get_next_block(self):
        try:
            if isinstance(self.return_code(), int):
                self._worker.set_code_block('')
                return
            if not self._exec_deque:
                self.ready_for_execution.emit()
                return
            with self._deque_lock:
                indicator_label, code_editor, output_box = self._exec_deque.popleft()
                with self._ui_lock:
                    self._current_indicator_label = indicator_label
                    self._current_output_box = output_box
                    code = code_editor.toPlainText()
            self._worker.set_code_block(code)
        except:
            __import__('traceback').print_exc()

    @QtCore.Slot(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit)
    def add_to_execution_queue(self, indicator_label: QtWidgets.QLabel,
                               code_editor: QtWidgets.QTextEdit,
                               output_box: QtWidgets.QTextEdit):
        if isinstance(self.return_code(), int):
            self.kernel_stopped.emit()
            return
        with self._deque_lock:
            self._exec_deque.append((indicator_label, code_editor, output_box))
            indicator_label.setText('[...]')
            output_box.setPlainText('')

    @QtCore.Slot(QtWidgets.QLabel, QtWidgets.QTextEdit, QtWidgets.QTextEdit, bool)
    def stop_block_execution(self, indicator_label: QtWidgets.QLabel,
                             code_editor: QtWidgets.QTextEdit,
                             output_box: QtWidgets.QTextEdit,
                             del_reason: bool):
        with self._ui_lock, self._deque_lock:
            new_deque = deque()
            found = False
            for indicator_label_avail, code_editor_avail, output_box_avail in self._exec_deque:
                if not found:
                    if indicator_label is indicator_label_avail:
                        found = True
                        indicator_label_avail.setText('')
                        continue
                    new_deque.appendleft((indicator_label_avail, code_editor_avail, output_box_avail))
                else:
                    indicator_label_avail.setText('')
            if not found:
                new_deque.clear()
                if indicator_label is self._current_indicator_label:
                    self._worker.interrupt()
                    self._current_indicator_label.setText('[STOP]')
                    self._current_indicator_label = None
                for indicator_label_avail, code_editor_avail, output_box_avail in self._exec_deque:
                    indicator_label_avail.setText('')
            if del_reason:
                self._current_indicator_label = None
                self._current_output_box = None
            self._exec_deque = new_deque

    @QtCore.Slot()
    def clear_execution_queue_slot(self):
        with self._deque_lock:
            for indicator_label_avail, code_editor_avail, output_box_avail in self._exec_deque:
                indicator_label_avail.setText('')
            self._exec_deque.clear()

    @QtCore.Slot()
    def interrupt_execution(self):
        self.clear_execution_queue_slot()
        self._worker.interrupt()

    def return_code(self) -> Union[int, None, type(...)]:
        if self._exec_process is None:
            return ...
        return self._exec_process.poll()


class ExecutionEnvironment(QtCore.QObject):
    def __init__(self, env_path: Union[str, None] = None):
        """
        Environment
        :param env_path: str path or None (if None => temp environment)
        """
        super().__init__()
        if not (env_path is None or isinstance(env_path, str)):
            raise ValueError('ExecutionEnvironment. Path to environment must be str or None')
        self.check_path(env_path)  # may throw
        self._env_path = env_path
        self._temporary_directory = None
        self._listener = None
        self._exec_processes = []
        self._created = False

    def create(self, clear_all_before_creating=False):
        """
        Create environment
        :param clear_all_before_creating: must be clear all files and dirs in env path before activating
        """
        if self._created:
            raise Exception('already created')
        try:
            if self._env_path is None:
                self._temporary_directory = tempfile.TemporaryDirectory(prefix='execution_environment_',
                                                                        ignore_cleanup_errors=True)
            else:
                self._temporary_directory = None
            env_path = self.path()
            self.check_path(env_path)
            env = venv.EnvBuilder(system_site_packages=False, clear=clear_all_before_creating,
                                  symlinks=False, upgrade=False, with_pip=True)
            env.create(env_path)
            self._created = True
        except PermissionError:
            self._created = True  # if exists and python.exe is started
        except:
            __import__('traceback').print_exc()

    def delete(self):
        """
        Delete environment (with env directory)
        """
        if self._created:
            self.kill_all_processes()
            if isinstance(self._temporary_directory, tempfile.TemporaryDirectory):
                self._temporary_directory.cleanup()
            elif os.path.exists(self._env_path):
                shutil.rmtree(self._env_path)
            self._temporary_directory = None
            self._created = False

    def path(self):
        """
        Return path to environment
        """
        if isinstance(self._temporary_directory, tempfile.TemporaryDirectory):
            return self._temporary_directory.name
        if self._env_path:
            return self._env_path

    @staticmethod
    def check_path(path: Union[str, None]):
        """
        Check path: exists; is dir; have read, write and execute access permissions
        :param path: path to check
        :raises NotADirectoryError if not exists or not dir
        :raises PermissionError if not have read, write and execute access permissions
        """
        if path is None:
            return
        if not os.path.exists(path) or not os.path.isdir(path):
            raise NotADirectoryError('ExecutionEnvironment. Path to environment must exist or be None')
        if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
            raise PermissionError('ExecutionEnvironment. Env directory must have all access permissions')

    def create_execution_process(self, *,
                                 address: str = 'localhost',
                                 port: Union[int, None] = None,
                                 password: bytes = b'secret') -> ExecutionProcess:
        """
        Create execution process
        """
        if self._created:
            exec_process = ExecutionProcess(env_path=self.path(),
                                            address=address,
                                            port=port,
                                            password=password)
            self._exec_processes.append(exec_process)
            return exec_process

    def interrupt_all_processes(self):
        """
        Interrupt execution processes
        """
        for exec_process in self._exec_processes:
            exec_process.interrupt_execution()

    def kill_all_processes(self):
        """
        Kill execution processes
        """
        for exec_process in self._exec_processes:
            exec_process.kill()
        self._exec_processes.clear()
