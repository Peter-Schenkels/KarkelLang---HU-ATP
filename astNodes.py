from typing import Dict
from tokens import *
from abc import ABC
import jsonpickle


class ASTNode(ABC):
    def __init__(self, parentNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            self.parentNode = parentNode
            self.lineNr = lineNr
            self.globalVariables = []
    
    def __str__(self,):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)   
     
class ParameterIdentifierNode(ASTNode):
    def __init__(self, parentNode: ASTNode, parameters: list, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.parameters = parameters        
           
class IdentifierNode(ASTNode):
    def __init__(self, parentNode: ASTNode, value: str, lineNr: int):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__(parentNode, lineNr)
            self.value = value
        

        
class FunctionCallNode(IdentifierNode):
    def __init__(self, parentNode: ASTNode, name: str, parameters: ParameterIdentifierNode, lineNr: int):
        super().__init__(parentNode, name, lineNr)
        self.parameters = parameters

class FunctionCallNode(IdentifierNode):
    def __init__(self, parentNode: ASTNode, name: str, parameters: ParameterIdentifierNode, lineNr: int):
        super().__init__(parentNode, name, lineNr)
        self.parameters = parameters
        
        
class PrimitiveNode(ASTNode):
    def __init__(self, parentNode: ASTNode, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__(parentNode, lineNr)
            self.identifier = identifier
            self.type = Types.PRIMITIVE
 
class OperatorNode(ASTNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.left = left
        self.right = right
        self.output = None
        
class AssignNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode,  lineNr: int, declaration: bool=False):
        super().__init__(parentNode, left, right, lineNr)
        self.declaration = declaration

class ParameterDeclarationNode(ASTNode):
    def __init__(self, parentNode: ASTNode, parameters: list, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.parameters = parameters
        
class CodeSequenceNode(ASTNode):
    def __init__(self, parentNode: ASTNode, globalVariables: list=None, codeSequence: list=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__(parentNode, lineNr)
            self.parentNode = parentNode
            self.Sequence = codeSequence
            self.LocalVariables = []
class CommentNode(ASTNode):
    
    def __init__(self, parentNode=None, lineNr: int = None, comment: str = None):
        self.value = comment
        super().__init__(parentNode, lineNr)

class FunctionNode(ASTNode):
    
    def __init__(self, parentNode: ASTNode|dict, returnType: Types=None, parameterTypes: ParameterDeclarationNode=None, codeSequence: CodeSequenceNode=None, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
            super().__init__( parentNode, lineNr)
        else:
            self.returnType = returnType
            self.parameterTypes = parameterTypes
            self.parameters = []
            self.codeSequenceNode = codeSequence
            self.identifier = identifier
            self.returnValue = None

class IntegerNode(PrimitiveNode):
    def __init__(self, parentNode: ASTNode|dict=None, value: int=None, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, identifier, lineNr)
            self.value = value
            if(value == None):
                self.value = 1
        self.type = Types.INTEGER
class StringNode(PrimitiveNode):   
    def __init__(self, parentNode : ASTNode|Dict, value: str=None, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:           
            super().__init__( parentNode, identifier, lineNr)
            self.value = value
            if(value == None):
                self.value = ""
            self.type = Types.STRING
class FunctionCallNode(PrimitiveNode):
    def __init__(self, parentNode :ASTNode|dict, value: FunctionNode=None, parameters: list=None, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)    
        else:
            super().__init__( parentNode, identifier, lineNr)
            self.value = value
            self.parameters = parameters



class FunctionDeclareNode(PrimitiveNode):
    def __init__(self, parentNode :ASTNode|dict, code: CodeSequenceNode=None, parameterTypes: ParameterDeclarationNode=None, identifier: IdentifierNode=None, returnType: type=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, identifier, lineNr)
            self.code = code
            self.parameterTypes = parameterTypes
            self.returnType = returnType
        
    def SetCode(self, code):
        return FunctionDeclareNode(self.parentNode, code, self.parameterTypes, self.identifier, self.returnType, self.lineNr)
    
    def SetParameterTypes(self, parameterTypes):
        return FunctionDeclareNode(self.parentNode, self.code, parameterTypes, self.identifier, self.returnType, self.lineNr)
    
    def SetReturnType(self, returnType):
        return FunctionDeclareNode(self.parentNode, self.code, self.parameterTypes, self.identifier, returnType, self.lineNr)
    
    def SetIdentifier(self, identifier):
        return FunctionDeclareNode(self.parentNode, self.code, self.parameterTypes, identifier, self.returnType, self.lineNr)
    
    def SetLineNr(self, lineNr):
        return FunctionDeclareNode(self.parentNode, self.code, self.parameterTypes, self.identifier, self.returnType, lineNr)

class KeywordNode(ASTNode):
    def __init__(self, parentNode: ASTNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.codeSequenceNode = codeSequenceNode

class ArrayNode(ASTNode):
    def __init__(self, _type: PrimitiveNode|dict, size: PrimitiveNode=None, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(_type)==dict):
            self.__dict__ = (_type)
        else:
            self.type = _type
            self.size = size
            self.identifier = identifier
            self.memory = []
            self.lineNr = lineNr
            self.index = None
            self.value = None

class ArrayAccesNode(ASTNode):
    def __init__(self, index: PrimitiveNode, identifier: IdentifierNode=None, lineNr: int=None):
        if(type(index)==dict):
            self.__dict__ = (index)
        else:
            self.index = index
            self.identifier = identifier
            self.lineNr = lineNr
  
class ReturnNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, value: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, None, lineNr)
        self.parentNode = parentNode
        self.value = value

class AdditionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
       
class SubtractionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)

class MultiplicationNode(OperatorNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)

class DivisionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)

class ComparisonNode(OperatorNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
class ComparisonNodeGreaterThan(ComparisonNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeSmallerThan(ComparisonNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeGreaterThanEqual(ComparisonNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeSmallerThanEqual(ComparisonNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeNotEuqal(ComparisonNode):
    def __init__(self, parentNode: ASTNode|dict, left: PrimitiveNode=None, right: PrimitiveNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = (parentNode)
        else:
            super().__init__( parentNode, left, right, lineNr)
        
class IfNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__( parentNode, codeSequenceNode, lineNr)
        self.comparison = comparison
class WhileNode(KeywordNode):
    def __init__(self, parentNode: ASTNode|dict, comparison: ComparisonNode=None, codeSequenceNode: CodeSequenceNode=None, lineNr: int=None):
        if(type(parentNode) == dict):
            self.__dict__ = parentNode
        else:
            super().__init__( parentNode, codeSequenceNode, lineNr)
            self.comparison = comparison

class ASTRoot():
    def __init__(self, args=None):
        if(type(args) == dict):
            self.__dict__ = (args)
        else:
            self.globalVariables = []
            self.globalVariables.append(FunctionNode(None, None, [IntegerNode(None, None, None, None)], [], IdentifierNode(None, "IntOut", 0), 0))
            self.globalVariables.append(FunctionNode(None, None, [StringNode(None, None, None, None)], [], IdentifierNode(None, "StringOut", 0), 0))
            self.globalVariables.append(FunctionNode(None, None, [IntegerNode(None, None, None, None)], [], IdentifierNode(None, "IntOutLine", 0), 0))
            self.globalVariables.append(FunctionNode(None, None, [StringNode(None, None, None, None)], [], IdentifierNode(None, "StringOutLine", 0), 0))
            self.codeSequenceNode = CodeSequenceNode(self, self.globalVariables, [], 0)
            self.tokens = tokens.copy()
    
    def __str__(self,):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)   