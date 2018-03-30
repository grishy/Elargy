import re
import json


class Lexer:
    token_specification = [
        ('LPAREN',      r'\('),
        ('RPAREN',      r'\)'),
        ('LBRACE',      r'\{'),
        ('RBRACE',      r'\}'),
        ('COLON',       r'\:'),
        ('SEMICOLON',   r'\;'),
        ('INTEGER',     r'\d+'),
        ('ID',          r'[A-Za-z]+'),
        ('PLUS',        r'\+'),
        ('ASSIGN',      r'='),
        ('NEWLINE',     r'\n'),
        ('SKIP',        r'[ \t]+'),
        ('MISMATCH',    r'.'),
    ]

    keywords = {'func', 'var', 'int'}

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.line_num = 1
        self.line_start = 0

        self.tok_regex = '|'.join('(?P<%s>%s)' %
                                  pair for pair in Lexer.token_specification)

    def tokenize(self):
        for mo in re.finditer(self.tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group(kind)

            if kind == 'NEWLINE':
                line_start = mo.end()
                self.line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(
                    f'{value!r} unexpected on line {self.line_num}')
            else:
                if kind == 'ID' and value in self.keywords:
                    kind = value

                column = mo.start() - self.line_start
                self.addToken(kind, value, column)

    def addToken(self, kind, value, column):
        self.tokens.append({
            "typ": kind,
            "val": value,
            "line": self.line_num,
            "column": column
        })

    def toJSON(self):
        return json.dumps(self.tokens, indent=2)

    def getTokens(self):
        return self.tokens
