from ast import AST, Return
import operator
from pickle import TUPLE
from platform import node
from astNodes import *
from tokens import *
from lexer import bcolors
import copy
from collections.abc import *
from typing import *

class ErrorClass():
    """ Stores where an error happened and what the error was
    """    
    def __init__(self, what: str, where: str):
        self.what = what
        self.where = where

class ParserObject():
    """Stores a state of the parser
    """
    def __init__(self, head: Token, tail: list=None, error: ErrorClass=None, tokens: list=None, rootAST: ASTRoot=None, currentFunctionDeclarationNode: FunctionDeclareNode=None):
        if(type(head) == dict):
            self.__dict__.update(head)
        else:   
            self.head = head
            self.tail = tail.copy()
            self.error = error
            self.tokens = tokens.copy()
            self.rootAST = rootAST
            self.currentFunctionDeclarationNode = currentFunctionDeclarationNode
    

def MoveForward(context: ParserObject) -> ParserObject:
    """Moves the head of the context tokens forward and sets the new head in the head value

    Args:
        context (ParserObject): The context to move the head of

    Returns:
        ParserObject: The new context with the head moved forward
    """    
    if(context.tail != []):
        head, *tail = context.tail
        return SetAttribute(SetAttribute(context, "tail", tail), "head", head)
    return context        

def GetExpectedParameterTokens(token: Token) -> list:
    """Returns the expected tokens for the current token type, acts like a lookup table.

    Args:
        token (Token): _description_

    Returns:
        list: _description_
    """    
    ParameterExpectedTokes = {
        "ParameterOpen" : ["ParameterClose", "PrimitiveType"],
        "PrimitiveType" : ["Identifier"],
        "Identifier" : ["ParameterClose", "Seperator"],
        "Seperator" : ["PrimitiveType"],
        "ParameterClose" : ["ContextOpen"]        
    }
    return ParameterExpectedTokes[token.type]

def AddErrorToContext(TARGET_CONTEXT: ParserObject, ERROR: ErrorClass) -> ParserObject:
    """Adds an error to the context

    Args:
        TARGET_CONTEXT (ParserObject): target context to add the error to
        ERROR (ErrorClass): the error to add

    Returns:
        ParserObject: the new context with the error added
    """    
    return ParserObject(TARGET_CONTEXT.head, TARGET_CONTEXT.tail, ERROR, TARGET_CONTEXT.tokens, TARGET_CONTEXT.rootAST, TARGET_CONTEXT.currentFunctionDeclarationNode)

