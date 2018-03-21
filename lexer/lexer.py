import re

token_pattern = r"""
(?P<int>[0-9]+)
|(?P<plus>[+])
|(?P<open_round_brackets>[(])
|(?P<close_round_brackets>[)])
|(?P<newline>\n)
|(?P<whitespace>\s)
"""

token_re = re.compile(token_pattern, re.VERBOSE)

class TokenizerException(Exception): pass

def tokenize(text):
    pos = 0
    while True:
        m = token_re.match(text, pos)
        if not m: break
        pos = m.end()
        tokname = m.lastgroup
        tokvalue = m.group(tokname)
        yield tokname, tokvalue
    if pos != len(text):
        raise TokenizerException('tokenizer stopped at pos %r of %r' % (
            pos, len(text)))

stuff2 = r'''
123 + 21332 +  (2345345)  + 1
'''

for tok in tokenize(stuff2):
    print(tok)
