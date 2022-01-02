import re
import jsonpickle
import json

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)
    
tokens = {
    "@" : "PrimitiveType",
    "->" : "Assignment",
    "<-" : "Return",
    "<<" : "Operator",
    ">>" : "Operator",
    "<>" : "Operator",
    "<" : "ContextOpen",
    ">" : "ContextClose",
    "\"" : "StringIndicator",
    "!" : "EndLine",
    "+" : "Operator",
    "-" : "Operator",
    "&" : "FunctionDeclaration",
    "[" : "ParameterOpen",
    "]" : "ParameterClose",
    "?:" : "KeyWord",
    "?" : "KeyWord",
    ":" : "KeyWord",
    "#" : "PrimitiveType",
    "," : "Seperator",
    "\n" : "NewLine"   
}
    
def matchToken(input : str, tokens : dict = tokens):
    tokenType = tokens.get(input)
    if(tokenType is None):
        pattern = re.compile("^[A-Za-z]+$")
        if(pattern.match(input) != None):
            return Token("Identifier", input)
        pattern = re.compile("\d+")
        if(pattern.match(input) != None):
            return Token("NumericValue", input)
        return Token("Error", input)
    return Token(tokenType, input)