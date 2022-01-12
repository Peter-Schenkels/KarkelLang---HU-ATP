from interpreter import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    
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
        print(bcolors.OKGREEN + "Test Assign Function Succeeded") 
    else:
        print(bcolors.WARNING + "Test Assign Function Failed")
        
def TestAssignOperator():        
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    VariableTwo = IntegerNode(None, 33, IdentifierNode(None, "left", 0), 0)
    VariableThree = IntegerNode(None, 36, IdentifierNode(None, "right", 0), 0)
    operatorNode = AdditionNode(None, VariableTwo, VariableThree, 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), operatorNode, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    codeSequenceNode.LocalVariables.append(VariableThree)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
     
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 69):
        print(bcolors.OKGREEN +"Test Assign operator Succeeded") 
    else:
        print(bcolors.WARNING + "Test Assign operator Failed")
        
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
        print(bcolors.OKGREEN +"Test Assign Succeeded") 
    else:
        print(bcolors.WARNING + "Test Assign Failed")

def TestIncorrectAssign():        
    VariableOne = StringNode(None, "Arkel", IdentifierNode(None, "Erkel", 0), 0)
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), IntegerNode(None, None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
    if(output.error.what == "Types do not match: "):
         print(bcolors.OKGREEN +"Test assign incorrect type Succeeded") 
    else:
        print(bcolors.WARNING + "Test assign incorrect type Failed")
    return output   
   
def TestAssignNonExistingVariable():        
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), IntegerNode(None, None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot) 
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 2553):
        print(bcolors.OKGREEN +"Test Assign Non existing variable Succeeded") 
    else:
        print(bcolors.WARNING + "Test Assign Non existing variable Failed")

    
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
         print(bcolors.OKGREEN +"Test return Succeeded") 
    else:
        print(bcolors.WARNING + "Test return Failed")
    return output

def TestReturnInCorrectReturnType():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error.what == "Incorrect return type: "):
         print(bcolors.OKGREEN +"Test return incorrect type Succeeded") 
    else:
        print(bcolors.WARNING + "Test return incorrect type Failed")
    return output   

def TestReturnInCorrectReturnValue():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error.what == "Incorrect return Value: "):
         print(bcolors.OKGREEN +"Test return incorrect value Succeeded") 
    else:
        print(bcolors.WARNING + "Test return incorrect value Failed")
    return output    

def TestIfStatement():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = IfNode()
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTNode(None, 0)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error.what == "Incorrect return Value: "):
         print(bcolors.OKGREEN +"Test return incorrect value Succeeded") 
    else:
        print(bcolors.WARNING + "Test return incorrect value Failed")
    return output      
        
if __name__ == '__main__':
    TestReturnCorrectReturnType()
    TestAssign()
    TestAssignFunction()
    TestAssignOperator()
    TestAssignNonExistingVariable()
    TestReturnInCorrectReturnType()
    TestReturnInCorrectReturnValue()
    TestIncorrectAssign()

