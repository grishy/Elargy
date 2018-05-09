

class ElParser:
    def __init__(self, grammarFile):
        grammar = open(grammarFile, "r")
        print(grammar.read())
