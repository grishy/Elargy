import re
import json
 
line = 1

def identifier(scanner, token): return "IDENT", token, scanner.match.regs[0], line
def operator(scanner, token):   return "OPERATOR", token, scanner.match.regs[0], line
def digit(scanner, token):      return "DIGIT", token, scanner.match.regs[0], line
def end_stmnt(scanner, token):  return "END_STATEMENT", scanner.match.regs[0], line
def next_line(scanner, token):  
    global line 
    line = line + 1
    return "NEXT_LINE", scanner.match.regs[0], line
 
scanner = re.Scanner([
    (r"[a-zA-Z_]\w*", identifier),
    (r"\+|\-|\\|\*|\=", operator),
    (r"[0-9]+(\.[0-9]+)?", digit),
    (r";", end_stmnt),
    (r"\n", next_line),
    (r"\s+", None),
    ])
 
tokens, remainder = scanner.scan("""
foo = 5 * 30; bar = bar - 60;
sdf
sdfg
""")

print(json.dumps(tokens, indent=4))