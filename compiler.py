from turtle import left

from black import err
from astNodes import *
from tokenParser import *

def addIndent(n):
    indent = "  "
    return indent + n


def getAvailableRegister(registerLookup: dict[str, int], registers=[*range(4, 7)]):
    if(len(registers) == 0):
        return None
    
    if(registers[0] in registerLookup.values()):
        return getAvailableRegister(registerLookup, registers[1:])
    else:
        return registers[0]

def compileReturnNode(node: ReturnNode, registerLookup: dict[str, int]):
    registerNr = registerLookup.get(node.value.identifier.value)
    if(registerNr):
        return [f"mov r1, r{registerNr}"], None
    else:
        return None, "Return Value could not be found"
    
def compileOperatorNode(node: OperatorNode, registerLookup: dict[str, int], outputRegister):

    left = ""
    right = ""
    
    if(node.left.identifier == None):
        left = f"#{node.left.value}"
    else:
        left = f"r{registerLookup.get(node.left.identifier.value)}"
        
    if(node.right.identifier == None):
        right = f"#{node.right.value}"
    else:
        right = f"r{registerLookup.get(node.right.identifier.value)}"
        
    if(type(node) == AdditionNode):
        return [f"add r{outputRegister}, {left}, {right}"], None
    elif(type(node) == MultiplicationNode):
        return [f"mul r{outputRegister}, {left}, {right}"], None
    elif(type(node) == SubtractionNode):
        return [f"sub r{outputRegister}, {left}, {right}"], None
    elif(type(node) == DivisionNode):
        return [f"sub r{outputRegister}, {left}, {right}"], None
    else:
        return "oops"

def addParameters(parameters: list[ASTNode], registerLookup={}, availableParameterRegisters=[*range(1, 4)]):
    if(len(availableParameterRegisters) > 0):
        if(len(parameters) != 0):
            prefix, error = addParameters(parameters[1:], registerLookup, availableParameterRegisters[1:])
            return prefix + [f"mov, r{availableParameterRegisters[0]}, r{registerLookup.get(parameters[0].identifier.value)}"], error
        else:
            return [], None
    else:
        return None, "Too many parameters (>3)"
    

def compileFunctionCallNode(node, registerNr, registerLookup):
    functionCall = node.right
    prefix, error = addParameters(functionCall.parameters, registerLookup)
    if(error == None):
        return prefix + [f"bl karkel_lang_{node.right.identifier.value}", f"mov r{registerNr}, r1"], None
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
        prefix, error = compileFunctionCallNode(node, registerNr, registerLookup)
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

def compileFunctionBodyCode(code: list[ASTNode], assembler: list[str]=[], registerLookup: dict[str, int]={}):
    
    if(len(code) > 0):
        
        # Execute code
        if(type(code[0]) == AssignNode):
            out, registers, error =  compileAssignNode(code[0], registerLookup)
        elif(type(code[0]) == ReturnNode):
            out, error = compileReturnNode(code[0], registerLookup)
            if(error == None):
                return out, None
        else:
            return []
        
        if(error == None):
            suffix, error = compileFunctionBodyCode(code[1:], assembler, registers)
            return out + suffix, error
        else:
            return None, out[1]
    
    return []
    
def addParametersToRegistersLookUp(parameters, registerLookup: dict[str, int]={}, availableParameterRegisters=[*range(1, 4)]):
    if(len(parameters) > 0):
        if(len(availableParameterRegisters) > 0):
            return addParametersToRegistersLookUp(parameters[1:], {parameters[0].identifier.value : availableParameterRegisters[0], **registerLookup}, availableParameterRegisters[1:])
        else:
            return None, "Too many parameters initialised (>3)"
    else:
        return registerLookup
        
        

def compileFunctionBody(node: FunctionDeclareNode):
    indent = "  "
    pushRegistersAssembler =  "push { r3, r4, r5, r6, r7, lr }"
    # storeParametersAssembler = "mov r3, r0" + [storeParametersAssembler] 
    popRegistersAssembler =  "pop { r3, r4, r5, r6, r7, pc }"
    bodyCodeAssembler, error = compileFunctionBodyCode(node.code.Sequence, registerLookup=addParametersToRegistersLookUp(node.parameterTypes))
    if(error == None):
        return list(map(addIndent, [pushRegistersAssembler] + bodyCodeAssembler + [popRegistersAssembler])), None
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
    out = list(map(compile, root.codeSequenceNode.Sequence))
    for function in out:
        for line in function[0]:
            print(line) 
        print("")
        
        
    return out[0]

              