# venv-1

import sys
from multiprocessing.connection import Listener, Connection


def read_write_function(conn_for_execution: Connection, conn_for_interrupting: Connection):
    try:
        while True:
            try:
                std, received_output = conn_for_execution.recv()
            except (ConnectionResetError, KeyboardInterrupt, EOFError) as e:
                print(e)
                break
            if std in ('<stderr>', '<stdout>'):
                file = sys.stderr if std == '<stderr>' else sys.stdout
                print('stream:', std)
                print('message:', repr(received_output)[1:-1], file=file)
            elif std == '<error>':  # error
                print('error:', repr(received_output)[1:-1], file=sys.stderr)
            elif std in ('<block>', '<read>', '<readlines>'):  # next block query or read input
                print('[Ctrl+C to send code block to client]')
                lines = []
                try:
                    while True:
                        line = input(std[1:] + ' ')
                        lines.append(line)
                except (KeyboardInterrupt, EOFError):
                    conn_for_execution.send('\n'.join(lines))
                    print(('' if lines else 'nothing ') + 'sended')
                    # --------------------- <!-- only to emulate "interrupt execution"
                    if lines and lines[-1] == '#interrupt':
                        print('[SERVER] Sleep before')
                        import time
                        time.sleep(3)
                        conn_for_interrupting.send('interrupt')
                        print('[SERVER] Interrupt message sended')
                    # --------------------- --> only to emulate "interrupt execution"
                    # --------------------- <!-- only to emulate "exit"
                    if lines and lines[-1] == '#exit':
                        print('[SERVER] Sleep before')
                        import time
                        time.sleep(3)
                        conn_for_interrupting.send('exit')
                        print('[SERVER] Exit message sended')
                    # --------------------- --> only to emulate "exit"
            elif std == '<readline>':
                print('[one line to send input data to client]')
                conn_for_execution.send(input(std[1:] + ' '))
                print(std[1:] + ' sended')
    except:
        __import__('traceback').print_exc()


ADDRESS = 'localhost'
PORT = 60000
PASS = 'secret'

print('#' * 42)
print('Address:', ADDRESS)
print('Port:', PORT)
print('Pass:', PASS)
print('#' * 42)
print('Waiting for a client...')

# --------------------- <!-- only to run the client app on the server side and prevent Ctrl+C crashes

"""
import signal
import subprocess
import os


def pre_exec():
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # ignore CTRL+C signal in the new process


executable = [os.path.join(os.path.abspath('ClientSide'), 'venv', 'Scripts', 'python'), '-uBq', 'client.py',
              f'--address={ADDRESS}',
              f'--port={PORT}',
              f'--password={PASS}',
              stdin=subprocess.DEVNULL]
if sys.platform.startswith('win'):
    exec_process = subprocess.Popen(executable, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
else:
    exec_process = subprocess.Popen(executable, preexec_fn=pre_exec)
"""

# --------------------- --> only to run the client app on the server side and prevent Ctrl+C crashes


# backlog = 2 --> Two clients: one for executing code blocks and one for interrupting execution
try:
    with Listener((ADDRESS, PORT), authkey=PASS.encode(encoding='utf-8'), backlog=2) as listener, \
            listener.accept() as conn_for_execution, listener.accept() as conn_for_interrupting:
        print('Connections accepted')
        print('#' * 42)
        read_write_function(conn_for_execution, conn_for_interrupting)
except:
    pass
