import re
import json


class Lexer:
    token_specification = [
        ('NUMBER',  r'\d+'),
        ('PLUS',  r'\+'),
        ('NEWLINE', r'\n'),
        ('SKIP',    r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    # keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.line_num = 1
        self.line_start = 0

        self.tok_regex = '|'.join('(?P<%s>%s)' %
                                  pair for pair in Lexer.token_specification)

    def tokenize(self):
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group(kind)

            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            else:
                # if kind == 'ID' and value in keywords:
                #     kind = value
                column = mo.start() - line_start
                addToken(kind, value)

    def addToken(self, kind, value):
        self.tokens.append({
            "typ": kind,
            "val": value,
            "line": self.line_num,
            "column": self.column
        })

    def toJSON(self):
        return json.dumps(self.tokens, indent=2)
