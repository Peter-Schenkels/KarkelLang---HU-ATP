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

class ErrorClass():
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where
        
class ParserObject():
    def __init__(self, head: Token, tail: list, error: ErrorClass, tokens: list, rootAST: ASTRoot, currentFunctionDeclarationNode: FunctionNode):
        self.head = head
        self.tail = tail.copy()
        self.error = error
        self.tokens = tokens.copy()
        self.rootAST = rootAST
        self.currentFunctionDeclarationNode = currentFunctionDeclarationNode
        
    def getCurrentTokenIndex(self):
        return len(self.tokens) - len(self.tail)
             
def MoveForward(context: ParserObject):
    context.head, *context.tail = context.tail
    return context        

def GetExpectedParameterTokens(token: Token):
    ParameterExpectedTokes = {
        "ParameterOpen" : ["ParameterClose", "PrimitiveType"],
        "PrimitiveType" : ["Identifier"],
        "Identifier" : ["ParameterClose", "Seperator"],
        "Seperator" : ["PrimitiveType"],
        "ParameterClose" : ["ContextOpen"]        
    }
    return ParameterExpectedTokes[token.type]

def ParseParameterTypes(context: ParserObject, expectedParameters: list=["ParameterClose", "PrimitiveType"]) -> ParserObject:
    if(context.head.type in expectedParameters):
        expectedParameters = GetExpectedParameterTokens(context.head)
        if(context.head.type == "PrimitiveType"):
            if(context.head.value == "@"):
                context = MoveForward(context)
                if(context.head.type in expectedParameters):
                    context.currentFunctionDeclarationNode.parameterTypes.append(StringNode(None, None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr))
            elif(context.head.value == "#"):
                context = MoveForward(context)
                if(context.head.type in expectedParameters):
                    context.currentFunctionDeclarationNode.parameterTypes.append(IntegerNode(None, None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr))        
            else:
                context.error = ErrorClass("Unexpected token in function parameter declaration", context.head.lineNr)
                return context
            expectedParameters = GetExpectedParameterTokens(context.head)
            context = MoveForward(context)
            return ParseParameterTypes(context, expectedParameters)
        elif(context.head.type == "Seperator"):
            expectedParameters = GetExpectedParameterTokens(context.head)
            context = MoveForward(context)
            return ParseParameterTypes(context, expectedParameters)
        elif(context.head.type == "ParameterClose"):
            context = MoveForward(context)
            return context
    else:
        context.error = ErrorClass("Unexpected token in function parameter declaration", context.head.lineNr)
        return context
        
def ParseFunctionDeclaration(context: ParserObject) -> ParserObject:  
    if(context.currentFunctionDeclarationNode == None):
        context.currentFunctionDeclarationNode = FunctionDeclareNode(context.rootAST, [], [], None, None, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type == "Identifier"):
            context.currentFunctionDeclarationNode.identifier = IdentifierNode(context.rootAST, context.head.value, context.head.lineNr)
            context = MoveForward(context)
            if(context.head.type == "ParameterOpen"):
                context = MoveForward(context)
                context = ParseParameterTypes(context)
                if(context.head.type == "Assignment"):
                    context = MoveForward(context)
                    if(context.head.type == "PrimitiveType"):
                        context.currentFunctionDeclarationNode.returnType = Types.INTEGER if context.head.value == "#" else Types.STRING
                        context = MoveForward(context)
                        if(context.head.type == "ContextOpen"):
                            context = TokensToAST(MoveForward(context))
                            context.rootAST.codeSequenceNode.Sequence.append(context.currentFunctionDeclarationNode)
                            context.currentFunctionDeclarationNode = None
                            return TokensToAST(context)
                        else:
                            context.error = ErrorClass("Function declaration error: Expected a context open token, got %s" % context.head.type, context.head.lineNr)
                            return context
                    else:
                        context.error = ErrorClass("Function declaration error: Expected a return type, got %s" % context.head.type, context.head.lineNr)
                        return context
                else:
                    context.error = ErrorClass("Function Declaration error: Expected Assignment token, got %s" % context.head.type, context.head.lineNr)
                    return context
            else:
                context.error = ErrorClass("Function Declaration error: Expected a Parameter Open token, got %s" % context.head.type, context.head.lineNr)
                return context
        else:
            context.error = ErrorClass("Function Declaration error: Expected a function identifier, got %s" % context.head.type, context.head.lineNr)
            return context
    else:
        context.error = ErrorClass("Function Declaration error: Can't declare function inside a function", context.head.lineNr)
        return context         

def ParseNewAssignment(context: ParserObject):
    if(context.head.value == "#"):
        left = IntegerNode()
        right = IntegerNode(None, 0, None, context.head.line)
    elif(context.head.value == "@"):
        left = StringNode()
        right = StringNode(None, "", None, context.head.line)
    else:
        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
        return context
    context = MoveForward(context)
    if(context.head.type == "Identifier"):
        left.identifier = IdentifierNode(None, context.head.value, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type =="Assignment"):
            return #DO STUFF
        elif(context.head.type == "Endline"):
            assignNode = AssignNode(None, left, right, context.head.lineNr)
            context.currentFunctionDeclarationNode.codeSequenceNode.Sequence.append(assignNode)
            context = MoveForward(context)
            return context
        else:
            context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
            return context
    else:
        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
        return context
    
def ParseAssignment(context: ParserObject):   
    return 

def ParseKeyword(context: ParserObject):
    ExpectedTokens = ["Identifier", "PrimitiveType"]
    context = MoveForward(context)
    if(context.head.type == "Identifier"):
        left = IdentifierNode(None, context.head.value, context.head.lineNr)
    elif(context.head.type == "PrimitiveType"):
        if(context.head.value == "#"):
            left = IntegerNode(None, context.head.value, None, context.head.lineNr)
        if(context.head.value == "@"):
            left = StringNode(None, context.head.value, None, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type == "Operator"):
            if(context.head.value == "<<"):
                comparison = ComparisonNodeSmallerThan(None, left, None, context.head.lineNr)    
                
    return

def TokensToAST(input: ParserObject) -> ParserObject: 
    
    ParserFunctions = {
    "FunctionDeclaration": ParseFunctionDeclaration,
    "PrimitiveType" : ParseNewAssignment,
    "Identifier" : ParseAssignment,
    "KeyWord"    : ParseKeyword
    }
    
    if(input.error != None):
        return input
    if(input.tail != []):
        if(input.head.type in ParserFunctions):
            input = TokensToAST(ParserFunctions[input.head.type](input))
        else:
            input.error = ErrorClass("Unexpected Token", input.getCurrentTokenIndex())
            return input
    return input;

def parse(tokens : list)->ASTRoot:
    root = ASTRoot()
    head, *tail = tokens
    context = ParserObject(head, tail, None, tokens, root, None)
    context = TokensToAST(context)
    if(context.error != None):
        print(context.error.what)
        print("On LineNr: " + str(context.error.where))
        return False