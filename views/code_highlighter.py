import keyword
import token
import tokenize
from copy import copy
from io import StringIO

from PySide6 import QtCore, QtGui, QtWidgets


class HighlightingRule:
    def __init__(self,
                 pattern: QtCore.QRegularExpression = None,
                 format: QtGui.QTextCharFormat = None):
        self.pattern = pattern
        self.format = format


class CodeHighlighter(QtGui.QSyntaxHighlighter):
    elements_foreground = {
        'KEYWORD': '#008000', 'BUILTIN_NAME': '#008000', 'DECORATOR': '#AA22FF',
        'CLASS_AND_DEF': '#0000FF', 'PROPERTY': '#0055AA', 'SELF': '#0055AA',
        token.LPAR: '#212121', token.RPAR: '#212121', token.COMMA: '#212121',
        token.DOT: '#212121', token.COLON: '#212121', token.SEMI: '#212121',
        token.LSQB: '#212121', token.RSQB: '#212121', token.LBRACE: '#212121',
        token.RBRACE: '#212121', token.STRING: '#BA2121', token.NUMBER: '#008800',
        token.NAME: '#212121', token.OP: '#AA22FF', token.ERRORTOKEN: '#FF0000',
        token.COMMENT: '#6E7781'
    }

    def __init__(self, text_editor: QtWidgets.QTextEdit):
        self.text_editor = text_editor
        super().__init__(text_editor.document())
        highlighting_rule = HighlightingRule()
        self.highlighting_rules = []

        # formats
        self.formats = dict()
        for element, color in self.elements_foreground.items():
            self.formats[element] = QtGui.QTextCharFormat()
            self.formats[element].setForeground(QtGui.QColor(color))

        # class, def
        highlighting_rule.format = copy(self.formats['CLASS_AND_DEF'])
        highlighting_rule.pattern = QtCore.QRegularExpression(r'(?<=class\s)(.*?)(?=[:(])|(?<=def\s)(.*?)(?=\()')
        self.highlighting_rules.append(copy(highlighting_rule))

        # keyword
        softkwlist = []
        try:
            softkwlist = list(keyword.softkwlist)
        except:
            pass
        keyword_patterns = list(keyword.kwlist) + softkwlist
        highlighting_rule.format = copy(self.formats['KEYWORD'])
        for pattern in keyword_patterns:
            highlighting_rule.pattern = QtCore.QRegularExpression(r'\b' + pattern + r'\b')
            self.highlighting_rules.append(copy(highlighting_rule))

        # builtin
        highlighting_rule.format = copy(self.formats['BUILTIN_NAME'])
        for builtin in set(__builtins__.keys()) | {'self'}:
            highlighting_rule.pattern = QtCore.QRegularExpression(r'\b' + builtin + r'\b')
            self.highlighting_rules.append(copy(highlighting_rule))

        # decorator
        highlighting_rule.format = copy(self.formats['DECORATOR'])
        highlighting_rule.pattern = QtCore.QRegularExpression(r'@\w+?\b')
        self.highlighting_rules.append(copy(highlighting_rule))

        # property/method
        highlighting_rule.format = copy(self.formats['PROPERTY'])
        highlighting_rule.pattern = QtCore.QRegularExpression(r'(?<=\.)[^0-9].+?\b')
        self.highlighting_rules.append(copy(highlighting_rule))

    def highlightBlock(self, text: str) -> None:
        text_copy = text
        previous_blocks = []
        previous_blocks_text = []
        previous_block = self.currentBlock().previous()
        while previous_block.isValid() and previous_block.userState() >= 1:
            previous_blocks.append(previous_block)
            previous_blocks_text.append(previous_block.text())
            previous_block = previous_block.previous()
        previous_blocks = previous_blocks[::-1]
        previous_blocks_text = previous_blocks_text[::-1]
        next_blocks = []
        next_blocks_text = []
        next_block = self.currentBlock().next()
        state_must_eq_1 = False
        while True:
            current_blocks = [*previous_blocks, self.currentBlock(), *next_blocks]
            current_blocks_text = [*previous_blocks_text, text_copy, *next_blocks_text]
            try:
                rules = []
                for tok in tokenize.generate_tokens(StringIO('\n'.join(current_blocks_text)).readline):
                    tok_format = None
                    if tok.exact_type in self.formats:
                        tok_format = self.formats[tok.exact_type]
                    elif tok.type in self.formats:
                        tok_format = self.formats[tok.type]
                    if tok_format:
                        start_line, start_position = tok.start
                        end_line, end_position = tok.end
                        start_line -= 1
                        end_line -= 1
                        rules.append((start_line, start_position, end_line, end_position, tok_format, tok.type))
                for start_line, start_position, end_line, end_position, tok_format, tok_type in rules:
                    for current_line_number in range(start_line, min(len(current_blocks), end_line + 1)):
                        current_block = current_blocks[current_line_number]
                        current_block_position = current_block.position()
                        from_ = 0
                        to_ = len(current_blocks_text[current_line_number]) - 1
                        if start_line == current_line_number:
                            from_ = start_position
                        if end_line == current_line_number:
                            to_ = end_position
                        count_ = to_ - from_
                        text_cursor = QtGui.QTextCursor(current_block)
                        text_cursor.setPosition(current_block_position + from_)
                        text_cursor.setPosition(current_block_position + to_, QtGui.QTextCursor.KeepAnchor)
                        text_cursor.setCharFormat(tok_format)
                        if tok_type is token.STRING:
                            current_blocks_text[current_line_number] = \
                                current_blocks_text[current_line_number][:from_] + '"' + ' ' * (count_ - 2) + \
                                '"' + current_blocks_text[current_line_number][to_:]
                        elif tok_type is token.COMMENT:
                            current_blocks_text[current_line_number] = \
                                current_blocks_text[current_line_number][:from_] + ' ' * count_ + \
                                current_blocks_text[current_line_number][to_:]
                        if current_line_number < end_line:
                            current_block.setUserState(1)
                break
            except BaseException as e:
                e = e.args
                if next_block.isValid():
                    while next_block.isValid():
                        next_blocks.append(next_block)
                        next_blocks_text.append(next_block.text())
                        next_block = next_block.next()
                    state_must_eq_1 = True
                    continue
                elif len(e) == 2 and isinstance(e[1], tuple):
                    gen = (x for x in e[1] if isinstance(x, int))
                    start_line = next(gen, 1)
                    start_position = next(gen, 0)
                    start_line -= 1
                    if start_line >= 1 and start_position == 0:
                        start_line -= 1
                        start_position = max(0, len(current_blocks_text[start_line]) - 1)
                    end_line, end_position = len(current_blocks), len(current_blocks_text[-1])
                    end_line -= 1
                    if current_blocks[-1].blockNumber() == self.currentBlock().blockNumber():
                        end_position = len(text_copy)
                    for current_line_number in range(start_line, min(len(current_blocks), end_line + 1)):
                        current_block = current_blocks[current_line_number]
                        current_block.setUserState(2)
                        current_block_position = current_block.position()
                        from_ = 0
                        to_ = len(current_blocks_text[current_line_number])
                        if start_line == current_line_number:
                            from_ = start_position
                        if end_line == current_line_number:
                            to_ = end_position
                        text_cursor = QtGui.QTextCursor(current_block)
                        text_cursor.setPosition(current_block_position + from_)
                        text_cursor.setPosition(current_block_position + to_, QtGui.QTextCursor.KeepAnchor)
                        text_cursor.setCharFormat(self.formats[token.ERRORTOKEN])
                self.setCurrentBlockState(2)
                return
        if state_must_eq_1:
            self.setCurrentBlockState(1)
        else:
            self.setCurrentBlockState(0)
        for current_block, current_block_text in zip(current_blocks, current_blocks_text):
            current_block_position = current_block.position()
            for rule in self.highlighting_rules:
                match_iterator = rule.pattern.globalMatch(current_block_text)
                while match_iterator.hasNext():
                    match = match_iterator.next()
                    from_ = match.capturedStart()
                    to_ = match.capturedEnd()
                    count_ = to_ - from_
                    text_cursor = QtGui.QTextCursor(current_block)
                    text_cursor.setPosition(current_block_position + from_)
                    text_cursor.setPosition(current_block_position + to_, QtGui.QTextCursor.KeepAnchor)
                    text_cursor.setCharFormat(rule.format)
                    current_block_text = current_block_text[:from_] + ' ' * count_ + current_block_text[to_:]
        return
