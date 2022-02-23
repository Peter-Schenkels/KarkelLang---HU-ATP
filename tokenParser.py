from ast import AST
from pickle import TUPLE
from astNodes import *
from tokens import *
from lexer import bcolors
import copy
from collections.abc import *
from typing import *


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
    #TODO: make const
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where


 
class ParserObject():
    #TODO: make const
    def __init__(self, head: Token, tail: list, error: ErrorClass, tokens: list, rootAST: ASTRoot, currentFunctionDeclarationNode: FunctionDeclareNode):
        self.head = head
        self.tail = tail.copy()
        self.error = error
        self.tokens = tokens.copy()
        self.rootAST = rootAST
        self.currentFunctionDeclarationNode = currentFunctionDeclarationNode
        
    #TODO: make const
    def getCurrentTokenIndex(self) -> int:
        return len(self.tokens) - len(self.tail)



#TODO: make const
def MoveForward(context: ParserObject) -> ParserObject:
    if(context.tail != []):
        context.head, *context.tail = context.tail
    return context        

#TODO: make const
def GetExpectedParameterTokens(token: Token) -> list:
    ParameterExpectedTokes = {
        "ParameterOpen" : ["ParameterClose", "PrimitiveType"],
        "PrimitiveType" : ["Identifier"],
        "Identifier" : ["ParameterClose", "Seperator"],
        "Seperator" : ["PrimitiveType"],
        "ParameterClose" : ["ContextOpen"]        
    }
    return ParameterExpectedTokes[token.type]

def AddErrorToContext(TARGET_CONTEXT: ParserObject, ERROR: ErrorClass):
    return ParserObject(TARGET_CONTEXT.head, TARGET_CONTEXT.tail, ERROR, TARGET_CONTEXT.tokens, TARGET_CONTEXT.rootAST, TARGET_CONTEXT.currentFunctionDeclarationNode)

#TODO: make const
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
      
#TODO: make const
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
#TODO: make const
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
    #TODO: make const
    def __init__(self, context, node, error):
        self.context = context
        self.node = node
        self.error = error

#TODO: make const
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

#TODO: make const
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

#TODO: make const
def ParseAssignValue(node: ASTNode, context: ParserObject) -> Tuple[ASTNode, ParserObject]:
    context = MoveForward(context)
    if(context.head.type == "StringIndicator"):
        output = ParseAssignString(context)
        if(output.error == None):
            node, context = output.node, output.context
        else:
            return output, context
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
                return None, output.context        
        else:
            node = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
    else:
        context.error = ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr)
        return ParseAssignObject(context, None, context.error), context     
    return ParseAssignObject(context, node, None), context       


#TODO: make const
def ParseAssignOperator(node: ASTNode, left: ASTNode, context: ParserObject, declaration: bool) ->ParseAssignObject:
    node = ParseOperator(context, node)

    output, context = ParseAssignValue(None, context)  
    if(output.error == None):
        node.right, context = output.node, output.context
    else:
        return output.context
    context = MoveForward(context)
    return ParseAssignObject(context, node, None)


#TODO: make const
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

#TODO: make const
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
            output, context = ParseAssignValue(right, context)  
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

#todo make fucntional
def ParseKeyword(INPUT_CONTEXT: ParserObject) -> ParserObject:
    type = INPUT_CONTEXT.head.value
    ASSING_VALUE_PARSE_OUTPUT, _ = ParseAssignValue(None, INPUT_CONTEXT)  
    if(ASSING_VALUE_PARSE_OUTPUT.error == None):
        LEFT, CONTEXT = ASSING_VALUE_PARSE_OUTPUT.node, MoveForward(ASSING_VALUE_PARSE_OUTPUT.context)
    else:
        return ASSING_VALUE_PARSE_OUTPUT.context

    if(CONTEXT.head.type == "Operator"):             
        OPERATOR_VALUE = CONTEXT.head.value
        output, PARSED_CONTEXT = ParseAssignValue(None, CONTEXT) 
        if(output.error == None):
                RIGHT, CONTEXT = output.node, MoveForward(output.context)
        else:
            return output.CONTEXT
        
        match OPERATOR_VALUE:
            case "<<": comparison = ComparisonNodeSmallerThan(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr)          
            case ">>": comparison = ComparisonNodeGreaterThan(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr)          
            case "<>": comparison = ComparisonNode(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr) 
            case "<<>": comparison = ComparisonNodeSmallerThanEqual(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr) 
            case "<>>": comparison = ComparisonNodeGreaterThanEqual(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr)
            case _ : return AddErrorToContext(PARSED_CONTEXT, ErrorClass("Unexpected operator", PARSED_CONTEXT.head.lineNr))
        
        codeSegment = FunctionDeclareNode(None, CodeSequenceNode(None, [], [], 0), [], None, None, 0)
        oldFunction = CONTEXT.currentFunctionDeclarationNode
        CONTEXT.currentFunctionDeclarationNode = codeSegment
        CONTEXT = TokensToAST(MoveForward(CONTEXT))
            
        if(type == "?"):
            node = IfNode(None, comparison, CONTEXT.currentFunctionDeclarationNode.code, CONTEXT.head.lineNr)
        elif(type == "O"):
            node = WhileNode(None, comparison, CONTEXT.currentFunctionDeclarationNode.code, CONTEXT.head.lineNr)
        else:
            CONTEXT.error = ErrorClass("Unexpected keyword", CONTEXT.head.lineNr)
            return CONTEXT
        CONTEXT.currentFunctionDeclarationNode = oldFunction
        CONTEXT.currentFunctionDeclarationNode.code.Sequence.append(node)
        return CONTEXT
    return

