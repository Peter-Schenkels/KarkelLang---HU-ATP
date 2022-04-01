# from turtle import left

# from black import err
from astNodes import *
from tokenParser import *

import random
import string

def get_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))

def addIndent(n):
    if(n[0] != '@' and n[:3] != "if_" and n[:10] != "while_true" and n[:7] != "end_if_" and n[:11] != "while_false"):
        indent = "    "
        return indent + n
    return n


def getAvailableRegister(registerLookup: dict[str, int], registers=[*range(4, 12)]):
    if(len(registers) == 0):
        return None
    
    if(registers[0] in registerLookup.values()):
        return getAvailableRegister(registerLookup, registers[1:])
    else:
        return registers[0]

def compileReturnNode(node: ReturnNode, registerLookup: dict[str, int]):
    comment = "@ return at line " + str(node.lineNr)
    registerNr = registerLookup.get(node.value.identifier.value)
    if(registerNr != None):
        return [comment] + [f"mov r0, r{registerNr}", "pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }"], None
    else:
        return None, "Return Value could not be found"

def compileNodeRegister(node, registerLookup: dict[str, int]):
    if(type(node) == FunctionCallNode):
        register = getAvailableRegister(registerLookup)
        out, error = compileFunctionCallNode(node, register, registerLookup)
        return f"r{register}", out, error, False, register
    elif(node.identifier == None):
        return f"#{node.value}", [], None, True, None
    else:
        return f"r{registerLookup.get(node.identifier.value)}", [], None, False, None
    
def getLeftRight(node, registerLookup: dict[str, int]):
    left, prefixLeft, error, left_literal, register = compileNodeRegister(node.left, registerLookup)
    right, prefixright, error, right_literal, _ = compileNodeRegister(node.right, registerLookup if register == None else {**registerLookup, left: register})
    prefix = prefixLeft + prefixright
    
    return left, right, prefix, error, (left_literal, right_literal)
      
def compileOperatorNode(node: OperatorNode, registerLookup: dict[str, int], outputRegister):
 
    left, right, prefix, error, literals = getLeftRight(node, registerLookup)
    
    if(error != None):
        return None, error
    
    if(literals[0] == True and literals[1] == True and type(node) == AdditionNode):
        right = f"#{int(left[1:]) + int(right[1:])}"
        left = f"r{outputRegister}"
    elif(literals[0] == True and literals[1] == True and type(node) == SubtractionNode):
        right = f"#{int(left[1:]) - int(right[1:])}"
        left = f"r{outputRegister}"
        return [f"mov r{outputRegister}, {right}"], None
    
    if(type(node) == AdditionNode):
        return prefix +  ["push { r0, r1 }", f"mov r0, {right}",  f"mov r1, {left}", f"add r{outputRegister}, r1, r0", "pop { r0, r1 }" ], None
    elif(type(node) == MultiplicationNode):
        return prefix + ["push { r0, r1 }", f"mov r0, {right}",  f"mov r1, {left}", f"mul r{outputRegister}, r1, r0", "pop { r0, r1 }" ], None
    elif(type(node) == SubtractionNode):
        return prefix +  ["push { r0, r1 }", f"mov r0, {right}",  f"mov r1, {left}", f"sub r{outputRegister}, r1, r0", "pop { r0, r1 }" ], None
    elif(type(node) == DivisionNode):
        return prefix + [f"sub r{outputRegister}, {left}, {right}"], None
    else:
        return "oops"

def addParameters(parameters: list[ASTNode], registerLookup={}, availableParameterRegisters=[1, 2, 3]):
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
        return None, "Too many parameters (>3)"
    

def compileFunctionCallNode(node, registerNr, registerLookup):
    comment = "@ Function call at line " + str(node.lineNr)
    functionCall = node
    prefix, error = addParameters(functionCall.parameters, registerLookup)
    if(error == None):
        return [comment] + ["push {r1, r2, r3}"] + prefix + [f"bl karkel_lang_{node.identifier.value}", f"mov r{registerNr}, r0", "pop {r1, r2, r3}" ], None
    else:
        return None, error
    
 
def compileAssignNode(node: AssignNode, registerLookup: dict[str, int]):
    comment = "@ assign at line " + str(node.lineNr)
    if(node.left.identifier.value not in registerLookup):
        registerNr = getAvailableRegister(registerLookup)
    else:
        registerNr = registerLookup.get(node.left.identifier.value)
    if(issubclass(type(node.right), OperatorNode)):
        prefix, error = compileOperatorNode(node.right, {**registerLookup, node.left.identifier.value : registerNr}, registerNr)
        return [comment] + prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    elif(type(node.right) == FunctionCallNode):
        prefix, error = compileFunctionCallNode(node.right, registerNr, registerLookup)
        return [comment] + prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    else:
        prefix = []
        right_value = node.right.value
    if(registerNr):
        if(right_value < 256):
            return [comment] + prefix + [f"mov r{registerNr}, #{right_value}"], {node.left.identifier.value : registerNr, **registerLookup}, None
        else:
            return [comment] + prefix + [f"ldr r{registerNr}, ={right_value}"], {node.left.identifier.value : registerNr}, None
    return None, None, ("too many local vars", node.lineNr)

