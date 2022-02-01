from astNodes import *
from tokens import *
from lexer import bcolors
import copy

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
    def __init__(self, head: Token, tail: list, error: ErrorClass, tokens: list, rootAST: ASTRoot, currentFunctionDeclarationNode: FunctionDeclareNode):
        self.head = head
        self.tail = tail.copy()
        self.error = error
        self.tokens = tokens.copy()
        self.rootAST = rootAST
        self.currentFunctionDeclarationNode = currentFunctionDeclarationNode
        
    def getCurrentTokenIndex(self) -> int:
        return len(self.tokens) - len(self.tail)
             
def MoveForward(context: ParserObject) -> ParserObject:
    if(context.tail != []):
        context.head, *context.tail = context.tail
    return context        

def GetExpectedParameterTokens(token: Token) -> list:
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

#Returns operator node based on token
def ParseOperator(context: ParserObject, right: PrimitiveNode) -> OperatorNode: 
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
        return None
    return right

class ParseAssignObject():
    def __init__(self, context, node, error):
        self.context = context
        self.node = node
        self.error = error

def ParseAssignArrayAcces(node: ASTNode, context: ParserObject, declaration: bool) -> ParseAssignObject:
    context = MoveForward(context)
    if(context.head.type == "NumericValue"):
        arrayIndex = IntegerNode(None, context.head.value, None, context.head.lineNr)
    elif(context.head.type == "Identifier"):
        arrayIndex = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
    else:
        context.error = ErrorClass("Unexpected token expected an Array index, got %s" % context.head.value, context.head.lineNr)
        return ParseAssignObject(context, None, context.error)
    if(declaration):
        if(type(node) == IntegerNode):
            node.value = 0
        elif(type(node) == StringNode):
            node.value = ""
        node = ArrayNode(node, arrayIndex, node.identifier, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type != "ArrayClose"):
            context.error = ErrorClass("Unexpected token expected an array close token, got %s" % context.head.value, context.head.lineNr)
            return ParseAssignObject(context, None, context.error)
        return ParseAssignObject(CheckEndlineAppendNode(node, MoveForward(context)), None, None)
    else:
        node = ArrayAccesNode(arrayIndex, node.identifier, context.head.lineNr) 
        context = MoveForward(context)
        if(context.head.type != "ArrayClose"):
            context.error = ErrorClass("Unexpected token expected an array close token, got %s" % context.head.value, context.head.lineNr)
            return ParseAssignObject(context, None, context.error)
        return ParseAssignObject(context, node, None)

def ParseLeftRightTypes(context) -> ASTNode:
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
        context.error = ErrorClass("Unexpected token during parsing, got %s" % context.head.value, context.head.lineNr)
        return None, None, context, None
    return left, right, context, declaration

def ParseAssignValue(node: ASTNode, context: ParserObject) -> ASTNode:
    context = MoveForward(context)
    if(context.head.type == "StringIndicator"):
        output = ParseAssignString(context)
        if(output.error == None):
            node, context = output.node, output.context
        else:
            return output
    elif(context.head.type == "NumericValue"):
        node = IntegerNode(None, int(context.head.value), None, context.head.lineNr)
    elif(context.head.type == "Identifier"):
        if(node != None):
            node.identifier = IdentifierNode(None, context.head.value, context.head.lineNr)     
        if(context.tail[0].type == "ParameterOpen"):
            output = ParseFunctionCallAssignment(context)
            context, node = output.context, output.functionCall
        elif(context.tail[0].type == "ArrayOpen"):
            output = ParseAssignArrayAcces(node, MoveForward(context), False)
            if(output.error == None):
                node, context = output.node,  output.context
            else:
                return output.context        
        else:
            node = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
    else:
        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
        return ParseAssignObject(context, None, context.error)     
    return ParseAssignObject(context, node, None)      


def ParseAssignOperator(node: ASTNode, left: ASTNode, context: ParserObject, declaration: bool) ->ParseAssignObject:
    node = ParseOperator(context, node)

    output = ParseAssignValue(None, context)  
    if(output.error == None):
        node.right, context = output.node, output.context
    else:
        return output.context
    context = MoveForward(context)
    return ParseAssignObject(context, node, None)


def ParseAssignString(context: ParserObject) -> ParseAssignObject:
    context = MoveForward(context)
    if(context.head.type == "Identifier"):
        node = node = StringNode(None, context.head.value, None, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type != "StringIndicator"):
            context.error = ErrorClass("Unexpected token 4, got %s" % context.head.value, context.head.lineNr)
            return ParseAssignObject(context, None, context.error)
    else:
        context.error = ErrorClass("Unexpected token 5,  got %s" % context.head.value, context.head.lineNr)
        return ParseAssignObject(context, None, context.error)
    return ParseAssignObject(context, node, None)

