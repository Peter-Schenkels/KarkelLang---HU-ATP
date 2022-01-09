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

def ExecuteAssignNode(node: AssignNode, context: FunctionNode, root: ASTRoot):
    left = None
    local = None
    localVariables = context.codeSequenceNode.LocalVariables
    if(node.left == None or node.right == None):
        return InterpreterObject(root, ErrorClass("Incorrect Assignation: ", node.lineNr))
    
    if(getIndexFromList(localVariables, node.left.identifier.value) >= 0):
        left = localVariables.pop(getIndexFromList(localVariables, node.left.identifier.value))
        local = True
    elif(getIndexFromList(root.globalVariables, node.left.identifier.value) >= 0):
        left = root.globalVariables.pop(getIndexFromList(root.globalVariables, node.left.identifier.value))
        local = False
    elif(node.left.identifier == None ):
        return InterpreterObject(root, ErrorClass("Incorrect Assignation, left variable cant be None: ", node.lineNr))
    else:
        left = node.left

    if(node.right.identifier == None):
        right = node.right 
    elif(getIndexFromList(localVariables, node.right.identifier.value) >= 0):
        right =  localVariables[getIndexFromList(localVariables, node.right.identifier.value)]
    elif(getIndexFromList(root.globalVariables, node.right.identifier.value)  >= 0):
        right =  root.globalVariables[getIndexFromList(root.globalVariables, node.right.identifier.value)]
    else:
        return InterpreterObject(root, ErrorClass("Incorrect Assignation: ", node.lineNr), context)
    if(type(right) == FunctionNode):
        if(right.returnType == type(left)):
            output = interpreter(right, root, None)
            right = output.currentFunction.returnValue
        else:
            return InterpreterObject(root, ErrorClass("Output type of function is does not match variable type: ", node.lineNr), context)
    if(type(left) == type(right)):
        left.value = right.value
        if(local):
            localVariables.append(left)
        elif(not local):
            root.globalVariables.append(left)
        return InterpreterObject(root, None, context)
   
    return InterpreterObject(root, ErrorClass("Types do not match: ", node.lineNr), context)

def ExecuteReturnNode(node: ReturnNode, context: FunctionNode, root: ASTRoot):
    if(node.value != None):
        returnValue = None
        localVariables = context.codeSequenceNode.LocalVariables
        if(node.value.identifier == None):
            returnValue = node.value.value
        elif(getIndexFromList(localVariables, node.value.identifier.value) >= 0):
            returnValue = localVariables[getIndexFromList(localVariables, node.value.identifier.value)]
        elif(getIndexFromList(root.globalVariables, node.value.identifier.value)  >= 0):
            returnValue = root.globalVariables[getIndexFromList(root.globalVariables, node.identifier.value)]
        else:
            return InterpreterObject(root, ErrorClass("Incorrect return Value: ", node.lineNr), context) 
        if(context.returnType == type(returnValue)):
            context.returnValue = node.value
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
            if(head == []):
                return InterpreterObject(node, root, None)
            if(type(head) == FunctionNode):
                node.codeSequenceNode.Sequence = tail
                output = interpreter(head, root, None)
                return interpreter(node, output.root, output.error)
            if(type(head) == AssignNode):
                node.codeSequenceNode.Sequence = tail
                output = ExecuteAssignNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
            if(type(head) == ReturnNode):
                node.codeSequenceNode.Sequence = tail
                output = ExecuteReturnNode(head, node, root)
                return interpreter(output.currentFunction, output.root, output.error)
        else:
            return InterpreterObject(root, None, node)
    else:
        print(error.what)
        print(error.where)
    
    
def TestAssignFunction():    
    returnVariable = IntegerNode(None, 69, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = ReturnNode(None, returnVariable, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(returnVariable)
    function = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Sukkel", 0), 0)
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), FunctionNode(None, IntegerNode, [], [], IdentifierNode([], "Sukkel", 0), 0), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(function)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    
    if(check.value == 69):
        print("Test Assign Function Succeeded") 
    else:
        print("Test Assign Function Failed")
    
def TestAssign():        
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), IntegerNode(None, None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
     
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 2553):
        print("Test Assign Succeeded") 
    else:
        print("Test Assign Failed")
    
def TestReturnCorrectReturnType():    
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.currentFunction.returnValue.value == 5):
         print("Test return Succeeded") 
    else:
        print("Test return Failed")
    return output
       
        
if __name__ == '__main__':
    TestReturnCorrectReturnType()
    TestAssign()
    TestAssignFunction()


    
    