def CheckEndlineAppendNode(NODE: ASTNode, CONTEXT: ParserObject) -> ParserObject:
    if(CONTEXT.head.type == "EndLine"):
        return MoveForward(AppendSequenceFromContext(CONTEXT, NODE))
    else:
        return AddErrorToContext(CONTEXT, ErrorClass("Expected endline, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))

def ParseReturnNumericValue(CONTEXT: ParserObject) -> ParserObject:
    RETURN_NODE = ReturnNode(None, IntegerNode(None, CONTEXT.head.value, None, CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return CheckEndlineAppendNode(RETURN_NODE, MoveForward(CONTEXT))

def ParseReturnIdentifier(CONTEXT: ParserObject) -> ParserObject:
    RETURN_NODE = ReturnNode(None, PrimitiveNode(None, IdentifierNode(None, CONTEXT.head.value, CONTEXT.head.lineNr), CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return CheckEndlineAppendNode(RETURN_NODE, MoveForward(MoveForward(CONTEXT)))

def appendToParameters(FUNCTION_CALL: FunctionCallNode, parameter: PrimitiveNode) -> FunctionCallNode:
    NEW_PARAMETERS = FUNCTION_CALL.parameters + [parameter]
    return FunctionCallNode(None, FUNCTION_CALL.value, NEW_PARAMETERS, FUNCTION_CALL.identifier, FUNCTION_CALL.lineNr)

def AppendSequenceFromContext(CONTEXT: ParserObject, NODE: ASTNode) -> Tuple[ParserObject, ASTNode]:
    # CONTEXT.currentFunctionDeclarationNode.code.Sequence.append(FUNCTION_CALL)
        
    FUNC_NODE = CONTEXT.currentFunctionDeclarationNode
    SEQUENCE = FUNC_NODE.code.Sequence + [NODE]
    CODE = CodeSequenceNode(None, FUNC_NODE.code.globalVariables, SEQUENCE, FUNC_NODE.lineNr)
    FUNCTION_DECLARE_NODE = FunctionDeclareNode(None, CODE, FUNC_NODE.parameterTypes, FUNC_NODE.identifier, FUNC_NODE.returnType, FUNC_NODE.lineNr)
    NEW_CONTEXT = ParserObject(CONTEXT.head, CONTEXT.tail, CONTEXT.error, CONTEXT.tokens, CONTEXT.rootAST, FUNCTION_DECLARE_NODE)
    return NEW_CONTEXT

def ParseParameters(CONTEXT: ParserObject, FUNCTION_CALL: FunctionCallNode, EXPECTED_TOKENS: list=["ParameterOpen"]) -> ParserObject:    
    if(CONTEXT.head.type in EXPECTED_TOKENS):
        match CONTEXT.head.type:
            case "ParameterOpen":
                return ParseParameters(MoveForward(CONTEXT), FUNCTION_CALL, ["Identifier", "NumericValue", "StringIndicator", "ParameterClose"])
            case "Seperator":
                return ParseParameters(MoveForward(CONTEXT), FUNCTION_CALL, ["Identifier", "NumericValue", "StringIndicator"])
            case "Identifier":
                NEW_FUNCTION_CALL = appendToParameters(FUNCTION_CALL, PrimitiveNode(None, IdentifierNode(None, CONTEXT.head.value, CONTEXT.head.lineNr), CONTEXT.head.lineNr))
                return ParseParameters(MoveForward(CONTEXT), NEW_FUNCTION_CALL, ["ParameterClose", "Seperator"])
            case "NumericValue":
                NEW_FUNCTION_CALL = appendToParameters(FUNCTION_CALL, IntegerNode(None, CONTEXT.head.value, None, CONTEXT.head.lineNr))
                return ParseParameters(MoveForward(CONTEXT), NEW_FUNCTION_CALL, ["ParameterClose", "Seperator"])
            case "StringIndicator":
                NEW_CONTEXT = MoveForward(CONTEXT)
                if(NEW_CONTEXT.head.type == "Identifier"):
                    PARAMETER = StringNode(None, NEW_CONTEXT.head.value, None, CONTEXT.head.lineNr)
                    CONTEXT = MoveForward(CONTEXT)
                    if(CONTEXT.head.type != "StringIndicator"):
                        return AddErrorToContext(CONTEXT, ErrorClass("Unexpected token 8, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))
                else:
                    return AddErrorToContext(CONTEXT, ErrorClass("Unexpected token 9, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))
                NEW_FUNCTION_CALL = appendToParameters(FUNCTION_CALL, PARAMETER)
                return ParseParameters(MoveForward(CONTEXT), NEW_FUNCTION_CALL, ["ParameterClose", "Seperator", "Return"])
            case "ParameterClose":       
                return AppendSequenceFromContext(CONTEXT, FUNCTION_CALL)
    else:
        return AddErrorToContext(CONTEXT, ErrorClass("Unexpected token while parsing parameters, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))
           
def ParseFunctionCall(CONTEXT: ParserObject) -> ParserObject:
    FUNCTION_CALL_NODE = FunctionCallNode(None, None, [], IdentifierNode(None, CONTEXT.head.value, CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return ParseParameters(MoveForward(CONTEXT), FUNCTION_CALL_NODE)

class FunctionCallObject():
    def __init__(self, context: ParserObject, functionCall: FunctionCallNode):
        self.context = context
        self.functionCall = functionCall


def PopSequenceFromContext(CONTEXT: ParserObject) -> Tuple[ParserObject, ASTNode]:
    NODE = CONTEXT.currentFunctionDeclarationNode
    *SEQUENCE, POPPED = NODE.code.Sequence
    CODE = CodeSequenceNode(None, NODE.code.globalVariables, SEQUENCE, NODE.lineNr)
    FUNCTION_DECLARE_NODE = FunctionDeclareNode(None, CODE, NODE.parameterTypes, NODE.identifier, NODE.returnType, NODE.lineNr)
    NEW_CONTEXT = ParserObject(CONTEXT.head, CONTEXT.tail, CONTEXT.error, CONTEXT.tokens, CONTEXT.rootAST, FUNCTION_DECLARE_NODE)
    return NEW_CONTEXT, POPPED
    
def ParseFunctionCallAssignment(CONTEXT: ParserObject) ->FunctionCallObject:
    NEW_CONTEXT = ParseFunctionCall(CONTEXT)
    if(NEW_CONTEXT.error == None):
        UPDATED_CONTEXT, POPPED = PopSequenceFromContext(NEW_CONTEXT)
        return FunctionCallObject(UPDATED_CONTEXT, POPPED)
    else:
        return FunctionCallObject(NEW_CONTEXT, None)


def CheckEndline(CONTEXT: ParserObject) -> ParserObject:
    if(CONTEXT.head.type == "EndLine"):
        return MoveForward(CONTEXT)
    else:
        ERROR = ErrorClass("Expected endline, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr)
        return AddErrorToContext(CONTEXT, ERROR)

def ParseIdentifier(CONTEXT: ParserObject):
    if(CONTEXT.tail[0].type == "Return"):
        return ParseReturnIdentifier(CONTEXT)
    elif(CONTEXT.tail[0].type == "ParameterOpen"):
        return CheckEndline(MoveForward(ParseFunctionCall(CONTEXT)))
    else:
        return ParseAssignment(CONTEXT)


def TokensToAST(CONTEXT: ParserObject) -> ParserObject: 
    
    PARSER_FUNCTIONS = {
    "FunctionDeclaration": ParseFunctionDeclaration,
    "PrimitiveType" : ParseAssignment,
    "Identifier" : ParseIdentifier,
    "KeyWord"    : ParseKeyword,
    "NumericValue" : ParseReturnNumericValue,
    "Comment" :  ParseComment
    }
    
    if(CONTEXT.error != None):
        return CONTEXT
    if(CONTEXT.tail != [] or CONTEXT.head != "ContextClose"):
        if(CONTEXT.head.type in PARSER_FUNCTIONS):
            return TokensToAST(PARSER_FUNCTIONS[CONTEXT.head.type](CONTEXT))
        elif(CONTEXT.head.type == "ContextClose"):
            return MoveForward(CONTEXT)
        else:
            ERROR = ErrorClass("Unexpected Token 10 got %s" % CONTEXT.head.value, CONTEXT.head.lineNr)
            return AddErrorToContext(CONTEXT, ERROR)
    return CONTEXT

def ParseComment(PREVIOUS_CONTEXT: ParserObject):
    CURRENT_CONTEXT = MoveForward(PREVIOUS_CONTEXT)
    if(CURRENT_CONTEXT.tail != []):
        if(CURRENT_CONTEXT.head.type == "Comment"):
            return MoveForward(CURRENT_CONTEXT)
        else:
            return ParseComment(CURRENT_CONTEXT)
    return CURRENT_CONTEXT
    
def Parse(TOKENS : list)->ASTRoot:
    if(TOKENS != []):
        HEAD, *TAIL = TOKENS
        INPUT_CONTEXT = ParserObject(HEAD, TAIL, None, TOKENS, ASTRoot(), None)
        OUTPUT_CONTEXT = TokensToAST(INPUT_CONTEXT)
        ROOT = OUTPUT_CONTEXT.rootAST
        if(OUTPUT_CONTEXT.error != None):
            print(bcolors.FAIL + OUTPUT_CONTEXT.error.what + ", On LineNr: " + str(OUTPUT_CONTEXT.error.where) + bcolors.RESET)
            return False
        return ROOT
    return None