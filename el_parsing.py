import copy

class ElParser:
    def __init__(self, grammar, table, lex):
        self.gm = grammar
        self.tl = table
        self.lx = lex
        self.lx.addToken("$",0,0)
        self.tree = {}

        operation = ''
        ind = 0
        states = [1]
        symbols =''
        
        while True:
            symb = self.lx.tokens[ind]
            t = symb['typ']
            st = states[-1]
            # print('Символ')
            # print(self.lx.tokens[ind]['typ'])
            # print('Состояния')
            # print(states)
            # print('Индекс')
            # print(ind)
            try:
                operation = self.tl.table[st][t]
            except:
                operation = 'error'

            
            if(operation == 'admission'):
                self.tree = self.lx.tokens[-2]
                print('ACEPT')
                break
            elif(operation[0] == 'R'):
                rul = self.gm.rules[int(operation[1:])-1]

                ln = len(rul.right_side)
                for x in range(ln):
                    states.pop(-1)

                tokens = self.lx.tokens[ind - ln:ind]
                ind-=1
                
                self.lx.tokens[ind] = {
                    'typ': rul.left_side,
                    'child' : tokens
                }
            elif(operation == 'error'):
                print('PARSE ERROR')
                break
            elif(operation[0] == 'S'):
                states.append(int(operation[1:]))
                ind = ind + 1
     
    def toJSON(self):
        pass