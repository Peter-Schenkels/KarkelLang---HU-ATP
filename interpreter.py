from astNodes import *
from tokenParser import *

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
    def __init__(self, root: ASTNode, error: ErrorClass, currentFunction: FunctionNode =None):
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
    if(name.identifier == None):
        output.variable = name.value
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        output.variable = localVariables[getIndexFromList(localVariables, name.identifier.value)]
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        output.variable = globalVariables[getIndexFromList(globalVariables, name.identifier.value)]
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        output.variable = parameters[getIndexFromList(parameters, name.identifier.value)]
    return output   
     
def PopVariableFromContext(globalVariables: list, localVariables: list, parameters: list, name: PrimitiveNode) -> VariableObject:
    output = VariableObject(None, None, None, None)
    if(name.identifier == None):
        output.variable = name.value
    elif(getIndexFromList(localVariables, name.identifier.value) >= 0):
        output.variable = localVariables.pop(getIndexFromList(localVariables, name.identifier.value))
        output.local = True
    elif(getIndexFromList(globalVariables, name.identifier.value) >= 0):
        output.variable = globalVariables.pop(getIndexFromList(globalVariables, name.identifier.value))
        output.local = False
    elif(getIndexFromList(parameters, name.identifier.value) >= 0):
        output.variable = parameters[getIndexFromList(parameters, name.identifier.value)]
        output.local = None

    output.localVariables = localVariables
    output.globalVariables = globalVariables
    return output

def ExecuteOperator(node: OperatorNode, context: FunctionNode, root: ASTRoot):
    left = GetVariableFromContext(root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters, node.left)
    right = GetVariableFromContext(root.globalVariables, context.codeSequenceNode.LocalVariables, context.parameters, node.right)
    output = OperatorObject(None ,None)
    if(type(left.variable) == type(right.variable)):
        if(type(node) == AdditionNode):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node.left.value = node.left.value + node.right.value
                output.output = node.left
            else:
                output.error = ErrorClass("Addition not available for this type", node.lineNr)
        elif(type(node) == SubtractionNode):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node.left.value = node.left.value + node.right.value
                output.output = node.left
            else:
                output.error = ErrorClass("Subtraction not available for this type", node.lineNr)
        elif(type(node) == MultiplicationNode):
            if(type(left.variable) in [IntegerNode]):
                node.left.value = node.left.value * node.right.value
                output.output = node.left
            else:
                output.error = ErrorClass("Multiplication not available for this type", node.lineNr)
        elif(type(node) == DivisionNode):
            if(type(left.variable) in [IntegerNode]):
                node.left.value = node.left.value / node.right.value
                output.output = node.left
            else:
                output.error = ErrorClass("Division not available for this type", node.lineNr)
        elif(type(node) == ComparisonNode):
            if(type(left.variable) in [IntegerNode, StringNode]):
                node.left.value = node.left.value == node.right.value
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
    localVariables = context.codeSequenceNode.LocalVariables
    if(node.left == None or node.right == None):
        return InterpreterObject(root, ErrorClass("Incorrect Assignation: ", node.lineNr))
    else:
        left = PopVariableFromContext(root.globalVariables, localVariables, context.parameters, node.left)
        if(left.variable == None):
            left.localVariables.append(node.left)
            left.variable = node.left
        root.globalVariables = left.globalVariables
        localVariables = left.localVariables
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
            right = PopVariableFromContext(root.globalVariables, localVariables, context.parameters, node.right)
            
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
                
        if(type(left.variable) == type(right.variable)):
            left.variable.value = right.variable.value
            if(left.local):
                localVariables.append(left.variable)
            elif(not local):
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
        if(context.returnType == type(returnValue.variable)):
            context.returnValue = returnValue.variable
            return InterpreterObject(root, None, context)
        else:
            return InterpreterObject(root, ErrorClass("Incorrect return type: ", node.lineNr), context)     
        

def interpreterRun(root: ASTRoot) -> InterpreterObject:
    mainNode = getItemFromList(root.globalVariables, "Main")
    if(mainNode != None):
        if(type(mainNode) == FunctionNode):
            return interpreter(mainNode, root)
    print("No main function found!")
    return False

def interpreter(node: FunctionNode, root: ASTRoot, error: ErrorClass = None) -> InterpreterObject:
    if(error == None):
        if(node.codeSequenceNode.Sequence != []):
            head, *tail = node.codeSequenceNode.Sequence
            node.codeSequenceNode.Sequence = tail
            if(head == []):
                return InterpreterObject(node, root, None)
            if(type(head) == FunctionNode):
                output = interpreter(head, root, None)
                return interpreter(node, output.root, output.error)
            if(type(head) == AssignNode):
                output = ExecuteAssignNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            if(type(head) == ReturnNode):
                output = ExecuteReturnNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            if(type(head) == IfNode):
                output = ExecuteReturnNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
        else:
            return InterpreterObject(root, None, node)
    else:
        return InterpreterObject([], error, None)
    


    
    