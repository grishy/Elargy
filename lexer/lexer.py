import collections
import re
import json

TOKENS = []


def addToken(kind, value, line_num, column):
    global TOKENS

    # Export
    # {
    #     "typ": "ID",
    #     "val": "tax",
    #     "line": 1,
    #     "column": 10,
    # }
    TOKENS.append({
        "typ": kind,
        "val": value,
        "line": line_num,
        "column": column
    })


def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}

    token_specification = [
        ('NUMBER',  r'\d+(\.\d*)?'),
        ('ASSIGN',  r':='),
        ('END',     r';'),
        ('ID',      r'[A-Za-z]+'),
        ('OP',      r'[+\-*/]'),
        ('NEWLINE', r'\n'),
        ('SKIP',    r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    line_num = 1
    line_start = 0

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
            if kind == 'ID' and value in keywords:
                kind = value
            column = mo.start() - line_start

            addToken(kind, value, line_num, column)


statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

# To list of tokens
tokenize(statements)

print(json.dumps(TOKENS, indent=2))
