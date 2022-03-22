from tokenParser import *

        
def SetAttribute(input: object, attributeName: str, attributeValue: object) -> object:
    attributes = input.__dict__
    if (attributeName in attributes):
        attributeIndex = list(attributes.keys()).index(attributeName)
        first_part = dict(dict(list(attributes.items())[:attributeIndex]), **{attributeName : attributeValue})
        new_attributes = dict(first_part, **dict(list(attributes.items())[attributeIndex+1:]))
        return type(input)(new_attributes)
    else:
        return None
    

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
        output = ParseAssignOperator(right, context)
        if(output.error == None):
            right, context  = output.node, output.context
        else:
            return output.context
    assignNode = AssignNode(None, left, right, context.head.lineNr, declaration)   
    return CheckEndlineAppendNode(assignNode, context)