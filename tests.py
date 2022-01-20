from interpreter import *

def TestAssignFunction():    
    returnVariable = IntegerNode(None, 69, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = ReturnNode(None, returnVariable, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(returnVariable)
    function = FunctionNode(None, Types.INTEGER, [], codeSequenceNode, IdentifierNode([], "Sukkel", 0), 0)
    functionCall = FunctionCallNode(None, None, [], IdentifierNode([], "Sukkel", 0), 0)
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), functionCall, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, Types.INTEGER, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(function)
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    
    if(check.value == 69):
        print(bcolors.OKGREEN + "Test Assign Function Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test Assign Function Failed"+ bcolors.RESET)
        
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
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
     
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 69):
        print(bcolors.OKGREEN +"Test Assign operator Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test Assign operator Failed"+ bcolors.RESET)
        
def TestAssign():        
    VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, PrimitiveNode(None, IdentifierNode(None, "Erkel", 0), 0), PrimitiveNode(None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
     
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 2553):
        print(bcolors.OKGREEN +"Test Assign Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test Assign Failed"+ bcolors.RESET)

def TestIncorrectAssign():        
    VariableOne = StringNode(None, "Arkel", IdentifierNode(None, "Erkel", 0), 0)
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), IntegerNode(None, None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)  
    if(output.error.what == "Types do not match: "):
         print(bcolors.OKGREEN +"Test assign incorrect type Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test assign incorrect type Failed"+ bcolors.RESET)
    return output   
   
def TestAssignNonExistingVariable():        
    VariableTwo = IntegerNode(None, 2553, IdentifierNode(None, "jerkel", 0), 0)
    lineOne = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Erkel", 0), 0), IntegerNode(None, None, IdentifierNode(None, "jerkel", 0), 0 ), 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableTwo)
    mainFunction = FunctionNode(None, type(AssignNode), [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot) 
    check = getItemFromList(output.currentFunction.codeSequenceNode.LocalVariables, "Erkel")
    if(check.value == 2553):
        print(bcolors.OKGREEN +"Test Assign Non existing variable Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test Assign Non existing variable Failed"+ bcolors.RESET)

    
# def TestReturnCorrectReturnType():    
#     VariableOne = IntegerNode(None, 5, IdentifierNode(None, "Erkel", 0), 0)
#     lineOne = ReturnNode(None, VariableOne, 0)
#     codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
#     codeSequenceNode.LocalVariables.append(VariableOne)
#     mainFunction = FunctionNode(None, Types.INTEGER, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
#     astRoot = ASTRoot()
#     astRoot.globalVariables.append(mainFunction)
#     output = interpreterRun(astRoot)   
#     if(output.currentFunction.returnValue.value == 5):
#          print(bcolors.OKGREEN +"Test return Succeeded"+ bcolors.RESET) 
#     else:
#         print(bcolors.WARNING + "Test return Failed"+ bcolors.RESET)
#     return output

def TestReturnInCorrectReturnType():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error.what == "Incorrect return type: "):
         print(bcolors.OKGREEN +"Test return incorrect type Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test return incorrect type Failed"+ bcolors.RESET)
    return output   

def TestReturnCorrectReturnType():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    codeSequenceNode.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, Types.STRING, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error == None):
         print(bcolors.OKGREEN +"Test return correct type Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test return correct type Failed"+ bcolors.RESET)
    return output   

def TestReturnInCorrectReturnValue():    
    VariableOne = StringNode(None, "Arkel is zelfstandige gemeetne", IdentifierNode(None, "Erkel", 0), 0)
    lineOne = ReturnNode(None, VariableOne, 0)
    codeSequenceNode = CodeSequenceNode(None, [], [lineOne], 0)
    mainFunction = FunctionNode(None, IntegerNode, [], codeSequenceNode, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.error.what == "Incorrect return Value: "):
         print(bcolors.OKGREEN +"Test return incorrect value Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test return incorrect value Failed"+ bcolors.RESET)
    return output    


