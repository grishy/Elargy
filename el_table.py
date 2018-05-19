import re
import json
import el_grammar


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
        # print(self)

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

    def toHTML(self):
        topList = sorted(list(self.gm.notTerm | self.gm.term))
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
