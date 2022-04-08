import re
import json
import jsonpickle
from enum import Enum

class Types (Enum):
    STRING = 'string'
    INTEGER = 'integer'
    PRIMITIVE = 'primitive'

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.lineNr = 0
        
    def __str__(self):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)
    
tokens = {
    "~" : "Comment",
    "@" : "PrimitiveType",
    "<-" : "Assignment",
    "->" : "Return",
    "X" : "ReturnTypeIndicator",
    "<<" : "Operator",
    ">>" : "Operator",
    "<>>" : "Operator",
    "<<>" : "Operator",
    "<>" : "Operator",
    "><" : "Operator",
    "+" : "Operator",
    "-" : "Operator",
    "*" : "Operator",
    "<" : "ContextOpen",
    ">" : "ContextClose",
    "{" : "StringIndicator",
    "}" : "StringIndicator",
    "(" : "ArrayOpen",
    ")" : "ArrayClose",
    "!" : "EndLine",
    "\\" : "Operator",
    "&" : "FunctionDeclaration",
    "[" : "ParameterOpen",
    "]" : "ParameterClose",
    "?:" : "KeyWord",
    "O" : "KeyWord",
    "?" : "KeyWord",
    ":" : "KeyWord",
    "#" : "PrimitiveType",
    "," : "Seperator",
    "\n" : "NewLine"   
}
    
def matchToken(input : str, tokens : dict = tokens):
    tokenType = tokens.get(input[0])
    if(tokenType is None):
        pattern = re.compile("^[@-~!-/:-?_ ]*$")
        if(pattern.match(input[0]) != None or input[0] == input[1]):
            return Token("Identifier", input[0])
        pattern = re.compile("\d+")
        if(pattern.match(input[0]) != None):
            return Token("NumericValue", input[0])
        return Token("Error", input[0])
    return Token(tokenType, input[0])