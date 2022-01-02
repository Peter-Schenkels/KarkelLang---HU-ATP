
import functools
from tokens import *

def split(input : str) ->list:
    pattern = re.compile("(\s)")
    return re.sub('', input)

def countCharacterUntil(input : list, match: str, stop : str) -> int:
    if(input== []): 
        print("Character not in the list")
        return int("-inf")
    head, *tail = input
    if(head == match): 
        return countCharacterUntil(tail, match, stop) + 1
    if(head == stop): 
        return 0
    return countCharacterUntil(tail, match, stop);
    
def checkError(input : list, lineNr : int = 1):
    if(input == []):
        return 0
    head, *tail = input
    if(head.type == "Error"):
        return lineNr
    if(head.type == "NewLine"):
        lineNr += 1
    return checkError(tail, lineNr)
    
def lexer(input : str) -> list:
    patternInclusions = re.compile("(\d+|\w+|@|->|<-|<<|>>|<>|<|>|\"|!|\+|\-|&|\[|\]|\?:|\?|:|#|,|\n)")
    patternExlusions = re.compile("\s")
    mismatches = patternInclusions.sub('', (patternExlusions.sub('', input)))
    if(len(mismatches) > 0):
        print("Uknown Token at line: " + str(countCharacterUntil(split(input), "\n", mismatches[0]) + 1))
        return []
    tokens  = list(map(matchToken, patternInclusions.findall(input)))
    lineNr = checkError(tokens)
    if(lineNr != 0):
        print("Invalid token at line: " + str(lineNr))
        return[]
    return tokens

if __name__ == '__main__':
    input = open("voorbeeld1.arw", "r")
    tokens = lexer(input.read())
    functools.reduce(print, tokens)