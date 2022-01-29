from astNodes import *
from tokenParser import *
from enum import Enum


#High order function to Get item from a list
def getItemFromList(items: list, target:str):
    if(items == []):
        return None
    head, *tail = items
    if(head.identifier.value == target):
        return head
    else:
        return getItemFromList(tail, target)
    
def getIndexFromList(items: list, target:str):
    if(items == []):
        return -float("inf")
    head, *tail = items
    if(head.identifier.value == target):
        return 0
    else:
        return getIndexFromList(tail, target) + 1


class InterpreterObject(object):
    def __init__(self, root: ASTRoot, error: ErrorClass, currentFunction: FunctionNode =None):
        self.root = root
        self.error = error
        self.currentFunction = currentFunction

class VariableObject():
    def __init__(self, variable: PrimitiveNode, local: bool, localVariables: list, globalVariables: list): 
        self.variable = variable
        self.local = local
        self.localVariables = localVariables
        self.globalVariables = globalVariables

class OperatorObject():
    def __init__(self, output: PrimitiveNode, Error: ErrorClass):
        self.output = output
        self.Error = Error
 
def GetVariableFromContext(globalVariables: list, localVariables: list, parameters: list, name: PrimitiveNode) -> VariableObject:
    output = VariableObject(None, None, None, None)
    if(name.identifier == None or name.identifier.value == None):
        output.variable = name
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        output.variable = localVariables[getIndexFromList(localVariables, name.identifier.value)]
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        output.variable = globalVariables[getIndexFromList(globalVariables, name.identifier.value)]
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        output.variable = parameters[getIndexFromList(parameters, name.identifier.value)]
    if(output.variable != None and type(output.variable) != FunctionNode):
        if(output.variable.type == Types.INTEGER):
            output.variable.value = int(output.variable.value)
        elif(output.variable.type == Types.STRING):
            output.variable.value = str(output.variable.value)
    return output   

def GetListOfVariablesObjectFromContext(variables: list, globalVariables: list, localVariables: list, parameters: list) -> list:
    if(variables != []):
        if(len(variables) > 1):
            head, *tail = variables
        else:
            head = variables[0]
            tail = []
        variable = GetVariableFromContext(globalVariables, localVariables, parameters, head)
        if(variable.variable != None):
            return [variable] + GetListOfVariablesFromContext(tail, globalVariables, localVariables, parameters)
        else:
            return
    else:
        return []
        
def GetListOfVariablesFromContext(variables: list, globalVariables: list, localVariables: list, parameters: list) -> list:
    if(variables != []):
        if(len(variables) > 1):
            head, *tail = variables
        else:
            head = variables[0]
            tail = []
        variable = GetVariableFromContext(globalVariables, localVariables, parameters, head)
        if(variable.variable != None):
            return [variable.variable] + GetListOfVariablesFromContext(tail, globalVariables, localVariables, parameters)
        else:
            return
    else:
        return []


def PopVariableFromContext(globalVariables: list, localVariables: list, parameters: list, name: PrimitiveNode) -> VariableObject:
    output = VariableObject(None, None, None, None)
    if(name.identifier == None):
        output.variable = name
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        output.variable = localVariables.pop(getIndexFromList(localVariables, name.identifier.value))
        output.local = True
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        output.variable = globalVariables.pop(getIndexFromList(globalVariables, name.identifier.value))
        output.local = False
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        output.variable = parameters[getIndexFromList(parameters, name.identifier.value)]
        output.local = None
    if(output.variable != None):
        if(output.variable.type == Types.INTEGER):
            output.variable.value = int(output.variable.value)
        elif(output.variable.type == Types.STRING):
            output.variable.value = str(output.variable.value)
    output.localVariables = localVariables
    output.globalVariables = globalVariables
    return output

