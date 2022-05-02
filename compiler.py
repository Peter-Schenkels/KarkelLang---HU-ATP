# from turtle import left

# from black import err
from multiprocessing.sharedctypes import Value
from re import L
from tokenize import String

from astNodes import *
from tokenParser import *
from functools import reduce

import random
import string

def get_id() -> str:
    """Generates a random identifier

    Returns:
        str: random identifier
    """    
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))

def addIndent(n: str) -> str:
    """Adds an indent to a string

    Args:
        n(str): input string

    Returns:
        str: indented string
    """    
    if(n[0] != '@' and n[:3] != "if_" and n[:10] != "while_true" and n[:7] != "end_if_" and n[:11] != "while_false"):
        indent = "    "
        return indent + n
    return n


def getAvailableRegister(registerLookup: dict[str, int], registers=[*range(4, 12)]) -> int:
    """ Gets an available register from the register lookup table.

    Args:
        registerLookup (dict[str, int]): available registers look up table
        registers (list, optional): registers to check. Defaults to [*range(4, 12)].

    Returns:
        int: available register
    """    
    if(len(registers) == 0):
        return None
    
    if(registers[0] in registerLookup.values()):
        return getAvailableRegister(registerLookup, registers[1:])
    else:
        return registers[0]

def compileReturnNode(node: ReturnNode, registerLookup: dict[str, int]) -> tuple[list[str], str]:
    """compiles the assembly code for a return node

    Args:
        node (ReturnNode): return node
        registerLookup (dict[str, int]): available registers look up table

    Returns:
        list[str]: assembly code for the return node
        str: error message if the return node could not be compiled
    """    
    comment = "@ return at line " + str(node.lineNr)
    registerNr = registerLookup.get(node.value.identifier.value)
    if(registerNr != None):
        return [comment] + [f"mov r0, r{registerNr}", "pop {r4-r11, pc }"], None
    else:
        return None, "Return Value could not be found, at line Nr" + str(node.lineNr)

def compileNodeRegister(node:ASTNode, registerLookup: dict[str, int], noLiterals:bool = False) -> tuple[str, list[str], str, bool, int]:
    """Compiles the assembly code for a register allocation.

    Args:
        node (ASTNode): node for assignation
        registerLookup (dict[str, int]): register lookup table
        noLiterals (bool, optional): Is the value inside a register or not. Defaults to False.

    Returns:
        str: Register string
        list[str]: Prefix assembly code
        str: Error message
        bool: new register has been allocated
        int: register number
    """    
    if(type(node) == FunctionCallNode):
        register = getAvailableRegister(registerLookup)
        out, error = compileFunctionCallNode(node, register, registerLookup)
        return f"r{register}", out, error, False, register
    elif(node.identifier == None):
        if(noLiterals is True):
            register = getAvailableRegister(registerLookup) 
            return f"r{register}", [f"mov r{register}, #{node.value}"], None, True, register
        else:
            return f"#{node.value}", [], None, True, None
    else:
        return f"r{registerLookup.get(node.identifier.value)}", [], None, False, None
    
def getLeftRight(node, registerLookup: dict[str, int], noLiterals = False)-> tuple[str, str, list[str], str, bool]:
    """Gets the left and right value of a comparison node

    Args:
        node (ASTNode): comparison node
        registerLookup (dict[str, int]): register lookup table
        noLiterals (bool, optional): Is the value inside a register or not. Defaults to False.

    Returns:
        tuple[str, str, list[str], str, bool]: left and right register assembly value, prefix assembly code, error message, literals
    """    
    left, prefixLeft, error, left_literal, register = compileNodeRegister(node.left, registerLookup, noLiterals)
    right, prefixright, error, right_literal, _ = compileNodeRegister(node.right, registerLookup if register == None else {**registerLookup, left: register}, noLiterals)
    prefix = prefixLeft + prefixright
    
    return left, right, prefix, error, (left_literal, right_literal)
      
