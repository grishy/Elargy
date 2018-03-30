from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor, EOF, visit_parse_tree

# Setting up our simple grammar
calc_grammar = """
number = r'\d+(\.\d+)?'
factor = number / "(" stmt ")"
term = factor (mulop factor)*
stmt = term (addop term)*
addop = "+" / "-"
mulop = "*" / "/"
calc = stmt EOF
"""

# Creating a visitor class to calculate the result


class CalcVisitor(PTNodeVisitor):

    def visit_number(self, node, children):
        return float(node.value)

    def visit_factor(self, node, children):
        # Children are list-like structure of VISITED node results
        # visits are made from depth to top
        return children[0]

    def visit_term(self, node, children):
        # For such rules you may use, for example children["factor"]
        # Though, you need to know, that children["factor"] is a list of ALL
        # factor's of this term
        if len(children) == 1:
            return children[0]
        else:
            res = children[0]
            for i in range(len(children) // 2):
                if children[2 * i + 1] == '*':
                    res *= children[2 * (i + 1)]
                else:
                    res /= children[2 * (i + 1)]
            return res

    def visit_stmt(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            res = children[0]
            for i in range(len(children) // 2):
                if children[2 * i + 1] == '+':
                    res += children[2 * (i + 1)]
                else:
                    res -= children[2 * (i + 1)]
            return res


# Don’t forget about root rule for your parser, as it will be produced as
# a parsing result
parser = ParserPEG(calc_grammar, "calc")
input_expr = "(4-1)*5+(2+4.67)+5.89/(1.2+7)"
print(input_expr)
parse_tree = parser.parse(input_expr)

result = visit_parse_tree(parse_tree, CalcVisitor(
    debug=True
))
print(result)
input_expr = "1 + 2 / (3 - 1 + 5)"
print(input_expr)
parse_tree = parser.parse(input_expr)

result = visit_parse_tree(parse_tree, CalcVisitor(
    debug=True
))
print(result)
