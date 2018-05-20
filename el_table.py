import re
import json
import el_grammar

#TO DO: R1 and admission in table 
xxx

class ElTable:
    TABLE = '''
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <table>
            <tr>
                %s
            </tr>
                %s
        </table>
    </body>

    <style>
        th {
            font-weight: bold;
            background: #dedede;
        }
        body {
            font-size:28px;
        }
        table {
            margin: 0 auto;
        }
        table, tr, td, th {
            border-spacing: unset;
            border: 1px solid #ccc;
            padding: 5px;
        }
    </style>
</html>
'''

    def __init__(self, grammar):
        self.gm = grammar
        self.table = {}

        self.setShift()
        self.setReverse()
        # print(self)

    def setShift(self):
        for numR, r in enumerate(self.gm.rules):
            for s in r.right_side:
                for l in s.left:
                    self.setСell(l, s.text, s.right)

    def setReverse(self):
        num_rules = 0
        for numR, r in enumerate(self.gm.rules):
            num_rules = num_rules + 1 
            last_index = r.right_side[-1].right
            last_symb = r.right_side[-1]
            search_Left_side = r.left_side
            self.getNextSymb(search_Left_side, num_rules, last_index)
            
            
                    
    def getNextSymb(self, search_Left_side, num_rules, last_index):
        next_symb = ''
        for numT, s in enumerate(self.gm.rules):
                j = -1
                for  t in s.right_side:
                    j=j+1
                    if(t.text == search_Left_side): 
                        if((t == s.right_side[-1]) & (t == s.right_side[0])):
                            self.getNextSymb(s.left_side, num_rules, last_index)
                        
                        if(t == s.right_side[-1]):
                            #print("Последний")
                            next_symb = '$'
                            self.setСell(last_index,next_symb, 'R%(rule)i'%{"rule":num_rules})
                        else: 
                            #print("    " + s.right_side[j+1].text)
                            next_symb = s.right_side[j+1].text
                            self.setСell(last_index,next_symb, 'R%(rule)i'%{"rule":num_rules})
                            #print("yes")

    def setСell(self, left, top, val):
        if left in self.table:
            self.table[left][top] = val
        else:
            self.table[left] = {}
            self.table[left][top] = val

    def toHTML(self):
        topList = sorted(list(self.gm.notTerm | self.gm.term))
        topList.append("$")
        leftList = sorted(list(self.gm.idxs))

        topHTML = ["<th>{}</th>".format(x) for x in [""] + topList]
        rowsHTML = []
        for l in leftList:
            row = "<tr><th>{}</th>".format(l)
            for t in topList:
                try:
                    row += "<td>{}</td>".format(self.table[l][t])
                except:
                    row += "<td></td>"
            rowsHTML.append(row + "</tr>")

        strTable = self.TABLE % ("\n".join(topHTML), "\n".join(rowsHTML))
        return strTable
