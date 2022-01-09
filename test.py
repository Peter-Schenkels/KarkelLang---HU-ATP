from interpreter import *

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
        print("Test Assign operator Succeeded") 
    else:
        print("Test Assign operator Failed")
        
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
    TestAssignOperator()

