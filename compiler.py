import sys
import lexer

# name = sys.argv[1] 
name = "tests/calc.elg" 

with open(name, 'r') as content_file:
    f = content_file.read()

    # To tokens
    lex = lexer.Lexer(f)
    lex.tokenize()
    # Save to temp dir
    lexerOut = open('temp/lexer.json', 'w+')
    lexerOut.write(lex.toJSON())
    lexerOut.close()


    # Parse
    