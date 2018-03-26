import sys
import lexer

# name = sys.argv[1] 
name = "tests/calc.elg" 

with open(name, 'r') as content_file:
    f = content_file.read()

    lex = lexer.Lexer(f)

    print(f)