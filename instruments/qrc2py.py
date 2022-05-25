import os
import re


def qrc2py(target_folder='.', output_folder=None, recursive=True):
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
    # filter qrc files
    pattern = re.compile(r'^.*\.qrc$', re.IGNORECASE)
    qrc_files = []
    for file in files:
        if pattern.match(file):
            qrc_files.append(file)
    # convert qrc files to py
    for qrc_file in qrc_files:
        if output_folder is None:
            py_file = os.path.basename(qrc_file)[:qrc_file.rfind('.')]
        else:
            basename_wo_ext = os.path.basename(qrc_file)
            basename_wo_ext = basename_wo_ext[:basename_wo_ext.rfind('.')]
            py_file = os.path.join(output_folder, basename_wo_ext)
        cmd = f'pyside6-rcc {qrc_file} > {py_file}_rc.py'
        os.popen(cmd)


if __name__ == '__main__':
    qrc2py(target_folder=os.path.join('..', 'resources'), output_folder=os.path.join('..', 'views', 'autogen'))
