import os
import re


def ui2py(target_folder='.', output_folder=None, recursive=True):
    # find all files
    files = []
    if recursive:
        for folder, _, folder_files in os.walk(target_folder):
            for file in folder_files:
                files.append(os.path.join(folder, file))
    else:
        folder, _, folder_files = next(os.walk(target_folder))
        for file in folder_files:
            files.append(os.path.join(folder, file))
    # filter ui files
    pattern = re.compile(r'^.*\.ui$', re.IGNORECASE)
    ui_files = []
    for file in files:
        if pattern.match(file):
            ui_files.append(file)
    # convert ui files to py
    for ui_file in ui_files:
        if output_folder is None:
            py_file = ui_file[:ui_file.rfind('.')]
        else:
            basename_wo_ext = os.path.basename(ui_file)
            basename_wo_ext = basename_wo_ext[:basename_wo_ext.rfind('.')]
            py_file = os.path.join(output_folder, basename_wo_ext)
        cmd = f'pyside6-uic --from-imports {ui_file} > {py_file}.py'
        os.popen(cmd)


if __name__ == '__main__':
    ui2py(target_folder=os.path.join('..', 'resources'), output_folder=os.path.join('..', 'views', 'autogen'))
