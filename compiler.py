from turtle import left

from black import err
from astNodes import *
from tokenParser import *

import random
import string

def get_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))

def addIndent(n):
    if(n[:3] != "if_" and n[:6] != "while_" and n[:7] != "end_if_"):
        indent = "  "
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
    registerNr = registerLookup.get(node.value.identifier.value)
    if(registerNr != None):
        return [f"mov r1, r{registerNr}", "pop {r4, r5, r6, r7, r8, r9, r10, r11, pc }"], None
    else:
        return None, "Return Value could not be found"
    
def getLeftRight(node, registerLookup: dict[str, int]):
    left = ""
    right = ""
    prefix = []
    error = None
    
    if(type(node.left) == FunctionCallNode):
        leftRegister = getAvailableRegister(registerLookup)
        out, error = compileFunctionCallNode(node.left, leftRegister, registerLookup)
        prefix = out + prefix
        registerLookup = {**registerLookup, "left" : leftRegister}
        left = f"r{leftRegister}"
    elif(node.left.identifier == None):
        left = f"#{node.left.value}"
    else:
        left = f"r{registerLookup.get(node.left.identifier.value)}"
        
    if(type(node.right) == FunctionCallNode):
        rightRegister = getAvailableRegister(registerLookup)
        out, error = compileFunctionCallNode(node.right, rightRegister, registerLookup)
        prefix = out + prefix
        registerLookup = {**registerLookup, "right" : rightRegister}
        right = f"r{rightRegister}"  
    elif(node.right.identifier == None):
        right = f"#{node.right.value}"
    else:
        right = f"r{registerLookup.get(node.right.identifier.value)}"
    
    return left, right, prefix, error     
      
def compileOperatorNode(node: OperatorNode, registerLookup: dict[str, int], outputRegister):
 
    left, right, prefix, error = getLeftRight(node, registerLookup)
    
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
        return "oops"

def addParameters(parameters: list[ASTNode], registerLookup={}, availableParameterRegisters=[0, 2, 3]):
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
    functionCall = node
    prefix, error = addParameters(functionCall.parameters, registerLookup)
    if(error == None):
        return ["push {r0, r2, r3}"] + prefix + [f"bl karkel_lang_{node.identifier.value}", f"mov r{registerNr}, r1", "pop {r0, r2, r3}" ], None
    else:
        return None, error
    
 
def compileAssignNode(node: AssignNode, registerLookup: dict[str, int]):
    if(node.left.identifier.value not in registerLookup):
        registerNr = getAvailableRegister(registerLookup)
    else:
        registerNr = registerLookup.get(node.left.identifier.value)
    if(issubclass(type(node.right), OperatorNode)):
        prefix, error = compileOperatorNode(node.right, {**registerLookup, node.left.identifier.value : registerNr}, registerNr)
        return prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    elif(type(node.right) == FunctionCallNode):
        prefix, error = compileFunctionCallNode(node.right, registerNr, registerLookup)
        return prefix, {**registerLookup, node.left.identifier.value : registerNr}, error
    else:
        prefix = []
        right_value = node.right.value
    if(registerNr):
        if(right_value < 256):
            return prefix + [f"mov r{registerNr}, #{right_value}"], {node.left.identifier.value : registerNr, **registerLookup}, None
        else:
            return prefix + [f"ldr r{registerNr}, ={right_value}"], {node.left.identifier.value : registerNr}, None
    return None, None, ("too many local vars", node.lineNr)

def compileIfNode(node: IfNode, registerLookup: dict[str, int]):
    ifBodyId = get_id()
    
    left, right, prefix, error = getLeftRight(node.comparison, registerLookup)
    
    if(error == None):
    
        comparisonType = type(node.comparison)

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

        ifComparisonAssembly = [f"cmp {left}, {right}", f"{cmpInstruction} if_{ifBodyId}", f"b end_if_{ifBodyId}"]
        ifTrue = [f"if_{ifBodyId}:"]
        ifBodyAssembly, error = compileFunctionBodyCode(node.codeSequenceNode.Sequence, registerLookup)
        if(error == None):
            ifEnd = [f"end_if_{ifBodyId}:"]
            return prefix + ifComparisonAssembly + ifTrue + ifBodyAssembly + ifEnd, error
        
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
        elif(type(code[0] == IfNode)):
            out, error = compileIfNode(code[0], registerLookup)
            registers = registerLookup
        else:
            return []
        
        if(error == None):
            suffix, error = compileFunctionBodyCode(code[1:], registers)
            return out + suffix, error
        else:
            return None, out[1]
    
    return []
    
def addParametersToRegistersLookUp(parameters, registerLookup: dict[str, int]={}, availableParameterRegisters=[0, 2, 3]):
    if(len(parameters) > 0):
        if(len(availableParameterRegisters) > 0):
            return addParametersToRegistersLookUp(parameters[1:], {parameters[0].identifier.value : availableParameterRegisters[0], **registerLookup}, availableParameterRegisters[1:])
        else:
            return None, "Too many parameters initialised (>3)"
    else:
        return registerLookup
        
        

def compileFunctionBody(node: FunctionDeclareNode):
    indent = "  "
    pushRegistersAssembler =  "push {r4, r5, r6, r7, r8, r9, r10, r11, lr }"
    # storeParametersAssembler = "mov r3, r0" + [storeParametersAssembler] 
    bodyCodeAssembler, error = compileFunctionBodyCode(node.code.Sequence, addParametersToRegistersLookUp(node.parameterTypes))
    if(error == None):
        return list(map(addIndent, [pushRegistersAssembler] + bodyCodeAssembler )), None
    else:
        return None, error
    
def compileFunctionDeclareNode(node: FunctionDeclareNode):
    functionPrefixAssembler = f"@ Function {node.identifier.value} at line {node.lineNr}"
    functionNameAssembler = f"karkel_lang_{node.identifier.value}:"
    bodyAssembler, error = compileFunctionBody(node)
    if(error == None):
        return [functionPrefixAssembler] + [functionNameAssembler] + bodyAssembler, None
    else:
        return None, error

def compile(node):
    if(type(node) == FunctionDeclareNode):
        return compileFunctionDeclareNode(node)

    else:
        return None

def compilerRun(root: ASTRoot):
    #todo check for errors
    out = [([".cpu cortex-m0", ".align 2"], None)] + list(map(compile, root.codeSequenceNode.Sequence))
    for function in out:
        for line in function[0]:
            print(line) 
        print("")
        
        
    return out[0]

              