# venv-2

import argparse
import os
import sys
from _thread import get_native_id
from code import InteractiveInterpreter
from io import TextIOWrapper, BytesIO
from multiprocessing.connection import Client, Connection
from threading import Thread, Event

parser = argparse.ArgumentParser(prog='client.py')
parser.add_argument('--address', nargs='?', help='address ("localhost" by default)')
parser.add_argument('--port', nargs='?', help='port ("60000" by default)')
parser.add_argument('--password', nargs='?', help='password ("secret" by default)')
args = parser.parse_args()

if os.path.exists(__file__) and os.path.basename(__file__).startswith('tmp'):
    os.remove(__file__)


class Redirector(TextIOWrapper):
    def __init__(self, conn: Connection, std: TextIOWrapper):
        super().__init__(buffer=BytesIO(), encoding=std.encoding, errors=std.errors,
                         newline=std.newlines, line_buffering=std.line_buffering,
                         write_through=std.write_through)
        self.std = std
        self._conn = conn

    def read(self, size: int = None) -> str:
        try:
            self._conn.send(('<read>', 'read operation'))
            return self._conn.recv()
        except BaseException as e:
            print(e, file=sys.__stderr__)
            return ''

    def readline(self, size: int = None) -> str:
        try:
            self._conn.send(('<readline>', 'readline operation'))
            return self._conn.recv()
        except BaseException as e:
            print(e, file=sys.__stderr__)
            return ''

    def readlines(self, hint: int = None) -> list[str]:
        try:
            self._conn.send(('<readlines>', 'readlines operation'))
            return self._conn.recv().splitlines()
        except BaseException as e:
            print(e, file=sys.__stderr__)
            return []

    def write(self, data):
        try:
            self._conn.send((self.std.name, data))
        except BaseException as e:
            print(e, file=sys.__stderr__)

    def writelines(self, lines: list[str]):
        try:
            self._conn.send((self.std.name, '\n'.join(lines)))
        except BaseException as e:
            print(e, file=sys.__stderr__)


class CodeBlocksInterpreter(InteractiveInterpreter):
    def __init__(self, conn_for_execution: Connection, conn_for_interrupting: Connection, locals: dict = None):
        super().__init__()
        self.locals = locals
        self._conn_for_execution = conn_for_execution
        self._conn_for_interrupting = conn_for_interrupting
        self._main_thread_id = get_native_id()
        self._ready_for_next_block = Event()
        self._ready_for_next_block.clear()
        self._can_interrupt = Event()
        self._can_interrupt.clear()
        self._thread = Thread(target=self._stop_and_exit_thread, daemon=False)

    def interact(self):
        self._thread.start()
        try:
            filename = '<input>'
            symbol = 'exec'
            while True:
                self._can_interrupt.clear()
                self._ready_for_next_block.wait()
                try:
                    self._conn_for_execution.send(('<block>', 'give me next block'))
                    code_block = self._conn_for_execution.recv() + '\n'
                    code = self.compile(source=code_block, filename=filename, symbol=symbol)
                    if code is None:
                        self.write('EOFError. Code block is incomplete')
                        continue
                    self._can_interrupt.set()
                    self.runcode(code)
                    self._can_interrupt.clear()
                except KeyboardInterrupt as e:
                    print(e, file=sys.__stderr__)
                except (OverflowError, SyntaxError, ValueError):
                    self.showsyntaxerror(filename)
                except SystemExit:
                    break
        except BaseException as e:
            print(e, file=sys.__stderr__)
        try:
            self._conn_for_execution.close()
        except:
            pass
        try:
            self._conn_for_interrupting.close()
        except:
            pass

    def _stop_and_exit_thread(self):
        try:
            while True:
                try:
                    self._ready_for_next_block.set()
                    received = self._conn_for_interrupting.recv()
                    if received == 'interrupt':
                        self._ready_for_next_block.clear()
                        if self._can_interrupt.is_set():
                            import ctypes
                            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._main_thread_id),
                                                                       ctypes.py_object(KeyboardInterrupt))
                    elif received == 'exit':
                        import ctypes
                        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._main_thread_id),
                                                                   ctypes.py_object(SystemExit))
                        break
                except (ConnectionResetError, EOFError):
                    break
        except BaseException as e:
            print(e, file=sys.__stderr__)

    def write(self, data: str):
        self._conn_for_execution.send(('<error>', data))


ADDRESS = args.address.strip('"\'') if isinstance(args.address, str) else 'localhost'
PORT = int(args.port) if isinstance(args.port, str) and args.port.isdigit() else 60000
PASS = args.password.strip('"\'').encode('utf-8') if isinstance(args.password, str) else b'secret'

# Two clients: one for executing code blocks and one for interrupting execution
try:
    with Client((ADDRESS, PORT), authkey=PASS) as conn_for_execution, \
            Client((ADDRESS, PORT), authkey=PASS) as conn_for_interrupting:
        sys.stdin = Redirector(conn_for_execution, sys.stdin)
        sys.stdout = Redirector(conn_for_execution, sys.stdout)
        sys.stderr = Redirector(conn_for_execution, sys.stderr)
        sys.__stdin__ = Redirector(conn_for_execution, sys.__stdin__)
        sys.__stdout__ = Redirector(conn_for_execution, sys.__stdout__)
        sys.__stderr__ = Redirector(conn_for_execution, sys.__stderr__)
        code_blocks_interpreter = CodeBlocksInterpreter(conn_for_execution, conn_for_interrupting,
                                                        locals={'__name__': '__main__'})
        code_blocks_interpreter.interact()
except:
    pass

if isinstance(sys.stdin, Redirector):
    sys.stdin = sys.stdin.std
if isinstance(sys.stdout, Redirector):
    sys.stdout = sys.stdout.std
if isinstance(sys.stderr, Redirector):
    sys.stderr = sys.stderr.std
if isinstance(sys.__stdin__, Redirector):
    sys.__stdin__ = sys.__stdin__.std
if isinstance(sys.__stdout__, Redirector):
    sys.__stdout__ = sys.__stdout__.std
if isinstance(sys.__stderr__, Redirector):
    sys.__stderr__ = sys.__stderr__.std
