import re
 
def identifier(scanner, token): return "IDENT", token
def operator(scanner, token):   return "OPERATOR", token
def digit(scanner, token):      return "DIGIT", token
def end_stmnt(scanner, token):  return "END_STATEMENT"
 
scanner = re.Scanner([
    (r"[a-zA-Z_]\w*", identifier),
    (r"\+|\-|\\|\*|\=", operator),
    (r"[0-9]+(\.[0-9]+)?", digit),
    (r";", end_stmnt),
    (r"\s+", None),
    ])
 
tokens, remainder = scanner.scan("foo = 5 * 30; bar = bar - 60;")
for token in tokens:
    print(token)