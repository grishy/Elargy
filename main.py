import elargy


with open("input/calc1.elg", 'r') as content_file:
    f = content_file.read()
    elargy.Parse(f, steps='./steps/')
