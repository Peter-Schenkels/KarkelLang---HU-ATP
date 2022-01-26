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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ErrorClass():
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where
        
class ParserObject():
    def __init__(self, head: Token, tail: list, error: ErrorClass, tokens: list, rootAST: ASTRoot, currentFunctionDeclarationNode: FunctionDeclareNode):
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
        context.currentFunctionDeclarationNode = FunctionDeclareNode(context.rootAST, CodeSequenceNode(None, [], [], context.head.lineNr), [], None, None, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type == "Identifier"):
            context.currentFunctionDeclarationNode.identifier = IdentifierNode(context.rootAST, context.head.value, context.head.lineNr)
            context = MoveForward(context)
            if(context.head.type == "ParameterOpen"):
                context = MoveForward(context)
                context = ParseParameterTypes(context)
                if(context.head.type == "ReturnTypeIndicator"):
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

def ParseAssignment(context: ParserObject):
    declaration = False
    if(context.head.value == "#"):
        left = IntegerNode(None, None, None, context.head.lineNr)
        right = IntegerNode(None, 0, None, context.head.lineNr)
        context = MoveForward(context)
        declaration = True
    elif(context.head.value == "@"):
        left = StringNode(None, None, None, context.head.lineNr)
        right = StringNode(None, "", None, context.head.lineNr)
        context = MoveForward(context)
        declaration = True
    elif(context.head.type == "Identifier"):
        left = PrimitiveNode(None, None, context.head.lineNr)
        right = PrimitiveNode(None, IdentifierNode(None, None, context.head.lineNr), context.head.lineNr)
    else:
        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
        return context
    if(context.head.type == "Identifier"):
        left.identifier = IdentifierNode(None, context.head.value, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type =="Assignment"):
            context = MoveForward(context)
            if(context.head.type == "StringIndicator"):
                right = StringNode(None, "", None, context.head.lineNr)
                context = MoveForward(context)
                if(context.head.type == "Identifier"):
                    right.value = context.head.value
                    context = MoveForward(context)
                    if(context.head.type != "StringIndicator"):
                        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
                        return context
                else:
                    context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
                    return context
            elif(context.head.type == "NumericValue"):
                right = IntegerNode(None, int(context.head.value), None, context.head.lineNr)
            elif(context.head.type == "Identifier"):
                right = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
            else:
                context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
                return context
        else:
            context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
            return context
    context = MoveForward(context)
    if(context.head.type == "Operator"):
        if(context.head.value == "+"):
            right = AdditionNode(None, right, None, context.head.lineNr)
        elif(context.head.value == "-"):
            right = SubtractionNode(None, right, None, context.head.lineNr)
        elif(context.head.value == "<<"):
            right = ComparisonNodeSmallerThan(None, right, None, context.head.lineNr)
        elif(context.head.value == ">>"):
            right = ComparisonNodeGreaterThan(None, right, None, context.head.lineNr)
        elif(context.head.value == "><"):
            right = ComparisonNode(None, right, None, context.head.lineNr)
        elif(context.head.value == "<>"):
            right = ComparisonNodeNotEuqal(None, right, None, context.head.lineNr)
        elif(context.head.value == "*"):
            right = MultiplicationNode(None, right, None, context.head.lineNr)
        elif(context.head.value == "\\"):
            right = DivisionNode(None, right, None, context.head.lineNr)
        else:
            context.error = ErrorClass("Unexpected operator, got %s" % context.head.value, context.head.lineNr)
            return context
        rightOperatorValue = None
        context = MoveForward(context)
        if(context.head.type == "StringIndicator"):
            context = MoveForward(context)
            if(context.head.type == "Identifier"):
                rightOperatorValue = StringNode(None, context.head.value, None, context.head.lineNr)
                context = MoveForward(context)
                if(context.head.type != "StringIndicator"):
                    context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
                    return context
                else:
                    context = MoveForward(context)
            else:
                context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
                return context
        elif(context.head.type == "NumericValue"):
           rightOperatorValue = IntegerNode(None, context.head.value, None, context.head.lineNr)
           context = MoveForward(context)
        elif(context.head.type == "Identifier"):
            rightOperatorValue = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
            context = MoveForward(context)
        else:
            context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
            return context
        right.right = rightOperatorValue
    assignNode = AssignNode(None, left, right, context.head.lineNr, declaration)   
    return CheckEndlineAppendNode(assignNode, context)

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

def CheckEndlineAppendNode(node: ASTNode, context: ParserObject):
    if(context.head.type == "EndLine"):
        context.currentFunctionDeclarationNode.code.Sequence.append(node)
        context = MoveForward(context)
    else:
        context.error = ErrorClass("Expected endline, got %s" % context.head.value, context.head.lineNr)
    return context

def ParseReturnNumericValue(context: ParserObject):
    returnNode = ReturnNode(None, IntegerNode(None, context.head.value, None, context.head.lineNr), context.head.lineNr)
    context = MoveForward(context)
    return CheckEndlineAppendNode(returnNode, context)


def ParseReturnIdentifier(context: ParserObject):
    returnNode = ReturnNode(None, PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr), context.head.lineNr)
    context = MoveForward(MoveForward(context))
    return CheckEndlineAppendNode(returnNode, context)

def ParseIdentifier(context: ParserObject):
    if(context.tail[0].type == "Return"):
        return ParseReturnIdentifier(context)
    else:
        return ParseAssignment(context)
        
def TokensToAST(input: ParserObject) -> ParserObject: 
    
    ParserFunctions = {
    "FunctionDeclaration": ParseFunctionDeclaration,
    "PrimitiveType" : ParseAssignment,
    "Identifier" : ParseIdentifier,
    "KeyWord"    : ParseKeyword,
    "NumericValue" : ParseReturnNumericValue
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
    root = context.rootAST
    if(context.error != None):
        print(bcolors.FAIL + context.error.what)
        print(bcolors.FAIL + "On LineNr: " + str(context.error.where) + bcolors.RESET)
        return False
    return root