import sys
from lexer import *
from tokenParser import *
from interpreter import interpreterRun

if __name__ == '__main__':
    file = sys.argv[1]
    input = open(file, "r")
    tokens = lexer(input.read())
    # functools.reduce(print, tokens)
    root = ASTRoot()
    root = parse(tokens)
    output = interpreterRun(root)
    if(output.error):
        print(bcolors.FAIL + output.error.what + "\nOn line: " + str(output.error.where) + bcolors.RESET)
    else:
        print("Ended: " + bcolors.OKGREEN + str(output.currentFunction.returnValue.value) + bcolors.RESET)