def ExecuteOperator(node: OperatorNode, context: FunctionNode, root: ASTRoot) -> OperatorObject:
    if(context != None):
        localVariables = context.codeSequenceNode.LocalVariables
        parameters = context.parameters
    else:
        localVariables = []
        parameters = []
    
    left = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
    right = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.right)
    output = OperatorObject(None ,None)
    if(type(left.variable) == type(right.variable)):
        if(type(node) == AdditionNode):
            if(type(left.variable) is IntegerNode):
                node.left = IntegerNode(None, int(left.variable.value) + int(right.variable.value), None, node.lineNr)
                output.output = node.left
            elif(type(left.variable) is StringNode):
                node.left = StringNode(None, str(left.variable.value) + str(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Addition not available for this type", node.lineNr)
        elif(type(node) == SubtractionNode):
            if(type(left.variable) in [IntegerNode]):
                node.left = IntegerNode(None, int(left.variable.value) - int(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Subtraction not available for this type", node.lineNr)
        elif(type(node) == MultiplicationNode):
            if(type(left.variable) in [IntegerNode]):
                node.left = IntegerNode(None, int(left.variable.value) * int(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Multiplication not available for this type", node.lineNr)
        elif(type(node) == DivisionNode):
            if(type(left.variable) in [IntegerNode]):
                node.left = IntegerNode(None, int(left.variable.value) / int(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Division not available for this type", node.lineNr)
        elif(type(node) == ComparisonNode):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node.left = IntegerNode(None, left.variable.value == right.variable.value, None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Comparison not available for this type", node.lineNr)
        elif(type(node) == ComparisonNodeGreaterThan):
            if(type(left.variable) in [IntegerNode]):
                node.left = IntegerNode(None, int(left.variable.value) > int(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Comparison not available for this type", node.lineNr)
        elif(type(node) == ComparisonNodeSmallerThan):
            if(type(left.variable) in [IntegerNode]):
                node.left = IntegerNode(None, int(left.variable.value) < int(right.variable.value), None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Comparison not available for this type", node.lineNr)
        elif(type(node) == ComparisonNodeNotEuqal):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node.left = IntegerNode(None, left.variable.value != right.variable.value, None, node.lineNr)
                output.output = node.left
            else:
                output.error = ErrorClass("Comparison not available for this type", node.lineNr)
        else:
            output.error = ErrorClass("Operator error", node.lineNr)
        return output
    else:
        output.error = ErrorClass("Operator error", node.lineNr)
        return output

def ExecuteAssignNode(node: AssignNode, context: FunctionNode, root: ASTRoot):
    left = None
    local = None
    if(context != None):
        localVariables = context.codeSequenceNode.LocalVariables
        parameters = context.parameters
    else:
        localVariables = []
        parameters = []
    if(node.left == None or node.right == None):
        return InterpreterObject(root, ErrorClass("Incorrect Assignation: ", node.lineNr))
    else:
        left = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
        if(left.variable == None):
            if(node.declaration):
                left.variable = node.left
                left.local = context != None
            else:
                return InterpreterObject(root, ErrorClass("Undefined variable: " +  node.left.identifier.value, node.lineNr))

        if(left == None ):
            return InterpreterObject(root, ErrorClass("Incorrect Assignation, left doesn't exist: ", node.lineNr))
        
        right = VariableObject(None, None, None, None)
        
        if(type(node.right) in [AdditionNode, SubtractionNode, MultiplicationNode, DivisionNode, ComparisonNode]):
            output = ExecuteOperator(node.right, context, root)
            if(output.Error == None):
                right.variable = output.output
            else:
                return InterpreterObject(root, output.Error, context)
        else:
            if(type(node.right) == FunctionCallNode):
                output = ExecuteFunctionCallNode(node.right, context, root)
                if( output.error != None):
                    return output
                right.variable = output.currentFunction.returnValue
            else:
                right = PopVariableFromContext(root.globalVariables, localVariables, parameters, node.right)
            
        if(right == None ):
            return InterpreterObject(root, ErrorClass("Incorrect Assignation, right is an incorrect value: ", node.lineNr))
        
        # Check if variable is not a value but function or Operator
        if(type(right.variable) == FunctionNode):
            output = interpreter(right.variable, root, None)
            right.variable = output.currentFunction.returnValue  
        elif(type(node.right) == OperatorNode):
            output = ExecuteOperator(node.right, context, root)
            if(output.error != None):
                right.variable = output.output
            else:
                InterpreterObject(root, output.error, context)
                
        if(type(left.variable) == type(right.variable) or type(left.variable.value) == type(right.variable.value)):
            left.variable.value = right.variable.value
            if(left.local):
                output = PopVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
                root.globalVariables = output.globalVariables
                localVariables = output.localVariables
                localVariables.append(left.variable)
            elif(not local or context == None):
                root.globalVariables.append(left.variable)
                
            return InterpreterObject(root, None, context)
    return InterpreterObject(root, ErrorClass("Types do not match: ", node.lineNr), context)

def ExecuteReturnNode(node: ReturnNode, context: FunctionNode, root: ASTRoot):
    if(node.value != None):
        localVariables = context.codeSequenceNode.LocalVariables
        returnValue = PopVariableFromContext(root.globalVariables, localVariables,context.parameters, node.value)
        root.globalVariables = returnValue.globalVariables
        localVariables = returnValue.localVariables
        if(returnValue.variable == None):
            return InterpreterObject(root, ErrorClass("Incorrect return Value: ", node.lineNr), context) 
        if(context.returnType == returnValue.variable.type):
            context.returnValue = returnValue.variable
            context.codeSequenceNode.Sequence = []
            return InterpreterObject(root, None, context)
        else:
            return InterpreterObject(root, ErrorClass("Incorrect return type: ", node.lineNr), context)     

def ExecuteIfNode(node: IfNode, context: FunctionNode, root: ASTRoot):
    if(node != None):
        output = ExecuteOperator(node.comparison, context, root)
        if(output.output.value):
            node.codeSequenceNode.Sequence += context.codeSequenceNode.Sequence
            context.codeSequenceNode.Sequence = node.codeSequenceNode.Sequence
            return interpreter(context, root, None)
        else:
            return InterpreterObject(root, None, context)
    return InterpreterObject(None, ErrorClass("Function stopped unexpectedly"), context.lineNr)
      

def interpreterRun(root: ASTRoot, error: ErrorClass = None) -> InterpreterObject:
    if(error == None):
        if(root.codeSequenceNode.Sequence != []):
            if(len(root.codeSequenceNode.Sequence) > 1):
                head, *tail = root.codeSequenceNode.Sequence    
            else:
                head = root.codeSequenceNode.Sequence[0]
                tail = []
            if(type(head) == FunctionDeclareNode):
                output = ExecuteFunctionDeclareNode(head, None, root)
                output.root.codeSequenceNode.Sequence = tail
                return interpreterRun(output.root, output.error)
            if(type(head) == AssignNode):
                output = ExecuteAssignNode(head, None, root)
                output.root.codeSequenceNode.Sequence = tail
                return interpreterRun(output.root, output.error)
        
        mainNode = getItemFromList(root.globalVariables, "Main")
        if(mainNode != None):
            if(type(mainNode) == FunctionNode):
                return interpreter(mainNode, root)
        print("No main function found!")
        return False
    else:
        print(error.what + error.where)
        return False

def ExecuteFunctionDeclareNode(node: FunctionDeclareNode, context: FunctionNode, root: ASTRoot):
    if(context == None):
        function = FunctionNode(None, node.returnType, node.parameterTypes, CodeSequenceNode(None, None, node.code.Sequence, node.lineNr), node.identifier, node.lineNr)
        root.globalVariables.append(function)
        return InterpreterObject(root, None, None)
    else:
        return InterpreterObject(None, ErrorClass("Cannot declare a function inside a function"), node.lineNr)

def CheckParameterTypes(parameters: list) -> int:
    if(parameters != []):
        if(len(parameters) == 1):
            return (type(parameters[0][0]) == type(parameters[0][1])) 
        head, *tail = parameters
        return (type(head[0]) == type(head[1])) + CheckParameterTypes(tail)
    return 0

def AssignValue(x: tuple):
    x[0].value = x[1].value
    return x[0]

def ExecuteFunctionCallNode(node: FunctionCallNode, context: FunctionNode, root: ASTRoot):
    output = GetVariableFromContext(root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters, node )
    function = output.variable
    if(function != None):
        if(type(function) == FunctionNode):
            parameters = GetListOfVariablesFromContext(node.parameters, root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters)
            parameterCheck = list(zip(function.parameterTypes, parameters))
            if(CheckParameterTypes(parameterCheck) == len(function.parameterTypes)):  
                if(len(parameters) == len(parameterCheck)):
                    parameters = list(zip(function.parameterTypes, parameters))             
                    function.parameters = list(map(AssignValue, parameters))
                    return interpreter(function, root, None)
                else:
                    return InterpreterObject(None, ErrorClass("Missing Parameters", node.lineNr), None)
                
            else:
                return InterpreterObject(None, ErrorClass("Parameters do not match function declaration", node.lineNr), context)
        else:
            return InterpreterObject(None, ErrorClass("Invalid function call", node.lineNr), context)
    else:
        return InterpreterObject(None, ErrorClass("Function doesnt exist", node.lineNr), context)
        

def interpreter(node: FunctionNode, root: ASTRoot, error: ErrorClass = None) -> InterpreterObject:
    if(error == None):
        if(node.codeSequenceNode.Sequence != []):
            head, *tail = node.codeSequenceNode.Sequence
            node.codeSequenceNode.Sequence = tail
            if(head == []):
                return InterpreterObject(node, root, None)
            elif(type(head) == FunctionNode):
                output = interpreter(head, root, None)
                return interpreter(node, output.root, output.error)
            elif(type(head) == AssignNode):
                output = ExecuteAssignNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == ReturnNode):
                output = ExecuteReturnNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == IfNode):
                output = ExecuteIfNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == FunctionDeclareNode):
                output = ExecuteFunctionDeclareNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == FunctionCallNode):
                output = ExecuteFunctionCallNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)    
        else:
            return InterpreterObject(root, None, node)
    else:
        return InterpreterObject([], error, None)
    


    
    