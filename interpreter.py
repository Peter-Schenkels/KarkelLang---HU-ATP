from astNodes import *
from tokenParser import *
from enum import Enum
import copy


def getItemFromList(items: list[ASTNode], target:str) -> ASTNode:
    """High order function to Get item from a list

    Args:
        items (list): list of items
        target (str): target items identifier value

    Returns:
        ASTNode: item from list
    """    
    if(items == []):
        return None
    head, *tail = items
    if(head.identifier.value == target):
        return head
    else:
        return getItemFromList(tail, target)
    
def getIndexFromList(items: list, target:str) -> int:
    """High order function to Get index from a list

    Args:
        items (list): input items
        target (str): target items identifier value

    Returns:
        int: index of the target item
    """
    if(items == []):
        return -float("inf")
    head, *tail = items
    if(head.identifier.value == target):
        return 0
    else:
        return getIndexFromList(tail, target) + 1


class InterpreterObject(object):
    """Interpreter Object to store the interpreter state
    """
    def __init__(self, root: ASTRoot|dict, error: ErrorClass=None, currentFunction: FunctionNode=None):
        if type(root) == dict:
            self.__dict__.update(root)
        else:
            self.root = root
            self.error = error
            self.currentFunction = currentFunction

class VariableObject():
    """Variable Object to store the variable return state"""
    def __init__(self, variable: PrimitiveNode|dict, local: bool=None, localVariables: list=None, globalVariables: list=None): 
        if type(variable) == dict:
            self.__dict__.update(variable)
        else:
            self.variable = variable
            self.local = local
            self.localVariables = localVariables
            self.globalVariables = globalVariables

class OperatorObject():
    """Operator Object to store the operator return state"""
    def __init__(self, output: PrimitiveNode|dict, Error: ErrorClass=None):
        if(type(output) == dict):
            self.__dict__.update(output)
        else:
            self.output = output
            self.error = Error
 
def GetVariableFromContext(globalVariables: list, localVariables: list, parameters: list, name: PrimitiveNode) -> VariableObject:
    """Searches a target variable from a list of global and local variables based on a name and returns a VariableObject

    Args:
        globalVariables (list): list of global variables
        localVariables (list): list of local variables
        parameters (list): list of function parameters
        name (PrimitiveNode): name of the target variable

    Returns:
        VariableObject: the matched the variable
    """
    output = VariableObject(None, None, None, None)
    if(name.identifier == None or name.identifier.value == None):
        output = SetAttribute(output, "variable", name)
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        output = SetAttribute(SetAttribute(output, "local", True), "variable", localVariables[getIndexFromList(localVariables, name.identifier.value)]) 
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        output = SetAttribute(SetAttribute(output, "local", False), "variable",  globalVariables[getIndexFromList(globalVariables, name.identifier.value)])
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        output = SetAttribute(output, "variable", parameters[getIndexFromList(parameters, name.identifier.value)])
    if(output.variable != None and type(output.variable) != FunctionNode):
        if(output.variable.type == Types.INTEGER):
            output.variable.value = int(output.variable.value) #should be functional
        elif(output.variable.type == Types.STRING):
            output.variable.value = str(output.variable.value) #should be functional
    return output   

def GetListOfVariablesObjectFromContext(variables: list, globalVariables: list, localVariables: list, parameters: list) -> list[VariableObject]:
    """Searches target variables from a list of global and local variables based on a name and returns a list with VariableObjects

    Args:
        variables (list): target variables
        globalVariables (list): list of global variables
        localVariables (list): list of local variables
        parameters (list): list of function parameters

    Returns:
        list: list of found target variables
    """
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
    """Searches target variables from a list of global and local variables based on a name and returns a list with the variable member of the VariableObject

    Args:
        variables (list): target variables
        globalVariables (list): list of global variables
        localVariables (list): list of local variables
        parameters (list): list of function parameters

    Returns:
        list: list of found target variables
    """
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
    """Searches a target variable from a list of global and local variables based on a name and pops a VariableObject from the list

    Args:
        globalVariables (list): list of global variables
        localVariables (list): list of local variables
        parameters (list): list of function parameters
        name (PrimitiveNode): name of the target variable

    Returns:
        VariableObject: the matched the variable
    """
    output = VariableObject(None, None, None, None)
    variable = None
    if(name.identifier == None):
        flag = None
        variable = name
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        flag = True
        variable = localVariables.pop(getIndexFromList(localVariables, name.identifier.value))
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        flag = False
        variable = globalVariables.pop(getIndexFromList(globalVariables, name.identifier.value))
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        flag = None
        variable = parameters[getIndexFromList(parameters, name.identifier.value)]
    if(variable):
        output = SetAttribute(SetAttribute(output, "local", flag), "variable", variable)
    if(output.variable != None):
        if(output.variable.type == Types.INTEGER):
            output.variable.value = int(output.variable.value)
        elif(output.variable.type == Types.STRING):
            output.variable.value = str(output.variable.value)
    output = SetAttribute(output, "localVariables", localVariables)
    output = SetAttribute(output, "globalVariables", globalVariables)
    return output

