import sys
import el_lexer
import el_parse

# name = sys.argv[1]
name = "examples/calc.elg"
steps = "steps/"

with open(name, 'r') as content_file:
    f = content_file.read()

    # To tokens
    lex = el_lexer.ElLexer(f)
    lex.tokenize()
    # Save to temp dir
    lexerOut = open(steps + 'lexer.json', 'w+')
    lexerOut.write(lex.toJSON())
    lexerOut.close()

    # Parser
    parse = el_parse.ElParser("grammar.bnf")
    # parse.Parse(lex)
    # parser.toJSON()
