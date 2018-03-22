from parglare import Parser, Grammar

grammar = r"""
E: E '+' E  {left, 1}
| E '-' E  {left, 1}
| E '*' E  {left, 2}
| E '/' E  {left, 2}
| E '^' E  {right, 3}
| '(' E ')'
| number;
number: /\d+(\.\d+)?/;
"""

def ttt(_, value):
    print(value)
    return float(value)

def pl(_, nodes):
    print(nodes)
    return nodes[0] + nodes[2]

actions = {
    "E": [pl,
          lambda _, nodes: nodes[0] - nodes[2],
          lambda _, nodes: nodes[0] * nodes[2],
          lambda _, nodes: nodes[0] / nodes[2],
          lambda _, nodes: nodes[0] ** nodes[2],
          lambda _, nodes: nodes[1],
          lambda _, nodes: nodes[0]],
    "number": ttt,
}

g = Grammar.from_string(grammar)
parser = Parser(g, debug=False, actions=actions)

result = parser.parse("34 + 4.6 / 2 * 4^2^2 + 78")

print("Result = ", result)