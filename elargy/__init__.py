import yaml
import elargy.el_lexer


def Parse(text, steps=None):
    if not steps:
        print("Без вывода промежуточных состояний")

    print(text)
