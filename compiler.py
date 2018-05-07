import sys
import lexer

# name = sys.argv[1]
name = "examples/calc.elg"
steps = "steps/"

NotTerm = []
prod = []
IDX = 1


class Symb:
    def __init__(self, name):
        self.name = name
        self.term = True if name in NotTerm else False
        self.left = []
        self.right = []

    def prnt(self):
        print(self.name, self.term, self.left, self.right)

def findAllProd(name):
    return [x for x in prod if name == x[0]]

def setIndex(name, idx):
    pList = findAllProd(name)

    for p in pList:
        print(p)


# Grammar
with open("grammar.bnf", "r") as content_file:
    lines = content_file.readlines()

    prod = [x.split(':') for x in lines]

    for i in range(len(prod)):
        prod[i] = [x.strip() for x in prod[i]]
        prod[i][1] = prod[i][1].split()

    NotTerm = set([x[0] for x in prod])

    for i in range(len(prod)):
        for y in range(len(prod[i][1])):
            prod[i][1][y] = Symb(prod[i][1][y])

    
with open(name, 'r') as content_file:
    f = content_file.read()

    # To tokens
    lex = lexer.Lexer(f)
    lex.tokenize()
    # Save to temp dir
    lexerOut = open(steps + 'lexer.json', 'w+')
    lexerOut.write(lex.toJSON())
    lexerOut.close()


    # Parser
    setIndex("S", 1)

    print("*" * 15)
    print(NotTerm)
    for x in prod:
        print(x[0])
        
        for i in x[1]:
            i.prnt()
        
        print("=" * 5)

