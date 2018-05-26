tokens = {
    'LPAREN':   r'\(',
    'RPAREN':   r'\)',
    'INTEGER':  r'\d+',
    'PLUS':     r'\+',
    'MINUS':    r'\-',
}

# Rules


def p_1(p):
    'S: E'
    pass


def p_2(p):
    'E: T PLUS E'
    pass


def p_3(p):
    'E: T'
    pass


def p_4(p):
    'T: F MINUS T'
    pass


def p_5(p):
    'T: F'
    pass


def p_6(p):
    'F: INTEGER'
    pass