def ParseAssignment(context: ParserObject) -> ParserObject:
    left, right, context, declaration = ParseLeftRightTypes(context)
    if(left is None or right is None):
        return context
    if(context.head.type == "Identifier"):
        left.identifier = IdentifierNode(None, context.head.value, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type == "ArrayOpen"):
            output = ParseAssignArrayAcces(left, context, declaration)
            if(output.error == None):
                if(output.node is None):
                    return output.context
                left = output.node
                context = MoveForward(output.context)
                
            else:
                return output.context
        if(context.head.type =="Assignment"):
            output = ParseAssignValue(right, context)  
            if(output.error == None):
                right, context = output.node, output.context
            else:
                return output.context
        else:
            context.error = ErrorClass("Unexpected token expected a Assignment token, got %s" % context.head.value, context.head.lineNr)
            return context
    else:
        context.error = ErrorClass("Unexpected token during parsing expected a Identifier, got %s" % context.head.value, context.head.lineNr)
        return context
    context = MoveForward(context)
    if(context.head.type == "Operator"):
        output = ParseAssignOperator(right, left, context, declaration)
        if(output.error == None):
            right, context  = output.node, output.context
        else:
            return output.context
    assignNode = AssignNode(None, left, right, context.head.lineNr, declaration)   
    return CheckEndlineAppendNode(assignNode, context)

def ParseKeyword(context: ParserObject) -> ParserObject:
    type = context.head.value
    output = ParseAssignValue(None, context)  
    if(output.error == None):
        left, context = output.node, output.context
    else:
        return output.context
    context = MoveForward(context)
    if(context.head.type == "Operator"):
        if(context.head.value == "<<"):
            comparison = ComparisonNodeSmallerThan(None, left, None, context.head.lineNr)          
        elif(context.head.value == ">>"):
            comparison = ComparisonNodeGreaterThan(None, left, None, context.head.lineNr)          
        elif(context.head.value == "<>"):
            comparison = ComparisonNode(None, left, None, context.head.lineNr) 
        elif(context.head.value == "<<>"):
            comparison = ComparisonNodeSmallerThanEqual(None, left, None, context.head.lineNr) 
        elif(context.head.value == "<>>"):
            comparison = ComparisonNodeGreaterThanEqual((None, left, None, context.head.lineNr))
        else:
            context.error = ErrorClass("Unexpected operator", context.head.lineNr)
            return context    
        output = ParseAssignValue(None, context)  
        if(output.error == None):
            comparison.right, context = output.node, output.context
        else:
            return output.context
        context = MoveForward(context)
        
        codeSegment = FunctionDeclareNode(None, CodeSequenceNode(None, [], [], 0), [], None, None, 0)
        oldFunction = context.currentFunctionDeclarationNode
        context.currentFunctionDeclarationNode = codeSegment
        context = TokensToAST(MoveForward(context))
            
        if(type == "?"):
            node = IfNode(None, comparison, context.currentFunctionDeclarationNode.code, context.head.lineNr)
        elif(type == "O"):
            node = WhileNode(None, comparison, context.currentFunctionDeclarationNode.code, context.head.lineNr)
        else:
            context.error = ErrorClass("Unexpected keyword", context.head.lineNr)
            return context
        context.currentFunctionDeclarationNode = oldFunction
        context.currentFunctionDeclarationNode.code.Sequence.append(node)
        return context
    return

def CheckEndlineAppendNode(node: ASTNode, context: ParserObject) -> ParserObject:
    if(context.head.type == "EndLine"):
        context.currentFunctionDeclarationNode.code.Sequence.append(node)
        context = MoveForward(context)
    else:
        context.error = ErrorClass("Expected endline, got %s" % context.head.value, context.head.lineNr)
    return context

def ParseReturnNumericValue(context: ParserObject) -> ParserObject:
    returnNode = ReturnNode(None, IntegerNode(None, context.head.value, None, context.head.lineNr), context.head.lineNr)
    context = MoveForward(context)
    return CheckEndlineAppendNode(returnNode, context)


def ParseReturnIdentifier(context: ParserObject) -> ParserObject:
    returnNode = ReturnNode(None, PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr), context.head.lineNr)
    context = MoveForward(MoveForward(context))
    return CheckEndlineAppendNode(returnNode, context)

