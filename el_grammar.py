def setToText(s):
    text = "{"
    text += " ".join([str(i) for i in s])
    return text + "}"


class ElRuleSymbol:
    def __init__(self, text):
        self.text = text
        self.type = "Term"
        self.left = set()
        self.right = -1

    def setLeft(self, idx):
        self.left.add(idx)

    def setRight(self, idx):
        self.right = idx


class ElRule:
    def __init__(self, text):
        self.text = text
        parts = text.split(":")
        self.left_side = parts[0]
        self.right_side = [ElRuleSymbol(t) for t in parts[1].split()]

    def setFirst(self, idx):
        self.right_side[0].left.add(idx)

    def toText(self):
        text = self.left_side + ": "
        for i in range(len(self.right_side)):
            text += setToText(self.right_side[i].left)
            text += self.right_side[i].text
            try:
                self.right_side[i + 1]
                # text += setToText(self.right_side[i].right) + " "
            except (IndexError, ValueError):
                text += "{" + str(self.right_side[i].right) + "}"
        return text + "\n"


class ElGrammar:
    def __init__(self, grammarFile):
        self.idxs = set()
        self.notTerm = set()
        self.term = set()

        self.rules_text = open(grammarFile, "r").readlines()
        self.rules = [ElRule(t) for t in self.rules_text]

        self.setType()
        self.setIndex()
        self.apply3()
        self.capture()

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

    def toText(self):
        text = ""
        for r in self.rules:
            text += r.toText()
        return text + "\n"

    def apply3(self):
        allSymb = []
        for r in self.rules:
            for s in r.right_side:
                allSymb.append(s)

        for i in range(len(allSymb)):
            s = allSymb[i]
            for f in range(i):
                if allSymb[f].text == s.text and allSymb[f].left == s.left:
                    s.right = allSymb[f].right

    def capture(self):
        for r in self.rules:
            for s in r.right_side:
                if s.type == "Not-Term":
                    self.notTerm.add(s.text)
                else:
                    self.term.add(s.text)
                self.idxs.update(s.left)
                self.idxs.add(s.right)