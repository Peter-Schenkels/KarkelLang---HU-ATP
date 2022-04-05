from re import S
import sys
from lexer import *
from tokenParser import *
from interpreter import interpreterRun
from compiler import compilerRun
from subprocess import check_call
import subprocess

compiling = True
      
def run(file: str):
    root = Parse(lexer(open(file, "r").read()))
    if(root):
        if(compiling is True):
            assembler, error = compilerRun(root)
            if(error == None):
                try:
                    file = open("ASM-output/" + file[6:-4] + ".asm", "x")
                except FileExistsError:
                    file = open("ASM-output/" + file[6:-4] + ".asm", "w")
                file.write(assembler)
                file.close()
                check_call(['wsl', 'touch','out.asm'])
                check_call(['wsl', 'echo',assembler, '>', 'out.asm'])
                check_call(['wsl', "arm-linux-gnueabi-as", "out.asm", "-o",  "out.o"])
                check_call(['wsl', "arm-linux-gnueabi-gcc", "out.o", "-o",  "out.elf", "-nostdlib"])
                try:
                    check_call(['wsl', "qemu-arm", "out.elf"])
                except subprocess.CalledProcessError as ret:
                    return ret.returncode
                return 0
            print(bcolors.FAIL + "Compiler error: " + error)
            return False
        else:
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
  