def ExecuteOperator(inputNode: OperatorNode, context: FunctionNode, root: ASTRoot) -> OperatorObject:
    """Executes an operator based on the inputNode and returns an OperatorObject

    Args:
        inputNode (OperatorNode): input operator node
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        OperatorObject: output state of the operator
    """    
    
    node = copy.deepcopy(inputNode)
    if(context != None):
        localVariables = context.codeSequenceNode.LocalVariables
        parameters = context.parameters
    else:
        localVariables = []
        parameters = []
    
    left = VariableObject(None, None, None, None)
    right = VariableObject(None, None, None, None)
    if(type(node.left) == FunctionCallNode):
        output = ExecuteFunctionCallNode(node.left, context, root)
        if( output.error != None):
            return output
        left = SetAttribute(left, "variable", output.currentFunction.returnValue)
    else:
        left = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
    if(type(node.right) == FunctionCallNode):
        output = ExecuteFunctionCallNode(node.right, context, root)
        if( output.error != None):
            return output
        right = SetAttribute(right, "variable", output.currentFunction.returnValue)
    else:
        right = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.right)
        
    output = OperatorObject(None ,None)
    if(type(left.variable) == type(right.variable)):
        if(type(node) == AdditionNode):
            if(type(left.variable) is IntegerNode):
                node = SetAttribute(node, "left", IntegerNode(None, int(left.variable.value) + int(right.variable.value), None, node.lineNr))
            elif(type(left.variable) is StringNode):
                node = SetAttribute(node, "left", StringNode(None, str(left.variable.value) + str(right.variable.value), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Addition not available for this type", node.lineNr))
        elif(type(node) == SubtractionNode):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(left.variable.value) - int(right.variable.value), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Subtraction not available for this type", node.lineNr))
        elif(type(node) == MultiplicationNode):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(left.variable.value) * int(right.variable.value), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Multiplication not available for this type", node.lineNr))
        elif(type(node) == DivisionNode):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(left.variable.value) / int(right.variable.value), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Division not available for this type", node.lineNr))
        elif(type(node) == ComparisonNode):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node = SetAttribute(node, "left", IntegerNode(None, left.variable.value == right.variable.value, None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        elif(type(node) == ComparisonNodeGreaterThan):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(int(left.variable.value) > int(right.variable.value)), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        elif(type(node) == ComparisonNodeSmallerThan):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(int(left.variable.value) < int(right.variable.value)), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        elif(type(node) == ComparisonNodeGreaterThanEqual):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(int(left.variable.value) >= int(right.variable.value)), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        elif(type(node) == ComparisonNodeSmallerThanEqual):
            if(type(left.variable) in [IntegerNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(int(left.variable.value) <= int(right.variable.value)), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        elif(type(node) == ComparisonNodeNotEuqal):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node = SetAttribute(node, "left", IntegerNode(None, int(left.variable.value != right.variable.value), None, node.lineNr))
            else:
                output = SetAttribute(output, "error", ErrorClass("Comparison not available for this type", node.lineNr))
        else:
            output = SetAttribute(output, "error", ErrorClass("Operator error", node.lineNr))
        output = SetAttribute(output, "output", node.left)
        return output
    else:
        output = SetAttribute(output, "error", ErrorClass("Operator error", node.lineNr))
        return output

def ExecuteFunction(function: FunctionNode, root: ASTRoot) -> int | str:
    """Executes a function Node

    Args:
        function (FunctionNode): Input function Node
        root (ASTRoot): root of the AST

    Returns:
        int | str: output of the executed function node
    """
    output = interpreter(copy.deepcopy(function), root, None)
    return output.currentFunction.returnValue  

def ExecuteAssignNode(node: AssignNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes an AssignNode

    Args:
        node (AssignNode): input AssignNode
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        InterpreterObject: output context of the executed AssignNode
    """
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
        #LEFT VARIABLE
        left = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
        if(left.variable == None):
            if(node.declaration):
                left = SetAttribute(left, "variable", node.left)
                left = SetAttribute(left, "local", (context != None))
            else:
                return InterpreterObject(root, ErrorClass("Undefined variable: " +  node.left.identifier.value, node.lineNr))

        if(left == None ):
            return InterpreterObject(root, ErrorClass("Incorrect Assignation, left doesn't exist: ", node.lineNr))
        
        
        #RIGHT VARIABLE
        right = VariableObject(None, None, None, None)
        
        if(type(node.right) in [AdditionNode, SubtractionNode, MultiplicationNode, DivisionNode, ComparisonNode]):
            output = ExecuteOperator(node.right, context, root)
            if(output.error == None):
                right = SetAttribute(right, "variable", output.output)
            else:
                return InterpreterObject(root, output.error, context)
        else:
            if(type(node.right) == FunctionCallNode):
                output = ExecuteFunctionCallNode(node.right, context, root)
                if( output.error != None):
                    return output
                right = SetAttribute(right, "variable", output.currentFunction.returnValue)
            else:
                right = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.right)
            
        if(right == None ):
            return InterpreterObject(root, ErrorClass("Incorrect Assignation, right is an incorrect value: ", node.lineNr))
        # Check if variable is not a value but function or Operator
        if(type(right.variable) == FunctionNode):
            right = SetAttribute(right, "variable",ExecuteFunction(right.variable, root))
        elif(type(node.right) == OperatorNode):
            output = ExecuteOperator(node.right, context, root)
            if(output.error != None):
                right = SetAttribute(right, "variable", output.output)
            else:
                InterpreterObject(root, output.error, context)
                
        if(type(node.right) == ArrayAccesNode):
            if(type(right.variable) == ArrayNode):
                index = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.right.index)
                if(index.variable.value < len(right.variable.memory)):
                    right = SetAttribute(right, "variable", SetAttribute(right.variable, "index", index.variable.value))
                    right = SetAttribute(right, "variable", SetAttribute(right.variable, "value", right.variable.memory[index.variable.value].value))
                else:
                    return InterpreterObject(root, ErrorClass("Index out of bounds", node.lineNr), context) 
            else:
                return InterpreterObject(root, ErrorClass("Incorrect Assignation, expected Array", node.lineNr), context) 
                
        if(type(node.left) == ArrayAccesNode):
            if(type(left.variable) == ArrayNode):
                index = GetVariableFromContext(root.globalVariables, localVariables, parameters, node.left.index)
                if(index.variable.value < len(left.variable.memory)):
                    left = SetAttribute(left, "variable", SetAttribute(left.variable, "index", index.variable.value))
                    left = SetAttribute(left, "variable", SetAttribute(left.variable, "value", left.variable.memory[index.variable.value].value))
                else:
                    return InterpreterObject(root, ErrorClass("Index out of bounds", node.lineNr), context) 
            else:
                return InterpreterObject(root, ErrorClass("Incorrect Assignation, expected Array", node.lineNr), context) 
            
            
        if(type(left.variable) == type(right.variable) or type(left.variable.value) == type(right.variable.value)):
            left.variable.value = right.variable.value #oof
            if(type(left.variable) == ArrayNode):
                left.variable.memory[left.variable.index].value = left.variable.value #big oof
            if(left.local):
                output = PopVariableFromContext(root.globalVariables, localVariables, parameters, node.left)
                root = SetAttribute(root, "globalVariables", output.globalVariables)
                context = SetAttribute(context, "codeSequenceNode", SetAttribute(context.codeSequenceNode, "LocalVariables", output.localVariables + [left.variable]))
            elif(local == False or context == None):
                root = SetAttribute(root, "globalVariables", root.globalVariables + [left.variable])
            elif(not local ):
                context = SetAttribute(context, "parameters", parameters + [left.variable])
                
            return InterpreterObject(root, None, context)
    return InterpreterObject(root, ErrorClass("Types do not match: ", node.lineNr), context)

def ExecuteReturnNode(node: ReturnNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes a ReturnNode

    Args:
        node (ReturnNode): input ReturnNode
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        InterpreterObject: output context of the executed ReturnNode
    """    
    if(node.value != None):
        localVariables = context.codeSequenceNode.LocalVariables
        returnValue = PopVariableFromContext(root.globalVariables, localVariables,context.parameters, node.value)
        root = SetAttribute(root, "globalVariables", returnValue.globalVariables)
        localVariables = returnValue.localVariables
        if(returnValue.variable == None):
            return InterpreterObject(root, ErrorClass("Incorrect return Value: ", node.lineNr), context) 
        if(context.returnType == returnValue.variable.type):
            context = SetAttribute(SetAttribute(context, "returnValue", returnValue.variable), "codeSequenceNode", SetAttribute(context.codeSequenceNode, "Sequence", []))
            return InterpreterObject(root, None, context)
        else:
            return InterpreterObject(root, ErrorClass("Incorrect return type: ", node.lineNr), context)     

def ExecuteIfNode(node: IfNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes an IfNode

    Args:
        node (IfNode): input IfNode
        context (FunctionNode): context of the function
        root (ASTRoot): Root of the AST

    Returns:
        InterpreterObject: output context of the executed IfNode
    """
    if(node != None):
        output = ExecuteOperator(node.comparison, context, root)
        if(output.output.value == 1):
            context = SetAttribute(context, "codeSequenceNode", SetAttribute(context.codeSequenceNode, "Sequence", node.codeSequenceNode.Sequence + context.codeSequenceNode.Sequence))
            return interpreter(context, root, None)
        else:
            return InterpreterObject(root, None, context)
    return InterpreterObject(None, ErrorClass("Function stopped unexpectedly"), context.lineNr)

def ExecuteWhileNode(node: WhileNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes a WhileNode

    Args:
        node (WhileNode): input WhileNode
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        InterpreterObject: output context of the executed WhileNode
    """
    if(node != None):
        output = ExecuteOperator(node.comparison, context, root)
        if(output.output.value == 1):
            return interpreter(SetAttribute(context, "codeSequenceNode", SetAttribute(context.codeSequenceNode, "Sequence", node.codeSequenceNode.Sequence + [copy.deepcopy(node)] + context.codeSequenceNode.Sequence)), root, None)
        else:
            return InterpreterObject(root, None, context)
    return InterpreterObject(None, ErrorClass("Function stopped unexpectedly"), context.lineNr)
      

def interpreterRun(root: ASTRoot, error: ErrorClass = None) -> InterpreterObject:
    """Executes the AST

    Args:
        root (ASTRoot): input AST
        error (ErrorClass, optional): current error. Defaults to None.

    Returns:
        InterpreterObject: output state of the AST
    """    
    if(error == None):
        if(root.codeSequenceNode.Sequence != []):
            if(len(root.codeSequenceNode.Sequence) > 1):
                head, *tail = root.codeSequenceNode.Sequence    
            else:
                head = root.codeSequenceNode.Sequence[0]
                tail = []
            if(type(head) == FunctionDeclareNode):
                output = ExecuteFunctionDeclareNode(head, None, root)
                output = SetAttribute(output, "root", SetAttribute(output.root, "codeSequenceNode", SetAttribute(output.root.codeSequenceNode, "Sequence", tail)))
                return interpreterRun(output.root, output.error)
            if(type(head) == AssignNode):
                output = ExecuteAssignNode(head, None, root)
                output = SetAttribute(output, "root", SetAttribute(output.root, "codeSequenceNode", SetAttribute(output.root.codeSequenceNode, "Sequence", tail)))
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

def ExecuteFunctionDeclareNode(node: FunctionDeclareNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes a FunctionDeclareNode

    Args:
        node (FunctionDeclareNode): input FunctionDeclareNode
        context (FunctionNode): context of the function
        root (ASTRoot): ast root
        
    Returns:
        InterpreterObject: output context of the executed FunctionDeclareNode
    """
    if(context == None):
        root = SetAttribute(root, "globalVariables", root.globalVariables + [FunctionNode(None, node.returnType, node.parameterTypes, CodeSequenceNode(None, None, node.code.Sequence, node.lineNr), node.identifier, node.lineNr)])
        return InterpreterObject(root, None, None)
    else:
        return InterpreterObject(None, ErrorClass("Cannot declare a function inside a function"), node.lineNr)

def CheckParameterTypes(parameters: list[(PrimitiveNode, PrimitiveNode)]) -> int:
    """Checks if the input parameter types correspond with the function parameters types

    Args:
        parameters (list[(PrimitiveNode, PrimitiveNode)]): list of parameters

    Returns:
        int: returns False if the types are incorrect, True if they are correct
    """    
    if(parameters != []):
        if(len(parameters) == 1):
            output = (type(parameters[0][0]) == type(parameters[0][1])) 
            return output
        head, *tail = parameters
        return (type(head[0]) == type(head[1])) + CheckParameterTypes(tail)
    return 0

def AssignValue(x: tuple):
    x[0].value = x[1].value #big oof
    return x[0]

def ExecuteFunctionCallNode(node: FunctionCallNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes a FunctionCallNode

    Args:
        node (FunctionCallNode): input FunctionCallNode  
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        InterpreterObject: output context of the executed FunctionCallNode
    """    
    output = copy.deepcopy(GetVariableFromContext(root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters, node ))
    function = output.variable
    if(function != None):
        if(type(function) == FunctionNode):
            parameters = GetListOfVariablesFromContext(node.parameters, root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters)
            parameterCheck = list(zip(function.parameterTypes, parameters))
            if(CheckParameterTypes(parameterCheck) == len(function.parameterTypes)):  
                if(len(parameters) == len(parameterCheck)):
                    parameters = list(zip(function.parameterTypes, parameters))
                    function = SetAttribute(function, "parameters", list(map(AssignValue, parameters)))             
                    if((function.identifier.value == "IntOut" or function.identifier.value =="StringOut") and len(parameters) == 1):
                        print(parameters[0][0].value, end = '')
                        return InterpreterObject(root, None, context)
                    elif((function.identifier.value == "IntOutLine" or function.identifier.value == "StringOutLine") and len(parameters) == 1):
                        print(parameters[0][0].value)
                        return InterpreterObject(root, None, context)
                    else:    
                        return interpreter(function, root, None)
                else:
                    return InterpreterObject(None, ErrorClass("Missing Parameters", node.lineNr), None)
                
            else:
                return InterpreterObject(None, ErrorClass("Parameters do not match function declaration", node.lineNr), context)
        else:
            return InterpreterObject(None, ErrorClass("Invalid function call", node.lineNr), context)
    else:
        return InterpreterObject(None, ErrorClass("Function doesnt exist", node.lineNr), context)


def initArrayMemory(node: ArrayNode, count=0) -> ArrayNode:
    """Initializes the memory of an arraynode

    Args:
        node (ArrayNode): _description_
        count (int, optional): _description_. Defaults to 0.

    Returns:
        ArrayNode: Output array node with initialised memory
    """    
    if(count != node.size):
        return initArrayMemory(SetAttribute(node, "memory", node.memory + [copy.deepcopy(node.type)]), count+1)
    else:
        return node

def ExecuteArrayNode(node: ArrayNode, context: FunctionNode, root: ASTRoot) -> InterpreterObject:
    """Executes an ArrayNode

    Args:
        node (ArrayNode): input ArrayNode
        context (FunctionNode): context of the function
        root (ASTRoot): root of the AST

    Returns:
        InterpreterObject: output context of the executed ArrayNode
    """    
    if(context != None):
        localVariables = context.codeSequenceNode.LocalVariables
        parameters = context.parameters
    else:
        localVariables = []
        parameters = []
    
    node = SetAttribute(node, "size", GetVariableFromContext(root.globalVariables, localVariables, parameters, node.size).variable.value)
    context = SetAttribute(context, "codeSequenceNode", SetAttribute(context.codeSequenceNode, "LocalVariables", context.codeSequenceNode.LocalVariables + [initArrayMemory(node)]))
    return InterpreterObject(root, None, context)

def interpreter(node: FunctionNode, root: ASTRoot, error: ErrorClass = None) -> InterpreterObject:
    """Executes a FunctionNode

    Args:
        node (FunctionNode): input FunctionNode
        root (ASTRoot): root of the AST
        error (ErrorClass, optional): current error. Defaults to None.

    Returns:
        InterpreterObject: output context of the executed FunctionNode
    """    
    if(error == None):
        if(node.codeSequenceNode.Sequence != []):
            head, *tail = node.codeSequenceNode.Sequence
            node = SetAttribute(node, "codeSequenceNode", SetAttribute(node.codeSequenceNode, "Sequence", tail))
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
            elif(type(head) == WhileNode):
                output = ExecuteWhileNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == FunctionDeclareNode):
                output = ExecuteFunctionDeclareNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == FunctionCallNode):
                output = ExecuteFunctionCallNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)    
            elif(type(head) == ArrayNode):
                output = ExecuteArrayNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            elif(type(head) == CommentNode):
                return interpreter(node, root, None)
        else:
            return InterpreterObject(root, None, node)
    else:
        return InterpreterObject([], error, None)
    


    
    