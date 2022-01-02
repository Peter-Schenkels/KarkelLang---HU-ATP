from tokens import *
from abc import ABC

class ASTNode(ABC):
    def __str__(self):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)    
    
class IdentifierNode(ASTNode):
    def __init__(self, parentNode: ASTNode, name: str):
        self.parentNode = parentNode
        self.name = name

class PrimitiveNode(ASTNode):
    def __init__(self, parentNode: ASTNode, identifier: IdentifierNode):
        self.parentNode = parentNode
        self.identifier = identifier
        
class StringNode(PrimitiveNode):
    def __init__(self, parentNode : ASTNode, value: str, identifier: IdentifierNode):
        self.parentNode = parentNode
        self.value = value
        self.identifier = identifier

class IntegerNode(PrimitiveNode):
    def __init__(self, parentNode: ASTNode, value: int, identifier: IdentifierNode):
        self.parentNode = parentNode
        self.value = value
        self.identifier = identifier

class OperatorNode(ASTNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right

class AdditionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right
       
class SubtractionNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right

class MultiplicationNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right

class DivideNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right    

class ComparisonNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right    
        
class AssignNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode):
        self.parentNode = parentNode
        self.left = left
        self.right = right    

class ParameterNode(ASTNode):
    def __init__(self, parentNode: ASTNode, parameters: list):
        self.parentNode = parentNode
        self.parameters = parameters
        
class CodeSequenceNode(ASTNode):
    def __init__(self, parentNode: ASTNode, globalVariables: list, codeSequence: list):
        self.parentNode = parentNode
        self.Sequence = codeSequence
        self.LocalVariables = list(PrimitiveNode) + globalVariables
        
class FunctionNode(PrimitiveNode):
    def __init__(self, parentNode: ASTNode, returnType: PrimitiveNode,  globalVariables: list, parameters: ParameterNode, codeSequence: list, identifier: IdentifierNode):
        self.parentNode = parentNode
        self.returnType = returnType
        self.codeSequenceNode = CodeSequenceNode(self, parameters + globalVariables, codeSequence)
        self.identifier = identifier
        
class KeywordNode(ASTNode):
    def __init__(self, parentNode: ASTNode, globalVariables: list):
        self.parentNode = parentNode
        self.codeSequenceNode = CodeSequenceNode(self, globalVariables, list(ASTNode))

class IfNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, globalVariables: list, codeSequence: list):
        self.parentNode = parentNode
        self.comparison = comparison
        self.codeSequenceNode = CodeSequenceNode(self, globalVariables, codeSequence)
        
class ElseIfNode(IfNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, globalVariables: list, codeSequence: list, ifNode: IfNode):
        self.parentNode = parentNode
        self.comparison = comparison
        self.ifNode = ifNode
        self.codeSequenceNode = CodeSequenceNode(self, globalVariables, codeSequence)
    
class ElseNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, globalVariables: list, codeSequence: list, ifNode: IfNode):
        self.parentNode = parentNode
        self.ifNode = ifNode
        self.codeSequenceNode = CodeSequenceNode(self, globalVariables, codeSequence)