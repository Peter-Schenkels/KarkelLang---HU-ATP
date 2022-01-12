from tokens import *
from abc import ABC
import jsonpickle

class ASTNode(ABC):
    def __init__(self, parentNode, lineNr: int):
        self.lineNr = lineNr
        self.parentNode = parentNode
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
        super().__init__(parentNode, lineNr)
        self.value = value
        
class FunctionCallNode(IdentifierNode):
    def __init__(self, parentNode: ASTNode, name: str, parameters: ParameterIdentifierNode, lineNr: int):
        super().__init__(parentNode, name, lineNr)
        self.parameters = parameters
        
class PrimitiveNode(ASTNode):
    def __init__(self, parentNode: ASTNode, identifier: IdentifierNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.identifier = identifier
 
class OperatorNode(ASTNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.left = left
        self.right = right
        self.output = None
        
class AssignNode(OperatorNode):
    def __init__(self, parentNode: ASTNode, left: PrimitiveNode, right: PrimitiveNode, lineNr: int):
        super().__init__(parentNode, left, right, lineNr)

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
    def __init__(self):
        super().__init__(None, None, None)  
    
    def __init__(self, parentNode: ASTNode, returnType: type, parameters: ParameterDeclarationNode, codeSequence: CodeSequenceNode, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, lineNr)
        self.returnType = returnType
        self.parameters = parameters
        self.codeSequenceNode = codeSequence
        self.identifier = identifier
        self.returnValue = None

class IntegerNode(PrimitiveNode):
    def __init__(self, parentNode: ASTNode, value: int, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.value = value
class StringNode(PrimitiveNode):   
    def __init__(self, parentNode : ASTNode, value: str, identifier: IdentifierNode, lineNr: int):
        super().__init__( parentNode, identifier, lineNr)
        self.value = value
        self.identifier = identifier
 
class KeywordNode(ASTNode):
    def __init__(self, parentNode: ASTNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__(parentNode, lineNr)
        self.parentNode = parentNode
        self.codeSequenceNode = codeSequenceNode
       
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
        
class IfNode(KeywordNode):
    def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, codeSequenceNode: CodeSequenceNode, lineNr: int):
        super().__init__( parentNode, codeSequenceNode, lineNr)
        self.comparison = comparison





        
# class FunctionNode(PrimitiveNode):
#     def __init__(self, parentNode: ASTNode, returnType: PrimitiveNode,  globalVariables: list, parameters: ParameterNode, codeSequence: list, identifier: IdentifierNode):
#         self.parentNode = parentNode
#         self.returnType = returnType
#         self.codeSequenceNode = CodeSequenceNode(self, parameters + globalVariables, codeSequence)
#         self.identifier = identifier
        



        
# class ElseIfNode(IfNode):
#     def __init__(self, parentNode: ASTNode, comparison: ComparisonNode, globalVariables: list, codeSequence: list, ifNode: IfNode):
#         self.parentNode = parentNode
#         self.comparison = comparison
#         self.ifNode = ifNode
#         self.codeSequenceNode = CodeSequenceNode(self, globalVariables, codeSequence)
    
# class ElseNode(KeywordNode):
#     def __init__(self, parentNode: ASTNode, globalVariables: list, codeSequence: list, ifNode: IfNode):
#         self.parentNode = parentNode
#         self.ifNode = ifNode
#         self.codeSequenceNode = CodeSequenceNode(self, globalVariables, codeSequence)

class ASTRoot():
    def __init__(self, tokens: list):
        self.globalVariables = list(ASTNode)
        self.codeSequenceNode = CodeSequenceNode(self, self.globalVariables, list(ASTNode))
        self.tokens = tokens.copy()