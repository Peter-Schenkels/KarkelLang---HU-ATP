from tokens import *
from abc import ABC
import jsonpickle


class ASTNode(ABC):
    def __init__(self, parentNode, lineNr: int):
        self.lineNr = lineNr
        self.parentNode = parentNode
        self.globalVariables = []
        self.code = []
    
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
    def __init__(self, parentNode: ASTNode, identifier: IdentifierNode, lineNr: int):
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
    def __init__(self, parentNode: ASTNode, globalVariables: list, codeSequence: list, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.Sequence = codeSequence
        self.LocalVariables = []

class FunctionNode(ASTNode):
    
    def __init__(self, parentNode: ASTNode, returnType: Types, parameterTypes: ParameterDeclarationNode, codeSequence: CodeSequenceNode, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, lineNr)
        self.returnType = returnType
        self.parameterTypes = parameterTypes
        self.parameters = []
        self.codeSequenceNode = codeSequence
        self.identifier = identifier
        self.returnValue = None

class IntegerNode(PrimitiveNode):
    def __init__(self, parentNode: ASTNode, value: int, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.value = value
        if(value == None):
            self.value = 1
        self.type = Types.INTEGER
class StringNode(PrimitiveNode):   
    def __init__(self, parentNode : ASTNode, value: str, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.value = value
        if(value == None):
            self.value = ""
        self.type = Types.STRING
class FunctionCallNode(PrimitiveNode):
    def __init__(self, parentNode :ASTNode, value: FunctionNode, parameters: list, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.value = value
        self.parameters = parameters

class FunctionDeclareNode(PrimitiveNode):
    def __init__(self, parentNode :ASTNode, code: CodeSequenceNode, parameterTypes: ParameterDeclarationNode, identifier: IdentifierNode, returnType: type, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.code = code
        self.parameterTypes = parameterTypes
        self.returnType = returnType
 
class KeywordNode(ASTNode):
    def __init__(self, parentNode: ASTNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.codeSequenceNode = codeSequenceNode

class ArrayNode(ASTNode):
    def __init__(self, type: PrimitiveNode, size: PrimitiveNode, identifier: IdentifierNode, lineNr: int):
        self.type = type
        self.size = size
        self.identifier = identifier
        self.memory = []
        self.lineNr = lineNr
        self.index = None
        self.value = None

class ArrayAccesNode(ASTNode):
    def __init__(self, index: PrimitiveNode, identifier: IdentifierNode, lineNr: int):
        self.index = index
        self.identifier = identifier
        self.lineNr = lineNr
  
class ReturnNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, value: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, None, lineNr)
        self.parentNode = parentNode
        self.value = value

class AdditionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
       
class SubtractionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)

class MultiplicationNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)

class DivisionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)

class ComparisonNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeGreaterThan(ComparisonNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeSmallerThan(ComparisonNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeGreaterThanEqual(ComparisonNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeSmallerThanEqual(ComparisonNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class ComparisonNodeNotEuqal(ComparisonNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__( parentNode, left, right, lineNr)
        
class IfNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__( parentNode, codeSequenceNode, lineNr)
        self.comparison = comparison
class WhileNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__( parentNode, codeSequenceNode, lineNr)
        self.comparison = comparison

class ASTRoot():
    def __init__(self):
        self.globalVariables = []
        self.globalVariables.append(FunctionNode(None, None, [IntegerNode(None, None, None, None)], [], IdentifierNode(None, "IntOut", 0), 0))
        self.globalVariables.append(FunctionNode(None, None, [StringNode(None, None, None, None)], [], IdentifierNode(None, "StringOut", 0), 0))
        self.globalVariables.append(FunctionNode(None, None, [IntegerNode(None, None, None, None)], [], IdentifierNode(None, "IntOutLine", 0), 0))
        self.globalVariables.append(FunctionNode(None, None, [StringNode(None, None, None, None)], [], IdentifierNode(None, "StringOutLine", 0), 0))
        self.codeSequenceNode = CodeSequenceNode(self, self.globalVariables, [], 0)
        self.tokens = tokens.copy()