class ElRuleSymbol:
    def __init__(self, text):
        self.text = text
        self.type = "Term"
        self.left = set()
        self.right = set()


class ElRule:
    def __init__(self, text):
        self.text = text
        parts = text.split(":")
        self.left_side = parts[0]
        self.right_side = [ElRuleSymbol(t) for t in parts[1].split()]

    def setFirst(self, idx):
        self.right_side[0].left.add(idx)


class ElParser:
    def __init__(self, grammarFile):
        self.rules_text = open(grammarFile, "r").readlines()
        self.rules = [ElRule(t) for t in self.rules_text]

        # Set "Not-Term" or "Term" in ElRuleSymbol
        self.setType()

        self.SetIndex()
        print(self.rules)

    def setType(self):
        not_ter = {r.left_side for r in self.rules}

        for r in self.rules:
            for s in r.right_side:
                s.type = "Not-Term" if s.text in not_ter else s.type

    def SetIndex(self):
        idx = 1
        for r in self.rules:
            r.setFirst(idx)
            first_sym = r.right_side[0]
            self.setFirstIndex(first_sym.text, idx)
            idx += 1
            first_sym.right.add(idx)
            

    def setFirstIndex(self, sym, idx):
        rules = self.findRuleLeft(sym)

        for r in rules:
            first_right =r.right_side[0]
            r.setFirst(idx)
            self.setFirstIndex(first_right.text, idx)
        
        

    def findRuleLeft(self, text):
        return [r for r in self.rules if r.left_side == text]