def compileIfNode(node: IfNode, registerLookup: dict[str, int]):
    comment = "@ if at line " + str(node.lineNr)
    ifBodyId = get_id()
    
    left, right, prefix, error, literals = getLeftRight(node.comparison, registerLookup)
    
    
    if(error == None):
        comparisonPrefix = ["push { r0, r1 }", f"mov r0, {right}",  f"mov r1, {left}",]
        cmpInstruction = getCmpInstruction(node.comparison)
        ifComparisonAssembly = comparisonPrefix + [f"cmp r0, r1", f"{cmpInstruction} if_{ifBodyId}", f"b end_if_{ifBodyId}"]
        ifTrue = [f"if_{ifBodyId}:"]
        ifBodyAssembly, error = compileFunctionBodyCode(node.codeSequenceNode.Sequence, registerLookup)
        if(error == None):
            ifEnd = [f"end_if_{ifBodyId}:"]
            return [comment] + prefix + ifComparisonAssembly + ifTrue + ifBodyAssembly + ifEnd, error
        
    return None, error

def getCmpInstruction(node: ComparisonNode):
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

def compileWhileNode(node: WhileNode, registerLookup: dict[str, int]):
    comment = "@ While loop at line: " + str(node.lineNr)
    WhileId = get_id()
    whileTrueId = f"while_true_{WhileId}"
    whileFalseId = f"while_false_{WhileId}"
    left, right, prefix, error, literals = getLeftRight(node.comparison, registerLookup)
    
    if(error == None):
        cmpInstruction = getCmpInstruction(node.comparison)
        whileComparisonAssembly = [f"cmp {left}, {right}", f"{cmpInstruction} {whileFalseId}"]
        whileBodyAssembly, error = compileFunctionBodyCode(node.codeSequenceNode.Sequence, registerLookup)
        if(error == None):
            return [comment] + [f"{whileTrueId}:"] + prefix + whileComparisonAssembly + whileBodyAssembly + [f"b {whileTrueId}"] + [f"{whileFalseId}:"], error
        
    return None, error


def compileFunctionBodyCode(code: list[ASTNode], registerLookup: dict[str, int]={}):
    
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
        else:
            return [], None
        
        if(error == None):
            suffix, error = compileFunctionBodyCode(code[1:], registers)
            return out + suffix, error
        else:
            return None, out[1]
    
    return [], None
    
def addParametersToRegistersLookUp(parameters, registerLookup: dict[str, int]={}, availableParameterRegisters=[1, 2, 3]):
    if(len(parameters) > 0):
        if(len(availableParameterRegisters) > 0):
            return addParametersToRegistersLookUp(parameters[1:], {parameters[0].identifier.value : availableParameterRegisters[0], **registerLookup}, availableParameterRegisters[1:])
        else:
            return None, "Too many parameters initialised (>3)"
    else:
        return registerLookup
        
def compileFunctionBody(node: FunctionDeclareNode):
    pushRegistersAssembler =  "push {r4, r5, r6, r7, r8, r9, r10, r11, lr }"
    bodyCodeAssembler, error = compileFunctionBodyCode(node.code.Sequence, addParametersToRegistersLookUp(node.parameterTypes))
    if(error == None):
        return list(map(addIndent, [pushRegistersAssembler] + bodyCodeAssembler )), None
    else:
        return None, error
    
def compileFunctionDeclareNode(node: FunctionDeclareNode):
    functionPrefixAssembler = f"@ Function {node.identifier.value} at line {node.lineNr}"
    functionNameAssembler = f"karkel_lang_{node.identifier.value}:"
    suffix = ""
    if(node.identifier.value == "Main"):
        functionNameAssembler = "_start:\n    mov r7, #0x1"
        suffix = "    swi 0"
    
    bodyAssembler, error = compileFunctionBody(node)
    if(error == None):
        return [functionPrefixAssembler] + [functionNameAssembler] + bodyAssembler[:-1] + [suffix] + [bodyAssembler[-1]], None
    else:
        return None, error

def compile(node):
    if(type(node) == FunctionDeclareNode):
        return compileFunctionDeclareNode(node)

    else:
        return None

def compilerRun(root: ASTRoot):
    #todo check for errors
    out = [([".global _start", ".section .text"], None)] + list(map(compile, root.codeSequenceNode.Sequence))
    assembler = ""
    for function in out:
        for line in function[0]:
            assembler += line + "\n"
        
    return assembler

              