def compileOperatorNode(node: OperatorNode, registerLookup: dict[str, int], outputRegister:int) -> tuple[list[str], str]:
    """ Compiles the assembly code for an operator node.

    Args:
        node (OperatorNode): input operator node
        registerLookup (dict[str, int]): available registers look up table
        outputRegister (int): output register of operator call

    Returns:
        list[str]: assembly code for the operator node
        str: error message if the operator node could not be compiled
    """    
    left, right, prefix, error, _ = getLeftRight(node, registerLookup, noLiterals = True)
    
    if(error != None):
        return None, error
    
    if(type(node) == AdditionNode):
        return prefix + [f"add r{outputRegister}, {left}, {right}"], None
    elif(type(node) == MultiplicationNode):
        return prefix + [f"mul r{outputRegister}, {left}, {right}"], None
    elif(type(node) == SubtractionNode):
        return prefix + [f"sub r{outputRegister}, {left}, {right}"], None
    elif(type(node) == DivisionNode):
        return prefix + [f"sub r{outputRegister}, {left}, {right}"], None
    else:
        return "oops", "Node doesn't exist, parser error at line:" + str(node.lineNr)

def addParameters(parameters: list[ASTNode], registerLookup:dict[str, int]={}, availableParameterRegisters: list[int]=[1, 2, 3]) -> tuple[list[str], str]:
    """Compiles the assembly code for parameter allocation for a function call
    
    Args:
        parameters (list[ASTNode]): input parameter list
        registerLookup (dict[str, int], optional): available registers look up table. Defaults to {}.
        availableParameterRegisters (list[int], optional): available parameter registers. Defaults to [1, 2, 3].

    Returns:
        list[str]: assembly code for the parameter allocation
        str: error message if the parameter allocation could not be compiled
    """    
    if(len(availableParameterRegisters) > 0):
        if(len(parameters) != 0):
            prefix, error = addParameters(parameters[1:], registerLookup, availableParameterRegisters[1:])
            if(parameters[0].identifier == None):
                moveValue = f"#{parameters[0].value}"
            else:
                moveValue = f"r{registerLookup.get(parameters[0].identifier.value)}"  
            return prefix + [f"mov r{availableParameterRegisters[0]}, {moveValue}"], error
        else:
            return [], None
    else:
        return None, "Too many parameters (>3), at lineNr" + str(parameters[0].lineNr)
    


def getPrintParameter(node:FunctionCallNode, registerNr:int, registerLookUp: dict[str, int]) -> tuple[list[str], str]:
    """Compiles the assembly code for a print function call

    Args:
        node (FunctionCallNode): input print function call node
        registerNr (int): Unused register number
        registerLookUp (dict[str, int]): register lookup table

    Returns:
        list[str]: The assembly code of the print function call.
        str: The error message if there was an error.
    """    
    
def getPrintParameter(node, registerLookUp):
    if(type(node.parameters[0]) == PrimitiveNode):
        prefix = ["push { r1, r2 }"]
        loadNumMemoryAssembly = [f"mov r1, r{registerLookUp.get(node.parameters[0].identifier.value)}", "ldr r2, =num", "str r1, [r2]", "ldr r1, =num", "mov r2, #1"]
        suffix = ["bl print", "pop { r1, r2 }"]
        return prefix + loadNumMemoryAssembly + suffix, None
    if(node.identifier.value in ["StringOutLine","StringOut"]):
        suffixEndline = "" if node.identifier.value == "StringOut" else "\n"
        asciiAssembly = [".section .data", f"{node.identifier.value}_str: .ascii \"{node.parameters[0].value + suffixEndline}n\""] 
        return asciiAssembly + [".section .text"] + [ "push {r1, r2}", f"ldr r1, ={node.identifier.value}_str", f"mov r2, #{len(node.parameters[0].value) +len(suffixEndline)}",  "bl print", "pop {r1, r2}"], None       
    elif(node.identifier.value in ["IntOutLine", "IntOut"]):
        suffixEndline = [] if node.identifier.value == "IntOut" else ["ldr r1, =newline", "bl print"]
        register = registerLookUp.get(node.parameters[0].identifier.value)
        return ["push { r1, r2}", f"mov r1, r{register}","add r1, r1, #30","add r2, #1","bl print"] + suffixEndline + ["pop {r1, r2}"], None
        
        