def ParseParameters(context: ParserObject, functionCall: FunctionCallNode, expectedTokens: list=["ParameterOpen"]) -> ParserObject:
    if(context.head.type in expectedTokens):
        if(context.head.type == "ParameterOpen"):
            return ParseParameters(MoveForward(context), functionCall, ["Identifier", "NumericValue", "StringIndicator", "ParameterClose"])
        elif(context.head.type == "Seperator"):
            return ParseParameters(MoveForward(context), functionCall, ["Identifier", "NumericValue", "StringIndicator"])
        elif(context.head.type == "Identifier"):
            functionCall.parameters.append(PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr))
            return ParseParameters(MoveForward(context), functionCall, ["ParameterClose", "Seperator"])
        elif(context.head.type == "NumericValue"):
            functionCall.parameters.append(IntegerNode(None, context.head.value, None, context.head.lineNr))
            return ParseParameters(MoveForward(context), functionCall, ["ParameterClose", "Seperator"])
        elif(context.head.type == "StringIndicator"):
            parameter = StringNode(None, "", None, context.head.lineNr)
            context = MoveForward(context)
            if(context.head.type == "Identifier"):
                parameter.value = context.head.value
                context = MoveForward(context)
                if(context.head.type != "StringIndicator"):
                    context.error = ErrorClass("Unexpected token 8, got %s" % context.head.value, context.head.lineNr)
                    return context
            else:
                context.error = ErrorClass("Unexpected token 9, got %s" % context.head.value, context.head.lineNr)
                return context
            functionCall.parameters.append(parameter)
            return ParseParameters(MoveForward(context), functionCall, ["ParameterClose", "Seperator", "Return"])
        elif(context.head.type == "ParameterClose"):
            context.currentFunctionDeclarationNode.code.Sequence.append(functionCall)
            return context
    else:
        context.error = ErrorClass("Unexpected token while parsing parameters, got %s" % context.head.value, context.head.lineNr)
        return context
           
def ParseFunctionCall(context: ParserObject):
    functionCallNode = FunctionCallNode(None, None, [], None, context.head.lineNr)
    functionCallNode.identifier = IdentifierNode(None, context.head.value, context.head.lineNr)
    return ParseParameters(MoveForward(context), functionCallNode)

class FunctionCallObject():
    def __init__(self, context: ParserObject, functionCall: FunctionCallNode):
        self.context = context
        self.functionCall = functionCall

def ParseFunctionCallAssignment(context: ParserObject) ->FunctionCallObject:
    context = ParseFunctionCall(context)
    if(context.error == None):
        head = context.currentFunctionDeclarationNode.code.Sequence.pop()
        return FunctionCallObject(context, head)
    else:
        return FunctionCallObject(context, None)

def CheckEndline(context: ParserObject) -> ParserObject:
    if(context.head.type == "EndLine"):
        context = MoveForward(context)
    else:
        context.error = ErrorClass("Expected endline, got %s" % context.head.value, context.head.lineNr)
    return context

def ParseIdentifier(context: ParserObject):
    if(context.tail[0].type == "Return"):
        return ParseReturnIdentifier(context)
    elif(context.tail[0].type == "ParameterOpen"):
        return CheckEndline(MoveForward(ParseFunctionCall(context)))
    else:
        return ParseAssignment(context)
    
def TokensToAST(input: ParserObject) -> ParserObject: 
    
    ParserFunctions = {
    "FunctionDeclaration": ParseFunctionDeclaration,
    "PrimitiveType" : ParseAssignment,
    "Identifier" : ParseIdentifier,
    "KeyWord"    : ParseKeyword,
    "NumericValue" : ParseReturnNumericValue,
    "Comment" :  ParseComment
    }
    
    if(input.error != None):
        return input
    if(input.tail != [] or input.head != "ContextClose"):
        if(input.head.type in ParserFunctions):
            input = TokensToAST(ParserFunctions[input.head.type](input))
        elif(input.head.type == "ContextClose"):
            return MoveForward(input)
        else:
            input.error = ErrorClass("Unexpected Token 10 got %s" % input.head.value, input.head.lineNr)
            return input
    return input

def ParseComment(input: ParserObject):
    input = MoveForward(input)
    if(input.tail != []):
        if(input.head.type == "Comment"):
            return MoveForward(input)
        else:
            return ParseComment(input)
    return input
    
        
def parse(tokens : list)->ASTRoot:
    if(tokens  != []):
        root = ASTRoot()
        head, *tail = tokens
        context = ParserObject(head, tail, None, tokens, root, None)
        context = TokensToAST(context)
        root = context.rootAST
        if(context.error != None):
            print(bcolors.FAIL + context.error.what + ", On LineNr: " + str(context.error.where) + bcolors.RESET)
            return False
        return root
    return None