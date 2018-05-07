import sys
import lexer

# name = sys.argv[1] 
name = "examples/main.elg" 
steps = "steps/" 

with open(name, 'r') as content_file:
    f = content_file.read()

    # To tokens
    lex = lexer.Lexer(f)
    lex.tokenize()
    # Save to temp dir
    lexerOut = open(steps +'lexer.json', 'w+')
    lexerOut.write(lex.toJSON())
    lexerOut.close()


    # Parse
    print('parse')