def compileFunctionCallNode(node:FunctionCallNode, registerNr:int, registerLookup:dict[str, int]) -> tuple[list[str], str]:
    """ Compiles a function call node.

    Args:
        node (FunctionCallNode): input function call node
        registerNr (int): output register number for the function call
        registerLookup (dict[str, int]): register look up table

    Returns:
        list[str]: assembly code for the function call
        str: error message if the function call could not be compiled
    """    
    if(registerNr == None):
        return None, "No register available, at line Nr:" + str(node.lineNr)
    
    if(node.identifier.value in ["StringOutLine", "IntOutLine","StringOut", "IntOut"]):
        return getPrintParameter(node, registerLookup)

    comment = "@ Function call at line " + str(node.lineNr)
    functionCall = node
    prefix, error = addParameters(functionCall.parameters, registerLookup)
    if(error == None):
        if(registerNr == 99):
            return [comment] + ["push {r1, r2, r3}"] + prefix + [f"bl karkel_lang_{node.identifier.value}", "pop {r1, r2, r3}" ], None
        return [comment] + ["push {r1, r2, r3}"] + prefix + [f"bl karkel_lang_{node.identifier.value}", "pop {r1, r2, r3}", f"mov r{registerNr}, r0" ], None
    else:
        return None, error
    
 
def compileAssignNode(node: AssignNode, registerLookup: dict[str, int]) -> tuple[list[str], dict[str, int], str]:
    """computes the assembly code for an assign node

    Args:
        node (AssignNode): assign node to compile
        registerLookup (dict[str, int]): register lookup table

    Returns:
        list[str]: assembly code
        dict[str, int]: register lookup table
        str: error message (None if no error)
    """    
    comment = "@ assign at line " + str(node.lineNr)
    if(node.left.identifier.value not in registerLookup):
        registerNr = getAvailableRegister(registerLookup)
        prexist = False
    else:
        registerNr = registerLookup.get(node.left.identifier.value)
        prexist = True
    if(issubclass(type(node.right), OperatorNode)):
        prefix, error = compileOperatorNode(node.right, {**registerLookup, node.left.identifier.value : registerNr}, registerNr)
        return [comment] + prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    elif(type(node.right) == FunctionCallNode):
        prefix, error = compileFunctionCallNode(node.right, registerNr, registerLookup)
        return [comment] + prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    elif(type(node.right) == PrimitiveNode):
        rightRegisterNR = registerLookup.get(node.right.identifier.value)
        if(prexist == False):
            return [comment] + [f"mov r{registerNr}, r{rightRegisterNR}"], {node.left.identifier.value : registerNr, **registerLookup}, None
        else:
            return [comment] + [f"mov r{registerNr}, r{rightRegisterNR}"], registerLookup, None
            
    else:
        prefix = []
        if(type(node.right) == StringNode):
            right_value = f"\'{node.right.value[0]}\'"
            cmp = ord(node.right.value[0])
        else:        

            right_value = node.right.value
            cmp = right_value
    if(registerNr != None):
        if(cmp < 256):
            return [comment] + prefix + [f"mov r{registerNr}, #{right_value}"], {node.left.identifier.value : registerNr, **registerLookup}, None
        else:
            return [comment] + prefix + [f"ldr r{registerNr}, ={right_value}"], {node.left.identifier.value : registerNr, **registerLookup}, None
    return None, None, ("too many local vars", node.lineNr)

def compileIfNode(node: IfNode, registerLookup: dict[str, int]) -> tuple[list[str], str]:
    """computes the if node and returns the assembly code

    Args:
        node (IfNode): input if node
        registerLookup (dict[str, int]): register lookup table

    Returns:
        list[str]: assembly code
        str: error message or None
    """    
    comment = "@ if at line " + str(node.lineNr)
    ifBodyId = get_id()
    
    left, right, prefix, error, literals = getLeftRight(node.comparison, registerLookup, noLiterals=True)
    
    
    if(error == None):
        cmpInstruction = getCmpInstruction(node.comparison)
        ifComparisonAssembly = [f"cmp {left}, {right}", f"{cmpInstruction} if_{ifBodyId}", f"b end_if_{ifBodyId}"]
        ifTrue = [f"if_{ifBodyId}:"]
        ifBodyAssembly, error = compileFunctionBodyCode(node.codeSequenceNode.Sequence, registerLookup)
        if(error == None):
            ifEnd = [f"end_if_{ifBodyId}:"]
            return [comment] + prefix + ifComparisonAssembly + ifTrue + ifBodyAssembly + ifEnd, error
        
    return None, error