def ParseParameterTypes(context: ParserObject, expectedParameters: list=["ParameterClose", "PrimitiveType"]) -> ParserObject:
    """Parses a line of parameter tokens until a parameter close token is found

    Args:
        context (ParserObject): the input parser context
        expectedParameters (list, optional): Teh expected types to be found in this fucntion call. Defaults to ["ParameterClose", "PrimitiveType"].

    Returns:
        ParserObject: The new context with the parsed parameters and the new head
    """    
    if(context.head.type in expectedParameters):
        expectedParameters = GetExpectedParameterTokens(context.head)
        if(context.head.type == "PrimitiveType"):

            if(context.head.value == "@"):
                context = MoveForward(context)
                if(context.head.type in expectedParameters):
                    node = StringNode(None, None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
            elif(context.head.value == "#"):
                context = MoveForward(context)
                if(context.head.type in expectedParameters):
                    node = IntegerNode(None, None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)        
            else:
                return AddErrorToContext(context, ErrorClass("Unexpected token in function parameter declaration", context.head.lineNr))
            parameterTypes = context.currentFunctionDeclarationNode.parameterTypes + [node]
            context = SetAttribute(context, "currentFunctionDeclarationNode", SetAttribute(context.currentFunctionDeclarationNode, "parameterTypes", parameterTypes))
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
        
        return AddErrorToContext(context, ErrorClass("Unexpected token in function parameter declaration", context.head.lineNr))
      
def ParseFunctionDeclaration(context: ParserObject) -> ParserObject:
    """Parses a function declaration into a function declare node

    Args:
        context (ParserObject): the input parser context

    Returns:
        ParserObject: The new parsed context with the function declare node
    """      
    if(context.currentFunctionDeclarationNode == None):
        context = SetAttribute(context, "currentFunctionDeclarationNode", FunctionDeclareNode(context.rootAST, CodeSequenceNode(None, [], [], context.head.lineNr), [], None, None, context.head.lineNr))
        context = MoveForward(context)
        if(context.head.type == "Identifier"):
            context = SetAttribute(context, "currentFunctionDeclarationNode", SetAttribute(context.currentFunctionDeclarationNode, "identifier", IdentifierNode(context.rootAST, context.head.value, context.head.lineNr)))
            context = MoveForward(context)
            if(context.head.type == "ParameterOpen"):
                context = MoveForward(context)
                context = ParseParameterTypes(context)
                if(context.head.type == "ReturnTypeIndicator"):
                    context = MoveForward(context)
                    if(context.head.type == "PrimitiveType"):
                        context = SetAttribute(context, "currentFunctionDeclarationNode", SetAttribute(context.currentFunctionDeclarationNode, "returnType",  Types.INTEGER if context.head.value == "#" else Types.STRING))
                        context = MoveForward(context)
                        if(context.head.type == "ContextOpen"):
                            context = TokensToAST(MoveForward(context))
                            newSequence = context.rootAST.codeSequenceNode.Sequence + [context.currentFunctionDeclarationNode]
                            context = SetAttribute(context, "rootAST", SetAttribute(context.rootAST, "codeSequenceNode", SetAttribute(context.rootAST.codeSequenceNode, "Sequence", newSequence)))                            
                            context.currentFunctionDeclarationNode = None
                            return TokensToAST(context)
                        else:
                            return AddErrorToContext(context, ErrorClass("Function declaration error: Expected a context open token, got %s" % context.head.type, context.head.lineNr))
                    else:     
                        return AddErrorToContext(context, ErrorClass("Function declaration error: Expected a return type, got %s" % context.head.type, context.head.lineNr))
                else:
                    return AddErrorToContext(context, ErrorClass("Function Declaration error: Expected Assignment token, got %s" % context.head.type, context.head.lineNr))
            else:
                return AddErrorToContext(context, ErrorClass("Function Declaration error: Expected a Parameter Open token, got %s" % context.head.type, context.head.lineNr))
        else:
            return AddErrorToContext(context, ErrorClass("Function Declaration error: Expected a function identifier, got %s" % context.head.type, context.head.lineNr))
    else:
        return AddErrorToContext(context, ErrorClass("Function Declaration error: Can't declare function inside a function", context.head.lineNr))  


def ParseOperator(context: ParserObject, right: PrimitiveNode) -> OperatorNode: 
    """Returns an operator node based on the token value

    Args:
        context (ParserObject): The current parser context
        right (PrimitiveNode): The right hand side of the operator
        
    Returns:
        OperatorNode: Output variable based on the token value
    """
    if(context.head.value == "+"):
        out = AdditionNode(None, right, None, context.head.lineNr)
    elif(context.head.value == "-"):
        out = SubtractionNode(None, right, None, context.head.lineNr)
    elif(context.head.value == "<<"):
        out = ComparisonNodeSmallerThan(None, right, None, context.head.lineNr)
    elif(context.head.value == ">>"):
        out = ComparisonNodeGreaterThan(None, right, None, context.head.lineNr)
    elif(context.head.value == "><"):
        out = ComparisonNode(None, right, None, context.head.lineNr)
    elif(context.head.value == "<>"):
        out = ComparisonNodeNotEuqal(None, right, None, context.head.lineNr)
    elif(context.head.value == "*"):
        out = MultiplicationNode(None, right, None, context.head.lineNr)
    elif(context.head.value == "\\"):
        out = DivisionNode(None, right, None, context.head.lineNr)
    else:
        return None
    return out

class ParseAssignObject():
    def __init__(self, context, node, error):
        self.context = context
        self.node = node
        self.error = error

def ParseAssignArrayAcces(node: ASTNode, context: ParserObject, declaration: bool) -> ParseAssignObject:
    """ Parses an assignment for an array at a certain index.

    Args:
        node (ASTNode): _description_
        context (ParserObject): _description_
        declaration (bool): _description_

    Returns:
        ParseAssignObject: _description_
    """    
    context = MoveForward(context)
    if(context.head.type == "NumericValue"):
        arrayIndex = IntegerNode(None, context.head.value, None, context.head.lineNr)
    elif(context.head.type == "Identifier"):
        arrayIndex = PrimitiveNode(None, IdentifierNode(None, context.head.value, context.head.lineNr), context.head.lineNr)
    else:
        context = AddErrorToContext(context, ErrorClass("Unexpected token expected an Array index, got %s" % context.head.value, context.head.lineNr))
        return ParseAssignObject(context, None, context.error)
    if(declaration):
        node = ArrayNode(node, arrayIndex, node.identifier, context.head.lineNr)
        context = MoveForward(context)
        if(context.head.type != "ArrayClose"):
            context = AddErrorToContext(context, ErrorClass("Unexpected token expected an array close token, got %s" % context.head.value, context.head.lineNr))
            return ParseAssignObject(context, None, context.error)
        return ParseAssignObject(CheckEndlineAppendNode(node, MoveForward(context)), None, None)
    else:
        node = ArrayAccesNode(arrayIndex, node.identifier, context.head.lineNr) 
        context = MoveForward(context)
        if(context.head.type != "ArrayClose"):
            context = AddErrorToContext(context, ErrorClass("Unexpected token expected an array close token, got %s" % context.head.value, context.head.lineNr)) 
            return ParseAssignObject(context, None, context.error)
        return ParseAssignObject(context, node, None)

def ParseLeftRightTypes(context: ParserObject) -> tuple[PrimitiveNode, PrimitiveNode, ParserObject, bool]:
    """Parses the left and right types based on the assignment value type

    Args:
        context (ParserObject): The context object

    Returns:
        tuple[PrimitiveNode, PrimitiveNode, ParserObject, bool]: The left and right types and the context object and a boolean indicating if the assignment is a declaration
    """    
    
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
        declaration = False
    else:
        return None, None, AddErrorToContext(context, ErrorClass("Unexpected token during parsing, got %s" % context.head.value, context.head.lineNr)), None
    return left, right, context, declaration


def ParseAssignValue(node: ASTNode, context: ParserObject) -> Tuple[ASTNode, ParserObject]:
    """Parses the assignment value of a variable

    Args:
        node (ASTNode): The node to assign the value to
        context (ParserObject): The context to parse from

    Returns:
        Tuple[ASTNode, ParserObject]: The assignment value and the context
    """    
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
            node = SetAttribute(node, "identifier", IdentifierNode(None, context.head.value, context.head.lineNr) )  
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
        context = AddErrorToContext(context, ErrorClass("Unexpected token, got %s" % context.head.value, context.head.lineNr))
        return ParseAssignObject(context, None, context.error), context     
    return ParseAssignObject(context, node, None), context       



def ParseAssignOperator(NODE: OperatorNode, INPUT_CONTEXT: ParserObject) ->ParseAssignObject:
    """Parses an operator node and turns it into an assignment node

    Args:
        NODE (OperatorNode): The node to assign to
        INPUT_CONTEXT (ParserObject): The context to parse from

    Returns:
        ParseAssignObject: The parsed node and the context
    """    
    NODE = ParseOperator(INPUT_CONTEXT, NODE)
    OUTPUT, _ = ParseAssignValue(None, INPUT_CONTEXT)  
    if(OUTPUT.error != None):
        return OUTPUT.context
    return ParseAssignObject(MoveForward(OUTPUT.context), type(NODE)(None, NODE.left, OUTPUT.node, NODE.lineNr), None)

def ParseAssignString(INPUT_CONTEXT: ParserObject) -> ParseAssignObject:
    """Parses a string assignment

    Args:
        INPUT_CONTEXT (ParserObject): The input context

    Returns:
        ParseAssignObject: The new output context
    """    
    CONTEXT = MoveForward(INPUT_CONTEXT)
    if(CONTEXT.head.type == "Identifier"):
        NODE = StringNode(None, CONTEXT.head.value, None, CONTEXT.head.lineNr)
        CONTEXT = MoveForward(CONTEXT)
        if(CONTEXT.head.type != "StringIndicator"):
            return AddErrorToContext(CONTEXT, ErrorClass("Unexpected token expected string indicator, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))
    else:
        return AddErrorToContext(CONTEXT, ErrorClass("Unexpected token, expected Identifier,  got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))
    return ParseAssignObject(CONTEXT, NODE, None)


def SetAttribute(input: object, attributeName: str, attributeValue: object) -> object:
    """ Instantiates a new object of the input object with the same fields but altered attribute value in a functional way but very dirty

    Args:
        input (object): Input object to copy
        attributeName (str): Name of the attribute to change
        attributeValue (object): New value of the attribute

    Returns:
        object: A new constructed object with the same fields as the input object but altered attribute value
    """    
    attributes = input.__dict__
    if (attributeName in attributes):
        attributeIndex = list(attributes.keys()).index(attributeName)
        first_part = dict(dict(list(attributes.items())[:attributeIndex]), **{attributeName : attributeValue})
        new_attributes = dict(first_part, **dict(list(attributes.items())[attributeIndex+1:]))
        return type(input)(new_attributes)
    else:
        return None

def ParseAssignment(context: ParserObject) -> ParserObject:
    """Parses an assignment statement and returns the resulting context

    Args:
        context (ParserObject): The context to parse the assignment statement from

    Returns:
        ParserObject: The new resulting context after parsing the assignment statement
    """    
    left, right, context, declaration = ParseLeftRightTypes(context)
    if(left is None or right is None):
        return context
    if(context.head.type == "Identifier"):
        left = SetAttribute(left, "identifier", IdentifierNode(None, context.head.value, context.head.lineNr))
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
                return output
        else:
            context.error = ErrorClass("Unexpected token expected a Assignment token, got %s" % context.head.value, context.head.lineNr)
            return context
    else:
        context.error = ErrorClass("Unexpected token during parsing expected a Identifier, got %s" % context.head.value, context.head.lineNr)
        return context
    context = MoveForward(context)
    if(context.head.type == "Operator"):
        output = ParseAssignOperator(right, context)
        if(output.error == None):
            right, context  = output.node, output.context
        else:
            return output.context
    assignNode = AssignNode(None, left, right, context.head.lineNr, declaration)   
    return CheckEndlineAppendNode(assignNode, context)

def SwapFunctionDeclNodeFromContext(CONTEXT: ParserObject, NODE: FunctionDeclareNode) -> ParserObject:
    return ParserObject(CONTEXT.head, CONTEXT.tail, CONTEXT.error, CONTEXT.tokens, CONTEXT.rootAST, NODE)
    
#todo SOMETHING WITH TYPE
def ParseKeyword(INPUT_CONTEXT: ParserObject) -> ParserObject:
    """Parses a keyword into a comparison node and appends it to an code sequence node

    Args:
        INPUT_CONTEXT (ParserObject): The context to parse the keyword from

    Returns:
        ParserObject: The new context after parsing the keyword
    """    
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
            case "><": comparison = ComparisonNodeNotEuqal(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr) 
            case "<<>": comparison = ComparisonNodeSmallerThanEqual(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr) 
            case "<>>": comparison = ComparisonNodeGreaterThanEqual(None, LEFT, RIGHT, PARSED_CONTEXT.head.lineNr)
            case _ : return AddErrorToContext(PARSED_CONTEXT, ErrorClass("Unexpected operator", PARSED_CONTEXT.head.lineNr))
        
        OLD_DECL = CONTEXT.currentFunctionDeclarationNode
        CONTEXT = TokensToAST(MoveForward(SwapFunctionDeclNodeFromContext(CONTEXT, FunctionDeclareNode(None, CodeSequenceNode(None, [], [], 0), [], None, None, 0))))
            
        if(type == "?"):
            node = IfNode(None, comparison, CONTEXT.currentFunctionDeclarationNode.code, CONTEXT.head.lineNr)
        elif(type == "O"):
            node = WhileNode(None, comparison, CONTEXT.currentFunctionDeclarationNode.code, CONTEXT.head.lineNr)
        else:
            return AddErrorToContext(CONTEXT, ErrorClass("Unexpected keyword", CONTEXT.head.lineNr))
        return AppendSequenceFromContext(SwapFunctionDeclNodeFromContext(CONTEXT, OLD_DECL), node)
    return

def CheckEndlineAppendNode(NODE: ASTNode, CONTEXT: ParserObject) -> ParserObject:
    """ Checks if the next token is a endline token, if so appends the node to the current context, if not returns the context with error

    Args:
        NODE (ASTNode): The node to append to the context
        CONTEXT (ParserObject): The context to append the node to

    Returns:
        ParserObject: The new context with the node appended or with an error
    """    
    if(CONTEXT.head.type == "EndLine"):
        return MoveForward(AppendSequenceFromContext(CONTEXT, NODE))
    else:
        return AddErrorToContext(CONTEXT, ErrorClass("Expected endline, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr))

def ParseReturnNumericValue(CONTEXT: ParserObject) -> ParserObject:
    """Parse a return statement with a numeric value

    Args:
        CONTEXT (ParserObject): The context to parse the return statement from

    Returns:
        ParserObject: The context after the return statement
    """    
    RETURN_NODE = ReturnNode(None, IntegerNode(None, CONTEXT.head.value, None, CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return CheckEndlineAppendNode(RETURN_NODE, MoveForward(CONTEXT))

def ParseReturnIdentifier(CONTEXT: ParserObject) -> ParserObject:
    """Parses a return statement with an identifier

    Args:
        CONTEXT (ParserObject): The context to parse from

    Returns:
        ParserObject: A new context with the parsed node
    """    
    RETURN_NODE = ReturnNode(None, PrimitiveNode(None, IdentifierNode(None, CONTEXT.head.value, CONTEXT.head.lineNr), CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return CheckEndlineAppendNode(RETURN_NODE, MoveForward(MoveForward(CONTEXT)))

def appendToParameters(FUNCTION_CALL: FunctionCallNode, parameter: PrimitiveNode) -> FunctionCallNode:
    """dirty functional way to append a parameter to a function call

    Args:
        FUNCTION_CALL (FunctionCallNode): The function call node to append to
        parameter (PrimitiveNode): The parameter to append

    Returns:
        FunctionCallNode: The function call node with the parameter appended
    """    
    NEW_PARAMETERS = FUNCTION_CALL.parameters + [parameter]
    return FunctionCallNode(None, FUNCTION_CALL.value, NEW_PARAMETERS, FUNCTION_CALL.identifier, FUNCTION_CALL.lineNr)

def AppendSequenceFromContext(CONTEXT: ParserObject, NODE: ASTNode) -> Tuple[ParserObject, ASTNode]:   
    """Dirty function to append a node to the current sequence by constructing a new context

    Args:
        CONTEXT (ParserObject): The current context
        NODE (ASTNode): The node to append to the sequence

    Returns:
        Tuple[ParserObject, ASTNode]: a tuple containing the new context and the appended node
    """       
    FUNC_NODE = CONTEXT.currentFunctionDeclarationNode
    SEQUENCE = FUNC_NODE.code.Sequence + [NODE]
    CODE = CodeSequenceNode(None, FUNC_NODE.code.globalVariables, SEQUENCE, FUNC_NODE.lineNr)
    FUNCTION_DECLARE_NODE = FunctionDeclareNode(None, CODE, FUNC_NODE.parameterTypes, FUNC_NODE.identifier, FUNC_NODE.returnType, FUNC_NODE.lineNr)
    NEW_CONTEXT = ParserObject(CONTEXT.head, CONTEXT.tail, CONTEXT.error, CONTEXT.tokens, CONTEXT.rootAST, FUNCTION_DECLARE_NODE)

    return NEW_CONTEXT

def ParseParameters(CONTEXT: ParserObject, FUNCTION_CALL: FunctionCallNode, EXPECTED_TOKENS: list=["ParameterOpen"]) -> ParserObject:
    """Parses the parameters of a function call

    Args:
        CONTEXT (ParserObject): the context of the parser 
        FUNCTION_CALL (FunctionCallNode): the function call node to append the parameters to
        EXPECTED_TOKENS (list, optional): Tokens to expect from the parser context. Defaults to ["ParameterOpen"].

    Returns:
        ParserObject: a new context with the new function call node
    """        
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
                    CONTEXT = MoveForward(NEW_CONTEXT)
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
    """ Parses a function call 

    Args:
        CONTEXT (ParserObject): the current context of the parser 

    Returns:
        ParserObject: a new context with the parsed function call 
    """    
    FUNCTION_CALL_NODE = FunctionCallNode(None, None, [], IdentifierNode(None, CONTEXT.head.value, CONTEXT.head.lineNr), CONTEXT.head.lineNr)
    return ParseParameters(MoveForward(CONTEXT), FUNCTION_CALL_NODE)

class FunctionCallObject():
    """FunctionCallObject is used to store the function call node and the context
    """    
    def __init__(self, context: ParserObject, functionCall: FunctionCallNode):
        self.context = context
        self.functionCall = functionCall


def PopSequenceFromContext(CONTEXT: ParserObject) -> Tuple[ParserObject, ASTNode]:
    """Dirty function that pops a sequence from the context by constructing a new parser object with one item less in the sequence

    Args:
        CONTEXT (ParserObject): The parser object to pop the sequence from

    Returns:
        Tuple[ParserObject, ASTNode]: The new parser object and the popped sequence
    """    
    NODE = CONTEXT.currentFunctionDeclarationNode
    *SEQUENCE, POPPED = NODE.code.Sequence
    CODE = CodeSequenceNode(None, NODE.code.globalVariables, SEQUENCE, NODE.lineNr)
    FUNCTION_DECLARE_NODE = FunctionDeclareNode(None, CODE, NODE.parameterTypes, NODE.identifier, NODE.returnType, NODE.lineNr)
    NEW_CONTEXT = ParserObject(CONTEXT.head, CONTEXT.tail, CONTEXT.error, CONTEXT.tokens, CONTEXT.rootAST, FUNCTION_DECLARE_NODE)
    return NEW_CONTEXT, POPPED
    
def ParseFunctionCallAssignment(CONTEXT: ParserObject) ->FunctionCallObject:
    """Parses a function call 

    Args:
        CONTEXT (ParserObject): input parser context

    Returns:
        FunctionCallObject: function call object
    """    
    NEW_CONTEXT = ParseFunctionCall(CONTEXT)
    if(NEW_CONTEXT.error == None):
        UPDATED_CONTEXT, POPPED = PopSequenceFromContext(NEW_CONTEXT)
        return FunctionCallObject(UPDATED_CONTEXT, POPPED)
    else:
        return FunctionCallObject(NEW_CONTEXT, None)


def CheckEndline(CONTEXT: ParserObject) -> ParserObject:
    """Checks if the head of the parser context is an endline token, if so, moves the context forward

    Args:
        CONTEXT (ParserObject): The parser context to check

    Returns:
        ParserObject: The updated parser context
    """    
    if(CONTEXT.head.type == "EndLine"):
        return MoveForward(CONTEXT)
    else:
        ERROR = ErrorClass("Expected endline, got %s" % CONTEXT.head.value, CONTEXT.head.lineNr)
        return AddErrorToContext(CONTEXT, ERROR)

def ParseIdentifier(CONTEXT: ParserObject) -> ParserObject:
    """Parses an identifier token

    Args:
        CONTEXT (ParserObject): The current context of the parser 

    Returns:
        ParserObject: The output context of the parser after parsing the identifier
    """    
    if(CONTEXT.tail[0].type == "Return"):
        return ParseReturnIdentifier(CONTEXT)
    elif(CONTEXT.tail[0].type == "ParameterOpen"):
        return CheckEndline(MoveForward(ParseFunctionCall(CONTEXT)))
    else:
        return ParseAssignment(CONTEXT)

def TokensToAST(CONTEXT: ParserObject) -> ParserObject: 
    """Parses the tokens and returns an AST

    Args:
        CONTEXT (ParserObject): Parser Context containing the state of the parser

    Returns:
        ParserObject: Parser Context containing the output state of the parser
    """    
    
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

def ParseComment(PREVIOUS_CONTEXT: ParserObject, current_comments: str="") -> ParserObject:
    """Parses a comment and returns the new context

    Args:
        PREVIOUS_CONTEXT (ParserObject): _description_

    Returns:
        ParserObject: the output context of the parse comment function
    """
    CURRENT_CONTEXT = MoveForward(PREVIOUS_CONTEXT)
    if(CURRENT_CONTEXT.tail != []):
        if(CURRENT_CONTEXT.head.type == "Comment"):          
            return MoveForward(AppendSequenceFromContext(CURRENT_CONTEXT, CommentNode(None, CURRENT_CONTEXT.head.lineNr, current_comments)))
        else:
            return ParseComment(CURRENT_CONTEXT, current_comments + CURRENT_CONTEXT.head.value + " ")
    return CURRENT_CONTEXT
    
def Parse(TOKENS : list[Token])->ASTRoot:
    """parses a list of tokens into an AST

    Args:
        TOKENS (list[Token]): List of token objects

    Returns:
        ASTRoot: the parsed AST root 
    """    
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