import re
import json
import el_grammar

class ElTable:
    def __init__(self, grammar):
        self.tokens = []
        self.line_num = 1
        self.line_start = 0
        print(grammar)
