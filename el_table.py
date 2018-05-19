import re
import json
import el_grammar


class ElTable:
    def __init__(self, grammar):
        self.gm = grammar
        self.table = {}

        self.setShift()
        print(self)

    def setShift(self):
        for numR, r in enumerate(self.gm.rules):
            for s in r.right_side:
                for l in s.left:
                    self.setСell(l, s.text, s.right)

    def setСell(self, left, top, val):
        if left in self.table:
            self.table[left][top] = val
        else:
            self.table[left] = {}
            self.table[left][top] = val
