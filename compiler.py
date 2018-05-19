import sys
import el_lexer
import el_grammar
import el_table

# name = sys.argv[1]
name = "examples/calc.elg"
steps = "steps/"

with open(name, 'r') as content_file:
    f = content_file.read()

    # Lexer
    lex = el_lexer.ElLexer(f)
    lex.tokenize()
    # Save to temp dir
    lexerOut = open(steps + 'lexer.json', 'w+')
    lexerOut.write(lex.toJSON())
    lexerOut.close()

    # Grammar
    grammar = el_grammar.ElGrammar("grammar.bnf")
    # Save to temp dir
    grammarOut = open(steps + 'grammar.txt', 'w+')
    grammarOut.write(grammar.toText())
    grammarOut.close()

    # Table
    table = el_table.ElTable(grammar)
    # Save to temp dir
    # tableOut = open(steps + 'table.txt', 'w+')
    # tableOut.write(table.toText())
    # tableOut.close()
