from astNodes import *
from tokens import *
from lexer import checkError


#           tokens 
#     "@" : "PrimitiveType",
#     "->" : "Assignment",
#     "<-" : "Return",
#     "<<" : "Operator",
#     ">>" : "Operator",
#     "<>" : "Operator",
#     "<" : "ContextOpen",
#     ">" : "ContextClose",
#     "\"" : "StringIndicator",
#     "!" : "EndLine",
#     "+" : "Operator",
#     "-" : "Operator",
#     "&" : "FunctionDeclaration",
#     "[" : "ParameterOpen",
#     "]" : "ParameterClose",
#     "?:" : "KeyWord",
#     "?" : "KeyWord",
#     ":" : "KeyWord",
#     "#" : "PrimitiveType",
#     "," : "Seperator",
#     "\n" : "NewLine"   


# class FunctionNode(PrimitiveNode):
#     def __init__(self, parentNode: ASTNode, returnType: PrimitiveNode,  globalVariables: list, parameters: ParameterNode, codeSequence: list, identifier: IdentifierNode):
#         self.parentNode = parentNode
#         self.returnType = returnType
#         self.codeSequenceNode = CodeSequenceNode(self, parameters + globalVariables, codeSequence)
#         self.identifier = identifier
        

class Error:
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where


def CreateIdentifierASTNode(token: Token, astRoot: ASTRoot):
    node = IdentifierNode(None, token)
    return node



def createErrorMessage(message: str, tokenNR: int, root: ASTRoot):
    tokensCopy = root.tokens.copy()
    tokensCopy.tokens[tokenNR].type = "Error"
    return Error(message, checkError(tokensCopy))
        

def CreateFunctionASTNode(tokens : list, root: ASTRoot):
    if(tokens == None):
        return [], [], Error("Expected a token", "End of File")
    head, *tail = tokens
    identifier, tail, error = CreateIdentifierASTNode(head, root)
    if(error != None):
        return [], [], error
    parameters, tail, error = CreateParametersASTNode(tail, root, ["ParameterOpen"])
    if(error != None):
        return [], [], error
    returnType, tail, error = CreateReturnTypeNode(tail, root)
    if(error != None):
        return [], [], error
    codeSequence, tail, error = CreateCodeSequenceASTNode(tail, root, ["OpeningContext"])
    if(error != None):
        return [], [], error

def CreatePrimitiveASTNode(token: Token, tokens : list, root: ASTRoot):
    if(token.value == "@"):
        node, tokens, error = CreateFunctionASTNode(tokens, root)
    return

def CreateReturnTypeNode(tokens: list, root: ASTRoot):
    head, *tail = tokens
    if(head.type != "ReturnType"):
        head, *tail = tail
        return CreatePrimitiveASTNode(head, tail, root)
    else:
        return [], [], createErrorMessage("Token is not a ReturnType", len(root.tokens) - len(tokens), root)

def ParseParametersDeclaration(tokens: list, root: ASTRoot, nextExpect: list = []):
    if(tokens == None):
        return [], [], Error("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type in nextExpect):
        if(head.type == "ParameterOpen"):
            nextExpect = ["PrimitiveType", "ParameterClose"]
            return ParseParametersDeclaration(tail, root, nextExpect)
        elif(head.type == "ParameterClose"):
            return None, tail, None
        elif(head.type == "PrimitiveType"):
            nextExpect = ["Seperator", "ParameterClose"]
            node, tail, error = CreatePrimitiveASTNode(head, tail, root)
            if(error == None):
                return list(node) + ParseParametersDeclaration(tail, root, nextExpect)
            return [], [], error
        elif(head.type == "Seperator"):
            nextExpect = ["PrimitiveType"]
            return ParseParametersDeclaration(tail, root, nextExpect)
        else:
            return [], [], createErrorMessage("Unknown error",  len(root.tokens) - len(tokens), root)
    else:
        return [], [], createErrorMessage("Excpected a " + head.type,  len(root.tokens) - len(tokens), root)

def CreateParametersASTNode(tokens: list, root: ASTRoot):
    if(tokens == []):
        return [], [], Error("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type != "ParameterOpen"):
        return [], [], createErrorMessage("Syntax Error: Expected a parameter opening", len(root.tokens) - len(tokens), root)
    return ParseParametersDeclaration(tail, root)

def IdentifyASTNode(head: Token, tokens : list, root: ASTRoot) -> ASTNode:
    if(head == []):
        return [], [], Error("Expected a token", "End of File")
    if(head.type == "PrimitiveType"):
        return CreatePrimitiveASTNode(head, tokens, root)
    
#Hier was je maar je was zo moe dus je ging maar lekker slapen!
def CreateCodeSequenceASTNode(tokens: list, root: ASTRoot, nextExpect: list):
    if(tokens == []):
        return [], Error("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type in nextExpect):
        if(head.type == "OpeningContext"):
            sequence = list(IdentifyASTNode())
            newSequence, tail, error = CreateCodeSequenceASTNode
            return sequence + newSequence, tail, error
        if(head.type == "ClosingContext"):
        
    return [], [], []


def parser(tokens : list, root: ASTRoot):
    if(input == []):
        return True
    head, *tail = tokens
    node, tail, error = IdentifyASTNode(head, tail,  root)
    if(error != None):
        print(error.what)
        print(error.where)
        return False
    root.codeSequenceNode.Sequence.append(node)
    return parser(tokens, root)

def parse(tokens : list):
    root = ASTRoot(tokens)
    parser(tokens, root)