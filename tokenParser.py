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
        

class ErrorClass():
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where


def CreateIdentifierASTNode(token: Token, tokens: Token, root: ASTRoot):
    node = IdentifierNode(None, token)
    if(tokens[0].type == "ParameterOpen"):
        head, *tail  = tokens
        node, tokens, error = ParseParameters(tail, root, ["NumericValue", "Identifier", "StringIndicator", "ParameterClose"])
        return node, tokens, error
    return node, tokens, []


def CreateStringASTNode(tokens: list, root: ASTRoot):
    if(tokens == None):
        return [], [], ErrorClass("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type == "Identifier" and tail[0].type == "StringIndicator"):
        value = StringNode(None, head.value, None)
        head, *tail = tail
        return value, tail, None 
    else:
        return [], [], ErrorClass("Expected a string", len(root.tokens)- len(tokens))
        


def CreateAssignOperatorASTNode(tokens: list, left: PrimitiveNode, root: ASTNode):
    if(tokens == None):
        return [], [], ErrorClass("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type in ["PrimitiveType", "NumericValue", "Identifier", "StringIndicator"]):
        if(head.type == "PrimitiveType"):
            node, tokens, error = CreatePrimitiveASTNode(head, tokens, root)
        if(head.type == "NumericValue"):
            node, tokens, error = CreateIntegerASTNode(head, tokens, root)
        if(head.type == "Identifier"):
            node, tokens, error = CreateIdentifierASTNode(head, tokens, root)
        if(head.type == "StringIndicator"):
            node, tokens, error = CreateStringASTNode(tokens, root)
        if(error != None):
            return [], [], error
        output = AssignNode(None, left, node)
        return output, tokens, []
    

def CreateIntegerASTNode(token: Token, tokens: list, root: ASTNode):
    if(tokens == None):
        return [], [], ErrorClass("Expected a token", "End of File")
    if(token.type == "NumericValue"):
        return IntegerNode(None, token, None), tokens, None
    if(token.type == "Identifier"):
        head, *tail = tokens
        identifer, tokens, error = CreateIdentifierASTNode(head, tail, root)
        if(error != None):
            return [], [], error
        head, *tail = tokens
        if(head.type == "EndLine"):
            return IntegerNode(None, None, identifer), tokens, error
        if(head.type == "operator" and head.value == "<>"):
            node, tokens, error = CreateAssignOperatorASTNode(tokens, token, root)
            if(error != None):
                return [], [], error
            
    

def ParseParameters(tokens: list, root: ASTRoot, nextExpect: list = []):
    if(tokens == None):
        return [], [], ErrorClass("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type in nextExpect):
        if(head.type == "NumericValue"):
            node, tokens, error = CreateIntegerASTNode(head, tail, root)


def createErrorMessage(message: str, tokenNR: int, root: ASTRoot):
    tokensCopy = root.tokens.copy()
    tokensCopy.tokens[tokenNR].type = "Error"
    return ErrorClass(message, checkError(tokensCopy))
        

def CreateFunctionASTNode(tokens : list, root: ASTRoot):
    if(tokens == None):
        return [], [], ErrorClass("Expected a token", "End of File")
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
        return [], [], ErrorClass("Expected a token", "End of File")
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
                parameters, tokens, error = ParseParametersDeclaration(tail, root, nextExpect)
                parameters += list(node)
                return parameters, tokens, error
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
        return [], [], ErrorClass("Expected a token", "End of File")
    head, *tail = tokens
    if(head.type != "ParameterOpen"):
        return [], [], createErrorMessage("Syntax Error: Expected a parameter opening", len(root.tokens) - len(tokens), root)
    parameters, tokens, error = ParseParametersDeclaration(tail, root)
    node = ParameterDeclarationNode(None, parameters, root)
    return node, tokens, error

def IdentifyASTNode(head: Token, tokens : list, root: ASTRoot) -> ASTNode:
    if(head == []):
        return [], [], ErrorClass("Expected a token", "End of File")
    if(head.type == "PrimitiveType"):
        return CreatePrimitiveASTNode(head, tokens, root)
    
#Hier was je maar je was zo moe dus je ging maar lekker slapen!
def CreateCodeSequenceASTNode(tokens: list, root: ASTRoot, nextExpect: list):
    if(tokens == []):
        return [], ErrorClass("Expected a token", "End of File")
    head, *tail = tokens
    sequence = list(IdentifyASTNode())
    if(head.type in nextExpect):
        if(head.type == "OpeningContext"):
            newSequence, tail, error = CreateCodeSequenceASTNode(tail, root, ["PrimitiveType", "Identifier", "ClosingContext"])
            if(error != None):
                return [], [], error
            return sequence + newSequence, tail, error
        if(head.type == "ClosingContext"):
            return sequence, tail, None
        if(head.type == "PrimitiveType"):
            node, tail, error = CreatePrimitiveASTNode(head, tokens, root)
        if(head.type == "Identifier"):
            node, tail, error = CreateIdentifierASTNode(head, tokens, root)
        
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