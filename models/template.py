import os
import pathlib
import re
from typing import List, Tuple

from slugify import slugify

DATASETS_TEMPLATES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'datasets')
assert os.path.exists(DATASETS_TEMPLATES_DIR), \
    f"Directory '{DATASETS_TEMPLATES_DIR}' is not exists"
assert os.path.isdir(DATASETS_TEMPLATES_DIR), \
    f"Object '{DATASETS_TEMPLATES_DIR}' is not a directory"

ARCHITECTURE_TEMPLATES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'architecture')
assert os.path.exists(ARCHITECTURE_TEMPLATES_DIR), \
    f"Directory '{ARCHITECTURE_TEMPLATES_DIR}' is not exists"
assert os.path.isdir(ARCHITECTURE_TEMPLATES_DIR), \
    f"Object '{ARCHITECTURE_TEMPLATES_DIR}' is not a directory"

TRAIN_VAL_TEST_TEMPLATES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'train_val_test')
assert os.path.exists(TRAIN_VAL_TEST_TEMPLATES_DIR), \
    f"Directory '{TRAIN_VAL_TEST_TEMPLATES_DIR}' is not exists"
assert os.path.isdir(TRAIN_VAL_TEST_TEMPLATES_DIR), \
    f"Object '{TRAIN_VAL_TEST_TEMPLATES_DIR}' is not a directory"

VISUALIZATION_TEMPLATES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'visualization')
assert os.path.exists(VISUALIZATION_TEMPLATES_DIR), \
    f"Directory '{VISUALIZATION_TEMPLATES_DIR}' is not exists"
assert os.path.isdir(VISUALIZATION_TEMPLATES_DIR), \
    f"Object '{VISUALIZATION_TEMPLATES_DIR}' is not a directory"

EXPORT_TEMPLATES_DIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'export')
assert os.path.exists(EXPORT_TEMPLATES_DIR), \
    f"Directory '{EXPORT_TEMPLATES_DIR}' is not exists"
assert os.path.isdir(EXPORT_TEMPLATES_DIR), \
    f"Object '{EXPORT_TEMPLATES_DIR}' is not a directory"


def list_templates(dir: str) -> List[Tuple[str, str, str]]:
    dir_path, dir_names, filenames = next(os.walk(dir,
                                                  topdown=True,
                                                  onerror=None,
                                                  followlinks=False), ('', [], []))
    filenames = [os.path.join(dir, filename) for filename in filenames]
    template_name_re = re.compile(r'# template-name:(.*)')
    template_type_re = re.compile(r'# template-type:(.*)')
    files = []  # list of tuples: (filename, template-name, template-type)
    for filename in filenames:
        try:
            template_name = None
            template_type = None
            with open(filename, 'r', encoding='utf-8') as fp:
                for line in fp.readlines():
                    line = line.strip(' \t\r\n')
                    match = template_name_re.match(line)
                    if bool(match):
                        if template_name is None:
                            template_name = match.group(1).lstrip(' \t')
                        else:
                            template_name += '\n' + match.group(1).lstrip(' \t')
                    if template_type is None:
                        match = template_type_re.match(line)
                        if bool(match):
                            template_type = match.group(1).lstrip(' \t')
            if template_name is not None and template_type is not None:
                files.append((filename, template_type, template_name))
        except:
            __import__('traceback').print_exc()
    return files


def get_template(dir: str, filename: str) -> List[Tuple[str, str, str]]:
    dir_path, dir_names, filenames = next(os.walk(dir,
                                                  topdown=True,
                                                  onerror=None,
                                                  followlinks=False), ('', [], []))
    filenames = [os.path.join(dir, filename) for filename in filenames]
    if filename in filenames:
        template_code_block_name_re = re.compile(r'#\s*?<code-block>(.*)')
        template_text_block_name_re = re.compile(r'#\s*?<text-block>(.*)')
        with open(filename, mode='r', encoding='utf-8') as fp:
            blocks = []  # elem -- tuple: (Type:Union['code', 'text'], Caption: str, Content: str)
            current_block = []
            for line in fp.readlines():
                line = line.rstrip(' \t\r\n')
                match_code_block = template_code_block_name_re.match(line)
                match_text_block = template_text_block_name_re.match(line)
                if bool(match_code_block) or bool(match_text_block):
                    if current_block:
                        blocks.append(tuple(current_block))
                    if bool(match_code_block):
                        block_type = 'code'
                        caption = match_code_block.group(1).lstrip(' \t')
                    else:
                        block_type = 'text'
                        caption = match_text_block.group(1).lstrip(' \t')
                    current_block = [block_type, caption, '']
                    continue
                if current_block:
                    current_block[2] += '\n' * bool(current_block[2]) + line
            if current_block:
                blocks.append(tuple(current_block))
        return blocks
    return [('text', '', 'no template found')]


def create_template(dir_or_filename: str, template_type: str,
                    template_name: str, blocks: List[Tuple[str, str, str]],
                    rename: bool = False):
    lines = []
    for name_part in template_name.splitlines():
        name_part = name_part.strip(" \t\r\n")
        lines.append(f'# template-name: {name_part}')
    template_type = template_type.strip(" \t\r\n")
    lines.append(f'# template-type: {template_type}')
    for block_type, caption, content in blocks:
        if block_type == 'code':
            caption = caption.strip(" \t\r\n")
            lines.append(rf'# <code-block> {caption}')
            lines.append(content)
        elif block_type == 'text':
            caption = caption.strip(" \t\r\n")
            lines.append(rf'# <text-block> {caption}')
            lines.append(content)
    dir = dir_or_filename if os.path.isdir(dir_or_filename) else os.path.dirname(dir_or_filename)
    if rename or os.path.isdir(dir_or_filename):
        filename = slugify(f'{template_type}_{template_name}',
                           entities=True, decimal=True, hexadecimal=True, max_length=50,
                           word_boundary=True, separator='_')
        filename = os.path.join(dir, filename + '.py')
    else:
        filename = dir_or_filename
    with open(filename, mode='w') as fp:
        fp.write('\n'.join(lines))
    return filename


def edit_template(filename: str, template_type: str, template_name: str, blocks: List[Tuple[str, str, str]],
                  rename: bool = False):
    template_filename = create_template(filename, template_type, template_name, blocks, rename)
    if os.path.isfile(filename) and os.path.exists(filename) and os.path.exists(template_filename) and \
            os.path.abspath(filename) != os.path.abspath(template_filename):
        del_template(filename)


def del_template(filename: str):
    os.remove(filename)