def getCmpInstruction(node: ComparisonNode) -> str:
    """gets cmp instruction for given comparison node

    Args:
        node (ComparisonNode): input comparison node

    Returns:
        str: cmp instruction
    """    
    comparisonType = type(node)

    if(comparisonType == ComparisonNodeSmallerThan):
        cmpInstruction = "blt"
    elif(comparisonType == ComparisonNodeGreaterThan):
        cmpInstruction = "bgt"
    elif(comparisonType == ComparisonNodeNotEuqal):
        cmpInstruction = "bne"
    elif(comparisonType == ComparisonNode):
        cmpInstruction = "beq"
    elif(comparisonType == ComparisonNodeSmallerThanEqual):
        cmpInstruction = "ble"
    elif(comparisonType == ComparisonNodeGreaterThanEqual):
        cmpInstruction = "bge"
    else:
        cmpInstruction = None
    return cmpInstruction

def compileWhileNode(node: WhileNode, registerLookup: dict[str, int]) -> tuple[list[str], str]:
    """Computes the assembly code for a while node

    Args:
        node (WhileNode): input while node
        registerLookup (dict[str, int]): register lookup table

    Returns:
        tuple[list[str], str]: assembly code and error message
    """    
    comment = "@ While loop at line: " + str(node.lineNr)
    WhileId = get_id()
    whileTrueId = f"while_true_{WhileId}"
    whileFalseId = f"while_false_{WhileId}"
    whileBodyId = f"while_body_{WhileId}"
    left, right, prefix, error, literals = getLeftRight(node.comparison, registerLookup, noLiterals=True)
    
    if(error == None):
        cmpInstruction = getCmpInstruction(node.comparison)
        whileComparisonAssembly = [f"cmp {left}, {right}", f"{cmpInstruction} {whileBodyId}", f"b {whileFalseId}", f"{whileBodyId}:"]
        whileBodyAssembly, error = compileFunctionBodyCode(node.codeSequenceNode.Sequence, registerLookup)
        if(error == None):
            return [comment] + [f"{whileTrueId}:"] + prefix + whileComparisonAssembly + whileBodyAssembly + [f"b {whileTrueId}", f"{whileFalseId}:"], error
        
    return None, error


def compileFunctionBodyCode(code: list[ASTNode], registerLookup: dict[str, int]={}) -> tuple[list[str], str]:
    """Computes the assembly code for a function body.

    Args:
        code (list[ASTNode]): list of ast nodes representing the function body.
        registerLookup (dict[str, int], optional): dictionary compiled of registers with corresponding variable names. Defaults to {}.

    Returns:
        list[str]: list of assembly code lines
        str: error message if there were any errors
    """    
    if(len(code) > 0):
        # Execute code
        if(type(code[0]) == AssignNode):
            out, registers, error =  compileAssignNode(code[0], registerLookup)
        elif(type(code[0]) == ReturnNode):
            out, error = compileReturnNode(code[0], registerLookup)
            if(error == None):
                return out, None
        elif(type(code[0]) == IfNode):
            out, error = compileIfNode(code[0], registerLookup)
            registers = registerLookup
        elif(type(code[0]) == WhileNode):
            out, error = compileWhileNode(code[0], registerLookup)
            registers = registerLookup
        elif(type(code[0]) == FunctionCallNode):
            out, error = compileFunctionCallNode(code[0], 99, registerLookup)
            registers = registerLookup 
        elif(type(code[0]) == CommentNode):
            out = ["@" + code[0].value]
            error = None
            registers = registerLookup 
        else:
            return [], None
        
        if(error == None):
            suffix, error = compileFunctionBodyCode(code[1:], registers)
            if(error == None):
                return out + suffix, error
            return None, error
        else:
            return None, error
    
    return [], None
    
