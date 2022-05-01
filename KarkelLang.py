from re import S
import sys
from lexer import *
from tokenParser import *
from interpreter import interpreterRun
from interpreter import InterpreterObject
from compiler import compilerRun
from subprocess import check_call
import subprocess
from platform import system
      
def run(file: str, compiling = True, name="out") -> (int | InterpreterObject):
    """Runs a karkelLang file, runs the compiler if compiling is true else it will interpret the file
    Args:
        file (str): ARW file to run
        compiling (bool, optional): If code should be interpreted or compiled. Defaults to True.

    Returns:
        int | InterpreterObject: returns the output of the compiler or the interpreter
    """
    root = Parse(lexer(open(file, "r").read()))
    if(root):
        if(compiling is True):
            assembler, error = compilerRun(root)
            if(error == None):
                try:
                    file = open("ASM-output/" + name + ".asm", "x")
                except FileExistsError:
                    file = open("ASM-output/" + name + ".asm", "w")
                file.write(assembler)
                file.close()
                return True
            print(bcolors.FAIL + "Compiler error: " + error)
            return False
        else:
            return interpreterRun(root)
    return False
    
def runOutput(file: str, compiling, name) -> (int | InterpreterObject):
    """Runs a karkelLang file and prints the output

    Args:
        file (str): ARW file to run
    """
    output = run(file, compiling, name)
    if(output):
        if(compiling is True):
            print(bcolors.OKGREEN +"Ended: " +  str(output) + bcolors.RESET)
        elif(output.error):
            print(bcolors.FAIL + output.error.what + "\nOn line: " + str(output.error.where) + bcolors.RESET)
        else:
            print("Ended: " + bcolors.OKGREEN + str(output.currentFunction.returnValue.value) + bcolors.RESET)
        
if __name__ == '__main__':
    file = sys.argv[1]
    name = "out"
    compiling = False
    if(sys.argv[2] != None):
        if(sys.argv[2] == "--compile"):
            compiling = True
            try:
                if(sys.argv[3] != None):
                    name = sys.argv[3]
            except IndexError:
                pass
        elif(sys.argv[2] == "--interpret"):
            compiling = False
    runOutput(file, compiling, name)
  