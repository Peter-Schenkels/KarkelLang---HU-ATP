import sys
from lexer import *
from tokenParser import *
from interpreter import interpreterRun
      
def run(file: str):
    root = Parse(lexer(open(file, "r").read()))
    if(root):
        return interpreterRun(root)
    return False

def runOutput(file: str):
    output = run(file)
    if(output):
        if(output.error):
            print(bcolors.FAIL + output.error.what + "\nOn line: " + str(output.error.where) + bcolors.RESET)
        else:
            print("Ended: " + bcolors.OKGREEN + str(output.currentFunction.returnValue.value) + bcolors.RESET)
        
if __name__ == '__main__':
    file = sys.argv[1]
    runOutput(file)
  