def addParametersToRegistersLookUp(parameters: list[ASTNode], registerLookup: dict[str, int]={}, availableParameterRegisters:list[int]=[1, 2, 3]) -> tuple[dict[str, int], str]:
    """add a list of parameters to the registerLookup dictionary.

    Args:
        parameters (_type_): _description_
        registerLookup (dict[str, int], optional): _description_. Defaults to {}.
        availableParameterRegisters (list, optional): _description_. Defaults to [1, 2, 3].

    Returns:
        dict[str, int] & str: new look up table for registers and the error message if there were any
    """    
    if(len(parameters) > 0):
        if(len(availableParameterRegisters) > 0):
            return addParametersToRegistersLookUp(parameters[1:], {parameters[0].identifier.value : availableParameterRegisters[0], **registerLookup}, availableParameterRegisters[1:])
        else:
            return None, "Too many parameters initialised (>3)"
    else:
        return registerLookup
        
def compileFunctionBody(node: FunctionDeclareNode) -> tuple[list[str], str]:
    """ Compiles the function body of a function to assembly code.

    Returns:
        list[str]: The assembly code of the function body.
        str: The error message if there was an error.
    """    
    pushRegistersAssembler =  "push {r4-r11, lr }"
    bodyCodeAssembler, error = compileFunctionBodyCode(node.code.Sequence, addParametersToRegistersLookUp(node.parameterTypes))
    if(error == None):
        return list(map(addIndent, [pushRegistersAssembler] + bodyCodeAssembler )), None
    else:
        return None, error
    
def compileFunctionDeclareNode(node: FunctionDeclareNode) -> tuple[list[str], str]:
    """Computes the assembly code for a function declaration node

    Args:
        node (FunctionDeclareNode): input function declare node

    Returns:
        list[str]: assembly code
        str: error message
    """    
    if(node.identifier.value == ""):
        pass
    functionPrefixAssembler = f"@ Function {node.identifier.value} at line {node.lineNr}"
    functionNameAssembler = f"karkel_lang_{node.identifier.value}:"
    filePrefixAssembler = []
    if(node.identifier.value == "Main"):
        filePrefixAssembler = ["_start:"] + list(map(addIndent, ["mov r7, #0x1","bl karkel_lang_Main", "swi 0"]))
    
    bodyAssembler, error = compileFunctionBody(node)
    if(error == None):
        return filePrefixAssembler + [functionPrefixAssembler] + [functionNameAssembler] + bodyAssembler, None
    else:
        return None, error


def generatePrint() -> tuple[list[str], str]:
    """Generates assembly for the print function

    Returns:
        (tuple[list[str], str]): Assembly for the print function and error message
    """
    return ["print:"] + list(map(addIndent, ["push { r7, lr }", "mov r7, #0x4", "swi 0", "pop { r7, pc }"])), None


def compile(node: FunctionDeclareNode):
    """Function that only compiles input function declare nodes

    Args:
        node (_type_): _description_

    Returns:
        _type_: _description_
    """    
    if(type(node) == FunctionDeclareNode):
        return compileFunctionDeclareNode(node)
    else:
        return None


def returnFile(lines: tuple[list[str], str], curAssembler: str) -> str:
    """Turns all the given lines in an assembly file

    Args:
        lines (tuple[list[str], str]): assembly lines with errors
    """   
    if lines != []:    
        head, *tail = lines
    else:
        return curAssembler, None
    
    out, error = returnFile( tail, curAssembler + reduce(lambda a, b: a+"\n"+b if b != None else "", head[0]) + "\n\n" )
    
    if(head[1] != None):
        return None, head[1]
    
    return  out, error
    
def compilerRun(root: ASTRoot) ->str:
    """Runs the compiler on the AST, and assembles the output

    Args:
        root (ASTRoot): input AST

    Returns:
        str: assembled output
    """    
    #todo check for errors
    out = [([".global _start", ".section .data", f"newline: .ascii \"\\n\"", f"num: .word 0", ".section .text"], None)] + [generatePrint()] + list(map(compile, root.codeSequenceNode.Sequence))
    
    return returnFile(out, "")
