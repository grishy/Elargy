import re
import json
import os


class ElLexer:
    token_specification = {
        # Special
        '_NEWLINE':  r'\n',
        '_SKIP':     r'[ \t]+',
        '_MISMATCH': r'.',
    }

    line_num = 1
    line_start = 0

    # Объединенный правила
    tok_regex = ""
    # Все токены после обработки
    tokens = []

    def __init__(self, tokens):
        all_tokens = {**tokens, **self.token_specification}
        regex_group = ['(?P<{}>{})'.format(key, value)
                       for key, value in all_tokens.items()]

        self.tok_regex = '|'.join(regex_group)

    def tokenize(self, text):
        for mo in re.finditer(self.tok_regex, text):
            type_ = mo.lastgroup
            value = mo.group(type_)

            if type_ == '_NEWLINE':
                line_start = mo.end()
                self.line_num += 1
            elif type_ == '_SKIP':
                pass
            elif type_ == '_MISMATCH':
                raise RuntimeError(
                    f'{value!r} unexpected on line {self.line_num}')
            else:
                column = mo.start() - self.line_start
                self.__add_token(type_, value, column)
        # Запись результата в файл
        self.__export()

    def __add_token(self, type_, value, column):
        self.tokens.append({
            "type": type_,
            "value": value,
            "line": self.line_num,
            "column": column
        })

    def __export(self):
        with open("./steps/lexer.json", 'w+') as f:
            f.write(json.dumps(self.tokens, indent=2))

    def get_tokens(self):
        return self.tokens
