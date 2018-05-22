class ElParser:
    def __init__(self, grammar, table, lex):
        self.gm = grammar
        self.tl = table
        self.lx = lex
        self.lx.addToken("$",0,0)
        operation = ''
        ind = 0
        states = [1]
        symbols =''
        while True:
            symb = self.lx.tokens[ind]['typ']
            st = states[-1]
            # print('Символ')
            # print(self.lx.tokens[ind]['typ'])
            # print('Состояния')
            # print(states)
            # print('Индекс')
            # print(ind)
            try:
                operation = self.tl.table[st][symb]
            except:
                operation = 'error'
            # print(operation)
            if(operation == 'admission'):
                print('ACEPT')
                break
            elif(operation[0] == 'R'):
                self.lx.tokens[ind-1]['typ'] = self.gm.rules[int(operation[1:])-1].left_side
                # print(self.lx.tokens[ind]['typ'])
                ln = len(self.gm.rules[int(operation[1:])-1].right_side)
                for x in range(ln):
                    states.pop(-1)
                ind = ind - 1
                pass
            elif(operation == 'error'):
                print('PARSE ERROR')
                break
            elif(operation[0] == 'S'):
                states.append(int(operation[1:]))
                ind = ind + 1
     
        # print(self)

    
    