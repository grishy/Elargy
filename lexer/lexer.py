import collections
import re
import json

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

def tokenize(code):

    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}

    token_specification = [
        ('NUMBER',  r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',  r':='),           # Assignment operator
        ('END',     r';'),            # Statement terminator
        ('ID',      r'[A-Za-z]+'),    # Identifiers
        ('OP',      r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE', r'\n'),           # Line endings
        ('SKIP',    r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',r'.'),            # Any other character
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
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

            tokens.append(Token(kind, value, line_num, column))
    
    return tokens

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

# To list of tokens
tokens = tokenize(statements)

print(json.dumps(tokens, indent=2))