class ElRuleSymbol:
    def __init__(self, text):
        self.text = text
        self.type = "Term"
        self.left = set()
        self.right = set()

    def setLeft(self, idx):
        self.left.add(idx)

    def setRight(self, idx):
        self.right.add(idx)

    def printSym(self):
        print(self.left,  end='')
        print(self.text,  end='')
        print(self.right,  end='')


class ElRule:
    def __init__(self, text):
        self.text = text
        parts = text.split(":")
        self.left_side = parts[0]
        self.right_side = [ElRuleSymbol(t) for t in parts[1].split()]

    def setFirst(self, idx):
        self.right_side[0].left.add(idx)

    def printRule(self):
        print(self.left_side, end=': ')
        for s in self.right_side:
            s.printSym()
        print()


class ElParser:
    def __init__(self, grammarFile):
        self.rules_text = open(grammarFile, "r").readlines()
        self.rules = [ElRule(t) for t in self.rules_text]

        self.setType()

        self.setIndex()

        self.printGram()

        

    def setType(self):
        """Расстановка символу их типа: Терменал/Не терминал"""
        not_ter = {r.left_side for r in self.rules}
        for r in self.rules:
            for s in r.right_side:
                s.type = "Not-Term" if s.text in not_ter else s.type

    def setIndex(self):
        """
        Предварительная расстановка индексов символам. Без использования 3 правила.
        """
        IDX = 1
        for r in self.rules:
            for i in range(len(r.right_side)):
                sym = r.right_side[i]
                try:
                    sym_next = r.right_side[i + 1]
                except (IndexError, ValueError):
                    sym_next = None

                # Если слева пусто -> ставим этому символу его и во всех правилах
                if len(sym.left) == 0:
                    sym.setLeft(IDX)
                    self.setLeftAll(sym, IDX)
                    IDX += 1

                # Ставим спарва указанный увеличенный символ
                sym.setRight(IDX)
                # У следующего символа тоже, на следующем этапе будет оптимизировано
                if sym_next is not None:
                    sym_next.setLeft(IDX)
                    self.setLeftAll(sym_next, IDX)

                IDX += 1

    def setLeftAll(self, sym, idx):
        """
        У всех парвил, где слева идёт указанный симовол, ставил справа у первого сивола указанный индекс.
        Для первого симовла выполняет эту функцию с таким же параметром.
        """
        for r in self.findRulesLeft(sym):
            first_sym = r.right_side[0]
            first_sym.setLeft(idx)
            self.setLeftAll(first_sym, idx)

    def findRulesLeft(self, sym):
        """Найти все паравила, где слева идет указанный символ"""
        return [r for r in self.rules if r.left_side == sym.text]

    def printGram(self):
        for r in self.rules:
            r.printRule()