def TestIfStatementTrue():
    VariableOne = StringNode(None, "Arkel", IdentifierNode(None, "Erkel", 0), 0)
    comparison = ComparisonNode(None, VariableOne, StringNode(None, "Arkel", None, 0), 0)
    code = [AssignNode(None, VariableOne, StringNode(None, "Klaar", None, 0),1), ReturnNode(None, IntegerNode(None, 69, None, 2), 2)]
    ifCodeSequence = CodeSequenceNode(None, [], code, 1)
    ifNode = IfNode(None, comparison, ifCodeSequence, 0)
    codeSequence = CodeSequenceNode(None, [], [ifNode], 0)
    codeSequence.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, Types.INTEGER, [], codeSequence, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.currentFunction.returnValue.value == 69):
         print(bcolors.OKGREEN +"Test If statement true return Succeeded"+ bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test If statement true return Failed"+ bcolors.RESET)
    return output     

def TestIfStatementNotTrue():
    VariableOne = StringNode(None, "Arkel", IdentifierNode(None, "Erkel", 0), 0)
    comparison = ComparisonNode(None, VariableOne, StringNode(None, "Zarkel", None, 0), 0)
    code = [AssignNode(None, VariableOne, StringNode(None, "Klaar", None, 0),1), ReturnNode(None, IntegerNode(None, 420, None, 2), 2)]
    ifCodeSequence = CodeSequenceNode(None, [], code, 1)
    ifNode = IfNode(None, comparison, ifCodeSequence, 0)
    notTrueReturn = ReturnNode(None, IntegerNode(None, 69, None, 3), 3)
    codeSequence = CodeSequenceNode(None, [], [ifNode, notTrueReturn], 0)
    codeSequence.LocalVariables.append(VariableOne)
    mainFunction = FunctionNode(None, Types.INTEGER, [], codeSequence, IdentifierNode([], "Main", 0), 0)
    astRoot = ASTRoot()
    astRoot.globalVariables.append(mainFunction)
    output = interpreterRun(astRoot)   
    if(output.currentFunction.returnValue.value == 69):
         print(bcolors.OKGREEN +"Test If statement not true return Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test If statement not true return Failed"+ bcolors.RESET)
    return output   


def TestReturnParameter():
    returnNode = ReturnNode(None, IntegerNode(None, None, IdentifierNode(None, "Arkel", 0), 0), 0)
    declarationFunction = FunctionDeclareNode(None, CodeSequenceNode(None, [], [returnNode], 0), [IntegerNode(None, None, IdentifierNode(None, "Arkel", 0), 0)], IdentifierNode(None, "Func", 0), Types.INTEGER, 0  )
    assign = AssignNode(None, IntegerNode(None, None, IdentifierNode(None, "Arkel", 0), 0), IntegerNode(None, 69, None, 0), 0)
    functionCall = FunctionCallNode(None, None, [IntegerNode(None, None, IdentifierNode(None, "Arkel", 0), 0)], IdentifierNode(None, "Func", 0), 0)
    declarationMain = FunctionDeclareNode(None, CodeSequenceNode(None, [], [assign, functionCall], 0), [IntegerNode(None, None, IdentifierNode(None, "Jerkelton", 0), 0)], IdentifierNode(None, "Main", 0), Types.INTEGER, 0  )  
    
    astRoot = ASTRoot()
   
    astRoot.codeSequenceNode.Sequence.append(declarationFunction)
    astRoot.codeSequenceNode.Sequence.append(declarationMain)

    output = interpreterRun(astRoot)
    if(output.currentFunction.returnValue.value == 69):
         print(bcolors.OKGREEN +"Test return parameter Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.WARNING + "Test return parameter Failed"+ bcolors.RESET)
    return output   
     
if __name__ == '__main__':
    TestReturnCorrectReturnType()
    TestAssign()
    TestAssignFunction()
    TestAssignOperator()
    TestAssignNonExistingVariable()
    TestReturnCorrectReturnType()
    TestReturnInCorrectReturnType()
    TestReturnInCorrectReturnValue()
    TestIncorrectAssign()
    TestIfStatementTrue()
    TestIfStatementNotTrue()
    TestReturnParameter()

