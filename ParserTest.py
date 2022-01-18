from lexer import *
from tokenParser import *



if __name__ == '__main__':
    input = open("testFunctionDeclaration.arw", "r")
    tokens = lexer(input.read())
    functools.reduce(print, tokens)
    root = parse(tokens)
    print(root)