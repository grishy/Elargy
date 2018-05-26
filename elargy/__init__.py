import elargy.el_lexer
import elargy.grammar


def Parse(text):
    lexer = el_lexer.ElLexer(grammar.tokens)
    lexer.tokenize(text)


